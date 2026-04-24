"""Agent that writes newsletter from summary."""
from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from datetime import datetime


class WriterAgent(BaseAgent):
    """
    Writes newsletter from topic summaries.
    
    Final step in the multi-agent pipeline.
    """
    
    def __init__(self, model_name: str = "openai/gpt-4o-mini"):
        instruction = (
            "You are a professional tech newsletter writer. Your goal is to write "
            "an engaging, concise, and informative daily AI/ML newsletter based on "
            "the provided topic summaries.\n\n"
            "Include:\n"
            "1. A catchy headline with the current date.\n"
            "2. A brief, engaging intro (2-3 sentences).\n"
            "3. Sections for each topic with the provided summaries.\n"
            "4. A concluding thought on the state of AI today."
        )
        super().__init__(
            name="WriterAgent",
            instruction=instruction,
            model_name=model_name
        )

    async def _prepare_context(self, input_data: Dict[str, str]) -> str:
        """Format the topic summaries for the newsletter."""
        summaries_str = "\n".join([f"### {topic}\n{summary}" for topic, summary in input_data.items()])
        date_str = datetime.now().strftime("%Y-%m-%d")
        return f"Current Date: {date_str}\n\nWrite a newsletter from these summaries:\n\n{summaries_str}"

    async def _finalize_result(self, result: str) -> str:
        """Return the final newsletter text."""
        return result.strip()
