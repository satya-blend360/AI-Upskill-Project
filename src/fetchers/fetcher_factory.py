"""Factory for creating news fetchers."""
from typing import List
from src.fetchers.base_fetcher import BaseFetcher
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.fetchers.github_fetcher import GitHubTrendingFetcher


class FetcherFactory:
    """
    Creates lists of fetchers based on configuration.
    
    This centralizes creation logic, preventing duplicated code 
    in main.py or tests.
    """
    
    @staticmethod
    def create_default_fetchers() -> List[BaseFetcher]:
        """Create the standard list of fetchers."""
        return [
            HackerNewsFetcher(),
            RSSFetcher("https://hnrss.org/frontpage"),
            GitHubTrendingFetcher()
        ]
    
    @staticmethod
    def create_custom_rss(feed_url: str) -> BaseFetcher:
        """Helper to create a single custom RSS fetcher."""
        return RSSFetcher(feed_url)
