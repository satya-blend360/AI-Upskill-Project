"""Fetch Trending GitHub Repositories (Proof of OCP)."""
import asyncio
import aiohttp
from typing import List
from datetime import datetime
from src.models.article import Article
from src.fetchers.base_fetcher import BaseFetcher
from src.services.text_cleaner import TextCleaner


class GitHubTrendingFetcher(BaseFetcher):
    """
    Fetches trending GitHub repositories.
    
    This is added in Milestone 2 to prove the Open/Closed Principle (OCP).
    We added this source without changing any core logic!
    """
    
    BASE_URL = "https://api.github.com/search/repositories"
    
    def __init__(self, transformer=None, storage=None):
        super().__init__(transformer, storage)
    
    def get_source_name(self) -> str:
        return "github_trending"
    
    async def fetch(self, limit: int = 10) -> List[Article]:
        """Fetch trending AI repositories."""
        print(f"📰 Fetching trending GitHub AI repositories...")
        
        # Search for AI-related repos trending
        query = "topic:artificial-intelligence sort:stars-desc"
        url = f"{self.BASE_URL}?q={query}&per_page={limit}"
        
        # Add basic headers (GitHub API likes these)
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    data = await response.json()
                    
                    if 'items' not in data:
                        return []
                    
                    articles = []
                    for repo in data['items']:
                        # USE TRANSFORMER (SRP/DIP)
                        if self.transformer:
                            article = self.transformer.transform_github(repo)
                        else:
                            article = self._repo_to_article_fallback(repo)
                            
                        if article:
                            articles.append(article)
                    
                    print(f"✅ Fetched {len(articles)} trending repos")
                    return articles
        except Exception as e:
            print(f"⚠️  Failed to fetch GitHub: {e}")
            return []
            
    def _repo_to_article_fallback(self, repo: dict) -> Article:
        """Fallback parsing if no transformer provided."""
        try:
            return Article(
                title=f"{repo['full_name']} (⭐ {repo['stargazers_count']})",
                url=repo['html_url'],
                published_at=datetime.now(),
                source=self.get_source_name(),
                summary=repo.get('description', '')[:200],
                score=repo.get('stargazers_count', 0)
            )
        except Exception:
            return None
