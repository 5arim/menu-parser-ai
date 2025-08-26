# llm_server.py
from __future__ import annotations
import os
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import uvicorn

# --- CONFIG: update model_path if your file lives elsewhere ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), "llm", "mistral-7b-instruct-v0.2.Q4_K_M.gguf")

# Tweak these for your CPU/RAM
LLM_N_CTX = 2048
LLM_N_THREADS = 8  # adjust to your machine

# Create model instance at startup (singleton)
llm = Llama(model_path=MODEL_PATH, n_ctx=LLM_N_CTX, n_threads=LLM_N_THREADS)

app = FastAPI(title="Local LLM Server (GGUF -> OpenAI-style)")

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: float = 0.0
    max_tokens: int = 512

@app.get("/v1/models")
def list_models():
    # Minimal listing so clients can sanity-check
    return {"object": "list", "data": [{"id": os.path.basename(MODEL_PATH), "object": "model"}]}

@app.post("/v1/chat/completions")
def chat_completions(req: ChatRequest):
    # Build a single prompt from messages
    prompt_parts = []
    for m in req.messages:
        role = m.role.lower()
        if role == "system":
            prompt_parts.append(f"[SYSTEM]: {m.content}")
        elif role == "user":
            prompt_parts.append(f"[USER]: {m.content}")
        elif role == "assistant":
            prompt_parts.append(f"[ASSISTANT]: {m.content}")
        else:
            prompt_parts.append(f"[{m.role.upper()}]: {m.content}")
    prompt = "\n".join(prompt_parts) + "\n\n[ASSISTANT]:"

    # Generate response
    out = llm.create_completion(
        prompt=prompt,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_p=0.95
    )

    # llama_cpp.create_completion returns a dict-like response. Common key: 'choices'[0]['text']
    choices = out.get("choices", [])
    text = ""
    if choices:
        text = choices[0].get("text") or choices[0].get("content") or ""
    text = text.strip()

    # Return OpenAI-like structure with assistant message content
    return {
        "id": "local-chat-1",
        "object": "chat.completion",
        "choices": [
            {"index": 0, "message": {"role": "assistant", "content": text}}
        ]
    }

if __name__ == "__main__":
    # Use uvicorn to run the FastAPI server
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
