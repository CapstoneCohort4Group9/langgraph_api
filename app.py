# from fastapi import FastAPI, Request
# from workflows.conversation_graph import build_graph

import streamlit as st
from src.config.settings import load_config
from src.graphs.conversation_graph import GraphBuilder


def main():
    st.set_page_config(
        page_title="Customer Conversational Intelligence", page_icon="🤖", layout="wide"
    )

    st.title("Customer Conversational Intelligence Platform")
    st.write("Analyze customer conversations using AI-powered agents")
    graph_builder = GraphBuilder()
    graph = graph_builder.setup_graph()
    # Initialize agents
    config = load_config()
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
                st.success(f"Intent: {result['intentMessage']}")
        else:
            st.warning("Please enter a conversation to analyze.")


if __name__ == "__main__":
    main()
