"""Orchestrate multiple news fetchers (SOLID Refactor)."""
import asyncio
from typing import List, Tuple
from src.models.article import Article
from src.fetchers.base_fetcher import BaseFetcher
from src.storage.markdown_storage import MarkdownStorage


class FetchOrchestrator:
    """
    Orchestrates fetching from multiple sources.
    
    This follows DIP (Dependency Inversion Principle) by
    depending on the BaseFetcher abstraction, not concrete classes.
    """
    
    def __init__(self, fetchers: List[BaseFetcher], storage: MarkdownStorage = None):
        """
        Initialize orchestrator with INJECTED dependencies.
        
        Args:
            fetchers: List of fetchers to use
            storage: Storage handler (injected)
        """
        self.fetchers = fetchers
        self.storage = storage or MarkdownStorage()
    
    async def fetch_all(self, limit_per_source: int = 30) -> List[Article]:
        """
        Fetch from all sources concurrently.
        
        Returns:
            Combined list of all articles
        """
        print("\n🚀 Starting fetch from all sources...")
        print(f"   Active Fetchers: {len(self.fetchers)}")
        
        # Create tasks for all fetchers
        # All fetchers now follow the same 'fetch()' contract
        tasks = [f.fetch(limit_per_source) for f in self.fetchers]
        
        # Fetch all concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine articles
        all_articles = []
        for fetcher, result in zip(self.fetchers, results):
            name = fetcher.get_source_name()
            if isinstance(result, Exception):
                print(f"⚠️  {name} failed: {result}")
            else:
                all_articles.extend(result)
        
        # Save combined results
        if all_articles:
            self.storage.save(all_articles, "all_articles.md")
        
        print(f"\n🎉 Total: {len(all_articles)} articles from {len(self.fetchers)} sources")
        return all_articles
