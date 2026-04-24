import os
import asyncio
from dotenv import load_dotenv

# Try to import required ADK components
try:
    from google.adk.agents import LlmAgent
    from google.adk.models.lite_llm import LiteLlm
    from google.adk.runners import Runner
    from google.adk.sessions.in_memory_session_service import InMemorySessionService
    from google.genai import types
except ImportError as e:
    print(f"Error: {e}")
    print("Please install required packages: pip install google-adk litellm google-genai")
    import sys
    sys.exit(1)

# Load environment variables
load_dotenv()

async def test_adk_openai():
    print("🚀 Testing Google ADK + OpenAI via LiteLLM using Runner\n")
    
    # 1. Verify OpenAI API Key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("❌ Error: OPENAI_API_KEY not found in .env file.")
        return

    # 2. Configure LiteLLM for OpenAI
    try:
        model = LiteLlm(model="openai/gpt-4o-mini")
        print("✅ LiteLlm wrapper initialized for openai/gpt-4o-mini")
    except Exception as e:
        print(f"❌ Failed to initialize LiteLlm: {e}")
        return

    # 3. Create the ADK Agent
    try:
        agent = LlmAgent(
            model=model,
            name="OpenAI_Powered_ADK_Agent",
            instruction="You are a helpful assistant running inside the Google Agent Development Kit, using an OpenAI model via LiteLLM."
        )
        print("✅ ADK LlmAgent created successfully")
    except Exception as e:
        print(f"❌ Failed to create ADK Agent: {e}")
        return

    # 4. Initialize Runner and Session Service
    try:
        session_service = InMemorySessionService()
        runner = Runner(
            agent=agent, 
            session_service=session_service, 
            app_name="TestApp",
            auto_create_session=True
        )
        print("✅ ADK Runner and InMemorySessionService initialized with auto_create_session=True")
    except Exception as e:
        print(f"❌ Failed to initialize infrastructure: {e}")
        return

    # 5. Run the Agent via Runner
    print("\n--- Running Agent Inference ---")
    try:
        user_input = types.Content(
            role="user",
            parts=[types.Part(text="Confirm that you are an OpenAI model working inside Google ADK via LiteLLM.")]
        )

        full_response = ""
        # Note: Runner.run is typically a standard generator (sync) or async generator.
        # Based on inspection, it's (self, ...) -> Generator[Event, None, None]
        # But in some versions it might be async. Let's try it as a sync generator first.
        # If it's sync, we can't use 'async for'.
        
        events = runner.run(
            user_id="test_user",
            session_id="test_session",
            new_message=user_input
        )

        for event in events:
            # ADK events usually have content or delta
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        full_response += part.text
            elif hasattr(event, 'delta') and event.delta:
                full_response += event.delta
        
        if full_response:
            print(f"Agent Response:\n{full_response}")
            print("\n✨ Success! Google ADK + OpenAI working via Runner.")
        else:
            print("⚠️ No text response received from agent.")
            print(f"Raw event dump: {events}")

    except Exception as e:
        print(f"❌ Inference failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ensure Windows encoding is handled
    os.environ["PYTHONUTF8"] = "1"
    asyncio.run(test_adk_openai())
