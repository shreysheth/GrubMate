from langchain.agents import AgentExecutor

from utils.agent.agent_initializer import agent
from core.logger_config import logger
from tools.rag_tool import vector_db_context_search_tool
from tools.sql_tool import mongo_db_sql_tool

def execute_agent(question:str, user_id:str):
    """Execute the agent with the provided input data."""

    logger.info(f"Executing agent with question: {question}")
    tools = [vector_db_context_search_tool, mongo_db_sql_tool]
    
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    response = agent_executor.invoke({"input" : question, "user_id": user_id})

    return response