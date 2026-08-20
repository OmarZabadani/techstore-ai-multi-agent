from pathlib import Path

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitter import RecursiveCharacterTextSplitter

Knowledge_Base_Path = Path("knowledge_base")


def load_document():
    loader = PyPDFDirectoryLoader(str(Knowledge_Base_Path))
    documents = loader.load()

    print(f"Loaded{len(documents)} Document pages")

    return documents

def split_document(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    return chunks

