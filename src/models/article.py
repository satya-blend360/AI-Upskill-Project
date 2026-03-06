"""Article data model."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    """
    Represents a news article.
    
    PURE data class. No business logic or formatting.
    This follows SRP (Single Responsibility Principle).
    """
    
    title: str
    url: str
    published_at: datetime
    source: str
    summary: str = ""
    score: int = 0
    
    def __post_init__(self):
        """Validate after initialization."""
        if not self.title:
            raise ValueError("Article must have a title")
        if not self.url:
            raise ValueError("Article must have a URL")
