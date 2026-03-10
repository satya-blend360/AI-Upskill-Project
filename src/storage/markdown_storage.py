"""Save articles to markdown files."""
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from src.models.article import Article


from src.storage.base_storage import ArticleStorage


class MarkdownStorage(ArticleStorage):
    """
    Saves articles to markdown files.
    
    Responsibilities:
    1. Format Article to Markdown (formatting logic)
    2. Write content to filesystem (file logic)
    """
    
    def __init__(self, base_path: str = "data/articles"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def _format_article(self, article: Article) -> str:
        """Format single article to Markdown."""
        return f"""## {article.title}

**Source:** {article.source}  
**URL:** {article.url}  
**Published:** {article.published_at.strftime('%Y-%m-%d %H:%M')}  
**Score:** {article.score}

{article.summary}
"""

    def save(self, articles: List[Article], filename: Optional[str] = None) -> Path:
        """Save list of articles to a single Markdown file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"articles_{timestamp}.md"
        
        filepath = self.base_path / filename
        
        # Build document
        doc_header = f"# News Articles\n\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n**Total Articles:** {len(articles)}\n\n---\n\n"
        
        body = "\n---\n\n".join([self._format_article(a) for a in articles])
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(doc_header)
            f.write(body)
            f.write("\n---\n")
            
        print(f"💾 Saved {len(articles)} articles to: {filepath}")
        return filepath
