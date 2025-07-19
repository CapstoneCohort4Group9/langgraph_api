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
    # Add other intents here (up to 34 total)
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
    tool_block = "<tools>\n" + ",\n".join(tool_entries) + "\n</tools>"

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
