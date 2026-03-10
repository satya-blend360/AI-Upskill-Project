"""Transform raw data to Article objects (SOLID Refactor)."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.models.article import Article
from src.services.text_cleaner import TextCleaner


class ArticleTransformer:
    """
    Transforms raw data from various sources to Article objects.
    
    Single Responsibility: Data transformation only.
    Uses TextCleaner service to clean content.
    """
    
    def __init__(self, cleaner: Optional[TextCleaner] = None):
        """
        Initialize with injected cleaner service.
        
        Args:
            cleaner: TextCleaner instance (DIP)
        """
        self.cleaner = cleaner or TextCleaner()
    
    def transform_hackernews(self, item: Dict[str, Any]) -> Optional[Article]:
        """
        Transform HackerNews API response to Article.
        
        Args:
            item: Raw HN item from API
            
        Returns:
            Article object or None if invalid
        """
        if not item or not item.get('url'):
            return None
            
        # Clean summary (from 'text' field)
        summary = item.get('text', '')
        summary = self.cleaner.clean_html(summary)
        summary = self.cleaner.truncate(summary, 200)
        
        return Article(
            title=item.get('title', 'No Title'),
            url=item['url'],
            published_at=datetime.fromtimestamp(item.get('time', 0)),
            source='hackernews',
            summary=summary,
            score=item.get('score', 0)
        )
    
    def transform_rss(self, entry: Any, source_name: str) -> Optional[Article]:
        """
        Transform RSS feed entry to Article.
        
        Args:
            entry: Raw entry from feedparser
            source_name: Name of the RSS source
            
        Returns:
            Article object or None if invalid
        """
        from dateutil import parser as date_parser
        url = entry.get('link', '')
        if not url:
            return None
            
        # Clean summary (from 'summary' or 'description')
        summary = entry.get('summary', entry.get('description', ''))
        summary = self.cleaner.clean_html(summary)
        summary = self.cleaner.truncate(summary, 200)
        
        # Parse date
        published_str = entry.get('published', entry.get('updated', ''))
        published_at = datetime.now()
        if published_str:
            try:
                published_at = date_parser.parse(published_str)
            except:
                pass
        
        return Article(
            title=entry.get('title', 'No Title'),
            url=url,
            published_at=published_at,
            source=source_name,
            summary=summary
        )

    def transform_github(self, repo: Dict[str, Any]) -> Optional[Article]:
        """
        Transform GitHub repo to Article.
        
        Args:
            repo: Raw repo from GitHub API
            
        Returns:
            Article object or None if invalid
        """
        try:
            description = repo.get('description', 'No description')
            description = self.cleaner.clean_html(description)
            description = self.cleaner.truncate(description, 200)
            
            return Article(
                title=f"{repo['full_name']} (⭐ {repo['stargazers_count']})",
                url=repo['html_url'],
                published_at=datetime.now(),
                source='github_trending',
                summary=description,
                score=repo.get('stargazers_count', 0)
            )
        except Exception:
            return None
