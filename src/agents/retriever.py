from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Assume faiss index is stored locally or in-memory
embedding = HuggingFaceEmbeddings()
faiss_index = FAISS.load_local("vector_index", embedding)


def retrieve_docs(query):
    return faiss_index.similarity_search(query, k=2)
