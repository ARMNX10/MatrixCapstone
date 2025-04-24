"""
LangMem-style memory module for Matrix AI Assistant.
Provides retrieval-augmented, context-aware memory for multi-turn conversation, games, and task state.
"""
import json
import os
from typing import List, Dict, Optional
from collections import deque
from datetime import datetime

class LangMem:
    def __init__(self, max_memories: int = 100):
        self.memories = deque(maxlen=max_memories)

    def add(self, memory: Dict):
        """Add a memory (dict with 'type', 'content', and optional 'meta')."""
        memory["timestamp"] = datetime.now().isoformat()
        self.memories.append(memory)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve the most relevant memories for the current query.
        For now, uses keyword overlap. For production, use embeddings.
        """
        scores = []
        for mem in self.memories:
            score = sum(1 for word in query.lower().split() if word in mem["content"].lower())
            scores.append((score, mem))
        scores.sort(reverse=True, key=lambda x: x[0])
        return [mem for score, mem in scores[:top_k] if score > 0]

    def get_context(self, query: str, top_k: int = 5) -> str:
        """
        Return a formatted string of the top-k relevant memories for prompt injection.
        """
        relevant = self.retrieve(query, top_k=top_k)
        if not relevant:
            return ""
        context = "\n[Relevant Memory]\n"
        for mem in relevant:
            context += f"- {mem['type']}: {mem['content']}"
            if 'meta' in mem:
                context += f" (meta: {json.dumps(mem['meta'])})"
            context += "\n"
        return context.strip()

    def reset(self):
        self.memories.clear()

    def save(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(list(self.memories), f, indent=2, ensure_ascii=False)

    def load(self, filepath: str):
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                self.memories = deque(json.load(f), maxlen=self.memories.maxlen)

# Singleton instance for app-wide use
langmem = LangMem(max_memories=150)
