from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.graphs.conversation_graph import GraphBuilder

router = APIRouter()
graph_builder = GraphBuilder()
graph = graph_builder.setup_graph()


@router.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message")
        user_id = data.get("user_id")

        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")

        # Run the LangGraph workflow with user_id as thread_id for checkpointing
        result = graph.invoke(
            {"input": user_input},
            config={"configurable": {"thread_id": user_id}},
        )

        return {"messages": result["messages"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    # Lightweight check for ALB
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ok"})
