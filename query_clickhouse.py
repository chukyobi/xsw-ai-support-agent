import sys
import os

# Add backend to path so Django settings can be loaded
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from ingestion.clickhouse_client import get_clickhouse_client

def print_table(rows, headers):
    if not rows:
        return
    
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))
    
    # Create format string
    fmt = " | ".join([f"{{:<{w}}}" for w in widths])
    
    # Print header
    print(fmt.format(*headers))
    print("-" * (sum(widths) + 3 * (len(headers) - 1)))
    
    # Print rows
    for row in rows:
        print(fmt.format(*[str(val) for val in row]))

def run_query(query):
    try:
        client = get_clickhouse_client()
        result = client.query(query)
        
        print(f"\nQuery: {query}\n")
        
        if result.result_rows:
            print_table(result.result_rows, result.column_names)
            print(f"\nTotal rows: {len(result.result_rows)}")
        else:
            print("No results found.")
            
    except Exception as e:
        print(f"Error running query: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        # Default query if none provided
        query = "SELECT * FROM events LIMIT 5"
        print("No query provided. Running default:")
    
    run_query(query)
