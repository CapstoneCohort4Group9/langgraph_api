import json
from src import logger
from jinja2 import Template

INTENT_TOOL_MAP = {
    "search_flight": [
        {
            "name": "search_flight",
            "description": "search_flight(origin: str, destination: str, departure_date: str, return_date: str, trip_type: str, airline: str, passengers: number, non_stop: boolean, departure_window: object, max_price: number, airline_preferences: array, direct_only: boolean, max_price_per_passenger: number, flight_preference: str, classname: str, preferred_time: str, budget: number, preferred_departure_time: str, budget_per_person: number, airline_type: str, layover_preference: str, direct_flights_only: boolean, preferences: object) -> list - Search for available flights based on user preferences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "departure_date": {"type": "string"},
                    "return_date": {"type": "string"},
                    "trip_type": {"type": "string"},
                    "airline": {"type": "string"},
                    "passengers": {"type": "number"},
                    "non_stop": {"type": "boolean"},
                    "departure_window": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "string"},
                            "end": {"type": "string"},
                        },
                        "required": ["start", "end"],
                    },
                    "max_price": {"type": "number"},
                    "airline_preferences": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "direct_only": {"type": "boolean"},
                    "max_price_per_passenger": {"type": "number"},
                    "flight_preference": {"type": "string"},
                    "classname": {"type": "string"},
                    "preferred_time": {"type": "string"},
                    "budget": {"type": "number"},
                    "preferred_departure_time": {"type": "string"},
                    "budget_per_person": {"type": "number"},
                    "airline_type": {"type": "string"},
                    "layover_preference": {"type": "string"},
                    "direct_flights_only": {"type": "boolean"},
                    "preferences": {
                        "type": "object",
                        "properties": {"direct_flight": {"type": "boolean"}},
                        "required": ["direct_flight"],
                    },
                },
                "required": ["origin", "destination", "departure_date", "trip_type"],
            },
        }
    ],
    "book_flight": [
        {
            "name": "book_flight",
            "description": "book_flight(origin: str, destination: str, departure_date: str, return_date: str, trip_type: str, airline: str, price: number, passengers: number, non_stop: boolean, price_per_passenger: number, classname: str, direct_only: boolean, preferred_time: str, price_per_person: number, layover_preference: str, flight_id: str, contact: str) -> dict - Book a selected flight with detailed preferences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "departure_date": {"type": "string"},
                    "return_date": {"type": "string"},
                    "trip_type": {"type": "string"},
                    "airline": {"type": "string"},
                    "price": {"type": "number"},
                    "passengers": {"type": "number"},
                    "non_stop": {"type": "boolean"},
                    "price_per_passenger": {"type": "number"},
                    "classname": {"type": "string"},
                    "direct_only": {"type": "boolean"},
                    "preferred_time": {"type": "string"},
                    "price_per_person": {"type": "number"},
                    "layover_preference": {"type": "string"},
                    "flight_id": {"type": "string"},
                    "contact": {"type": "string"},
                },
                "required": [
                    "origin",
                    "destination",
                    "departure_date",
                    "trip_type",
                    "airline",
                    "price",
                    "passengers",
                    "contact",
                ],
            },
        }
    ],
    "confirm_booking": [
        {
            "name": "book_flight",
            "description": "book_flight(origin: str, destination: str, departure_date: str, return_date: str, trip_type: str, airline: str, price: number, passengers: number, non_stop: boolean, price_per_passenger: number, classname: str, direct_only: boolean, preferred_time: str, price_per_person: number, layover_preference: str, flight_id: str, contact: str) -> dict - Book a selected flight with detailed preferences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "departure_date": {"type": "string"},
                    "return_date": {"type": "string"},
                    "trip_type": {"type": "string"},
                    "airline": {"type": "string"},
                    "price": {"type": "number"},
                    "passengers": {"type": "number"},
                    "non_stop": {"type": "boolean"},
                    "price_per_passenger": {"type": "number"},
                    "classname": {"type": "string"},
                    "direct_only": {"type": "boolean"},
                    "preferred_time": {"type": "string"},
                    "price_per_person": {"type": "number"},
                    "layover_preference": {"type": "string"},
                    "flight_id": {"type": "string"},
                    "contact": {"type": "string"},
                },
                "required": [
                    "origin",
                    "destination",
                    "departure_date",
                    "trip_type",
                    "airline",
                    "price",
                    "passengers",
                    "contact",
                ],
            },
        }
    ],
    "provide_booking_info": [
        {
            "name": "book_flight",
            "description": "book_flight(origin: str, destination: str, departure_date: str, return_date: str, trip_type: str, airline: str, price: number, passengers: number, non_stop: boolean, price_per_passenger: number, classname: str, direct_only: boolean, preferred_time: str, price_per_person: number, layover_preference: str, flight_id: str, contact: str) -> dict - Book a selected flight with detailed preferences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "departure_date": {"type": "string"},
                    "return_date": {"type": "string"},
                    "trip_type": {"type": "string"},
                    "airline": {"type": "string"},
                    "price": {"type": "number"},
                    "passengers": {"type": "number"},
                    "non_stop": {"type": "boolean"},
                    "price_per_passenger": {"type": "number"},
                    "classname": {"type": "string"},
                    "direct_only": {"type": "boolean"},
                    "preferred_time": {"type": "string"},
                    "price_per_person": {"type": "number"},
                    "layover_preference": {"type": "string"},
                    "flight_id": {"type": "string"},
                    "contact": {"type": "string"},
                },
                "required": [
                    "origin",
                    "destination",
                    "departure_date",
                    "trip_type",
                    "airline",
                    "price",
                    "passengers",
                    "contact",
                ],
            },
        }
    ],
    "check_flight_status": [
        {
            "name": "check_flight_status",
            "description": "check_flight_status(flight_number: str, date: str, last_name: str, origin: str, destination: str, airline: str, confirmation_number: str, departure_airport: str, booking_reference: str, destination_airport: str, departure_city: str, arrival_city: str, arrival_airport: str, destination_city: str) -> dict - Check the current status of a flight using flight details and passenger information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_number": {"type": "string"},
                    "date": {"type": "string"},
                    "last_name": {"type": "string"},
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "airline": {"type": "string"},
                    "confirmation_number": {"type": "string"},
                    "departure_airport": {"type": "string"},
                    "booking_reference": {"type": "string"},
                    "destination_airport": {"type": "string"},
                    "departure_city": {"type": "string"},
                    "arrival_city": {"type": "string"},
                    "arrival_airport": {"type": "string"},
                    "destination_city": {"type": "string"},
                },
                "required": [
                    "flight_number",
                    "date",
                    "last_name",
                    "confirmation_number",
                ],
            },
        }
    ],
    "change_flight": [
        {
            "name": "change_flight",
            "description": "change_flight(confirmation_number: str, departure_city: str, arrival_city: str, desired_date_range: str, booking_reference: str, new_travel_date: str, new_date: str, new_time: str, origin: str, destination: str, new_destination: str, airline: str, new_departure_date: str, new_arrival_date: str, new_flight_date: str, new_flight_time: str, fare_type: str, modification_type: str, new_classname: str, change_type: str, flight_number: str, date: str, new_flight: str, change_fee: number, original_departure: str, original_arrival: str, preferred_new_dates: array, airline_preference: str, new_flight_number: str, new_departure_time: str, new_departure_date_offset_days: number) -> dict - Modify a previously booked flight with new travel preferences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "confirmation_number": {"type": "string"},
                    "departure_city": {"type": "string"},
                    "arrival_city": {"type": "string"},
                    "desired_date_range": {"type": "string"},
                    "booking_reference": {"type": "string"},
                    "new_travel_date": {"type": "string"},
                    "new_date": {"type": "string"},
                    "new_time": {"type": "string"},
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "new_destination": {"type": "string"},
                    "airline": {"type": "string"},
                    "new_departure_date": {"type": "string"},
                    "new_arrival_date": {"type": "string"},
                    "new_flight_date": {"type": "string"},
                    "new_flight_time": {"type": "string"},
                    "fare_type": {"type": "string"},
                    "modification_type": {"type": "string"},
                    "new_classname": {"type": "string"},
                    "change_type": {"type": "string"},
                    "flight_number": {"type": "string"},
                    "date": {"type": "string"},
                    "new_flight": {"type": "string"},
                    "change_fee": {"type": "number"},
                    "original_departure": {"type": "string"},
                    "original_arrival": {"type": "string"},
                    "preferred_new_dates": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "airline_preference": {"type": "string"},
                    "new_flight_number": {"type": "string"},
                    "new_departure_time": {"type": "string"},
                    "new_departure_date_offset_days": {"type": "number"},
                },
                "required": [
                    "confirmation_number",
                    "booking_reference",
                    "origin",
                    "destination",
                    "flight_number",
                    "date",
                ],
            },
        }
    ],
    "check_trip_prices": [
        {
            "name": "search_flight_prices",
            "description": "search_flight_prices(origin: str, destination: str, departure_date: str, return_date: str, departure_date_range: List[str], sort_by: str, limit: int, passengers: dict, direct_flight: bool, cabin_classname: str, preferences: dict, return_date_range: List[str], trip_type: str, nonstop: bool, travel_classname: str) -> list - Retrieve available flight pricing options with filters like date ranges, trip type, passengers, and travel class.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "departure_date": {"type": "string"},
                    "return_date": {"type": "string"},
                    "departure_date_range": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "sort_by": {"type": "string"},
                    "limit": {"type": "number"},
                    "passengers": {
                        "type": "object",
                        "properties": {
                            "adults": {"type": "number"},
                            "children": {"type": "number"},
                            "infants": {"type": "number"},
                        },
                        "additionalProperties": True,
                    },
                    "direct_flight": {"type": "boolean"},
                    "cabin_classname": {"type": "string"},
                    "preferences": {"type": "object", "additionalProperties": True},
                    "return_date_range": {"type": "array", "items": {"type": "string"}},
                    "trip_type": {"type": "string"},
                    "nonstop": {"type": "boolean"},
                    "travel_classname": {"type": "string"},
                },
                "required": [
                    "origin",
                    "destination",
                    "departure_date",
                    "trip_type",
                    "passengers",
                ],
            },
        }
    ],
    "check_flight_prices": [
        {
            "name": "check_flight_prices",
            "description": "check_flight_prices(origin: str, destination: str, departure_date: str, return_date: str, passengers: dict, preferred_airlines: list, departure_date_range: list, return_date_range: list) -> list - Retrieve flight prices based on route, dates, passenger count, and airline preferences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "departure_date": {"type": "string"},
                    "return_date": {"type": "string"},
                    "passengers": {
                        "type": "object",
                        "properties": {"adults": {"type": "number"}},
                    },
                    "preferred_airlines": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "departure_date_range": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "return_date_range": {"type": "array", "items": {"type": "string"}},
                },
                "required": [
                    "origin",
                    "destination",
                    "departure_date",
                    "passengers",
                ],
            },
        }
    ],
    "check_flight_reservation": [
        {
            "name": "check_flight_reservation",
            "description": "check_flight_reservation(...) -> dict - Check details of a flight reservation based on name, booking reference, travel dates, and preferences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "last_name": {"type": "string"},
                    "departure_city": {"type": "string"},
                    "arrival_city": {"type": "string"},
                    "full_name": {"type": "string"},
                    "destination_city": {"type": "string"},
                    "booking_reference": {"type": "string"},
                    "email": {"type": "string"},
                    "first_name": {"type": "string"},
                    "date_of_birth": {"type": "string"},
                    "flight_number": {"type": "string"},
                    "departure_date": {"type": "string"},
                    "return_date": {"type": "string"},
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "flight_date_range": {
                        "type": "object",
                        "properties": {
                            "start_date": {"type": "string"},
                            "end_date": {"type": "string"},
                        },
                    },
                    "flight_date": {"type": "string"},
                    "travel_date": {"type": "string"},
                    "passenger_count": {"type": "number"},
                    "confirmation_number": {"type": "string"},
                    "date_range": {
                        "type": "object",
                        "properties": {
                            "start_date": {"type": "string"},
                            "end_date": {"type": "string"},
                        },
                    },
                    "travel_dates": {"type": "array", "items": {"type": "string"}},
                    "travel_start_date": {"type": "string"},
                    "travel_end_date": {"type": "string"},
                    "date_of_travel": {"type": "string"},
                    "travelers": {"type": "number"},
                    "preferences": {
                        "type": "object",
                        "properties": {"direct_flight": {"type": "boolean"}},
                    },
                    "travel_month_year": {"type": "string"},
                    "trip_date": {"type": "string"},
                    "date": {"type": "string"},
                },
                "required": [
                    "last_name",
                    "booking_reference",
                    "departure_date",
                    "origin",
                    "destination",
                ],
            },
        }
    ],
    "cancel_flight": [
        {
            "name": "cancel_booking",
            "description": "cancel_booking(confirmation_number: str) -> dict - Cancel a flight reservation using the booking confirmation number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "confirmation_number": {
                        "type": "string",
                        "description": "The unique booking confirmation number associated with the reservation to be canceled.",
                    }
                },
                "required": ["confirmation_number"],
            },
        }
    ],
    "check_baggage_allowance": [
        {
            "name": "query_policy_rag_db",
            "description": "query_policy_rag_db(input: str) -> dict - This function is best suited for any policy and document releated customer query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The natural language query or question to be answered.",
                    }
                },
                "required": ["query"],
            },
        }
    ],
}


