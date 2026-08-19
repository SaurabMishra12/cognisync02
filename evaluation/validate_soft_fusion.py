"""
validate_soft_fusion.py
========================
Fast validation of the Soft Adaptive Fusion fix.
Runs Seed 42 only.  Prints:
  - Per-query alpha & confidence diagnostics (first 10 queries)
  - CogniSync vs Vanilla RAG: MRR / NDCG@5 / Recall@5
  - Breakdown by difficulty: easy / medium / hard
"""
import warnings; warnings.filterwarnings('ignore')
import time, math, random, sqlite3, re, json
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sklearn.datasets import fetch_20newsgroups

# ── Config ─────────────────────────────────────────────────────────────────
SEED            = 42
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
DEFAULT_TOP_K   = 5
RESULTS_DIR     = Path('results'); RESULTS_DIR.mkdir(exist_ok=True)

print(f"Loading model: {EMBEDDING_MODEL} ...")
MODEL = SentenceTransformer(EMBEDDING_MODEL)
print("Model loaded.\n")

# ── Dataset (same as full eval) ─────────────────────────────────────────────
WORKFLOW_TOPICS = [
    ('auth','JWT Authentication','backend'),
    ('db_schema','Database Schema','backend'),
    ('microservice','Microservice Context','architecture'),
    ('ci_cd','CI/CD Pipeline','devops'),
    ('monitoring','Observability Stack','devops'),
    ('api_gateway','API Gateway Rate Limiting','backend'),
    ('caching','Distributed Caching','backend'),
    ('frontend','React Architecture','frontend'),
    ('ml_pipeline','ML Training Pipeline','mlops'),
    ('search','Elasticsearch Design','backend'),
    ('auth_oauth','OAuth2 Flow','security'),
    ('logging','Structured Logging','devops'),
    ('container','Docker Compose','devops'),
    ('grpc','gRPC Service Contract','backend'),
    ('migration','Database Migration','backend'),
    ('rbac','RBAC Access Control','security'),
    ('queue','Message Queue','backend'),
    ('cdn','CDN Cache Invalidation','frontend'),
    ('testing','Integration Testing','qa'),
    ('secrets','Secrets Management','security'),
]
TOPIC_SPECS = {
    'auth':        {'base':'15-minute expiry','para':'900-second validity window','alt':'60-minute expiry','tech':'PyJWT+Redis','q_kw':'JWT expiry','q_para':'session token lifetime'},
    'db_schema':   {'base':'UUID primary keys','para':'128-bit row identifiers','alt':'auto-incrementing integer PKs','tech':'Alembic+PostgreSQL','q_kw':'primary keys','q_para':'row identifier scheme'},
    'microservice':{'base':'strict domain boundary','para':'decoupled bounded contexts','alt':'shared database schema','tech':'gRPC+Protobuf','q_kw':'domain boundary','q_para':'inter-service coupling'},
    'ci_cd':       {'base':'require 2 PR approvals','para':'dual sign-off before merge','alt':'admin bypass override','tech':'GitHub Actions','q_kw':'PR approvals','q_para':'merge gate policy'},
    'monitoring':  {'base':'10% trace sampling','para':'one-in-ten request capture','alt':'100% full trace sampling','tech':'OpenTelemetry','q_kw':'trace sampling','q_para':'telemetry capture rate'},
    'api_gateway': {'base':'100 RPM rate limit','para':'100 requests-per-minute throttle','alt':'unlimited bursting','tech':'nginx+Lua','q_kw':'rate limit','q_para':'inbound request throttle'},
    'caching':     {'base':'5-minute TTL cache-aside','para':'lazy-load with 300s expiration','alt':'write-through no expiry','tech':'redis-py','q_kw':'cache TTL','q_para':'object persistence window'},
    'frontend':    {'base':'Atomic Design system','para':'composable UI component hierarchy','alt':'monolithic render trees','tech':'React+Storybook','q_kw':'Atomic Design','q_para':'UI composition rules'},
    'ml_pipeline': {'base':'DVC data versioning','para':'immutable dataset snapshots with DVC','alt':'manual S3 uploads','tech':'MLflow+DVC','q_kw':'data versioning','q_para':'artifact immutability'},
    'search':      {'base':'2 shards 1 replica','para':'dual partitions single backup copy','alt':'5 shards 2 replicas','tech':'elasticsearch-py','q_kw':'shard count','q_para':'index partitioning strategy'},
    'auth_oauth':  {'base':'PKCE S256 mandatory','para':'SHA-256 code verifier required','alt':'implicit grant permitted','tech':'Authlib+FastAPI','q_kw':'PKCE flow','q_para':'OAuth security challenge'},
    'logging':     {'base':'correlation-id injection','para':'request trace-context propagation','alt':'plain stdout only','tech':'structlog','q_kw':'correlation-id','q_para':'distributed request tracing'},
    'container':   {'base':'512 MB RAM limit','para':'half-gigabyte memory ceiling','alt':'unbounded resource access','tech':'Docker Compose','q_kw':'memory limit','q_para':'container resource quota'},
    'grpc':        {'base':'proto3 optional fields','para':'field presence tracking enabled','alt':'proto2 required fields','tech':'grpcio+buf','q_kw':'optional fields','q_para':'protobuf field presence'},
    'migration':   {'base':'reversible down() migrations','para':'bidirectional schema rollback paths','alt':'forward-only one-way','tech':'Alembic','q_kw':'down() method','q_para':'schema rollback strategy'},
    'rbac':        {'base':'deny-by-default policy','para':'explicit allowlist whitelist only','alt':'wildcard admin grants','tech':'Casbin+FastAPI','q_kw':'deny-by-default','q_para':'baseline permission model'},
    'queue':       {'base':'DLQ with 3 retries','para':'triple-attempt fallback queueing','alt':'silent drop on failure','tech':'Celery+RabbitMQ','q_kw':'retry count','q_para':'failure recovery strategy'},
    'cdn':         {'base':'Cache-Control immutable','para':'infinite max-age directive on assets','alt':'no-cache validation','tech':'CloudFront','q_kw':'cache immutable','q_para':'edge cache retention policy'},
    'testing':     {'base':'Pact contract tests','para':'consumer-driven service contracts','alt':'full E2E Selenium scripts','tech':'pact-python','q_kw':'contract tests','q_para':'boundary verification approach'},
    'secrets':     {'base':'Vault dynamic credentials','para':'ephemeral leased DB passwords','alt':'hardcoded .env files','tech':'hvac+psycopg2','q_kw':'dynamic creds','q_para':'short-lived credential strategy'},
}
NOISE_POOL = [
    'Updated the README with new local setup instructions.',
    'Bumped base alpine image to address recent libssl CVEs.',
    'Fixed typo in user onboarding email template.',
    'Weekly sync rescheduled from Friday to Thursday.',
]

