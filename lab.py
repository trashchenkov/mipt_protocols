"""Запуск локальных учебных серверов и небольшие клиенты протоколов."""
from __future__ import annotations

import atexit
import html
import json
import os
import queue
import signal
import socket
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

import httpx
from dotenv import load_dotenv
from langchain_gigachat import GigaChat

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
RUNTIME = ROOT / ".runtime"
PROTOCOL_VERSION = "2026-07-28"
SERVERS: dict[str, LocalProcess] = {}


def make_model(**kwargs):
    return GigaChat(
        use_api_v2=True, model=os.getenv("GIGACHAT_MODEL", "GigaChat-3-Ultra"),
        temperature=0.01, timeout=120, **kwargs,
    )


def future_date(days=21):
    from datetime import date, timedelta
    return (date.today() + timedelta(days=days)).isoformat()


def safe_log(text):
    for key in ("GIGACHAT_CREDENTIALS", "GIGACHAT_ACCESS_TOKEN"):
        if value := os.getenv(key):
            text = text.replace(value, "[скрыто]")
    return text


class LocalProcess:
    """Собственный дочерний процесс; журнал хранится вне учебных материалов."""

    def __init__(self, name, args, *, stdin=False):
        RUNTIME.mkdir(exist_ok=True)
        self.name = name
        self.log_path = RUNTIME / f"{name}.log"
        self.log = self.log_path.open("w", encoding="utf-8")
        options = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
                   if os.name == "nt" else {"start_new_session": True})
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
        self.process = subprocess.Popen(
            args, cwd=ROOT, env=env, text=True, encoding="utf-8",
            stdin=subprocess.PIPE if stdin else subprocess.DEVNULL,
            stdout=subprocess.PIPE if stdin else self.log, stderr=self.log,
            **options,
        )

    def read_log(self, lines=30):
        self.log.flush()
        return safe_log("\n".join(self.log_path.read_text(errors="replace").splitlines()[-lines:]))

    def stop(self):
        if self.process.poll() is None:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(self.process.pid), "/T", "/F"],
                               capture_output=True, check=False)
            else:
                try:
                    os.killpg(self.process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                if os.name != "nt":
                    try:
                        os.killpg(self.process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                else:
                    self.process.kill()
                self.process.wait(timeout=5)
        if self.process.stdin:
            self.process.stdin.close()
        self.log.close()


def stop_all():
    for server in list(SERVERS.values()):
        server.stop()
    SERVERS.clear()


atexit.register(stop_all)


def start_server(name, script=None, *, port, ready_path="/", args=(), agent_server=False):
    if old := SERVERS.pop(name, None):
        old.stop()
    with socket.socket() as sock:
        sock.settimeout(.3)
        if sock.connect_ex(("127.0.0.1", port)) == 0:
            raise RuntimeError(f"Порт {port} уже занят. Выберите другой порт или остановите свой сервер.")
    command = ([sys.executable, "-m", "langgraph_cli", "dev", "--no-reload", "--no-browser", "--port", str(port)]
               if agent_server else [sys.executable, "-m", str(Path(script).with_suffix("")).replace(os.sep, ".").replace("/", "."), *map(str, args)])
    server = LocalProcess(name, command)
    SERVERS[name] = server
    deadline = time.monotonic() + 90
    try:
        while time.monotonic() < deadline:
            if server.process.poll() is not None:
                raise RuntimeError(f"Сервер завершился:\n{server.read_log()}")
            try:
                response = httpx.get(f"http://127.0.0.1:{port}{ready_path}", timeout=1)
                if response.status_code < 500:
                    print(f"{name}: готов, порт {port}, PID {server.process.pid}")
                    return server
            except httpx.HTTPError:
                pass
            time.sleep(.2)
        raise TimeoutError(f"Сервер не готов:\n{server.read_log()}")
    except BaseException:
        server.stop()
        SERVERS.pop(name, None)
        raise


def decode_json_response(response):
    response.raise_for_status()
    if "text/event-stream" in response.headers.get("content-type", ""):
        candidates = [json.loads(line[5:].strip()) for line in response.text.splitlines()
                      if line.startswith("data:") and line[5:].strip() != "[DONE]"]
        return next(item for item in reversed(candidates) if "result" in item or "error" in item)
    return response.json()


async def mcp_request(method, params=None, *, version=PROTOCOL_VERSION, request_meta=True):
    params = dict(params or {})
    if request_meta:
        params["_meta"] = {"io.modelcontextprotocol/protocolVersion": version,
                           "io.modelcontextprotocol/clientCapabilities": {}}
    headers = {"Accept": "application/json, text/event-stream", "Mcp-Method": method,
               "MCP-Protocol-Version": version}
    if method == "tools/call":
        headers["Mcp-Name"] = params["name"]
    payload = {"jsonrpc": "2.0", "id": str(uuid4()), "method": method, "params": params}
    async with httpx.AsyncClient(timeout=30) as http:
        response = await http.post("http://127.0.0.1:8765/mcp", headers=headers, json=payload)
    return payload, decode_json_response(response), dict(response.headers)


async def discover_agent(base_url, *, assistant_id=None):
    async with httpx.AsyncClient(timeout=60) as http:
        response = await http.get(base_url.rstrip("/") + "/.well-known/agent-card.json",
                                  params={"assistant_id": assistant_id} if assistant_id else None)
        response.raise_for_status()
        return response.json()


async def platform_card(base_url="http://127.0.0.1:9300"):
    async with httpx.AsyncClient(timeout=60) as http:
        response = await http.post(base_url + "/assistants/search", json={"graph_id": "travel"})
        response.raise_for_status()
        assistant_id = response.json()[0]["assistant_id"]
    return await discover_agent(base_url, assistant_id=assistant_id)


@dataclass
class A2AReply:
    request: dict
    task: dict
    text: str


async def ask_a2a(card, text):
    interface = next(i for i in card["supportedInterfaces"]
                     if i["protocolBinding"] == "JSONRPC" and i["protocolVersion"] == "1.0")
    payload = {"jsonrpc": "2.0", "id": str(uuid4()), "method": "SendMessage", "params": {
        "message": {"messageId": str(uuid4()), "role": "ROLE_USER", "parts": [{"text": text}]}}}
    async with httpx.AsyncClient(timeout=300) as http:
        response = await http.post(interface["url"], headers={"A2A-Version": "1.0"}, json=payload)
        response.raise_for_status()
        envelope = response.json()
    if "error" in envelope:
        raise RuntimeError(f"A2A: {envelope['error']}")
    task = envelope["result"]["task"]
    if task["status"]["state"] != "TASK_STATE_COMPLETED":
        raise RuntimeError(f"Задача не завершилась успешно: {task['status']}")
    answer = "\n".join(p["text"] for a in task.get("artifacts", [])
                       for p in a.get("parts", []) if "text" in p)
    if not answer.strip():
        raise RuntimeError("Задача не вернула текстовый artifact")
    return A2AReply(payload, task, answer)


async def agui_events(port, text):
    payload = {"threadId": str(uuid4()), "runId": str(uuid4()), "state": {}, "tools": [],
               "context": [], "forwardedProps": {}, "messages": [
                   {"id": str(uuid4()), "role": "user", "content": text}]}
    events = []
    async with httpx.AsyncClient(timeout=240) as http:
        async with http.stream("POST", f"http://127.0.0.1:{port}/agent", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line.startswith("data:"):
                    continue
                event = json.loads(line[5:].strip())
                events.append(event)
                kind = event["type"]
                if kind == "TEXT_MESSAGE_CONTENT":
                    print(event.get("delta", ""), end="", flush=True)
                elif kind in {"RUN_STARTED", "RUN_FINISHED", "RUN_ERROR", "TOOL_CALL_START", "TOOL_CALL_RESULT"}:
                    print(f"\n{kind}: {event.get('toolCallName', event.get('message', ''))}", flush=True)
                if kind == "RUN_ERROR":
                    raise RuntimeError(event.get("message", "Ошибка AG-UI"))
    if not any(e["type"] == "RUN_FINISHED" for e in events):
        raise RuntimeError("Поток завершился без RUN_FINISHED")
    return events


def a2ui_operations(events):
    for event in events:
        if event.get("type") == "TOOL_CALL_RESULT":
            try:
                payload = json.loads(event.get("content", ""))
            except (ValueError, TypeError):
                continue
            if isinstance(payload, dict) and "a2ui_operations" in payload:
                return payload["a2ui_operations"]
    raise ValueError("В потоке нет описания A2UI")


def preview_a2ui(operations):
    """Учебный статический просмотр базовых компонентов A2UI v0.9."""
    components = {c["id"]: c for op in operations for c in op.get("updateComponents", {}).get("components", [])}
    def render(identifier, seen=frozenset()):
        if identifier in seen or identifier not in components:
            return ""
        node = components[identifier]
        seen = seen | {identifier}
        kind = node.get("component")
        if kind == "Text":
            value = node.get("text", "")
            text = html.escape(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False))
            return f'<p style="margin:6px 0">{text}</p>'
        if kind == "Divider":
            return "<hr>"
        children = node.get("children", [node["child"]] if "child" in node else [])
        if not isinstance(children, list):
            return "<pre>List: " + html.escape(json.dumps(children, ensure_ascii=False)) + "</pre>"
        body = "".join(render(child, seen) for child in children)
        style = "display:flex;gap:18px;flex-wrap:wrap" if kind == "Row" else ""
        if kind == "Card":
            style += ";border:1px solid #7bbfa6;border-radius:14px;padding:20px;background:#f1fff8"
        return f'<div style="{style}">{body}</div>'
    return '<div style="color:#123;font:16px sans-serif;padding:16px">' + render("root") + "</div>"


class ACPClient:
    """Stdio-клиент: уведомления и решения по session/request_permission."""

    def __init__(self, *, permission_handler=None, on_update=None):
        if old := SERVERS.pop("acp", None):
            old.stop()
        self.server = LocalProcess("acp", [sys.executable, "-m", "servers.acp_server"], stdin=True)
        SERVERS["acp"] = self.server
        self.responses = queue.Queue()
        self.counter = 0
        self.permission_handler = permission_handler
        self.on_update = on_update
        self.permission_log = []
        def read():
            for line in self.server.process.stdout:
                try:
                    self.responses.put(json.loads(line))
                except ValueError:
                    self.responses.put({"invalid_stdout": safe_log(line)})
            self.responses.put(None)
        threading.Thread(target=read, daemon=True).start()

    def request(self, method, params, timeout=300):
        self.counter += 1
        request = {"jsonrpc": "2.0", "id": self.counter, "method": method, "params": params}
        self.server.process.stdin.write(json.dumps(request, ensure_ascii=False) + "\n")
        self.server.process.stdin.flush()
        updates = []
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"ACP: истекло время ожидания {method}")
            try:
                message = self.responses.get(timeout=remaining)
            except queue.Empty as error:
                raise TimeoutError(f"ACP: истекло время ожидания {method}") from error
            if message is None:
                raise RuntimeError(f"ACP-процесс завершился:\n{self.server.read_log()}")
            # Запрос агента и запрос клиента имеют независимые пространства id.
            if "method" in message and "id" in message:
                reply = {"jsonrpc": "2.0", "id": message["id"]}
                if message["method"] == "session/request_permission":
                    permission = message["params"]
                    options = permission.get("options", [])
                    reject = next((o["optionId"] for o in options if o["kind"] == "reject_once"), None)
                    selected = self.permission_handler(permission) if self.permission_handler else reject
                    outcome = ({"outcome": "selected", "optionId": selected}
                               if selected in {o["optionId"] for o in options}
                               else {"outcome": "cancelled"})
                    reply["result"] = {"outcome": outcome}
                    self.permission_log.append({"request": permission, "outcome": outcome})
                else:
                    reply["error"] = {"code": -32601, "message": "Client method not implemented"}
                self.server.process.stdin.write(json.dumps(reply, ensure_ascii=False) + "\n")
                self.server.process.stdin.flush()
                continue
            if message.get("id") == self.counter:
                if "error" in message:
                    raise RuntimeError(f"ACP: {message['error']}")
                return request, message["result"], updates
            if "invalid_stdout" in message:
                raise RuntimeError(f"В stdout ACP попала диагностика: {message['invalid_stdout']}")
            updates.append(message)
            if self.on_update:
                self.on_update(message)

    def stop(self):
        self.server.stop()
        SERVERS.pop("acp", None)
