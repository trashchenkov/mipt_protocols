"""Публикация общего агента через a2a-sdk: задача, статусы, artifact."""
import uvicorn
from a2a.helpers import new_task_from_user_message, new_text_message, new_text_part
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from starlette.applications import Starlette

from agents.travel import travel_graph


class TravelExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.current_task is None:
            await event_queue.enqueue_event(new_task_from_user_message(context.message))
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.start_work(new_text_message("Ищу поездку", task_id=context.task_id, context_id=context.context_id))
        async with travel_graph() as agent:
            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": context.get_user_input()}]},
                config={"recursion_limit": 60},
            )
        for message in result["messages"]:
            message.pretty_print()
        await updater.add_artifact([new_text_part(str(result["messages"][-1].content), media_type="text/plain")], name="answer")
        await updater.complete()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        await TaskUpdater(event_queue, context.task_id, context.context_id).cancel()


card = AgentCard(
    name="Агент Туту", description="Поиск поездки через MCP Туту", version="0.1.0",
    supported_interfaces=[AgentInterface(url="http://127.0.0.1:9100", protocol_binding="JSONRPC", protocol_version="1.0")],
    capabilities=AgentCapabilities(streaming=True), default_input_modes=["text/plain"], default_output_modes=["text/plain"],
    skills=[AgentSkill(id="travel", name="Поиск поездки", description="Поезда, самолёты, автобусы и отели", tags=["travel"])],
)
handler = DefaultRequestHandler(agent_executor=TravelExecutor(), task_store=InMemoryTaskStore(), agent_card=card)
app = Starlette(routes=create_agent_card_routes(card) + create_jsonrpc_routes(handler, "/"))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9100, log_level="warning")
