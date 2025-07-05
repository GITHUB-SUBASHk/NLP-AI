"""
llm_fallback.py - LLM-based open-domain fallback module using Mistral

✅ Uses HuggingFace Pipeline / Ollama / vLLM / Llama.cpp API
✅ Simple open-ended query handler
✅ Invoked after RASA + RAG both fail
"""

import os
import requests

LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/api/generate")
LLM_MODEL = os.getenv("LLM_MODEL", "mistral")

def call_llm(prompt: str) -> str:
    """
    Calls local Mistral LLM instance (e.g., Ollama or web UI).
    :param prompt: user message or fallback input
    :return: generated response
    """
    try:
        payload = {
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(LLM_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "🤖 Sorry, I couldn't generate a reply.")
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return "🤖 LLM is unavailable at the moment."