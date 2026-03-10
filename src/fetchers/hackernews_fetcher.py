"""Fetch top stories from HackerNews (SOLID Refactor)."""
import asyncio
import aiohttp
from typing import List, Optional
from datetime import datetime
from src.models.article import Article
from src.utils.rate_limiter import RateLimiter
from src.fetchers.base_fetcher import BaseFetcher
from src.services.text_cleaner import TextCleaner


from src.strategies.rate_limit_strategy import RateLimitStrategy, SemaphoreStrategy


class HackerNewsFetcher(BaseFetcher):
    """Fetches top stories from HackerNews API."""
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    
    def __init__(self, transformer=None, storage=None, rate_limiter: Optional[RateLimitStrategy] = None):
        super().__init__(transformer, storage)
        self.rate_limiter = rate_limiter or SemaphoreStrategy(max_concurrent=10)
    
    def get_source_name(self) -> str:
        return "hackernews"
    
    async def fetch(self, limit: int = 30) -> List[Article]:
        """Fetch top stories from HackerNews."""
        print(f"📰 Fetching {limit} stories from {self.get_source_name()}...")
        
        story_ids = await self._fetch_top_story_ids()
        articles = await self._fetch_stories(story_ids[:limit])
        
        print(f"✅ Fetched {len(articles)} stories from {self.get_source_name()}")
        return articles
    
    async def _fetch_top_story_ids(self) -> List[int]:
        url = f"{self.BASE_URL}/topstories.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    
    async def _fetch_stories(self, story_ids: List[int]) -> List[Article]:
        tasks = [self._fetch_story(story_id) for story_id in story_ids]
        stories = await asyncio.gather(*tasks)
        return [s for s in stories if s is not None]
    
    async def _fetch_story(self, story_id: int) -> Optional[Article]:
        url = f"{self.BASE_URL}/item/{story_id}.json"
        try:
            async with self.rate_limiter:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        data = await response.json()
                        
                        if not data or not data.get('url'):
                            return None
                        
                        # USE TRANSFORMER (SRP/DIP)
                        if self.transformer:
                            return self.transformer.transform_hackernews(data)
                        
                        # Fallback if no transformer
                        return Article(
                            title=data.get('title', 'No Title'),
                            url=data['url'],
                            published_at=datetime.fromtimestamp(data.get('time', 0)),
                            source=self.get_source_name(),
                            summary=data.get('text', '')[:200],
                            score=data.get('score', 0)
                        )
        except Exception as e:
            print(f"⚠️  Failed to fetch {self.get_source_name()} story {story_id}: {e}")
            return None
