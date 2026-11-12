"""Deep Agent как ACP-процесс: stdout занят JSON-RPC, диагностика идёт в stderr."""
import asyncio
import os
import sys
from contextlib import redirect_stdout
from pathlib import Path

from acp import run_agent
from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend
from deepagents_acp.server import AgentServerACP, AgentSessionContext
from langgraph.checkpoint.memory import MemorySaver

from lab import make_model


async def main():
    model = make_model(streaming=True)
    try:
        def build_agent(context: AgentSessionContext):
            workspace = Path(context.cwd).resolve(strict=True)
            with redirect_stdout(sys.stderr):
                return create_deep_agent(
                    model=model,
                    backend=LocalShellBackend(
                        root_dir=workspace, virtual_mode=True,
                        env={"PATH": str(Path(sys.executable).parent) + os.pathsep + os.defpath},
                    ),
                    checkpointer=MemorySaver(),
                    interrupt_on={"edit_file": True, "write_file": True, "execute": True},
                    system_prompt=(
                        "Ты coding-агент учебного проекта. Отвечай кратко по-русски. "
                        f"Рабочая папка: {workspace}. Python: {sys.executable}. "
                        "Работай только с файлами этой задачи в рабочей папке. "
                        "Файловые инструменты используют пути от корня проекта: /trip_budget.py и /test_trip_budget.py. "
                        "Сначала прочитай код и тесты. Если просят только анализ, ничего не меняй и не запускай. "
                        "Для исправления используй edit_file, для проверки — execute. "
                        "Если клиент отклонил действие, не повторяй его: сообщи об отказе и заверши ответ. "
                        "После успешной проверки дай краткий итог и заверши ответ."
                    ),
                )
        await run_agent(AgentServerACP(build_agent))
    finally:
        await model._client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