random.seed(42)
sessions, eval_queries = [], []
for wf_idx, (topic_id, topic_name, domain) in enumerate(WORKFLOW_TOPICS):
    wf_id = f'wf{wf_idx+1:02d}'; ts = TOPIC_SPECS[topic_id]
    noise = random.choice(NOISE_POOL)
    sess_texts = [
        f'[{topic_name}] Architecture finalized. Standard: {ts["base"]} via {ts["tech"]}. All components must comply.',
        f'[{topic_name}] Peripheral note: {noise}',
        f'[{topic_name}] Temporary override: Due to {ts["tech"]} issues, relaxing constraint to {ts["alt"]} for current sprint only.',
        f'[{topic_name}] Team confirmed {ts["para"]} satisfies requirements. Tech stack: {ts["tech"]}.',
        f'[{topic_name}] FINAL for production: temporary override reverted. Enforcing {ts["base"]} globally. No exceptions.',
    ]
    for turn, content in enumerate(sess_texts, 1):
        sid = f'{wf_id}_s{turn}'
        sessions.append({'session_id': sid, 'chunk_ids': [f'{sid}_chunk_0'], 'content': content})
    eval_queries += [
        {'query': f'What is the {ts["q_kw"]} policy for {topic_name}?', 'difficulty': 'easy',
         'ground_truth_chunk_ids': [f'{wf_id}_s1_chunk_0']},
        {'query': f'How is {ts["q_kw"]} implemented using {ts["tech"]}?', 'difficulty': 'easy',
         'ground_truth_chunk_ids': [f'{wf_id}_s1_chunk_0']},
        {'query': f'Find the {domain} standard for {ts["q_para"]}.', 'difficulty': 'medium',
         'ground_truth_chunk_ids': [f'{wf_id}_s1_chunk_0', f'{wf_id}_s4_chunk_0']},
        {'query': f'Summarise the technical decision on {ts["q_para"]} during {topic_name} design.', 'difficulty': 'medium',
         'ground_truth_chunk_ids': [f'{wf_id}_s4_chunk_0']},
        {'query': f'What is the final {ts["q_kw"]} rule deployed to production after the sprint override?', 'difficulty': 'hard',
         'ground_truth_chunk_ids': [f'{wf_id}_s5_chunk_0']},
        {'query': f'Was the temporary {ts["alt"]} change kept, or did we revert to the original {ts["q_para"]}?', 'difficulty': 'hard',
         'ground_truth_chunk_ids': [f'{wf_id}_s3_chunk_0', f'{wf_id}_s5_chunk_0']},
    ]

