"""Проверка среды без обращения к модели; --qr проверяет нативный декодер."""
import argparse
import importlib.metadata
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]


def main(qr=False):
    load_dotenv(ROOT / ".env")
    print("Python:", sys.version.split()[0])
    assert sys.version_info[:2] == (3, 12), "Нужен Python 3.12 из uv sync"
    for package in ["deepagents", "langchain", "langchain-gigachat", "gigachat", "mcp", "a2a-sdk", "langgraph-api", "agent-client-protocol"]:
        print(package, importlib.metadata.version(package))
    print("GigaChat: ключ задан" if os.getenv("GIGACHAT_CREDENTIALS") else "GigaChat: заполните .env перед модельными примерами")
    from mcp import Client  # noqa: F401
    from deepagents_acp.server import AgentServerACP  # noqa: F401
    if qr:
        with tempfile.TemporaryDirectory() as directory:
            image = str(Path(directory) / "qr.png")
            original = "https://example.com/mipt-protocols"
            subprocess.run([sys.executable, str(ROOT / "skills/qr-code/scripts/qr_generate.py"), original, image], check=True)
            read = subprocess.run([sys.executable, str(ROOT / "skills/qr-code/scripts/qr_read.py"), image],
                                  check=True, capture_output=True, text=True, encoding="utf-8")
            assert read.stdout.strip() == original
            print("QR: генерация и обратное чтение прошли")
    print("Проверка завершена; запросы к модели не выполнялись")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qr", action="store_true")
    main(parser.parse_args().qr)
