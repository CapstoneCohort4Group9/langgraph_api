from langgraph.graph import StateGraph
from tools.tools import detect_intent_tool
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI

# from agents.sentiment_analyzer import analyze_sentiment
from agents.retriever import getRetriever

# from agents.llm_responder import generate_reply
from agents.summarizer import summarize

# def sentiment_node(state):
#     sentiment = analyze_sentiment(state["query"])
#     return {"sentiment": sentiment, **state}

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: str
    intentMessage: str
    text: str


def intent(state):
    print("Running intent detection...", state["messages"])
    intent = detect_intent_tool.run(state["messages"])
    print("DEBUG: Detected intent:", intent)
    return {**state, "intentMessage": intent}


def retriever_node(state):
    print("DEBUG:", state)
    retriever = getRetriever()
    question = state["query"]
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    retrieval_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    result = retrieval_chain.invoke(question)
    print("DEBUG RESULT:", result)
    return {"ragContext": result, **state}


# def response_node(state):
#     response = generate_reply(state["query"], state["docs"], state.get("chat_history", ""))
#     chat = state.get("chat_history", "")
#     updated_history = f"{chat}\nUser: {state['query']}\nBot: {response}"
#     return {"response": response, "chat_history": updated_history, **state}


def summarizer(state):
    print("Running summarization...", state)
    print("DEBUG:", state)
    summary = summarize(state)
    print("DEBUG: Summary result:", summary)
    return summary


def build_graph():
    # graph = StateGraph(State)

    # Parallel: Intent + Sentiment
    # graph.add_node("sentiment", sentiment_node)
    # graph.add_node("intent", RunnableLambda(intent))

    # Sequential: Following sentiment and intent
    # graph.add_node("retriever", retriever_node)
    # graph.add_node("responder", response_node)
    # graph.add_node("summarizer", RunnableLambda(summarizer))

    # Entry
    # graph.set_entry_point(["sentiment", "intent"])
    # graph.add_edge("sentiment", "retriever")
    # graph.add_edge("intent", "retriever")
    # graph.add_edge("retriever", "responder")
    # graph.set_entry_point("intent")
    # graph.add_edge("intent", "summarizer")

    # graph.set_finish_point("summarizer")

    builder = StateGraph(State)
    builder.add_node("intent", RunnableLambda(intent))
    builder.add_node("summarizer", RunnableLambda(summarizer))
    builder.set_entry_point("intent")
    builder.add_edge("intent", "summarizer")
    builder.set_finish_point("summarizer")

    return builder.compile()
