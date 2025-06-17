from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Assume faiss index is stored locally or in-memory
embedding = HuggingFaceEmbeddings()
faiss_index = FAISS.load_local(
    "my_faiss_index", embedding, allow_dangerous_deserialization=True
)


def getRetriever():
    return faiss_index.as_retriever(search_kwargs={"k": 3})
