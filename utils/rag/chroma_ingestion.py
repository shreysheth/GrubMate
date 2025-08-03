import os

from core.settings import settings
from core.logger_config import logger
from client.model_client import embedding_model, tokenizer

from langchain_docling.loader import ExportType, DoclingLoader
from docling.chunking import HybridChunker
from langchain_chroma import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.documents import Document


def ensure_directories():
    """Ensure required directories exist."""

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)


def __load_documents(file_path):
    """Load chunked documents from file."""

    logger.info(f"Loading documents from {file_path}.")
    hybridChunker = HybridChunker(tokenizer=tokenizer)
    logger.info("Hybrid chunker initialized")
    loader = DoclingLoader(
        file_path=file_path, export_type=ExportType.DOC_CHUNKS, chunker=hybridChunker
    )
    documents = loader.load()
    logger.info(f"Loaded {len(documents)} documents.")

    return documents


def __create_chunks(documents: list[Document], file_name: str):
    """Create chunks from documents."""
    for chunk in documents:
        chunk.metadata["file_name"] = file_name
        chunk.metadata["page_number"] = chunk.metadata["dl_meta"]["doc_items"][0][
            "prov"
        ][0]["page_no"]

    chunks = filter_complex_metadata(documents)

    logger.info(f"Created {len(chunks)} chunks.")
    return chunks


def __save_to_chroma(chunks: list[Document], chroma_path: str, store_name: str):
    """Save chunks to Chroma."""

    vector_store = Chroma(
        persist_directory=chroma_path,
        embedding_function=embedding_model,
        collection_name=store_name,
    )
    vector_store.add_documents(chunks)
    logger.info(f"Saved {len(chunks)} chunks to {chroma_path}.")


def generate_data_store(file_name: str):
    """Generate data store from uploaded file."""

    logger.info(
        f"Generating data store from uploaded file: {file_name}."
    )
    ensure_directories()
    upload_file_path = f"{settings.UPLOAD_DIR}\{file_name}"
    vector_store_dir_path = f"{settings.VECTOR_STORE_DIR}\{settings.VECTOR_STORE_NAME}"
    documents = __load_documents(upload_file_path)
    chunks = __create_chunks(documents, file_name)
    __save_to_chroma(
        chunks=chunks,
        chroma_path=vector_store_dir_path,
        store_name=settings.VECTOR_STORE_NAME
    )

    logger.info(f"Data store generated for uploaded file: {file_name}.")
