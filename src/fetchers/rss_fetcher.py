"""Fetch articles from RSS feeds (SOLID Refactor)."""
import asyncio
import feedparser
from typing import List, Optional
from datetime import datetime
from dateutil import parser as date_parser
from src.models.article import Article
from src.fetchers.base_fetcher import BaseFetcher
from src.services.text_cleaner import TextCleaner


class RSSFetcher(BaseFetcher):
    """Fetches articles from RSS feeds."""
    
    def __init__(self, feed_url: str, transformer=None, storage=None):
        super().__init__(transformer, storage)
        self.feed_url = feed_url
    
    def get_source_name(self) -> str:
        # Extract host from URL
        return self.feed_url.split('//')[-1].split('/')[0]
    
    async def fetch(self, limit: int = 30) -> List[Article]:
        """Fetch articles from RSS feed."""
        print(f"📰 Fetching from RSS: {self.feed_url}")
        
        loop = asyncio.get_event_loop()
        feed = await loop.run_in_executor(
            None, 
            feedparser.parse,
            self.feed_url
        )
        
        articles = []
        for entry in feed.entries[:limit]:
            # USE TRANSFORMER (SRP/DIP)
            if self.transformer:
                article = self.transformer.transform_rss(entry, self.get_source_name())
            else:
                article = self._parse_entry_fallback(entry)
                
            if article:
                articles.append(article)
        
        print(f"✅ Fetched {len(articles)} RSS articles from {self.get_source_name()}")
        return articles
    
    def _parse_entry_fallback(self, entry) -> Optional[Article]:
        """Fallback parsing if no transformer provided."""
        try:
            url = entry.get('link', '')
            if not url:
                return None
            
            return Article(
                title=entry.get('title', 'No Title'),
                url=url,
                published_at=datetime.now(),
                source=self.get_source_name(),
                summary=entry.get('summary', '')[:200]
            )
        except Exception:
            return None
