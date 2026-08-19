import os
import logging
import sys

# Mute Huggingface verbose output which breaks JSON-RPC stdout
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# Setup Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, ".qdrant")

# Connect to Qdrant Local Database (Pure Python/Rust binaries, NO C++ Compilers needed!)
client = QdrantClient(path=DB_PATH)

_text_model = None
_vision_model = None

def get_text_model():
    global _text_model
    if _text_model is None:
        import sys
        print("Loading Text Embedding Model (MiniLM)...", file=sys.stderr)
        _text_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _text_model

def get_vision_model():
    global _vision_model
    if _vision_model is None:
        import sys
        print("Loading Vision Embedding Model (CLIP)...", file=sys.stderr)
        _vision_model = SentenceTransformer("clip-ViT-B-32")
    return _vision_model

# Initialize Collections safely
collections = [c.name for c in client.get_collections().collections]

if "faraday_text" not in collections:
    client.create_collection(
        collection_name="faraday_text",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

if "faraday_vision" not in collections:
    client.create_collection(
        collection_name="faraday_vision",
        vectors_config=VectorParams(size=512, distance=Distance.COSINE)
    )

def query_hybrid(query_text: str, limit: int = 5):
    """Hits deep-text system and returns standard Markdown."""
    
    text_vector = get_text_model().encode(query_text).tolist()
    
    results = client.query_points(
        collection_name="faraday_text",
        query=text_vector,
        limit=limit
    )
    
    merged = []
    for r in results.points:
        merged.append({
            "type": "text",
            "content": r.payload.get("text", ""),
            "metadata": {"source": r.payload.get("source", "Unknown")}
        })
        
    return {"results": merged}

def ingest_text(documents, metadatas, ids):
    import sys
    import logging
    
    BATCH_SIZE = 64
    total = len(documents)
    sys.stderr.write(f"Starting batch embedding of {total} chunks...\n")
    sys.stderr.flush()
    
    for i in range(0, total, BATCH_SIZE):
        batch_docs = documents[i : i + BATCH_SIZE]
        batch_metas = metadatas[i : i + BATCH_SIZE]
        batch_ids = ids[i : i + BATCH_SIZE]
        
        # Batch encode is 50x-100x faster than a loop
        vectors = get_text_model().encode(batch_docs, show_progress_bar=False).tolist()
        
        points = []
        for vector, doc, meta, _id in zip(vectors, batch_docs, batch_metas, batch_ids):
            payload = {"text": doc, "source": meta.get("source", "Unknown")}
            points.append(PointStruct(id=_id, vector=vector, payload=payload))
            
        client.upsert(
            collection_name="faraday_text",
            points=points
        )
        
        sys.stderr.write(f"Ingested {min(i + BATCH_SIZE, total)}/{total} chunks...\n")
        sys.stderr.flush()
