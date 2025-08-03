from langchain.agents import Tool

from utils.rag.chroma_query_engine import vector_db_context_search

vector_db_context_search_tool = Tool(
    name="vector_db_context_search",
    func=vector_db_context_search,
    description="""
Use this tool for answering **menu-related questions** where the user's query may involve interpreting context, understanding item descriptions, or inferring information from menu details. It is designed to respond to queries about food items, availability, ingredients, pricing, dietary categories, and recommendations based on a restaurant's uploaded menu.

This tool searches the menu using **semantic search via vector embeddings**, allowing it to retrieve the most relevant chunks of information based on meaning — not just keyword matching. The responses are grounded strictly in the content of the uploaded menu.

Common use cases include:
    - Asking about **ingredients or allergens** in a dish
    - Inquiring about **vegetarian or vegan options**
    - Finding **spicy, popular, or chef-recommended** dishes
    - Checking for **availability** of certain items or combos
    - Clarifying **portion sizes, combos, or price details**

This tool is ideal for:
    - **Natural, flexible menu queries** where users may not know exact item names
    - **Customer support** or chatbot flows that need to answer from the actual menu
    - Ensuring that answers are **accurate and compliant** with the uploaded data

It is not intended for taking orders, accessing user-specific data, or performing database writes. Use it when you want to **understand and respond based on the restaurant's official menu**, providing grounded, document-derived responses.
"""

)