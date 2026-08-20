from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "chroma_db"


def get_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )


def get_retriever():
    vector_store = get_vector_store()

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )


def retrieve_documents(query):
    retriever = get_retriever()

    return retriever.invoke(query)


if __name__ == "__main__":
    documents = retrieve_documents("What is the return policy?")

    for i, document in enumerate(documents, 1):
        print(f"\n--- Result {i} ---")
        print(document.page_content)