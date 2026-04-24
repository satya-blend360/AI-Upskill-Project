"""Agent that summarizes filtered articles."""
from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent
from src.skills.search_skill import SearchSkill
import json


class SummarizerAgent(BaseAgent):
    """
    Summarizes filtered articles into a daily digest.
    
    Can use SearchSkill if needed, but primarily summarizes the input batch.
    """
    
    def __init__(self, model_name: str = "openai/gpt-4o-mini"):
        instruction = (
            "You are an expert AI news summarizer. Your task is to take a list of filtered "
            "AI/ML articles and group them by logical topics (e.g., 'Large Language Models', "
            "'AI Tools', 'Research'). For each topic, provide a 2-3 sentence executive summary "
            "of the key developments.\n\n"
            "Output your response ONLY as a JSON object where keys are topic names and values "
            "are the summaries."
        )
        super().__init__(
            name="SummarizerAgent",
            instruction=instruction,
            model_name=model_name
        )
        self.search_skill = SearchSkill()

    async def _prepare_context(self, input_data: List[Dict[str, Any]]) -> str:
        """Prepare the list of filtered articles for summarization."""
        articles_str = json.dumps(input_data, indent=2)
        return f"Summarize these filtered AI/ML articles by topic:\n\n{articles_str}"

    async def _finalize_result(self, result: str) -> Dict[str, str]:
        """Extract and parse the topic summaries."""
        try:
            clean_json = result.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0]
            elif "```" in clean_json:
                clean_json = clean_json.split("```")[1].split("```")[0]
            
            return json.loads(clean_json)
        except Exception as e:
            print(f"Error parsing summarizer response: {e}")
            return {"Summary": result}