# ── Corpus ──────────────────────────────────────────────────────────────────
print("Fetching 20newsgroups corpus ...")
cats = ['comp.sys.mac.hardware','comp.windows.x','sci.electronics','sci.crypt']
ng_dataset = fetch_20newsgroups(subset='train', categories=cats)
rng_base = random.Random(42)
ng_indices = rng_base.sample(range(len(ng_dataset.data)), 2000)
ng_docs = [ng_dataset.data[i] for i in ng_indices]
ng_ids  = [f'ng_{i}' for i in ng_indices]

bm_docs = [s['content']           for s in sessions]
bm_ids  = [s['chunk_ids'][0]      for s in sessions]
bm_qs   = [q['query']             for q in eval_queries]
bm_gt   = [q['ground_truth_chunk_ids'] for q in eval_queries]
bm_diff = [q['difficulty']         for q in eval_queries]

all_docs = ng_docs + bm_docs
all_ids  = ng_ids  + bm_ids
print(f"Corpus: {len(all_docs)} docs\n")

# ── Metrics ──────────────────────────────────────────────────────────────────
def _hit(r, g, k): return int(bool(set(r[:k]) & set(g)))
def recall_at_k(all_r, all_g, k): return float(np.mean([_hit(r,g,k) for r,g in zip(all_r,all_g)]))
def mrr_score(all_r, all_g):
    out=[]
    for r,g in zip(all_r,all_g):
        gt=set(g); out.append(next((1.0/(i+1) for i,x in enumerate(r) if x in gt), 0.0))
    return float(np.mean(out))
def ndcg_at_k(all_r, all_g, k):
    def _d(r,g):
        gt=set(g); ideal=min(len(gt),k)
        idcg=sum(1.0/math.log2(i+2) for i in range(ideal))
        if idcg==0: return 0.0
        return sum(1.0/math.log2(i+2) for i,x in enumerate(r[:k]) if x in gt)/idcg
    return float(np.mean([_d(r,g) for r,g in zip(all_r,all_g)]))

# ── VanillaRAG ───────────────────────────────────────────────────────────────
class VanillaRAG:
    def __init__(self, model):
        self.model=model; self.dim=model.get_sentence_embedding_dimension()
        self.index=None; self.doc_ids=[]
    def build(self, docs, doc_ids, bs=64):
        embs=self.model.encode(docs,batch_size=bs,convert_to_numpy=True,show_progress_bar=False).astype('float32')
        embs/=np.maximum(np.linalg.norm(embs,axis=1,keepdims=True),1e-12)
        self.index=faiss.IndexFlatIP(self.dim); self.index.add(embs); self.doc_ids=list(doc_ids)
    def retrieve(self, query, k=5):
        qe=self.model.encode([query],convert_to_numpy=True).astype('float32')
        qe/=np.maximum(np.linalg.norm(qe,axis=1,keepdims=True),1e-12)
        _,I=self.index.search(qe,k)
        return [self.doc_ids[i] for i in I[0] if i>=0]

