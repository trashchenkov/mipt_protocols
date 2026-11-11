"""Deep Agent как ACP-процесс: stdout занят JSON-RPC, диагностика идёт в stderr."""
import asyncio
import sys
from contextlib import redirect_stdout

from acp import run_agent
from deepagents import create_deep_agent
from deepagents_acp.server import AgentServerACP
from langgraph.checkpoint.memory import MemorySaver

from lab import make_model


async def main():
    model = make_model(streaming=True)
    try:
        with redirect_stdout(sys.stderr):
            agent = create_deep_agent(model=model, checkpointer=MemorySaver(),
                                      system_prompt="Отвечай кратко по-русски. Для приветствия инструменты не нужны.")
        await run_agent(AgentServerACP(agent))
    finally:
        await model._client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
