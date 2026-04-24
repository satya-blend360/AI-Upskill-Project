"""Simple tools for the news agent."""
from typing import Dict, Any

def get_article_summary(url: str) -> Dict[str, Any]:
    """
    Simulates fetching and summarizing the full content of an article from a URL.
    Use this when you need more detail than just the headline to judge relevance.
    
    Args:
        url: The full URL of the article to 'fetch'.
    """
    print(f"🔧 Tool Call: get_article_summary({url})")
    # In a real scenario, this would use BeautifulSoup or a dedicated API.
    # For Milestone 3, we'll provide a mock response that helps the agent.
    return {
        "url": url,
        "status": "success",
        "summary": (
            "This is a simulated full-text summary of the article. "
            "It confirms the article discusses advanced machine learning architectures "
            "and their practical applications in modern software engineering."
        ),
        "word_count": 150,
        "sentiment": "positive"
    }
