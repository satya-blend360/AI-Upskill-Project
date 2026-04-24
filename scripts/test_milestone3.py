import os
import asyncio
from dotenv import load_dotenv
from src.agents.news_filter_agent import NewsFilterAgent

# Load environment variables
load_dotenv()

async def main():
    print("🚀 Milestone 3: Testing Agent with Tools\n")
    
    # 1. Initialize the agent
    agent = NewsFilterAgent()
    
    # 2. Sample articles for testing
    # Including an ambiguous title to see if it uses the tool
    test_articles = [
        {
            "title": "OpenAI releases GPT-4o-mini",
            "url": "https://openai.com/blog/gpt-4o-mini"
        },
        {
            "title": "A Breakthrough in Modern Computing",
            "url": "https://example.com/breakthrough"
        }
    ]
    
    print(f"Feeding {len(test_articles)} articles to the agent...")
    
    # 3. Run filtering
    results = await agent.execute(test_articles)
    
    # 4. Show results
    print("\n--- Filtering Results ---")
    import json
    print(json.dumps(results, indent=2))
    
    if any(r.get('relevant') for r in results):
        print("\n✅ Milestone 3 Success: Agent filtered articles and potentially used tools!")
    else:
        print("\n⚠️ No relevant articles found. Check logic or model output.")

if __name__ == "__main__":
    # Ensure Windows encoding
    os.environ["PYTHONUTF8"] = "1"
    asyncio.run(main())
