from core.logger_config import logger
from utils.rag.chroma_ingestion import generate_data_store
from models.api_response import ApiResponseModel
from models.chroma_ingestion import ChromaIngestionSchema

from fastapi import APIRouter


router = APIRouter()


@router.post("/generate_store/", response_model=ApiResponseModel)
def process_data_file_endpoint(file_name: str):
    """Process uploaded data file and create vector database."""

    try:
        generate_data_store(file_name)
        return ApiResponseModel(
            status=200, message="Data file processed successfully.", is_error=False
        ).to_dict()

    except Exception as ex:
        logger.error(f"Error processing {file_name}: {ex}")
        return ApiResponseModel(
            message=f"Error processing {file_name}: {str(ex)}",
            status=500,
            is_error=True,
        ).to_dict()
