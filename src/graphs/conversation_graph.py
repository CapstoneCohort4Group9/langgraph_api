from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

# import redis
from langgraph.checkpoint.redis import RedisSaver
from langchain_core.runnables import RunnableLambda
from src.config.settings import load_config
from src.nodes.finalmodelresponse import FinalModelResponseNode
from src.nodes.parsetoolcall import ParseToolCallToolNode
from src.state.state import State
from src.nodes.intent import IntentToolNode
from src.nodes.sentiment import SentimentToolNode
from src.nodes.callbedrockmodel import CallingBedrockModelToolNode
from src.nodes.calltoolorragapi import CallTravelOrRAGAPINode
from src.nodes.appendtoolresult import AppendToolResultNode


class GraphBuilder:
    def __init__(self):
        self.graph = StateGraph(State)
        self.settings = load_config()
        self.DB_URI = self.settings.REDIS_HOST + ":" + str(self.settings.REDIS_PORT)

    def build_graph(self):
        """
        Build a graph to generate blogss based on topic
        """
        self.intent_node_obj = IntentToolNode()
        self.sentiment_node_obj = SentimentToolNode()
        self.call_bedrock_model_node_obj = CallingBedrockModelToolNode()
        self.parse_tool_call_node_obj = ParseToolCallToolNode()

        ## Nodes
        self.graph.add_node("intent", RunnableLambda(self.intent_node_obj.process))
        self.graph.add_node(
            "sentiment", RunnableLambda(self.sentiment_node_obj.process)
        )
        self.graph.add_node(
            "call_bedrock_model",
            RunnableLambda(self.call_bedrock_model_node_obj.process),
        )
        self.graph.add_node(
            "parse_tool_call",
            RunnableLambda(self.parse_tool_call_node_obj.process),
        )
        self.graph.add_node(
            "call_travel_or_rag_api",
            RunnableLambda(CallTravelOrRAGAPINode().process),
        )
        self.graph.add_node(
            "append_tool_result",
            RunnableLambda(AppendToolResultNode().process),
        )
        self.graph.add_node(
            "final_model_response", RunnableLambda(FinalModelResponseNode().process)
        )

        ## Edges
        self.graph.add_edge(START, "intent")
        self.graph.add_edge("intent", "sentiment")
        self.graph.add_edge("sentiment", "call_bedrock_model")
        self.graph.add_edge("call_bedrock_model", "parse_tool_call")
        self.graph.add_edge("parse_tool_call", "call_travel_or_rag_api")
        self.graph.add_edge("call_travel_or_rag_api", "append_tool_result")
        self.graph.add_edge("append_tool_result", "final_model_response")
        self.graph.add_edge("final_model_response", END)

        return self.graph

    def setup_graph(self):
        self.graph = self.build_graph()
        # r = redis.Redis(
        #     host=self.settings.REDIS_HOST,
        #     port=self.settings.REDIS_PORT,
        # )

        # Create Redis checkpointer
        checkpointer = InMemorySaver()
        # return self.graph.compile()
        with RedisSaver.from_conn_string(self.DB_URI) as checkpointer:
            checkpointer.setup()
            return self.graph.compile(checkpointer=checkpointer)
