# MemoryAgent - Qwen Cloud AI Hackathon

**Track 1: MemoryAgent** | Global AI Hackathon with Qwen Cloud

## Live Demo
https://memoryagent.vercel.app

## Architecture
3-agent pipeline powered by Qwen-Max:
1. Ingestion Agent - extracts facts from user input
2. Memory Store (Alibaba Cloud OSS) - persists memories
3. Retrieval Agent - finds relevant context
4. Response Agent - generates personalized reply

## Run Locally
```bash
git clone https://github.com/BWM0223/reapr-qwen-agent
pip install -r requirements.txt
export DASHSCOPE_API_KEY=your_key
python main.py
```

## Track
Track 1: MemoryAgent
