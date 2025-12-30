import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from .clickhouse_tool import ClickHouseTool

def get_investigation_agent():
    # check for api key
    if not os.environ.get("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    # 1. Initialize LLM (Llama 3 via Groq)
    # Using llama-3.3-70b-versatile for better reasoning capabilities on complex SQL tasks
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=0
    )

    # 2. Define Tools
    tools = [ClickHouseTool()]

    # 3. System prompt for the agent
    system_message = """You are an expert Support Engineer Agent.
Your goal is to diagnose user issues by querying the ClickHouse database.

The database has a table called 'events'.
Key columns:
- event_id (String)
- user_id (String)
- event (String): e.g., 'page_view', 'payment_failed', 'add_to_cart'
- timestamp (DateTime)
- properties (String): JSON string containing details like error_code, amount, browser, etc.

Process:
1. Understand the user's complaint.
2. Formulate a hypothesis (e.g., "Maybe they have failed payments").
3. Use the 'clickhouse_sql' tool to query data. 
   - Tip: ALWAYS filter by the specific user_id if provided.
   - Tip: Check the 'properties' column for error messages.
4. Analyze the returned data.
5. Provide a Root Cause Analysis.

Don't give up until you find concrete evidence in the data."""

    # 4. Create Agent using create_react_agent (LangChain 1.2.0+ with LangGraph)
    agent_executor = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_message
    )
    
    return agent_executor

