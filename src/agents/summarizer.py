from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI

template = "Detail the following conversation:\n{query}"
prompt = PromptTemplate.from_template(template)
llm = ChatOpenAI()

chain = llm | prompt


def summarize(state):
    print("Running summarization with state:", state)
    # result = chain.invoke({"query": state["intentMessage"]})
    # print("DEBUG: Summarization result:", result)
    # return {**state, "text": result["text"]}
    return {**state, "summary": state["intentMessage"]}
