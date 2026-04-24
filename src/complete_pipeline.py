"""Complete multi-agent pipeline with MCP."""
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from src.orchestrator import FetchOrchestrator
from src.fetchers.fetcher_factory import FetcherFactory
from src.storage.markdown_storage import MarkdownStorage
from src.transformers.article_transformer import ArticleTransformer
from src.agents.news_filter_agent import NewsFilterAgent
from src.agents.summarizer_agent import SummarizerAgent
from src.agents.writer_agent import WriterAgent
from src.database.db_manager import DatabaseManager

# Load environment variables
load_dotenv()

async def run_complete_pipeline():
    """
    Run the complete multi-agent pipeline:
    1. Fetch articles from all sources.
    2. Store them in the SQLite database.
    3. Filter articles for AI/ML relevance using NewsFilterAgent.
    4. Summarize relevant articles by topic using SummarizerAgent.
    5. Write a daily newsletter from summaries using WriterAgent.
    """
    print("=" * 70)
    print("🚀 Complete AI News Intelligence Pipeline: Fetch -> DB -> Filter -> Summary -> Write")
    print("=" * 70)
    
    # --- Step 1: Fetch ---
    print("\n📰 Step 1: Fetching articles...")
    transformer = ArticleTransformer()
    storage = MarkdownStorage()
    fetchers = FetcherFactory.create_default_fetchers(transformer=transformer, storage=storage)
    orchestrator = FetchOrchestrator(fetchers=fetchers, storage=storage)
    raw_articles = await orchestrator.fetch_all(limit_per_source=10)
    print(f"✅ Fetched {len(raw_articles)} total articles.")
    
    # --- Step 2: Store in Database ---
    print("\n💾 Step 2: Storing in database...")
    db = DatabaseManager()
    await db.initialize()
    for art in raw_articles:
        await db.insert_article({
            "title": art.title,
            "url": art.url,
            "source": art.source,
            "published_at": art.published_at.isoformat(),
            "summary": art.summary
        })
    print("✅ Database updated.")
    
    # --- Step 3: Filter ---
    print("\n🤖 Step 3: Filtering with AI NewsFilterAgent...")
    filter_agent = NewsFilterAgent()
    # Use the first 20 from DB for processing
    db_articles = await db.query_articles(limit=20)
    articles_to_filter = [{"title": a["title"], "url": a["url"]} for a in db_articles]
    filtered_results = await filter_agent.execute(articles_to_filter)
    
    # Extract only relevant ones
    relevant_articles = [res for res in filtered_results if isinstance(res, dict) and res.get("relevant")]
    print(f"✅ Found {len(relevant_articles)} relevant AI/ML articles.")
    
    if not relevant_articles:
        print("❌ No relevant articles found. Pipeline stopping.")
        return

    # --- Step 4: Summarize ---
    print("\n📝 Step 4: Summarizing with SummarizerAgent...")
    summarizer = SummarizerAgent()
    topic_summaries = await summarizer.execute(relevant_articles)
    print(f"✅ Summarized into {len(topic_summaries)} topics.")
    
    # --- Step 5: Write Newsletter ---
    print("\n✍️  Step 5: Writing Newsletter with WriterAgent...")
    writer = WriterAgent()
    newsletter_text = await writer.execute(topic_summaries)
    
    # Save final output
    output_dir = os.path.join("data", "output")
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(output_dir, f"newsletter_{date_str}.md")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(newsletter_text)
    
    print("\n" + "=" * 70)
    print(f"✨ SUCCESS: Newsletter generated and saved to {file_path}")
    print("=" * 70)
    print(f"\nFinal Newsletter Preview:\n{newsletter_text[:300]}...")

if __name__ == "__main__":
    # Ensure Windows encoding
    os.environ["PYTHONUTF8"] = "1"
    asyncio.run(run_complete_pipeline())
