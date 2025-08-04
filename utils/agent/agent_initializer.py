from langchain.agents import create_react_agent
from tools.rag_tool import vector_db_context_search_tool
from tools.sql_tool import mongo_db_sql_tool
from client.model_client import llm
from core.logger_config import logger
from langchain_core.prompts import PromptTemplate
from prompts import AGENT_PROMPT

logger.info("Initializing agent with vector_db_context_search_tool and mongo_db_sql_tool")

prompt = PromptTemplate.from_template(AGENT_PROMPT)
tools = [vector_db_context_search_tool, mongo_db_sql_tool]

agent = create_react_agent(llm, tools, prompt)

logger.info("Agent initialized successfully")