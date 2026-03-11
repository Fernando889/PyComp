# Import Libraries
import os
import glob
import torch
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import login
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Create HF_TOKEN and EMBEDDING_MODELS
load_dotenv(override=True)
device = "cuda" if torch.cuda.is_available() else "cpu"
HF_TOKEN = os.getenv("HF_TOKEN")
EMBEDDING_MODELS = HuggingFaceEmbeddings(
    model_name=os.getenv("EMBEDDING_MODELS"),
    model_kwargs={"device": device},
    encode_kwargs={"normalize_embeddings": True}
)

login(token=HF_TOKEN,
      add_to_git_credential=True)

# Create path for DB_NAME and KNOWLEDGE_BASE
DB_NAME = str(Path(__file__).parent.parent/"vector_db")
KNOWLEDGE_BASE = str(Path(__file__).parent.parent/"python_doc_md")


def fetch_documents():  # Create fetch_documents function
    documents = []
    folders = glob.glob(str(Path(KNOWLEDGE_BASE)/"*"))
    for folder in folders:
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(
            path=folder,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        folder_docs = loader.load()
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            doc.page_content = f"{doc_type}\n\n{doc.page_content}"
            documents.append(doc)

    return documents


def create_chunks(documents):  # Create create_chunks function
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
    )
    chunks = text_splitter.split_documents(documents=documents)
    return chunks


def create_embedding(chunks):
    if os.path.exists(DB_NAME):
        Chroma(persist_directory=DB_NAME,
               embedding_function=EMBEDDING_MODELS).delete_collection()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=EMBEDDING_MODELS,
        persist_directory=DB_NAME
    )
    collection = vector_store._collection
    count = collection.count()
    sample_embedding = collection.get(
        limit=1,
        include=["embeddings"]
    )["embeddings"][0]
    dimension = len(sample_embedding)

    print(
        f"There are: {count:,} vector with {dimension:,} dimension in vector store")
    return vector_store


# Run Ingestion
if __name__ == "__main__":
    documents = fetch_documents()
    chunks = create_chunks(documents=documents)
    create_embedding(chunks=chunks)
    print(f"Ingestion Complete")
