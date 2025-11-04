# main.py (Final Version - Zephyr 7B Beta on Hugging Face via OpenAI-Compatible API)

import os
import pickle
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import uvicorn
from dotenv import load_dotenv
import openai  # Using OpenAI client for Hugging Face

# --- 1. Load Environment Variables ---
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN must be set in the .env file.")

# --- 2. Configure the OpenAI Client for Hugging Face ---
client = openai.OpenAI(
    base_url="https://router.huggingface.co/hf-inference/v1",  # New router endpoint
    api_key=HF_TOKEN,
)
print("✅ OpenAI client configured for Hugging Face Inference API (Zephyr 7B Beta).")

# --- 3. Load AI/ML Components ---
print("🔄 Loading vector database, index, and embedding model...")
try:
    with open("data/vector_store.pkl", "rb") as f:
        vector_store = pickle.load(f)
    with open("data/nn_index.pkl", "rb") as f:
        nn_index = pickle.load(f)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print(f"✅ Successfully loaded. Database contains {len(vector_store['chunks'])} chunks.")
except FileNotFoundError as e:
    print(f"❌ Error loading files: {e}. Make sure the 'data' directory and files exist.")
    exit()

# --- 4. Initialize FastAPI App ---
app = FastAPI(
    title="Government Schemes RAG Chatbot API (Zephyr Edition)",
    description="An API to get answers about Indian government schemes, powered by Hugging Face Zephyr-7B.",
    version="4.1.0"
)

# --- Add CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Define Request/Response Models ---
class ChatRequest(BaseModel):
    query: str
    top_k: int = 5

class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]

# --- RAG Logic ---
def get_rag_response(query: str, top_k: int):
    print(f"🧠 Retrieving context for query: '{query}'")
    query_embedding = model.encode([query])
    distances, indices = nn_index.kneighbors(query_embedding, n_neighbors=top_k)
    context_str = ""
    source_citations = {}

    for idx in indices[0]:
        context_str += vector_store["chunks"][idx] + "\n---\n"
        meta = vector_store["metadata"][idx]
        source_url = meta.get("source_url", "#")
        if source_url not in source_citations:
            source_citations[source_url] = meta.get("scheme_title", "Source Link")

    # --- PROMPT FORMAT FOR ZEPHYR MODEL ---
    system_prompt = """You are an expert assistant for Indian government schemes. 
Your task is to answer the user's question based ONLY on the provided context below.
- Be precise and directly answer the question.
- If the context contains eligibility criteria, benefits, or application steps, list them clearly using bullet points.
- If the information to answer the question is not in the context, respond:
  "Based on the provided information, I can't answer this question."
- Do not use any information outside of the provided context."""

    user_prompt = f"""
**CONTEXT:**
---
{context_str}
---

**USER'S QUESTION:**
{query}
"""

    print("🤖 Generating response with Hugging Face Zephyr-7B model...")
    try:
        completion = client.chat.completions.create(
            model="HuggingFaceH4/zephyr-7b-beta",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=512,
        )

        answer = completion.choices[0].message.content.strip()
        sources_list = [{"title": title, "url": url} for url, title in source_citations.items()]
        print("✅ LLM response generated successfully.")
        return answer, sources_list

    except Exception as e:
        print(f"❌ LLM generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"LLM generation error: {e}")

# --- Define API Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        answer, sources = get_rag_response(query=request.query, top_k=request.top_k)
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

# --- Run the Server ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
