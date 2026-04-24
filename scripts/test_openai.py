import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_openai_key():
    # Try to get the key from the command line argument first, then from the environment
    api_key = sys.argv[1] if len(sys.argv) > 1 else os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("Error: OPENAI_API_KEY not found in .env or provided as an argument.")
        print("Usage: python scripts/test_openai.py <your_openai_api_key>")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    
    try:
        print("Testing OpenAI API key...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Connection successful!' if you can read this."}
            ],
            max_tokens=10
        )
        print(f"Response from OpenAI: {response.choices[0].message.content.strip()}")
        print("Success! Your OpenAI API key is valid.")
    except Exception as e:
        print(f"Error connecting to OpenAI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_openai_key()
