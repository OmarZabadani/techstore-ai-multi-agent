from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "chroma_db"


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_store = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)


retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)


def retrieve_documents(query):
    return retriever.invoke(query)

