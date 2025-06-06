# from fastapi import FastAPI, Request
# from workflows.conversation_graph import build_graph

import streamlit as st
from config.settings import load_config
from workflows.conversation_graph import build_graph

# app = FastAPI()
# graph = build_graph()


# @app.post("/chat")
# async def chat(request: Request):
#     data = await request.json()
#     query = data.get("query")
#     session = data.get("session", {})
#     state = {"query": query, **session}
#     result = graph.invoke(state)

#     return {
#         "bot_response": result["response"],
#         "intent": result["intent"],
#         "sentiment": result["sentiment"],
#         "summary": result["summary"],
#         "chat_history": result["chat_history"],
#     }


def main():
    st.set_page_config(
        page_title="Customer Conversational Intelligence", page_icon="🤖", layout="wide"
    )

    st.title("Customer Conversational Intelligence Platform")
    st.write("Analyze customer conversations using AI-powered agents")

    # Initialize agents
    config = load_config()
    graph = build_graph()
    # Input section
    st.header("Input")
    conversation = st.text_area(
        "Enter customer conversation",
        height=200,
        placeholder="Paste the customer conversation here...",
    )

    if st.button("Analyze"):
        if conversation:
            with st.spinner("Analyzing conversation..."):
                # Run parallel analysis
                print("Running analysis on conversation:", conversation)
                state = {"messages": conversation}
                result = graph.invoke(state)
                print("my results", result)
                st.success(f"Result: {result['text']}")
        else:
            st.warning("Please enter a conversation to analyze.")


if __name__ == "__main__":
    main()
