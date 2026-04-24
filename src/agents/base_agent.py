"""Base class for AI agents using Google ADK."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

class BaseAgent(ABC):
    """
    Base class for all AI agents.
    
    Implements Template Method pattern:
    - execute() orchestrates the workflow
    - Subclasses implement specific steps
    """
    
    def __init__(self, name: str, instruction: str, model_name: str = "openai/gpt-4o-mini", tools: List[Any] = None):
        """Initialize agent with ADK components."""
        self.name = name
        self.model = LiteLlm(model=model_name)
        self.instruction = instruction
        self.tools = tools or []
        
        # Create ADK Agent
        self.agent = LlmAgent(
            model=self.model,
            name=self.name,
            instruction=self.instruction,
            tools=self.tools
        )
        
        # Setup infrastructure
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=self.agent,
            session_service=self.session_service,
            app_name="AI_Upskill_Project",
            auto_create_session=True
        )

    async def execute(self, input_data: Any) -> Any:
        """
        Execute agent workflow (Template Method).
        """
        print(f"\n🤖 {self.name} starting...")
        
        # Step 1: Prepare Context
        context = await self._prepare_context(input_data)
        
        # Step 2: Process with LLM
        result = await self._process(context)
        
        # Step 3: Finalize Result
        final_output = await self._finalize_result(result)
        
        print(f"✅ {self.name} complete")
        return final_output

    @abstractmethod
    async def _prepare_context(self, input_data: Any) -> str:
        """Prepare the string prompt for the LLM."""
        pass

    async def _process(self, prompt: str) -> str:
        """Default processing using ADK Runner."""
        user_input = types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        )
        
        full_response = ""
        try:
            # ADK Runner.run returns a sync generator
            events = self.runner.run(
                user_id="system",
                session_id=f"{self.name}_session",
                new_message=user_input
            )
            
            for event in events:
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            full_response += part.text
                elif hasattr(event, 'delta') and event.delta:
                    full_response += event.delta
        except Exception as e:
            print(f"❌ Error during agent processing: {e}")
            return f"Error: {e}"
        
        return full_response

    @abstractmethod
    async def _finalize_result(self, result: str) -> Any:
        """Parse or save the LLM output."""
        pass
