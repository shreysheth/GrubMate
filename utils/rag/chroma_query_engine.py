import json

from typing import Dict
import json

from core.logger_config import logger
from client.model_client import embedding_model as embedding_function
from core.settings import settings

from langchain_chroma import Chroma
from models.tool_response import RAGResponseModel, ToolResponseModel


def __get_vector_db_instance(store: str):
    """Prepare database for vector store."""

    logger.info(f"Preparing database for vector store: {store}")
    vector_store_dir_path = f"{settings.VECTOR_STORE_DIR}\{store}"
    vector_db = Chroma(
        persist_directory=vector_store_dir_path,
        embedding_function=embedding_function,
        collection_name=store,
        collection_metadata={"hnsw:space": "cosine"},
    )

    logger.info(f"Database initialized for vector store: {store}")

    return vector_db


def __search_vector_db(vector_db: Chroma, query: str, topK: int):
    """Search database for query."""

    logger.info(f"Searching database for query: {query}")
    results = vector_db.similarity_search_with_relevance_scores(query, k=topK)
    normalized_results = [(doc, (1 + score) / 2) for doc, score in results]
    filtered_results = [doc for doc in normalized_results]
    logger.info(f"Found {len(filtered_results)} relevant results for query: {query}")
    return filtered_results


def __prepare_context(filtered_results, query: str):
    """Prepare template for chat model."""

    logger.info(f"Preparing context for query: {query}")
    context = (
        "\n\n-----------------------------------------------------\n\n".join(
            [doc.page_content for doc, _ in filtered_results]
        )
        if filtered_results
        else None
    )

    return context


def vector_db_context_search(question: str):

    store = settings.VECTOR_STORE_NAME

    try:
        vector_db = __get_vector_db_instance(store=store)
        vector_results = __search_vector_db(
            vector_db=vector_db, query=question, topK=settings.TOP_K_CONTEXT_RESULTS
        )
        context = __prepare_context(filtered_results=vector_results, query=question)

        response = ToolResponseModel(
            data=[
                RAGResponseModel(
                    context=context, vector_results=vector_results
                ).to_dict()
            ],
            status=200,
            message="RAG query executed successfully.",
            is_error=False,
        ).to_dict()

        return json.dumps(response, indent=4)

    except Exception as e:
        logger.error(f"Error in querying rag: {e}")

        return json.dumps(
            ToolResponseModel(
                data=None,
                status=500,
                message=f"Error executing rag query: {str(e)}",
                is_error=True,
            ).to_dict(),
            indent=4,
        )
