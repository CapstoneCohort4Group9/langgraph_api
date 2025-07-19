from src.state.state import State
import json
import httpx
from src import logger
from src.config.settings import load_config

settings = load_config()


class CallTravelOrRAGAPINode:
    """
    Node logic enhanced with tool integration.
    """

    def __init__(self):
        self.BOOK_FLIGHT_API_URL = settings.NON_AI_API_URL + "/book_flight"
        self.SEARCH_FLIGHT_API_URL = settings.NON_AI_API_URL + "/search_flight"
        self.CHECK_FLIGHT_STATUS_API_URL = (
            settings.NON_AI_API_URL + "/check_flight_status"
        )
        self.CHANGE_FLIGHT_API_URL = settings.NON_AI_API_URL + "/change_flight"
        self.CHECK_TRIP_PRICES_API_URL = settings.NON_AI_API_URL + "/check_trip_prices"
        self.CHECK_FLIGHT_PRICES_API_URL = (
            settings.NON_AI_API_URL + "/check_flight_prices"
        )
        self.CHECK_FLIGHT_RESERVATION_API_URL = (
            settings.NON_AI_API_URL + "/check_flight_reservation"
        )
        self.CANCEL_FLIGHT_API_URL = settings.NON_AI_API_URL + "/cancel_flight"

    def process(self, state: State) -> State:
        logger.info(
            f"inside CallTravelOrRAGAPINode state is : {state} and tool_call is: {state.get('tool_call', '')}"
        )
        if not state.get("tool_call"):
            return {**state, "tool_output": "No tool_call found."}

        try:
            tool = json.loads(state["tool_call"])
            name = tool.get("name")
            args = tool.get("arguments", {})
            logger.info(f"Calling tool: {name} with args: {args}")
            # Route to appropriate external service
            if name == "query_policy_rag_db":
                r = httpx.post(settings.RAG_API_URL, json={"query": state["input"]})
                logger.info(f"RAG API response: {r.json()}")
                return {**state, "rag_response": r.json()["answer"]}

            elif name == "search_flight":
                r = httpx.post(self.SEARCH_FLIGHT_API_URL, json=args)
                logger.info(f"Search flight response: {r.json()}")
                return {**state, "tool_output": r.json()["data"]}

            elif name == "book_flight":
                r = httpx.post(self.BOOK_FLIGHT_API_URL, json=args)
                return {**state, "tool_output": r.json()["data"]}

            elif name == "check_flight_status":
                r = httpx.post(self.CHECK_FLIGHT_STATUS_API_URL, json=args)
                return {**state, "tool_output": r.json()["data"]}

            elif name == "change_flight":
                r = httpx.post(self.CHANGE_FLIGHT_API_URL, json=args)
                return {**state, "tool_output": r.json()["data"]}

            elif name == "check_trip_prices":
                r = httpx.post(self.CHECK_TRIP_PRICES_API_URL, json=args)
                return {**state, "tool_output": r.json()["data"]}

            elif name == "check_flight_prices":
                r = httpx.post(self.CHECK_FLIGHT_PRICES_API_URL, json=args)
                return {**state, "tool_output": r.json()["data"]}

            elif name == "check_flight_reservation":
                r = httpx.post(self.CHECK_FLIGHT_RESERVATION_API_URL, json=args)
                return {**state, "tool_output": r.json()["data"]}

            elif name == "cancel_flight":
                r = httpx.post(self.CANCEL_FLIGHT_API_URL, json=args)
                return {**state, "tool_output": r.json()["data"]}

            elif name == "check_baggage_allowance":
                r = httpx.get(settings.BAGGAGE_STATUS_API_URL, params=args)
                return {**state, "tool_output": r.json()["data"]}

            else:
                return {**state, "tool_output": f"Unknown tool: {name}"}

        except Exception as e:
            return {**state, "tool_output": f"Tool call parsing failed: {str(e)}"}
