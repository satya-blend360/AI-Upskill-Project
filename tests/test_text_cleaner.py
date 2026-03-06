"""Tests for TextCleaner service."""
import pytest
from src.services.text_cleaner import TextCleaner


def test_clean_html():
    """Test HTML stripping and entity decoding."""
    cleaner = TextCleaner()
    raw = "Hello <p>World</p> &#x2F; Test"
    clean = cleaner.clean_html(raw)
    
    assert "World" in clean
    assert "<p>" not in clean
    assert "/" in clean


def test_truncate():
    """Test text truncation."""
    cleaner = TextCleaner()
    text = "This is a very long sentence that needs to be shortened."
    truncated = cleaner.truncate(text, limit=20)
    
    assert len(truncated) <= 23 # 20 + "..."
    assert truncated.endswith("...")
    assert "sentence" not in truncated


def test_clean_empty():
    """Test cleaning empty input."""
    cleaner = TextCleaner()
    assert cleaner.clean_html("") == ""
    assert cleaner.clean_html(None) == ""
