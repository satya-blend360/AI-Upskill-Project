"""Tests for NewsFilterAgent."""
import pytest
import os
import asyncio
from dotenv import load_dotenv
from src.agents.news_filter_agent import NewsFilterAgent

# Load environment variables
load_dotenv()

@pytest.mark.asyncio
async def test_news_filter_agent_filtering():
    """Test that the agent filters articles and returns JSON results."""
    # Ensure OPENAI_API_KEY is present
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not found in environment")
        
    agent = NewsFilterAgent()
    
    test_articles = [
        {
            "title": "OpenAI GPT-4.5 Released",
            "url": "https://openai.com/blog/gpt-4-5"
        },
        {
            "title": "10 Best Pasta Recipes for 2024",
            "url": "https://example.com/pasta"
        }
    ]
    
    results = await agent.execute(test_articles)
    
    # Should return a list of results
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Check that GPT-4.5 is found relevant
    gpt_result = next((r for r in results if "GPT-4.5" in r.get("title", "")), None)
    if gpt_result:
        assert gpt_result.get("relevant") is True
        assert gpt_result.get("relevance_score") >= 8

    # Check that Pasta is not relevant
    pasta_result = next((r for r in results if "Pasta" in r.get("title", "")), None)
    if pasta_result:
        # A good agent should find pasta not relevant to AI
        assert pasta_result.get("relevant") is False or pasta_result.get("relevance_score") < 5
