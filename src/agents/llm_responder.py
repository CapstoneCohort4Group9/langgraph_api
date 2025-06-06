from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

llm = ChatOpenAI(temperature=0)


def generate_reply(query, docs, chat_history):
    context = "\n\n".join([doc.page_content for doc in docs])
    system_prompt = f"Context: {context}\nChat History: {chat_history}\nUser: {query}"
    response = llm.predict(system_prompt)
    return response
