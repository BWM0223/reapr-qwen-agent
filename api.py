from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import chat, MemoryStore
import os

app = FastAPI(title="MemoryAgent API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

store = MemoryStore()
history = []

class Message(BaseModel):
    content: str

@app.post("/chat")
async def chat_endpoint(message: Message):
    try:
        response = chat(message.content, store, history)
        return {"response": response, "memory_stats": store.stats()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memories")
async def get_memories():
    return {"memories": store.get_all(), "stats": store.stats()}

@app.get("/health")
async def health():
    return {"status": "ok", "model": "qwen-max"}
