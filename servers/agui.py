"""Агент за AG-UI endpoint; --a2ui добавляет генерацию интерфейса."""
import argparse
from contextlib import asynccontextmanager

import uvicorn
from ag_ui_langgraph import LangGraphAgent, add_langgraph_fastapi_endpoint
from deepagents import create_deep_agent
from fastapi import FastAPI
from langchain.mcp import MCPAdapter
from langgraph.checkpoint.memory import MemorySaver

from compat.a2ui_tool import get_a2ui_tools
from lab import make_model


def create_app(use_a2ui=False):
    @asynccontextmanager
    async def lifespan(app):
        model, renderer = make_model(streaming=True), make_model()
        try:
            async with MCPAdapter("https://mcp.tutu.ru/mcp") as adapter:
                tools = await adapter.list_tools()
                prompt = "Отвечай по-русски кратко. Сведения о поездках получай из инструментов Туту."
                if use_a2ui:
                    tools.append(get_a2ui_tools({"model": renderer}))
                    prompt += (
                        " Покажи одну карточку через generate_a2ui. Используй простые статические Text, Card, Column, Row, Divider. "
                        "После одного успешного a2ui_operations сообщи, что карточка готова, и заверши ответ."
                    )
                graph = create_deep_agent(model=model, tools=tools, system_prompt=prompt, checkpointer=MemorySaver())
                add_langgraph_fastapi_endpoint(app, LangGraphAgent(name="travel", graph=graph, emit_raw_events=False), "/agent")
                yield
        finally:
            await renderer._client.aclose()
            await model._client.aclose()
    return FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a2ui", action="store_true")
    parser.add_argument("--port", type=int, default=9200)
    options = parser.parse_args()
    uvicorn.run(create_app(options.a2ui), host="127.0.0.1", port=options.port, log_level="warning")
