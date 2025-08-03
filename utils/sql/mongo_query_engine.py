import json
from typing import Dict

from langchain import PromptTemplate
from langchain.chains import LLMChain
from prompts import MONGO_QUERY_GENERATION_PROMPT

from client.mongo_client import db
from client.model_client import llm
from models.tool_response import ToolResponseModel, MongoQueryResponseModel
from core.logger_config import logger


prompt_template = PromptTemplate(
    input_variables=["question", "user_id"], template=MONGO_QUERY_GENERATION_PROMPT
)

query_chain = LLMChain(llm=llm, prompt=prompt_template)


def __generate_mongo_query(question: str, user_id:str):
    """Generate a MongoDB query from a natural language question."""

    logger.info(f"Generating MongoDB query for question: {question}")
    query = query_chain.run({"question": question, "user_id": user_id})

    logger.info(f"Generated MongoDB query: {query.strip()}")

    return query.strip()


def __execute_mongo_query(query: str):
    """Execute a MongoDB query and return the results."""

    logger.info("setting up local context for query execution.")
    local_context = {"db": db}

    logger.info("Executing query in local context.")
    exec(f"result = {query}", {}, local_context)

    logger.info("Query executed successfully.")
    result = local_context["result"]

    logger.info(f"Query result: {result}")

    return result


def mongo_tool_logic(input: str):

    try:
        input_dict: Dict = json.loads(input)
        question = input.get("question")
        user_id = input.get("user_id")
        query = __generate_mongo_query(question, user_id)
        result = __execute_mongo_query(query)

        response = ToolResponseModel(
            data=[MongoQueryResponseModel(results=result).to_dict()],
            status=200,
            message="Mongo query executed successfully.",
            is_error=False,
        ).to_dict()

        return json.dumps(response, indent=4)

    except Exception as e:
        logger.error(f"Error executing mongo query: {e}")

        return json.dumps(
            ToolResponseModel(
                data=None,
                status=500,
                message=f"Error executing mongo query: {str(e)}",
                is_error=True,
            ).to_dict(),
            indent=4,
        )
