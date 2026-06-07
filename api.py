"""
Mentat API — FastAPI backend for the BM25 search engine.
Serves search results from pre-crawled programming resources.
"""

import json
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from bm25_search import BM25Search

# ---------------------------------------------------------------------------
# Load documents & initialise search
# ---------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "documents.json")

print("⏳ Loading documents …")
with open(DATA_PATH) as f:
    docs = json.load(f)
print(f"✅ Loaded {len(docs)} documents")

search_engine = BM25Search(docs)
print("✅ BM25 index built")

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Mentat Search API",
    description="BM25-powered search across GitHub, Reddit & Medium programming resources.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@app.get("/api/search")
def search(q: str = Query(..., min_length=1, description="Search query"), top_k: int = Query(10, ge=1, le=50)):
    """Run a BM25 search and return ranked results."""
    results = search_engine.search(q, top_k=top_k)
    return {
        "query": q,
        "total": len(results),
        "results": [
            {
                "title": doc["title"],
                "url": doc["url"],
                "preview": doc.get("preview", doc["content"][:200]),
                "score": round(score, 4),
                "source": _detect_source(doc["url"]),
            }
            for doc, score in results
        ],
    }


@app.get("/api/stats")
def stats():
    """Return corpus statistics."""
    sources = {}
    for doc in docs:
        src = _detect_source(doc["url"])
        sources[src] = sources.get(src, 0) + 1

    return {
        "total_documents": len(docs),
        "sources": sources,
    }


# ---------------------------------------------------------------------------
# Serve the frontend (static files)
# ---------------------------------------------------------------------------
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

if os.path.isdir(FRONTEND_DIR):

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

    # Serve static assets before the catch-all
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _detect_source(url: str) -> str:
    if "github.com" in url:
        return "github"
    if "reddit.com" in url:
        return "reddit"
    if "medium.com" in url:
        return "medium"
    return "other"