# ── CogniSync Soft Adaptive Fusion ───────────────────────────────────────────
class CogniSyncHybrid:
    def __init__(self, model):
        self.model=model; self.dim=model.get_sentence_embedding_dimension()
        self.index=None; self.doc_ids=[]; self.cur=None; self._db=None
        self.confidence_threshold = 0.15

    def build(self, docs, doc_ids, bs=64):
        self.doc_ids=list(doc_ids)
        embs=self.model.encode(docs,batch_size=bs,convert_to_numpy=True,show_progress_bar=False).astype('float32')
        embs/=np.maximum(np.linalg.norm(embs,axis=1,keepdims=True),1e-12)
        self.index=faiss.IndexFlatIP(self.dim); self.index.add(embs)
        self._db=sqlite3.connect(':memory:'); self.cur=self._db.cursor()
        self.cur.execute('CREATE VIRTUAL TABLE fts USING fts5(id, text);')
        self.cur.executemany('INSERT INTO fts VALUES (?, ?)', zip(doc_ids, docs))
        self._db.commit()

    def calibrate(self, queries):
        gaps = []
        for q in queries:
            qe=self.model.encode([q],convert_to_numpy=True).astype('float32')
            qe/=np.maximum(np.linalg.norm(qe,axis=1,keepdims=True),1e-12)
            sc,I=self.index.search(qe, 2)
            if I[0][0] >= 0 and I[0][1] >= 0:
                gaps.append(float(sc[0][0] - sc[0][1]))
        self.confidence_threshold = float(np.percentile(gaps, 60)) if gaps else 0.10
        print(f"  [CogniSync] Threshold P60 = {self.confidence_threshold:.4f}")
        print(f"  [CogniSync] Gap range: min={min(gaps):.4f}  median={np.median(gaps):.4f}  max={max(gaps):.4f}")

    def normalize(self, scores_dict):
        vals = list(scores_dict.values())
        if not vals: return {}
        mn, mx = min(vals), max(vals)
        if mx - mn < 1e-8: return {k: 0.5 for k in scores_dict}
        return {k: (v - mn)/(mx - mn) for k,v in scores_dict.items()}

    def retrieve(self, query, k=5, _debug=False):
        top_k_search = min(k*4, len(self.doc_ids))
        qe=self.model.encode([query],convert_to_numpy=True).astype('float32')
        qe/=np.maximum(np.linalg.norm(qe,axis=1,keepdims=True),1e-12)
        sc,I=self.index.search(qe, top_k_search)
        faiss_results = {self.doc_ids[int(I[0,j])]: float(sc[0,j])
                         for j in range(len(I[0])) if I[0,j]>=0}
        fts_results = {}
        try:
            clean_words = [w for w in re.sub(r'[^\w\s]', '', query).split() if w]
            if clean_words:
                safe_q = ' OR '.join(clean_words)
                self.cur.execute('SELECT id, -bm25(fts) FROM fts WHERE text MATCH ? LIMIT ?',
                                 (safe_q, top_k_search))
                fts_results = {row[0]: float(row[1]) for row in self.cur.fetchall()}
        except:
            pass

        faiss_norm = self.normalize(faiss_results)
        fts_norm   = self.normalize(fts_results)

        faiss_sorted = sorted(faiss_norm.items(), key=lambda x: x[1], reverse=True)
        top1 = faiss_sorted[0][1] if len(faiss_sorted) > 0 else 0.0
        top2 = faiss_sorted[1][1] if len(faiss_sorted) > 1 else 0.0
        confidence_gap = top1 - top2
        threshold = self.confidence_threshold
        confidence = confidence_gap / (threshold + 1e-8)
        confidence = max(0.0, min(confidence, 1.0))
        alpha = 0.6 + 0.3 * confidence

        # Only admit FTS-exclusive docs if they have strong signal (>0.35).
        # Prevents paraphrased/noisy FTS results from displacing correct FAISS docs.
        MIN_FTS_ENTRY = 0.35
        candidate_ids = set(faiss_norm.keys()) | {
            cid for cid, score in fts_norm.items() if score > MIN_FTS_ENTRY
        }
        final_scores = {}
        for cid in candidate_ids:
            s_sem = faiss_norm.get(cid, 0.0)
            s_lex = fts_norm.get(cid, 0.0)
            score = (alpha * s_sem) + ((1.0 - alpha) * s_lex)
            if s_lex > 0.5:
                score += 0.07
            final_scores[cid] = score

        ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        if _debug:
            return [d for d,_ in ranked[:k]], confidence, alpha
        return [d for d,_ in ranked[:k]]

