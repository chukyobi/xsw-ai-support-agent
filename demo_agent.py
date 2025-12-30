
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
try:
    from agent.investigation_agent import get_investigation_agent
except ImportError:
    # Fallback if running directly from backend dir
    sys.path.append(os.path.dirname(__file__))
    from agent.investigation_agent import get_investigation_agent

def main():
    print("=== XSW AI Support Agent Demo ===\n")
    
    # Check for API Key
    if not os.environ.get("GROQ_API_KEY"):
        print(" Error: GROQ_API_KEY environment variable not found.")
        print("\nTo run this agent, you must provide a Groq API Key.")
        print("Please export it in your terminal:")
        print('  export GROQ_API_KEY="gsk_..."')
        print("\nThen run this script again.")
        return

    print("Initializing Agent...")
    try:
        agent = get_investigation_agent()
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return

    # Mock user complaint
    user_id = "user_42"  # Let's hope this user exists in our random data or we pick one that does
    print(f"\nScenario: User '{user_id}' reported 'I keep getting errors when trying to pay'.")
    print("Agent is investigating...\n")
    
    query = f"Investigate why user '{user_id}' is facing payment issues. Find the root cause from the events table."
    
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": query}]})
        print("\n=== Agent Analysis ===")
        # LangGraph returns messages in the result
        final_message = result['messages'][-1]
        print(final_message.content)
        print("======================")
    except Exception as e:
        print(f"\nAgent execution failed: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
