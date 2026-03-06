"""Abstract base class for all news fetchers."""
from abc import ABC, abstractmethod
from typing import List
from src.models.article import Article


class BaseFetcher(ABC):
    """
    Contract for all news fetchers.
    
    This allows the Orchestrator to work with ANY fetcher
    without knowing its specific implementation (OCP).
    """
    
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
