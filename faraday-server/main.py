from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

import database

app = FastAPI(
    title="Faraday Context Server",
    description="Local RestAPI exposing the Faraday Vault to Vibe-Coding tools (Antigravity, Cursor, etc.)",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str
    limit: int = 5

@app.get("/")
def health_check():
    return {"status": "online", "model": "Hybrid (CLIP + MiniLM)"}

@app.post("/search")
def search_brain(request: QueryRequest):
    """
    Given a query text, search the Vector Brain across both Text and Vision collections.
    Returns highly relevant Markdown snippets and Image Paths.
    """
    try:
        results = database.query_hybrid(request.query, request.limit)
        return {"query": request.query, "context": results["results"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Bound to Localhost. Data is 100% safe from external internet access.
    uvicorn.run(app, host="127.0.0.1", port=8000)
