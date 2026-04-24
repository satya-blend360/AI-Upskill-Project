"""Agent that filters AI-relevant articles using Google ADK + OpenAI."""
import json
from typing import List, Dict, Any
from src.agents.base_agent import BaseAgent
from src.tools.web_tools import get_article_summary

class NewsFilterAgent(BaseAgent):
    """Filters articles for AI/ML relevance using ADK + OpenAI and tools."""
    
    def __init__(self, model_name: str = "openai/gpt-4o-mini"):
        """Initialize with filtering instructions and tools."""
        instruction = (
            "You are an expert AI/ML news analyst. Your task is to filter a list of articles "
            "and identify which ones are relevant to Artificial Intelligence, Machine Learning, "
            "Deep Learning, LLMs, or related fields.\n\n"
            "If the title is ambiguous, use the 'get_article_summary' tool to fetch more information "
            "about the URL before making your final judgment.\n\n"
            "For each article, you must:\n"
            "1. Determine if it is relevant (True/False).\n"
            "2. Assign a relevance score (1-10).\n"
            "3. Provide a brief reasoning.\n\n"
            "Output your response ONLY as a JSON array of objects with the following keys:\n"
            '- "title": (string)\n'
            '- "relevant": (boolean)\n'
            '- "relevance_score": (integer)\n'
            '- "reasoning": (string)'
        )
        super().__init__(
            name="NewsFilterAgent",
            instruction=instruction,
            model_name=model_name,
            tools=[get_article_summary]
        )

    async def _prepare_context(self, input_data: List[Dict[str, Any]]) -> str:
        """Prepare the list of articles for the LLM."""
        articles_str = json.dumps(input_data, indent=2)
        return f"Filter the following articles for AI/ML relevance:\n\n{articles_str}"

    async def _finalize_result(self, result: str) -> List[Dict[str, Any]]:
        """Extract and parse JSON from the LLM response."""
        try:
            clean_json = result.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0]
            elif "```" in clean_json:
                clean_json = clean_json.split("```")[1].split("```")[0]
            
            return json.loads(clean_json)
        except Exception as e:
            print(f"Error parsing agent response: {e}")
            return []
