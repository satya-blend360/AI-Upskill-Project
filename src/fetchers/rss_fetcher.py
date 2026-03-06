"""Fetch articles from RSS feeds (SOLID Refactor)."""
import asyncio
import feedparser
from typing import List
from datetime import datetime
from dateutil import parser as date_parser
from src.models.article import Article
from src.fetchers.base_fetcher import BaseFetcher
from src.services.text_cleaner import TextCleaner


class RSSFetcher(BaseFetcher):
    """Fetches articles from RSS feeds."""
    
    def __init__(self, feed_url: str):
        self.feed_url = feed_url
        self.cleaner = TextCleaner()
    
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
            article = self._parse_entry(entry)
            if article:
                articles.append(article)
        
        print(f"✅ Fetched {len(articles)} RSS articles from {self.get_source_name()}")
        return articles
    
    def _parse_entry(self, entry) -> Article:
        """Parse RSS entry to Article."""
        try:
            url = entry.get('link', '')
            if not url:
                return None
            
            # Use CLEANER service for summary
            summary = entry.get('summary', entry.get('description', ''))
            summary = self.cleaner.clean_html(summary)
            summary = self.cleaner.truncate(summary, 200)
            
            # Parse date
            published_str = entry.get('published', entry.get('updated', ''))
            published_at = datetime.now()
            if published_str:
                try:
                    published_at = date_parser.parse(published_str)
                except:
                    pass
            
            return Article(
                title=entry.get('title', 'No Title'),
                url=url,
                published_at=published_at,
                source=self.get_source_name(),
                summary=summary
            )
        except Exception as e:
            print(f"⚠️  Failed to parse RSS entry from {self.get_source_name()}: {e}")
            return None
