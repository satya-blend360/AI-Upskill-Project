"""Storage interface (SOLID Refactor)."""
from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path
from src.models.article import Article


class ArticleStorage(ABC):
    """
    Abstract interface for article storage.
    
    Allows different storage implementations without changing fetchers.
    Follows Dependency Inversion Principle.
    """
    
    @abstractmethod
    def save(self, articles: List[Article], filename: Optional[str] = None) -> Path:
        """
        Save articles to storage.
        
        Args:
            articles: Articles to save
            filename: Optional filename
            
        Returns:
            Path or identifier where articles were saved
        """
        pass
