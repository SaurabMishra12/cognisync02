"""
diagnose_medium.py
Shows exactly which medium queries lose hits and why.
"""
import warnings; warnings.filterwarnings('ignore')
import re, random, sqlite3, math
import numpy as np, faiss
from sentence_transformers import SentenceTransformer
from sklearn.datasets import fetch_20newsgroups

MODEL = SentenceTransformer('all-MiniLM-L6-v2')

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
NOISE_POOL = ['Updated README.', 'Bumped alpine image.', 'Fixed typo.', 'Rescheduled sync.']

random.seed(42)
sessions, eval_queries = [], []
for wf_idx, (topic_id, topic_name, domain) in enumerate(WORKFLOW_TOPICS):
    wf_id = f'wf{wf_idx+1:02d}'; ts = TOPIC_SPECS[topic_id]; noise = random.choice(NOISE_POOL)
    sess_texts = [
        f'[{topic_name}] Architecture finalized. Standard: {ts["base"]} via {ts["tech"]}. All components must comply.',
        f'[{topic_name}] Peripheral note: {noise}',
        f'[{topic_name}] Temporary override: relaxing constraint to {ts["alt"]} for current sprint.',
        f'[{topic_name}] Team confirmed {ts["para"]} satisfies requirements. Tech stack: {ts["tech"]}.',
        f'[{topic_name}] FINAL: enforcing {ts["base"]} globally. No exceptions.',
    ]
    for turn, content in enumerate(sess_texts, 1):
        sid = f'{wf_id}_s{turn}'; sessions.append({'id': f'{sid}_chunk_0', 'content': content})
    eval_queries.append({'q': f'Find the {domain} standard for {ts["q_para"]}.', 'diff':'medium',
                         'gt':[f'{wf_id}_s1_chunk_0', f'{wf_id}_s4_chunk_0']})
    eval_queries.append({'q': f'Summarise the technical decision on {ts["q_para"]} during {topic_name} design.',
                         'diff':'medium','gt':[f'{wf_id}_s4_chunk_0']})

cats = ['comp.sys.mac.hardware','comp.windows.x','sci.electronics','sci.crypt']
ng = fetch_20newsgroups(subset='train', categories=cats)
rng = random.Random(42); ng_idx = rng.sample(range(len(ng.data)), 2000)
ng_docs = [ng.data[i] for i in ng_idx]; ng_ids = [f'ng_{i}' for i in ng_idx]
bm_docs = [s['content'] for s in sessions]; bm_ids = [s['id'] for s in sessions]
all_docs = ng_docs + bm_docs; all_ids  = ng_ids  + bm_ids

print(f"Encoding {len(all_docs)} docs...")
embs = MODEL.encode(all_docs, batch_size=64, convert_to_numpy=True, show_progress_bar=False).astype('float32')
embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
index = faiss.IndexFlatIP(384); index.add(embs)
db = sqlite3.connect(':memory:'); cur = db.cursor()
cur.execute('CREATE VIRTUAL TABLE fts USING fts5(id, text);')
cur.executemany('INSERT INTO fts VALUES (?,?)', zip(all_ids, all_docs)); db.commit()

# Calibrate threshold
bm_qs = [q['q'] for q in eval_queries]
gaps = []
for q in bm_qs:
    qe = MODEL.encode([q], convert_to_numpy=True).astype('float32')
    qe /= np.maximum(np.linalg.norm(qe,axis=1,keepdims=True),1e-12)
    sc,I = index.search(qe, 2)
    if I[0][0]>=0 and I[0][1]>=0: gaps.append(float(sc[0][0]-sc[0][1]))
threshold = float(np.percentile(gaps, 60)) if gaps else 0.10
print(f"Threshold (P60) = {threshold:.4f}\n")

def normalize(d):
    vals = list(d.values())
    if not vals: return {}
    mn, mx = min(vals), max(vals)
    if mx-mn < 1e-8: return {k:0.5 for k in d}
    return {k:(v-mn)/(mx-mn) for k,v in d.items()}

losses, gains = 0, 0
MIN_FTS_ENTRY = 0.35

print("MEDIUM QUERY LOSS CASES:")
print("="*70)
for q_info in eval_queries:
    q, gt = q_info['q'], q_info['gt']
    qe = MODEL.encode([q], convert_to_numpy=True).astype('float32')
    qe /= np.maximum(np.linalg.norm(qe,axis=1,keepdims=True),1e-12)
    sc, I = index.search(qe, 20)
    faiss_res = {all_ids[int(I[0,j])]: float(sc[0,j]) for j in range(20) if I[0,j]>=0}
    faiss_norm = normalize(faiss_res)
    try:
        words = [w for w in re.sub(r'[^\w\s]','',q).split() if w]
        cur.execute('SELECT id, -bm25(fts) FROM fts WHERE text MATCH ? LIMIT 20', (' OR '.join(words),))
        fts_res = {row[0]: float(row[1]) for row in cur.fetchall()}
    except: fts_res = {}
    fts_norm = normalize(fts_res)

    faiss_sorted = sorted(faiss_norm.items(), key=lambda x:x[1], reverse=True)
    gap = faiss_sorted[0][1]-faiss_sorted[1][1] if len(faiss_sorted)>1 else 0
    van_top5 = [d for d,_ in faiss_sorted[:5]]
    van_hit = any(g in van_top5 for g in gt)

    conf = min(gap/threshold, 1.0); alpha = 0.6+0.3*conf
    cands = set(faiss_norm.keys()) | {cid for cid,s in fts_norm.items() if s>MIN_FTS_ENTRY}
    final = {}
    for cid in cands:
        ss = faiss_norm.get(cid, 0.0); sl = fts_norm.get(cid, 0.0)
        score = alpha*ss + (1-alpha)*sl
        if sl > 0.5: score += 0.07
        final[cid] = score
    fused_top5 = [d for d,_ in sorted(final.items(), key=lambda x:x[1], reverse=True)[:5]]
    fused_hit = any(g in fused_top5 for g in gt)

    if van_hit and not fused_hit:
        losses += 1
        print(f"\nLOSS #{losses}: {q[:70]}")
        print(f"  GT: {gt}")
        gt_in_faiss = [(g, faiss_norm.get(g,'—'), fts_norm.get(g,'—')) for g in gt]
        print(f"  GT FAISS/FTS norms: {gt_in_faiss}")
        print(f"  conf={conf:.3f}  alpha={alpha:.4f}  gap={gap:.4f}")
        print(f"  Vanilla top5: {van_top5}")
        print(f"  Fused   top5: {fused_top5}")
        new_in_fused = [d for d in fused_top5 if d not in van_top5]
        if new_in_fused:
            for d in new_in_fused:
                print(f"  [intruder] {d}: fts_norm={fts_norm.get(d,0):.4f}")
        else:
            print("  No new docs from FTS -- GTs were re-ranked DOWN by alpha weighting")
            for g in gt:
                if g in van_top5:
                    van_rank = van_top5.index(g)
                    fused_rank = fused_top5.index(g) if g in fused_top5 else 99
                    print(f"    GT {g}: vanilla rank={van_rank+1}  fused rank={fused_rank+1}")
                    print(f"      sem={faiss_norm.get(g,0):.4f}  lex={fts_norm.get(g,0):.4f}"
                          f"  fused_score={final.get(g,0):.4f}")
    elif fused_hit and not van_hit:
        gains += 1

print(f"\nSummary: {losses} losses, {gains} gains out of {len(eval_queries)} medium queries")
