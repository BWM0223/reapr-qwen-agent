#!/usr/bin/env python3
"""
MemoryAgent - Production-grade long-term memory agent using Qwen-Max
H0 Qwen Cloud AI Hackathon Submission
"""
import os
import json
import hashlib
from datetime import datetime
from typing import Optional
import dashscope
from dashscope import Generation

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY", "")

# ============================================================
# AGENT 1: Memory Ingestion Agent
# Extracts entities, facts, and preferences from user input
# ============================================================

def memory_ingestion_agent(user_input: str, existing_memories: list) -> dict:
    """Extract structured memories from user input using Qwen-Max."""
    prompt = f"""
You are a Memory Ingestion Agent. Extract structured facts from this user message.

Existing memories (for deduplication):
{json.dumps(existing_memories[-10:], indent=2) if existing_memories else "None yet"}

User message: {user_input}

Extract and return JSON with:
- facts: list of atomic facts to remember (e.g. "User prefers dark mode")
- entities: key entities mentioned (people, places, preferences, projects)
- importance: 1-10 score (10=critical personal info, 1=casual mention)
- category: one of [preference, fact, goal, relationship, project, other]

Return ONLY valid JSON."""
    
    response = Generation.call(
        model="qwen-max",
        messages=[{"role": "user", "content": prompt}],
        result_format="message"
    )
    
    try:
        content = response.output.choices[0].message.content
        # Strip markdown if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        return {"facts": [], "entities": [], "importance": 1, "category": "other"}


# ============================================================
# AGENT 2: Retrieval Agent
# Finds relevant memories for the current query
# ============================================================

def retrieval_agent(query: str, memories: list) -> list:
    """Find the most relevant memories for a given query using Qwen-Max."""
    if not memories:
        return []
    
    prompt = f"""
You are a Memory Retrieval Agent. Find the most relevant memories for this query.

Query: {query}

Available memories:
{json.dumps(memories, indent=2)}

Return a JSON array of the IDs of the top 5 most relevant memories.
Return ONLY a JSON array like: ["id1", "id2", "id3"]"""
    
    response = Generation.call(
        model="qwen-max",
        messages=[{"role": "user", "content": prompt}],
        result_format="message"
    )
    
    try:
        content = response.output.choices[0].message.content
        if "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            if content.startswith("json"):
                content = content[4:].strip()
        ids = json.loads(content)
        return [m for m in memories if m.get("id") in ids]
    except:
        return memories[:5]  # fallback: return most recent


# ============================================================
# AGENT 3: Response Agent
# Generates personalized response using retrieved memories
# ============================================================

def response_agent(user_query: str, relevant_memories: list, conversation_history: list) -> str:
    """Generate a personalized response using Qwen-Max with memory context."""
    memory_context = ""
    if relevant_memories:
        facts = []
        for m in relevant_memories:
            facts.extend(m.get("facts", []))
        memory_context = "
".join(f"- {f}" for f in facts)
    
    system_prompt = f"""You are a personalized AI assistant with long-term memory.
You remember personal facts, preferences, and context about the user.

What you know about the user:
{memory_context if memory_context else "No memories yet - this is a new user"}

Use this context to give personalized, helpful responses.
Reference specific memories when relevant.
Be conversational and human."""
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history[-6:])  # last 3 turns
    messages.append({"role": "user", "content": user_query})
    
    response = Generation.call(
        model="qwen-max",
        messages=messages,
        result_format="message"
    )
    
    return response.output.choices[0].message.content


# ============================================================
# MEMORY STORE
# Simple persistent store (production: Alibaba Cloud OSS)
# ============================================================

class MemoryStore:
    def __init__(self, storage_path: str = "memories.json"):
        self.path = storage_path
        self.memories = self._load()
    
    def _load(self) -> list:
        try:
            with open(self.path) as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.memories, f, indent=2)
    
    def add(self, extracted: dict, original_text: str):
        memory_id = hashlib.md5(original_text.encode()).hexdigest()[:8]
        memory = {
            "id": memory_id,
            "facts": extracted.get("facts", []),
            "entities": extracted.get("entities", []),
            "importance": extracted.get("importance", 1),
            "category": extracted.get("category", "other"),
            "original": original_text[:200],
            "timestamp": datetime.utcnow().isoformat(),
        }
        # Deduplicate by ID
        self.memories = [m for m in self.memories if m["id"] != memory_id]
        self.memories.append(memory)
        self.memories.sort(key=lambda x: x.get("importance", 1), reverse=True)
        self._save()
        return memory
    
    def get_all(self) -> list:
        return self.memories
    
    def stats(self) -> dict:
        return {
            "total_memories": len(self.memories),
            "categories": list(set(m.get("category") for m in self.memories)),
            "avg_importance": sum(m.get("importance", 1) for m in self.memories) / max(len(self.memories), 1)
        }


# ============================================================
# MAIN PIPELINE
# ============================================================

def chat(user_input: str, store: MemoryStore, history: list) -> str:
    """
    Full 3-agent pipeline:
    1. Ingest new memories from input
    2. Retrieve relevant existing memories
    3. Generate personalized response
    """
    print(f"[Ingestion Agent] Processing input...")
    extracted = memory_ingestion_agent(user_input, store.get_all())
    
    if extracted.get("facts"):
        memory = store.add(extracted, user_input)
        print(f"[Memory Store] Saved {len(extracted["facts"])} facts (importance: {extracted["importance"]})")
    
    print(f"[Retrieval Agent] Finding relevant memories...")
    relevant = retrieval_agent(user_input, store.get_all())
    print(f"[Retrieval Agent] Found {len(relevant)} relevant memories")
    
    print(f"[Response Agent] Generating personalized response...")
    response = response_agent(user_input, relevant, history)
    
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response})
    
    return response


if __name__ == "__main__":
    store = MemoryStore()
    history = []
    
    print("MemoryAgent - Powered by Qwen-Max")
    print(f"Memory stats: {store.stats()}")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit"]:
            break
        if not user_input:
            continue
        
        response = chat(user_input, store, history)
        print(f"\nAgent: {response}\n")
        print(f"[Stats] {store.stats()}\n")
