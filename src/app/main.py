from fastapi import FastAPI
from .router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="LLM Orchestrator",
    description="Orchestrates LLM-based travel chatbot using LangGraph",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
