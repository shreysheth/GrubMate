from fastapi import APIRouter, Depends
from datetime import datetime

from models.api_response import ApiResponseModel
from models.chat import ChatModel, MessageModel, ThreadModel, ChatResponseModel
from utils.agent.agent_executer import execute_agent
from core.logger_config import logger
from utils.sql.mongo_operations import create_document
from utils.shared.uuid import generate_message_uuid, generate_thread_uuid

router = APIRouter()


@router.post("/chat", response_model=ApiResponseModel)
def chat_endpoint(chatObj: ChatModel):
    """Endpoint to handle chat requests."""

    try:

        logger.info(f"Received chat input: {chatObj.question}")
        response = execute_agent(chatObj.question, chatObj.user_id)

        logger.info(f"Chat response: {response}")

        if not chatObj.thread_id:
            thread = create_document(
                "threads", ThreadModel(user_id=chatObj.user_id, created_at=datetime.now()).to_dict()
            )
            chatObj.thread_id = thread["inserted_id"]

        message = create_document(
            "messages",
            MessageModel(
                thread_id=chatObj.thread_id, message=response["output"], created_at=datetime.now()
            ).to_dict(),
        )
        chat_response = ChatResponseModel(
            message=response["output"],
            user_id=chatObj.user_id,
            thread_id=chatObj.thread_id,
            message_id=message["inserted_id"],
        ).to_dict()
        return ApiResponseModel(
            data=chat_response,
            message="Chat processed successfully",
            status=200,
            is_error=False,
        ).to_dict()

    except Exception as e:
        logger.error(f"Error processing chat: {e}")

        return ApiResponseModel(
            status=500, message=f"Error processing chat: {str(e)}", is_error=True
        ).to_dict()
