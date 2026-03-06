"""Service for cleaning and formatting text."""
import html
import re
from bs4 import BeautifulSoup


class TextCleaner:
    """
    Cleans and formats text from various sources.
    
    Responsibilities:
    1. Strip HTML tags
    2. Decode HTML entities (e.g., &#x2F; -> /)
    3. Truncate text cleanly
    """
    
    @staticmethod
    def clean_html(text: str) -> str:
        """
        Strip HTML tags and decode entities.
        
        Args:
            text: Raw text (possibly with HTML)
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # 1. Use BeautifulSoup to strip HTML (best way!)
        soup = BeautifulSoup(text, "html.parser")
        clean_text = soup.get_text()
        
        # 2. Decode any remaining HTML entities
        clean_text = html.unescape(clean_text)
        
        # 3. Clean up extra whitespace/newlines
        clean_text = " ".join(clean_text.split())
        
        return clean_text.strip()
    
    @staticmethod
    def truncate(text: str, limit: int = 200) -> str:
        """Truncate text to limit with ellipsis."""
        if not text or len(text) <= limit:
            return text
        
        return text[:limit].rsplit(' ', 1)[0] + "..."


# Quick test
if __name__ == "__main__":
    raw_text = 'Hello <p>World!</p> This is a test &#x2F; story.'
    clean = TextCleaner.clean_html(raw_text)
    print(f"Raw:   {raw_text}")
    print(f"Clean: {clean}")
    assert "/" in clean
    assert "<p>" not in clean
    print("✅ TextCleaner works!")
