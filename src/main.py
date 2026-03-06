"""Main entry point (SOLID Refactor)."""
import asyncio
import sys
from src.orchestrator import FetchOrchestrator
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.fetchers.github_fetcher import GitHubTrendingFetcher
from src.storage.markdown_storage import MarkdownStorage


async def main():
    """Main function demonstrating Dependency Injection."""
    print("=" * 60)
    print("  AI Agent Onboarding - News Fetcher (SOLID Version)")
    print("=" * 60)
    
    # 1. Setup fetchers (Extension point - add new ones here!)
    fetchers = [
        HackerNewsFetcher(),
        RSSFetcher("https://hnrss.org/frontpage"),
        GitHubTrendingFetcher(), # Added with zero core code changes!
    ]
    
    # 2. Setup storage
    storage = MarkdownStorage()
    
    # 3. Inject dependencies into Orchestrator
    orchestrator = FetchOrchestrator(fetchers=fetchers, storage=storage)
    
    try:
        # 4. Run pipeline
        articles = await orchestrator.fetch_all()
        
        print("\n" + "=" * 60)
        print(f"✅ Success! Fetched {len(articles)} articles total")
        print("=" * 60)
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
