"""Tests for HackerNews fetcher (Updated for SOLID)."""
import pytest
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.models.article import Article


@pytest.mark.asyncio
async def test_fetch_returns_articles():
    """Test that fetch returns list of articles."""
    fetcher = HackerNewsFetcher()
    
    # Check source name (OCP requirement)
    assert fetcher.get_source_name() == "hackernews"
    
    articles = await fetcher.fetch(limit=3)
    
    # Should get some articles
    assert len(articles) > 0
    assert len(articles) <= 3
    
    # Each should be an Article
    for article in articles:
        assert isinstance(article, Article)
        assert article.source == 'hackernews'
