from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type, List
import json
import sys
import os

# Add project root to path to import ingestion module
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ingestion.clickhouse_client import get_clickhouse_client

class ClickHouseQueryInput(BaseModel):
    query: str = Field(description="The SQL query to execute against ClickHouse. Use proper ClickHouse SQL syntax.")

class ClickHouseTool(BaseTool):
    name: str = "clickhouse_sql"
    description: str = """
    Execute SQL queries against the ClickHouse database.
    Use this to look up events, check table schemas, or find anomalies.
    The primary table is 'events'.
    Common columns: user_id, event, timestamp, properties.
    """
    args_schema: Type[BaseModel] = ClickHouseQueryInput

    def _run(self, query: str) -> str:
        try:
            client = get_clickhouse_client()
            print(f"\n[Agent Tool] Executing: {query}")
            
            # Run query
            result = client.query(query)
            
            # Limit results to prevent context window overflow
            MAX_ROWS = 20
            
            if not result.result_rows:
                return "Query executed successfully but returned 0 rows."
            
            rows = result.result_rows[:MAX_ROWS]
            
            # Format as simple text representation
            output = [f"Columns: {result.column_names}"]
            for row in rows:
                output.append(str(row))
            
            if len(result.result_rows) > MAX_ROWS:
                output.append(f"... ({len(result.result_rows) - MAX_ROWS} more rows truncated)")
                
            return "\n".join(output)
            
        except Exception as e:
            return f"Error executing query: {str(e)}"

    def _arun(self, query: str):
        # Async not implemented for this demo
        raise NotImplementedError("Async not implemented")
