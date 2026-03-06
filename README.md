# AI Agent Onboarding - v3.3 Self-Paced Edition

A professional-grade AI agent system built using SOLID principles and the Model Context Protocol (MCP).

## Project Overview
This project is a multi-agent news aggregation system that:
1.  **Fetches:** Concurrently pulls news from HackerNews and RSS feeds.
2.  **Refactors:** Uses SOLID principles to ensure code is extensible.
3.  **Filters:** Employs AI agents to judge relevance to AI/ML topics.
4.  **Summarizes:** Creates topic-based summaries using Gemini LLM.
5.  **Writes:** Produces a final newsletter digest.

## Tech Stack
- **Python 3.11+**
- **Google Generative AI (Gemini)**
- **MCP (Model Context Protocol)**
- **SQLite** for article storage
- **aiohttp** for async operations

## How to Run
1.  **Install dependencies:** `pip install -r requirements.txt`
2.  **Setup .env:** Copy `.env.example` to `.env` and add your API keys.
3.  **Run pipeline:** (Coming in M4) `python src/complete_pipeline.py`

## Milestone Progress
- [x] M0: Setup & Architecture
- [ ] M1: Async News Fetcher
- [ ] M2: SOLID Refactoring
- [ ] M3: AI Agent with Tools
- [ ] M4: MCP-Powered Pipeline
- [ ] M5: Evaluation & Docs
