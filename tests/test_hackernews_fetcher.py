"""Tests for HackerNews fetcher."""
import pytest
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.models.article import Article


@pytest.mark.asyncio
async def test_fetch_returns_articles():
    """Test that fetch returns list of articles."""
    fetcher = HackerNewsFetcher()
    articles = await fetcher.fetch(limit=5)
    
    # Should get some articles
    assert len(articles) > 0
    assert len(articles) <= 5
    
    # Each should be an Article
    for article in articles:
        assert isinstance(article, Article)
        assert article.title
        assert article.url
        assert article.source == 'hackernews'
