from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableLambda
from src.state.state import State
from src.nodes.intent import IntentToolNode
from src.nodes.summarizer import SummarizerNode


class GraphBuilder:
    def __init__(self):
        self.graph = StateGraph(State)

    def build_graph(self):
        """
        Build a graph to generate blogss based on topic
        """
        self.intent_node_obj = IntentToolNode()
        self.summarizer_node_obj = SummarizerNode()
        ## Nodes
        self.graph.add_node("intent", RunnableLambda(self.intent_node_obj.process))
        self.graph.add_node(
            "summarizer", RunnableLambda(self.summarizer_node_obj.process)
        )

        ## Edges
        self.graph.add_edge(START, "intent")
        self.graph.add_edge("intent", "summarizer")
        self.graph.add_edge("summarizer", END)

        return self.graph

    def setup_graph(self):
        self.graph = self.build_graph()
        return self.graph.compile()
