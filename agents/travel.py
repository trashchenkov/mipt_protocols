"""Общая логика агента Туту для двух серверных реализаций A2A."""
from contextlib import asynccontextmanager

from deepagents import create_deep_agent
from langchain.mcp import MCPAdapter

from lab import make_model

SYSTEM_PROMPT = (
    "Ты агент по поездкам. Отвечай по-русски кратко. Данные бери из инструментов Туту. "
    "Для поиска билетов вызови подходящий инструмент. После успешного поиска дай ответ с "
    "маршрутом, датой, номером поезда и ценой. Не оформляй заказ."
)


@asynccontextmanager
async def travel_graph():
    model = make_model()
    try:
        async with MCPAdapter("https://mcp.tutu.ru/mcp") as adapter:
            yield create_deep_agent(model=model, tools=await adapter.list_tools(), system_prompt=SYSTEM_PROMPT)
    finally:
        await model._client.aclose()
