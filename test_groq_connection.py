#!/usr/bin/env python3
"""
Quick test to verify Groq API connection
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_groq():
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        return False
    
    print(f"✓ GROQ_API_KEY found: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        from langchain_groq import ChatGroq
        
        print("Testing Groq API connection...")
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )
        
        # Simple test message
        response = llm.invoke("Say 'Hello, I am working!' and nothing else.")
        print(f"✓ Groq API is working!")
        print(f"Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Groq API connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_groq()
