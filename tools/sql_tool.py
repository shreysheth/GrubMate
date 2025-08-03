from langchain.agents import Tool

from utils.sql.mongo_query_engine import mongo_tool_logic

mongo_db_sql_tool = Tool(
    name="mongo_db_sql_tool",
    func=mongo_tool_logic,
    description="""
Use this tool for handling **structured data operations** on the restaurant's order database. It leverages an LLM to interpret user intent and automatically **generate MongoDB queries** for CRUD operations, offering a seamless natural language interface to your database.

This tool connects directly to the MongoDB database and supports both **transactional actions** and **analytical queries** through LLM-generated commands, making it easy to interact with user orders using plain English.

Common use cases include:
    - Creating or updating **customer orders**
    - Canceling or removing **existing orders**
    - Fetching **order history** for a specific user
    - Finding **popular dishes** based on aggregated order data
    - Retrieving or modifying **menu items** stored in MongoDB

This tool is ideal for:
    - **Natural language-driven database interactions** without hardcoding queries
    - **Order management** tasks by support agents or automated chatbots
    - **Real-time analytics** and insights (e.g., most ordered item, order frequency)
    - Integrating database access into a **multi-tool LangChain agent**

It is not intended for unstructured document search, external APIs, or long-form text generation. Use it when you want to **translate user intents into MongoDB operations** and return structured, schema-validated results such as insert confirmations, query results, or update statuses.
"""
)