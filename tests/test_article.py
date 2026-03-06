"""Tests for Article model (Updated for SRP)."""
from src.models.article import Article
from datetime import datetime
import pytest


def test_article_creation():
    """Test creating article."""
    article = Article(
        title="Test",
        url="https://test.com",
        published_at=datetime.now(),
        source="test"
    )
    assert article.title == "Test"
    assert article.url == "https://test.com"


def test_article_validation():
    """Test article validation."""
    with pytest.raises(ValueError):
        Article(
            title="",  # Empty title should fail
            url="https://test.com",
            published_at=datetime.now(),
            source="test"
        )

# NOTE: test_article_to_markdown removed because 
# Article no longer handles formatting (SRP).
