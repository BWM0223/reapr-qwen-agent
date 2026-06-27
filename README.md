# MemoryAgent — Qwen Cloud AI Hackathon

**Track 1: MemoryAgent** | Global AI Hackathon with Qwen Cloud

A production-grade long-term memory agent that learns your personal context,
preferences and knowledge over time using Qwen-Max and Alibaba Cloud.

## Live Demo
https://reapr-qwen-agent.vercel.app

## Architecture

```
User Input
    │
    ▼
[Memory Ingestion Agent]  ──▶  Qwen-Max (extract entities + facts)
    │
    ▼
[Vector Store] (in-memory + Alibaba Cloud OSS for persistence)
    │
    ▼
[Retrieval Agent]  ──▶  Qwen-Max (semantic search + context injection)
    │
    ▼
[Response Agent]  ──▶  Qwen-Max (personalized response with full context)
```

## Why This Wins Track 1 (MemoryAgent)

1. **Multi-agent pipeline**: 3 specialized Qwen agents working in sequence
2. **Real persistence**: Memories stored on Alibaba Cloud OSS
3. **Production architecture**: Modular, testable, scalable
4. **Solves a real problem**: LLMs forget everything between sessions

## Stack
- **LLM**: Qwen-Max via DashScope API
- **Orchestration**: Custom Python agent pipeline
- **Storage**: Alibaba Cloud OSS (memory persistence)
- **API**: FastAPI on Alibaba Cloud ECS
- **Frontend**: Next.js on Vercel

## Setup

```bash
git clone https://github.com/BWM0223/reapr-qwen-agent
cd reapr-qwen-agent
pip install -r requirements.txt
cp .env.example .env
# Add your DASHSCOPE_API_KEY and ALIBABA_CLOUD credentials
python main.py
```

## Track
Track 1: MemoryAgent