def get_tool_prompt_for_intent(intent: str, messages) -> str:
    tools = INTENT_TOOL_MAP.get(intent, [])
    tool_entries = []

    for tool in tools:
        entry = (
            "{\n"
            '  "type": "function",\n'
            '  "function": {\n'
            f'    "name": "{tool["name"]}",\n'
            f'    "description": "{tool["description"]}",\n'
            f'    "parameters": {tool["parameters"]}\n'
            "  }\n"
            "}"
        )
        tool_entries.append(entry)
    logger.info(
        json.dumps(
            {
                "message": f"Generated tool entries for intent '{intent}'",
                "intent": intent,
                "tool_entries": tool_entries,
            },
            indent=2,
        )
    )
    tool_block = 'You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags. You may call one or more functions to assist with the user query. Don\'t make assumptions about what values to plug into functions. Here are the available tools: <tools> {"type": "function", "function": {"name": "query", "description": "query(query: str) - query(input: str) -> dict - This function is best suited for any policy and document releated customer query. call this for check_baggage_allowance.\n\n    Args:\n        query(str): The natural language query or question to be answered.", "parameters": {"properties": {"query": {"description": "The natural language query or question to be answered.", "type": "string"}}, "required": ["query"], "type": "object"}} </tools>Use the following pydantic model json schema for each tool call you will make: {"properties": {"name": {"title": "Name", "type": "string"}, "arguments": {"title": "Arguments", "type": "object"}}, "required": ["name", "arguments"], "title": "FunctionCall", "type": "object"}}\nFor each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:\n<tool_call>\n{"name": <function-name>, "arguments": <args-dict>}\n</tool_call>'

    # messages.append({"role": "system", "content": tool_block})
    template_str = """{%- macro json_to_python_type(json_spec) %}
{%- set basic_type_map = {
    "string": "str",
    "number": "float",
    "integer": "int",
    "boolean": "bool"
} %}

{%- if basic_type_map[json_spec.type] is defined %}
    {{- basic_type_map[json_spec.type] }}
{%- elif json_spec.type == "array" %}
    {{- "list[" +  json_to_python_type(json_spec|items) + "]"}}
{%- elif json_spec.type == "object" %}
    {%- if json_spec.additionalProperties is defined %}
        {{- "dict[str, " + json_to_python_type(json_spec.additionalProperties) + ']'}}
    {%- else %}
        {{- "dict" }}
    {%- endif %}
{%- elif json_spec.type is iterable %}
    {{- "Union[" }}
    {%- for t in json_spec.type %}
      {{- json_to_python_type({"type": t}) }}
      {%- if not loop.last %}
        {{- "," }} 
    {%- endif %}
    {%- endfor %}
    {{- "]" }}
{%- else %}
    {{- "Any" }}
{%- endif %}
{%- endmacro %}


{{- bos_token }}
{{- '<|im_start|>system
' }}
{{- "You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags. You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug into functions. Here are the available tools: <tools> " }}
{%- for tool in tools %}
    {%- if tool.function is defined %}
        {%- set tool = tool.function %}
    {%- endif %}
    {{- '{"type": "function", "function": ' }}
    {{- '{"name": "' + tool.name + '", ' }}
    {{- '"description": "' + tool.name + '(' }}
    {%- for param_name, param_fields in tool.parameters.properties|items %}
        {{- param_name + ": " + json_to_python_type(param_fields) }}
        {%- if not loop.last %}
            {{- ", " }}
        {%- endif %}
    {%- endfor %}
    {{- ")" }}
    {%- if tool.return is defined %}
        {{- " -> " + json_to_python_type(tool.return) }}
    {%- endif %}
    {{- " - " + tool.description + "\n\n" }}
    {%- for param_name, param_fields in tool.parameters.properties|items %}
        {%- if loop.first %}
            {{- "    Args:\n" }}
        {%- endif %}
        {{- "        " + param_name + "(" + json_to_python_type(param_fields) + "): " + param_fields.description|trim }}
    {%- endfor %}
    {%- if tool.return is defined and tool.return.description is defined %}
        {{- "\n    Returns:\n        " + tool.return.description }}
    {%- endif %}
    {{- '"' }}
    {{- ', "parameters": ' }}
    {%- if tool.parameters.properties | length == 0 %}
        {{- "{}" }}
    {%- else %}
        {{- tool.parameters|tojson }}
    {%- endif %}
    {{- "}" }}
    {%- if not loop.last %}
        {{- "\n" }}
    {%- endif %}
{%- endfor %}
{{- " </tools>" }}
{{- 'Use the following pydantic model json schema for each tool call you will make: {"properties": {"name": {"title": "Name", "type": "string"}, "arguments": {"title": "Arguments", "type": "object"}}, "required": ["name", "arguments"], "title": "FunctionCall", "type": "object"}}
' }}
{{- "For each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:
" }}
{{- "<tool_call>
" }}
{{- '{"name": <function-name>, "arguments": <args-dict>}
' }}
{{- '</tool_call><|im_end|>\n' }}
{%- for message in messages %}
    {%- if message.role == "user" or message.role == "system" or (message.role == "assistant" and message.tool_calls is not defined) %}
        {{- '<|im_start|>' + message.role + '\n' + message.content + '<|im_end|>' + '\n' }}
    {%- elif message.role == "assistant" %}
        {{- '<|im_start|>' + message.role }}
    {%- for tool_call in message.tool_calls %}
       {{- '
<tool_call>
' }}           {%- if tool_call.function is defined %}
                {%- set tool_call = tool_call.function %}
            {%- endif %}
            {{- '{' }}
            {{- '"name": "' }}
            {{- tool_call.name }}
            {{- '"' }}
            {{- ', '}}
            {%- if tool_call.arguments is defined %}
                {{- '"arguments": ' }}
                {%- if tool_call.arguments is string %}
                    {{- tool_call.arguments }}
                {%- else %}
                    {{- tool_call.arguments|tojson }}
                {%- endif %}
            {%- endif %}
             {{- '}' }}
            {{- '\n</tool_call>' }}
    {%- endfor %}
        {{- '<|im_end|>\n' }}
    {%- elif message.role == "tool" %}
        {%- if loop.previtem and loop.previtem.role != "tool" %}
            {{- '<|im_start|>tool\n' }}
        {%- endif %}
        {{- '<tool_response>\n' }}
        {{- message.content }}
        {%- if not loop.last %}
            {{- '\n</tool_response>\n' }}
        {%- else %}
            {{- '\n</tool_response>' }}
        {%- endif %}
        {%- if not loop.last and loop.nextitem.role != "tool" %}
            {{- '<|im_end|>' }}
        {%- elif loop.last %}
            {{- '<|im_end|>' }}
        {%- endif %}
    {%- endif %}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|im_start|>assistant\n' }}
{%- endif %}
"""
    template = Template(template_str)
    return template.render(messages=messages, tools=tools)
