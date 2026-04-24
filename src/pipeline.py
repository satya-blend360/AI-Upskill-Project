"""Complete pipeline: Fetch -> Filter."""
import asyncio
import os
from dotenv import load_dotenv
from src.orchestrator import FetchOrchestrator
from src.fetchers.fetcher_factory import FetcherFactory
from src.storage.markdown_storage import MarkdownStorage
from src.transformers.article_transformer import ArticleTransformer
from src.agents.news_filter_agent import NewsFilterAgent

# Load environment variables
load_dotenv()

async def run_pipeline():
    """
    Run complete pipeline.
    1. Fetch articles from all sources.
    2. Filter with AI agent for AI/ML relevance.
    """
    print("=" * 60)
    print("🚀 Complete AI News Pipeline: Fetch + Filter")
    print("=" * 60)
    
    # --- Step 1: Fetch ---
    print("\n📰 Step 1: Fetching articles...")
    
    # Setup services using the same pattern as main.py
    transformer = ArticleTransformer()
    storage = MarkdownStorage()
    fetchers = FetcherFactory.create_default_fetchers(
        transformer=transformer, 
        storage=storage
    )
    
    orchestrator = FetchOrchestrator(fetchers=fetchers, storage=storage)
    
    # Fetch from all sources (limiting for speed)
    raw_articles = await orchestrator.fetch_all(limit_per_source=5)
    print(f"✅ Fetched {len(raw_articles)} total articles.")
    
    if not raw_articles:
        print("❌ No articles fetched. Pipeline stopping.")
        return

    # --- Step 2: Filter with AI ---
    print("\n🤖 Step 2: Filtering with AI Agent...")
    agent = NewsFilterAgent()
    
    # Prepare data for the agent (subset for efficiency)
    articles_to_filter = []
    # Take a small batch to filter
    for art in raw_articles[:10]:
        articles_to_filter.append({
            "title": art.title,
            "url": art.url
        })
    
    # Execute agent (Template Method pattern from BaseAgent)
    results = await agent.execute(articles_to_filter)
    
    # --- Step 3: Display results ---
    print("\n" + "=" * 60)
    print("📊 AI Filtered Results (Relevant only):")
    print("=" * 60)
    
    relevant_count = 0
    if isinstance(results, list):
        for res in results:
            if res.get('relevant'):
                relevant_count += 1
                print(f"\n✅ {res['title']}")
                print(f"   Score: {res['relevance_score']}/10")
                print(f"   Reason: {res['reasoning']}")
    else:
        print(f"⚠️ Agent returned unexpected result format: {type(results)}")
    
    print(f"\n✨ Summary: Found {relevant_count} relevant AI/ML articles out of {len(articles_to_filter)} processed.")
    print("=" * 60)

if __name__ == "__main__":
    # Ensure Windows encoding
    os.environ["PYTHONUTF8"] = "1"
    asyncio.run(run_pipeline())
