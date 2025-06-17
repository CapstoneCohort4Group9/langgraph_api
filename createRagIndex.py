from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Load PDF from local file
pdf_path = "ragDocs/Airline_Regulations_v1.0.pdf"  # 🔁 Replace with your file path
loader = PyMuPDFLoader(pdf_path)
documents = loader.load()

# Optional: Chunk large documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)


# Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create FAISS index
faiss_index = FAISS.from_documents(docs, embedding_model)

# Save index locally
faiss_index.save_local("my_faiss_index")
