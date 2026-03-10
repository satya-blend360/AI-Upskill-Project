"""Abstract base class for all news fetchers."""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.article import Article


class BaseFetcher(ABC):
    """
    Contract for all news fetchers.
    
    This allows the Orchestrator to work with ANY fetcher
    without knowing its specific implementation (OCP).
    
    Implements Template Method pattern:
    - fetch_and_save() defines the algorithm skeleton.
    - fetch() is the customization point for subclasses.
    """
    
    def __init__(self, transformer=None, storage=None):
        """
        Initialize fetcher with injected dependencies (DIP).
        
        Args:
            transformer: ArticleTransformer instance
            storage: Storage instance (e.g., MarkdownStorage)
        """
        self.transformer = transformer
        self.storage = storage
    
    @abstractmethod
    async def fetch(self, limit: int = 30) -> List[Article]:
        """
        Fetch articles from source.
        
        Args:
            limit: Maximum articles to fetch
            
        Returns:
            List of standardized Article objects
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Return the name of the source (e.g., 'hackernews')."""
        pass

    async def fetch_and_save(self, limit: int = 30) -> List[Article]:
        """
        Fetch articles and save to storage (Template Method).
        
        Args:
            limit: Maximum articles to fetch
            
        Returns:
            List of fetched articles
        """
        articles = await self.fetch(limit)
        
        if articles and self.storage:
            filename = f"{self.get_source_name()}_articles.md"
            self.storage.save(articles, filename)
            
        return articles
