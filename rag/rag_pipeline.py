from pathlib import Path

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


KNOWLEDGE_BASE_PATH = Path("knowledge_base")
CHROMA_PATH = "chroma_db"


def load_documents():
    loader = PyPDFDirectoryLoader(str(KNOWLEDGE_BASE_PATH))
    documents = loader.load()

    print(f"Loaded {len(documents)} pages")

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    return chunks


def create_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vector_store(chunks):
    embeddings = create_embeddings()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    print("Documents stored in Chroma")

    return vector_store


def build_rag():
    documents = load_documents()
    chunks = split_documents(documents)
    vector_store = create_vector_store(chunks)

    return vector_store


if __name__ == "__main__":
    build_rag()