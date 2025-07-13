from fastapi import APIRouter, Request, HTTPException
from src.graphs.conversation_graph import GraphBuilder

router = APIRouter()
graph_builder = GraphBuilder()
graph = graph_builder.setup_graph()


@router.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        messages = data.get("messages", [])

        # Run the LangGraph workflow
        result = graph.invoke({"input": user_input, "messages": messages})

        return {"messages": result["messages"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
