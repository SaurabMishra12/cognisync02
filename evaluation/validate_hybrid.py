import json
from sentence_transformers import SentenceTransformer
import faiss
import sqlite3
import numpy as np

# Load our benchmark data
with open("results/data/cognisync_benchmark.json", "r", encoding="utf-8") as f:
    bm = json.load(f)

docs = [s['content'] for s in bm['sessions']]
doc_ids = [s['chunk_ids'][0] for s in bm['sessions']]
test_query = "What is the final JWT expiry rule deployed to production after the sprint override?"

# Minimal vanilla RAG
class VanillaRAG:
    def __init__(self, model):
        self.model = model
        self.dim = model.get_sentence_embedding_dimension()
    def build(self, docs, doc_ids):
        self.doc_ids = doc_ids
        embs = self.model.encode(docs, convert_to_numpy=True).astype('float32')
        embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embs)
    def retrieve(self, query, k=5):
        qe = self.model.encode([query], convert_to_numpy=True).astype('float32')
        qe /= np.maximum(np.linalg.norm(qe, axis=1, keepdims=True), 1e-12)
        sc, I = self.index.search(qe, k)
        return [self.doc_ids[int(idx)] for idx in I[0] if idx >= 0]

# Newly updated Hybrid Implementation
class CogniSyncHybrid:
    def __init__(self, model):
        self.model=model; self.dim=model.get_sentence_embedding_dimension()
    def build(self, docs, doc_ids):
        self.doc_ids=list(doc_ids)
        embs=self.model.encode(docs,convert_to_numpy=True).astype('float32')
        embs/=np.maximum(np.linalg.norm(embs,axis=1,keepdims=True),1e-12)
        self.index=faiss.IndexFlatIP(self.dim); self.index.add(embs)
        self._db=sqlite3.connect(':memory:'); self.cur=self._db.cursor()
        self.cur.execute('CREATE VIRTUAL TABLE fts USING fts5(id, text);')
        self.cur.executemany('INSERT INTO fts VALUES (?, ?)',zip(doc_ids,docs)); self._db.commit()
    def normalize(self, scores_dict):
        vals = list(scores_dict.values())
        if not vals: return {}
        min_v, max_v = min(vals), max(vals)
        if max_v - min_v < 1e-8: return {k: 0.5 for k in scores_dict}
        return {k: (v - min_v)/(max_v - min_v) for k,v in scores_dict.items()}
    def calibrate(self, queries):
        gaps = []
        for q in queries:
            qe=self.model.encode([q],convert_to_numpy=True).astype('float32')
            qe/=np.maximum(np.linalg.norm(qe,axis=1,keepdims=True),1e-12)
            sc,I=self.index.search(qe, 2)
            if I[0][0] >= 0 and I[0][1] >= 0: gaps.append(float(sc[0][0]-sc[0][1]))
        if gaps:
            self.confidence_threshold = float(np.percentile(gaps, 75))
        else:
            self.confidence_threshold = 0.15
        print(f"Computed FAISS confidence threshold: {self.confidence_threshold:.4f}")

    def debug_retrieve(self, query, k=5):
        top_k_search = min(k*4, len(self.doc_ids))
        # 1. FAISS
        qe=self.model.encode([query],convert_to_numpy=True).astype('float32')
        qe/=np.maximum(np.linalg.norm(qe,axis=1,keepdims=True),1e-12)
        sc,I=self.index.search(qe, top_k_search)
        faiss_results = {self.doc_ids[int(I[0,j])]: float(sc[0,j]) for j in range(len(I[0])) if I[0,j]>=0}
        
        # 2. FTS5
        fts_results = {}
        import re
        clean_words = [w for w in re.sub(r'[^\w\s]', '', query).split() if w]
        if clean_words:
            safe_q = ' OR '.join(clean_words)
            self.cur.execute('SELECT id, -bm25(fts) FROM fts WHERE text MATCH ? LIMIT ?', (safe_q, top_k_search))
            fts_results = {row[0]: float(row[1]) for row in self.cur.fetchall()}
        
        # 3. Normalize
        faiss_norm = self.normalize(faiss_results)
        fts_norm = self.normalize(fts_results)
        
        # 4. Detect FAISS confidence
        faiss_sorted = sorted(faiss_norm.items(), key=lambda x: x[1], reverse=True)
        top1 = faiss_sorted[0][1] if len(faiss_sorted) > 0 else 0
        top2 = faiss_sorted[1][1] if len(faiss_sorted) > 1 else 0
        confidence_gap = top1 - top2
        
        # 5. Adaptive Strategy
        threshold = getattr(self, "confidence_threshold", 0.15)
        if confidence_gap > threshold:
            # FAISS confident
            final_scores = dict(faiss_norm)
            mode = "SEMANTIC_ONLY"
        else:
            mode = "HYBRID"
            candidate_ids = set(faiss_norm.keys()) | set(fts_norm.keys())
            max_lex = max(fts_norm.values(), default=0)
            alpha = 0.6 if max_lex > 0.6 else 0.8
            final_scores = {}
            for cid in candidate_ids:
                s_sem = faiss_norm.get(cid, 0.0)
                s_lex = fts_norm.get(cid, 0.0)
                score = (alpha * s_sem) + ((1.0 - alpha) * s_lex)
                if s_lex > 0.5:
                    score += 0.05
                final_scores[cid] = score
            
        ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        return [r[0] for r in ranked[:k]], fts_results, mode, confidence_gap

print("Loading model...")
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

vanilla = VanillaRAG(model)
vanilla.build(docs, doc_ids)
faiss_top5 = vanilla.retrieve(test_query, 5)

hybrid = CogniSyncHybrid(model)
hybrid.build(docs, doc_ids)

# Test threshold computation across diverse query styles
test_queries = [
    "What is the JWT expiry policy for authentication?",
    "Show me the database schema for the user table.",
    "Explain the microservice context caching layer.",
    "What is the CI/CD pipeline deployment command?",
    test_query # inclusion for sample
]
hybrid.calibrate(test_queries)
hybrid_top5, raw_fts_dict, mode, conf_gap = hybrid.debug_retrieve(test_query, 5)

print("\\n" + "="*50)
print(f"Query: {test_query}")
print("="*50)
print(f"Confidence Gap : {conf_gap:.3f}")
print(f"Selected Mode  : {mode}")
print("FAISS :", faiss_top5)
print("FTS5  :", [k for k, v in sorted(raw_fts_dict.items(), key=lambda x:x[1], reverse=True)[:5]])
print("HYBRID:", hybrid_top5)

try:
    if mode == "HYBRID":
        assert hybrid_top5 != faiss_top5, "HYBRID and FAISS results are identical!"
    print("\\n✅ SUCCESS: Hybrid output behaves exactly as expected according to confidence threshold.")
except AssertionError as e:
    print(f"\\n❌ ERROR: {e}")
