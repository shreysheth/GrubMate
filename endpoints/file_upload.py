from fastapi import File, UploadFile, APIRouter
from pathlib import Path

from core.settings import settings
from core.logger_config import logger
from models.api_response import ApiResponseModel

router = APIRouter()


@router.post("/upload_file/", response_model=ApiResponseModel)
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file.
    The file will be saved in the specified upload directory.
    """

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_location = upload_dir / file.filename

    try:
        logger.info(f"Saving file to {file_location}")
        with open(file_location, "wb") as f:
            f.write(await file.read())

        logger.info(f"File {file.filename} uploaded successfully.")

        return ApiResponseModel(
            status=200,
            message=f"File '{file.filename}' uploaded successfully.",
            is_error=False,
        ).to_dict()

    except Exception as e:
        logger.error(f"Error saving file {file.filename}: {e}")
        return ApiResponseModel(
            status=500, message=f"Error saving file: {str(e)}", is_error=True
        ).to_dict()
