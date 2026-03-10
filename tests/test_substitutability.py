"""Test Liskov Substitution Principle (LSP) and Substitutability."""
import pytest
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.fetchers.github_fetcher import GitHubTrendingFetcher
from src.transformers.article_transformer import ArticleTransformer
from src.storage.markdown_storage import MarkdownStorage


@pytest.mark.asyncio
async def test_all_fetchers_substitutable():
    """
    Test that all fetchers can be used interchangeably.
    
    This proves Liskov Substitution Principle (LSP).
    Any subclass of BaseFetcher should work with the same interface.
    """
    transformer = ArticleTransformer()
    storage = MarkdownStorage("data/test")
    
    # Create all fetchers
    fetchers = [
        HackerNewsFetcher(transformer=transformer, storage=storage),
        RSSFetcher("https://hnrss.org/frontpage", transformer=transformer, storage=storage),
        GitHubTrendingFetcher(transformer=transformer, storage=storage)
    ]
    
    # Each fetcher should work identically
    for fetcher in fetchers:
        # 1. Interface Check
        assert hasattr(fetcher, 'fetch')
        assert hasattr(fetcher, 'get_source_name')
        assert hasattr(fetcher, 'fetch_and_save')
        
        # 2. Functional Check (fetch some articles)
        # We use a small limit to speed up the test
        articles = await fetcher.fetch(limit=1)
        assert isinstance(articles, list)
        
        # 3. Structural Check (if articles returned)
        if articles:
            article = articles[0]
            assert hasattr(article, 'title')
            assert hasattr(article, 'url')
            assert hasattr(article, 'source')
            assert hasattr(article, 'summary')
            assert hasattr(article, 'published_at')
        
        # 4. Source Name Check
        source = fetcher.get_source_name()
        assert isinstance(source, str)
        assert len(source) > 0
    
    print("✅ All fetchers are substitutable!")
