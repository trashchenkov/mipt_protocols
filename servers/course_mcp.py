"""Учебные tools, resources и prompts; stdio по умолчанию или --http."""
import argparse
import json
from pathlib import Path

from mcp.server import MCPServer
from mcp.server.mcpserver.prompts.base import UserMessage

DATA = Path(__file__).resolve().parents[1] / "data/course"
FILES = {"mcp": "mcp_intro.md", "a2a": "a2a_intro.md"}
server = MCPServer("mipt-protocols")


@server.resource("course://overview", mime_type="text/markdown")
def overview() -> str:
    """Описание учебного курса протоколов."""
    return "Курс МФТИ: MCP, A2A, AG-UI, A2UI, ACP и Skills. Практика на Deep Agents и GigaChat."


@server.resource("course://topics", mime_type="application/json")
def topics() -> str:
    """Темы и имена соответствующих учебных файлов."""
    return json.dumps(FILES, ensure_ascii=False)


@server.prompt(name="prepare_lecture_brief")
def prepare_lecture_brief(topic_name: str, audience: str) -> list[UserMessage]:
    """Шаблон справки по теме для заданной аудитории."""
    return [UserMessage(
        f"Подготовь краткую справку по теме {topic_name} для аудитории: {audience}. "
        "Используй переданный контекст курса и доступные инструменты чтения материалов. "
        "В справке укажи назначение протокола и один пример его применения."
    )]


@server.tool()
def list_topic_artifacts(topic_name: str) -> dict:
    """Получить список материалов темы mcp или a2a."""
    name = topic_name.strip().lower()
    if name not in FILES:
        raise ValueError("Доступные темы: mcp, a2a")
    return {"topic": name, "files": [FILES[name]]}


@server.tool()
def read_artifact_head(path: str, max_lines: int = 6) -> dict:
    """Прочитать начало файла внутри папки учебных материалов."""
    if not 1 <= max_lines <= 40:
        raise ValueError("max_lines должен быть от 1 до 40")
    target = (DATA / path).resolve()
    if not target.is_relative_to(DATA.resolve()) or not target.is_file():
        raise ValueError("Файл должен находиться внутри data/course")
    return {"path": path, "text": "\n".join(target.read_text(encoding="utf-8").splitlines()[:max_lines])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8765)
    options = parser.parse_args()
    if options.http:
        server.run(transport="streamable-http", host="127.0.0.1", port=options.port)
    else:
        server.run(transport="stdio")
