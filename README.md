# Customer Conversational Intelligence Platform

A sophisticated conversational intelligence platform powered by Large Language Models (LLMs) that analyzes customer interactions using multiple specialized agents.

## Features

- Sentiment Analysis Agent (using Hugging Face models)
- Intent Classification Agent (using Hugging Face models)
- Retrieval Agent
- Interactive Streamlit Frontend
- LangGraph for agent orchestration
- LangSmith for monitoring and tracing
- LangChain for LLM integration

## Project Structure

```
convo_ai/
├── app.py                    # Streamlit frontend application
├── src/                    # Core application code
│   ├── agents/            # Agent implementations
│   ├── config/            # Configuration files
│   ├── llms/              # llm models
│   ├── utils/             # Utility functions
│   ├── graphs/            # Langgrapgh grapgh builder
│   ├── nodes/             # Langgrapgh nodes
│   ├── state/             # Langgrapgh state
│   └── tools/             # Tools
├── tests/                 # Test files
├── .env.example          # Example environment variables
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

4. Run the application:
```bash
streamlit run app.py
```

## Development

- Use `black` for code formatting
- Use `isort` for import sorting
- Use `mypy` for type checking
- Write tests using `pytest`


     +-----------------------------+
     |   New User Message (Turn 2) |
     +--------------+--------------+
                    ↓
        +--------------------------+
        |  Fetch Previous Context  | ← from S3 / database
        +--------------------------+
                    ↓
     +----------- Async Parallel Execution -----------+
     |                                               |
     | +----------------+  +------------------------+ |
     | | Intent Agent   |  | Sentiment Analyzer     | |
     | +----------------+  +------------------------+ |
     +------------------------------------------------+
                     ↓       ↓
            +--------------------------+
            |   Context Retriever Agent|
            +--------------------------+
                     ↓
            +--------------------------+
            | ReAct Based API Agent    |
            +--------------------------+
                     ↓
     +----------------+    +----------------------+
     | Summarizer     |    | Logging & Monitoring |
     +----------------+    +----------------------+
                     ↓
            +--------------------------+
            | Send Reply to User + Save|
            +--------------------------+