"""Main entry point (SOLID Refactor)."""
import asyncio
import sys
from src.orchestrator import FetchOrchestrator
from src.fetchers.fetcher_factory import FetcherFactory
from src.storage.markdown_storage import MarkdownStorage


from src.transformers.article_transformer import ArticleTransformer


async def main():
    """Main function demonstrating SOLID Architecture."""
    print("=" * 60)
    print("  AI Agent Onboarding - News Fetcher (Professional Grade)")
    print("=" * 60)
    
    # 0. Setup core services (DIP)
    transformer = ArticleTransformer()
    storage = MarkdownStorage()
    
    # 1. Use FACTORY to get our tools (Centralized configuration)
    fetchers = FetcherFactory.create_default_fetchers(
        transformer=transformer, 
        storage=storage
    )
    
    # 2. Setup Orchestrator (DIP)
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
