# AI Agent Onboarding Project

**Multi-agent news aggregation system with MCP integration**

A production-ready AI agent pipeline that fetches, filters, summarizes, and writes AI/ML news newsletters.

## Features

- 🚀 **Async News Fetching** from multiple sources (HackerNews, RSS, GitHub)
- 🤖 **AI-Powered Filtering** using Google ADK + OpenAI (GPT-4o-mini via LiteLLM)
- 🔧 **MCP Integration** with a production Database Server
- 📝 **Multi-Agent Pipeline** (Filter → Summarize → Write)
- 💾 **SQLite Database** for persistent article storage
- 📊 **Evaluation Framework** with automated quality measurement
- ✅ **SOLID Architecture** and professional software engineering patterns

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API Key (configured in `.env`)

### Installation

```bash
# Clone repo
git clone https://github.com/your-username/AI-Upskill-Project.git
cd AI-Upskill-Project

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Ensure .env has:
# OPENAI_API_KEY=your_key_here
```

### Run Complete Pipeline

```bash
# Set PYTHONPATH and run
$env:PYTHONPATH='.'; python src/complete_pipeline.py

# Output:
# - data/output/newsletter_YYYY-MM-DD.md (final newsletter)
# - data/news_agent.db (article database)
```

## Architecture

The system follows a modular, agentic flow:

1.  **Fetchers**: Concurrent async retrieval from HN, RSS, and GitHub Trending.
2.  **Database (MCP)**: Persistent storage managed by a SQLite-backed MCP server.
3.  **NewsFilterAgent**: Analyzes titles/summaries to judge AI/ML relevance.
4.  **SummarizerAgent**: Groups relevant news into topics and generates executive summaries.
5.  **WriterAgent**: Crafts a professional, engaging daily newsletter.

## Evaluation

We use a "Golden Dataset" of hand-labeled cases to measure quality.
- **Accuracy:** 100% (on current benchmark)
- **F1 Score:** 1.00

To run evaluation:
```bash
$env:PYTHONPATH='.'; python src/evaluation/evaluator.py
```

## Project Structure

- `src/agents/`: AI agent implementations (BaseAgent, Filter, Summarizer, Writer)
- `src/mcp/`: Model Context Protocol servers and clients
- `src/database/`: SQLite storage management
- `src/fetchers/`: Async data retrieval services
- `src/skills/`: High-level agent capabilities (e.g., SearchSkill)
- `src/evaluation/`: Quality measurement framework
- `src/complete_pipeline.py`: Main end-to-end entry point

## License

MIT
