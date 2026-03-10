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
    def create_default_fetchers(transformer=None, storage=None) -> List[BaseFetcher]:
        """
        Create the standard list of fetchers with injected dependencies.
        """
        return [
            HackerNewsFetcher(transformer=transformer, storage=storage),
            RSSFetcher("https://hnrss.org/frontpage", transformer=transformer, storage=storage),
            GitHubTrendingFetcher(transformer=transformer, storage=storage)
        ]
    
    @staticmethod
    def create_custom_rss(feed_url: str, transformer=None, storage=None) -> BaseFetcher:
        """Helper to create a single custom RSS fetcher."""
        return RSSFetcher(feed_url, transformer=transformer, storage=storage)
