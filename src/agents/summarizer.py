from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from config.settings import Config

template = "Detail the following conversation:\n{query}"
prompt = PromptTemplate.from_template(template)
llm = ChatOpenAI()

chain = LLMChain(llm=llm, prompt=prompt)


def summarize(state):
    print("Running summarization with state:", state)
    result = chain.invoke({"query": state["intentMessage"]})
    print("DEBUG: Summarization result:", result)
    return {**state, "text": result["text"]}