# ── Build systems ─────────────────────────────────────────────────────────────
print("Building VanillaRAG ...")
van = VanillaRAG(MODEL); van.build(all_docs, all_ids)

print("Building CogniSync ...")
cog = CogniSyncHybrid(MODEL); cog.build(all_docs, all_ids)
cog.calibrate(bm_qs)
print()

# ── Diagnostics: alpha varies across queries ──────────────────────────────────
print("=" * 60)
print("DIAGNOSTIC: confidence & alpha on first 10 benchmark queries")
print("=" * 60)
print(f"{'Query[:50]':<52} {'Conf':>5} {'Alpha':>6}")
print("-" * 60)
for i, q in enumerate(bm_qs[:10]):
    _, conf, alp = cog.retrieve(q, k=DEFAULT_TOP_K, _debug=True)
    print(f"  {q[:50]:<50} {conf:>5.3f}  {alp:>6.4f}")
print()

# ── Full eval on benchmark queries (all 120) ──────────────────────────────────
van_ret, cog_ret = [], []
for q in bm_qs:
    van_ret.append(van.retrieve(q, k=DEFAULT_TOP_K))
    cog_ret.append(cog.retrieve(q, k=DEFAULT_TOP_K))

# ── Overall metrics ───────────────────────────────────────────────────────────
def metrics(all_r, all_g):
    return {
        'Recall@5':  recall_at_k(all_r, all_g, 5),
        'MRR':       mrr_score(all_r, all_g),
        'NDCG@5':    ndcg_at_k(all_r, all_g, 5),
    }

van_m = metrics(van_ret, bm_gt)
cog_m = metrics(cog_ret, bm_gt)

print("=" * 60)
print(f"{'METRIC':<12} {'Vanilla RAG':>12} {'CogniSync':>12} {'Delta':>8}")
print("-" * 60)
for k_ in ['Recall@5', 'MRR', 'NDCG@5']:
    delta = cog_m[k_] - van_m[k_]
    sign  = '+' if delta >= 0 else ''
    print(f"  {k_:<10} {van_m[k_]:>12.4f} {cog_m[k_]:>12.4f} {sign}{delta:>7.4f}")
print()

# ── Breakdown by difficulty ───────────────────────────────────────────────────
print("=" * 60)
print("BREAKDOWN BY DIFFICULTY")
print("=" * 60)
for diff in ('easy', 'medium', 'hard'):
    idx = [i for i,q in enumerate(eval_queries) if q['difficulty'] == diff]
    vr_ = [van_ret[i] for i in idx]; vg_ = [bm_gt[i] for i in idx]
    cr_ = [cog_ret[i] for i in idx]; cg_ = [bm_gt[i] for i in idx]
    vm  = metrics(vr_, vg_); cm = metrics(cr_, cg_)
    print(f"\n  [{diff.upper()}]  n={len(idx)}")
    print(f"  {'METRIC':<12} {'Vanilla':>10} {'CogniSync':>11} {'Delta':>8}")
    print(f"  {'-'*45}")
    for k_ in ['Recall@5', 'MRR', 'NDCG@5']:
        delta = cm[k_] - vm[k_]
        sign  = '+' if delta >= 0 else ''
        print(f"  {k_:<12} {vm[k_]:>10.4f} {cm[k_]:>11.4f} {sign}{delta:>7.4f}")
print()

# ── Save results ──────────────────────────────────────────────────────────────
out = {
    'seed': SEED,
    'overall': {'vanilla': van_m, 'cognisync': cog_m,
                'delta': {k: cog_m[k]-van_m[k] for k in cog_m}},
    'by_difficulty': {}
}
for diff in ('easy', 'medium', 'hard'):
    idx = [i for i,q in enumerate(eval_queries) if q['difficulty'] == diff]
    vr_ = [van_ret[i] for i in idx]; vg_ = [bm_gt[i] for i in idx]
    cr_ = [cog_ret[i] for i in idx]
    vm  = metrics(vr_, vg_); cm = metrics(cr_, vg_)
    out['by_difficulty'][diff] = {'vanilla': vm, 'cognisync': cm,
                                   'delta': {k: cm[k]-vm[k] for k in cm}}

with open(RESULTS_DIR / 'soft_fusion_validation.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"Results saved to results/soft_fusion_validation.json")
print("\nDONE.")
