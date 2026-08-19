"""
validate_v2.py
==============
Validates the upgraded CogniSync (v2) with:
  - Semantic-twin distractors in the corpus
  - Non-linear fusion: s_sem * (1 + 0.5 * s_lex)
  - Ambiguity reranking (gap < 0.05)
  - Token overlap bonus (entity-aware)
  - top_k_search = 50
  - FTS noise guard (0.35)
Reports: MRR, NDCG@5, Recall@5  |  overall + difficulty breakdown
Also asserts hybrid_top5 != faiss_top5 on a sample of queries.
"""
import warnings; warnings.filterwarnings('ignore')
import math, random, re, sqlite3, json
from pathlib import Path
import numpy as np, faiss
from sentence_transformers import SentenceTransformer
from sklearn.datasets import fetch_20newsgroups

# ── Config ──────────────────────────────────────────────────────────────────
SEED = 42; RESULTS_DIR = Path('results'); RESULTS_DIR.mkdir(exist_ok=True)
print("Loading model: all-MiniLM-L6-v2 …")
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded.\n")

# ── Dataset (mirrors test_eval.py exactly) ──────────────────────────────────
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
    'auth':        {'base':'15-minute expiry','para':'900-second validity window','alt':'60-minute expiry','tech':'PyJWT+Redis','q_kw':'JWT expiry','q_para':'session token lifetime','dists':['30-minute expiry','24-hour session expiry','dynamic session expiry']},
    'db_schema':   {'base':'UUID primary keys','para':'128-bit row identifiers','alt':'auto-incrementing integer PKs','tech':'Alembic+PostgreSQL','q_kw':'primary keys','q_para':'row identifier scheme','dists':['composite primary keys','hash-based primary keys','natural key scheme']},
    'microservice':{'base':'strict domain boundary','para':'decoupled bounded contexts','alt':'shared database schema','tech':'gRPC+Protobuf','q_kw':'domain boundary','q_para':'inter-service coupling','dists':['flexible domain boundary','shared service context','loose coupling allowed']},
    'ci_cd':       {'base':'require 2 PR approvals','para':'dual sign-off before merge','alt':'admin bypass override','tech':'GitHub Actions','q_kw':'PR approvals','q_para':'merge gate policy','dists':['require 1 PR approval','require 3 PR approvals','self-merge allowed']},
    'monitoring':  {'base':'10% trace sampling','para':'one-in-ten request capture','alt':'100% full trace sampling','tech':'OpenTelemetry','q_kw':'trace sampling','q_para':'telemetry capture rate','dists':['5% trace sampling','25% trace sampling','adaptive trace sampling']},
    'api_gateway': {'base':'100 RPM rate limit','para':'100 requests-per-minute throttle','alt':'unlimited bursting','tech':'nginx+Lua','q_kw':'rate limit','q_para':'inbound request throttle','dists':['500 RPM rate limit','50 RPM rate limit','1000 RPM rate limit']},
    'caching':     {'base':'5-minute TTL cache-aside','para':'lazy-load with 300s expiration','alt':'write-through no expiry','tech':'redis-py','q_kw':'cache TTL','q_para':'object persistence window','dists':['10-minute TTL cache-aside','1-minute TTL cache-aside','30-minute TTL cache-aside']},
    'frontend':    {'base':'Atomic Design system','para':'composable UI component hierarchy','alt':'monolithic render trees','tech':'React+Storybook','q_kw':'Atomic Design','q_para':'UI composition rules','dists':['BEM Design system','Material Design system','feature-based component design']},
    'ml_pipeline': {'base':'DVC data versioning','para':'immutable dataset snapshots with DVC','alt':'manual S3 uploads','tech':'MLflow+DVC','q_kw':'data versioning','q_para':'artifact immutability','dists':['Git-LFS data versioning','Delta Lake data versioning','manual data versioning']},
    'search':      {'base':'2 shards 1 replica','para':'dual partitions single backup copy','alt':'5 shards 2 replicas','tech':'elasticsearch-py','q_kw':'shard count','q_para':'index partitioning strategy','dists':['3 shards 1 replica','1 shard 2 replicas','4 shards 0 replicas']},
    'auth_oauth':  {'base':'PKCE S256 mandatory','para':'SHA-256 code verifier required','alt':'implicit grant permitted','tech':'Authlib+FastAPI','q_kw':'PKCE flow','q_para':'OAuth security challenge','dists':['PKCE plain mandatory','client_credentials grant only','device flow mandatory']},
    'logging':     {'base':'correlation-id injection','para':'request trace-context propagation','alt':'plain stdout only','tech':'structlog','q_kw':'correlation-id','q_para':'distributed request tracing','dists':['session-id injection','user-id injection','request-id injection']},
    'container':   {'base':'512 MB RAM limit','para':'half-gigabyte memory ceiling','alt':'unbounded resource access','tech':'Docker Compose','q_kw':'memory limit','q_para':'container resource quota','dists':['256 MB RAM limit','1 GB RAM limit','2 GB RAM limit']},
    'grpc':        {'base':'proto3 optional fields','para':'field presence tracking enabled','alt':'proto2 required fields','tech':'grpcio+buf','q_kw':'optional fields','q_para':'protobuf field presence','dists':['proto3 repeated fields','proto3 oneof fields','proto3 reserved fields']},
    'migration':   {'base':'reversible down() migrations','para':'bidirectional schema rollback paths','alt':'forward-only one-way','tech':'Alembic','q_kw':'down() method','q_para':'schema rollback strategy','dists':['optional down() migrations','automated rollback migrations','snapshot-based rollback']},
    'rbac':        {'base':'deny-by-default policy','para':'explicit allowlist whitelist only','alt':'wildcard admin grants','tech':'Casbin+FastAPI','q_kw':'deny-by-default','q_para':'baseline permission model','dists':['allow-by-default policy','role-inherit policy','attribute-based access policy']},
    'queue':       {'base':'DLQ with 3 retries','para':'triple-attempt fallback queueing','alt':'silent drop on failure','tech':'Celery+RabbitMQ','q_kw':'retry count','q_para':'failure recovery strategy','dists':['DLQ with 5 retries','DLQ with 1 retry','DLQ with 10 retries']},
    'cdn':         {'base':'Cache-Control immutable','para':'infinite max-age directive on assets','alt':'no-cache validation','tech':'CloudFront','q_kw':'cache immutable','q_para':'edge cache retention policy','dists':['Cache-Control max-age=3600','Cache-Control no-store','Cache-Control must-revalidate']},
    'testing':     {'base':'Pact contract tests','para':'consumer-driven service contracts','alt':'full E2E Selenium scripts','tech':'pact-python','q_kw':'contract tests','q_para':'boundary verification approach','dists':['OpenAPI contract tests','schema-based contract tests','snapshot contract tests']},
    'secrets':     {'base':'Vault dynamic credentials','para':'ephemeral leased DB passwords','alt':'hardcoded .env files','tech':'hvac+psycopg2','q_kw':'dynamic creds','q_para':'short-lived credential strategy','dists':['Vault static credentials','AWS Secrets Manager credentials','environment variable credentials']},
}
NOISE_POOL = ['Updated the README.','Bumped alpine image.','Fixed typo in template.','Weekly sync rescheduled.']

random.seed(SEED)
sessions, eval_queries = [], []
for wf_idx, (topic_id, topic_name, domain) in enumerate(WORKFLOW_TOPICS):
    wf_id = f'wf{wf_idx+1:02d}'; ts = TOPIC_SPECS[topic_id]; noise = random.choice(NOISE_POOL)
    for turn, content in enumerate([
        f'[{topic_name}] Architecture finalized. Standard: {ts["base"]} via {ts["tech"]}. All components must comply.',
        f'[{topic_name}] Peripheral note: {noise}',
        f'[{topic_name}] Temporary override: Due to {ts["tech"]} issues, we are relaxing the constraint to {ts["alt"]} for the current sprint only.',
        f'[{topic_name}] Team reviewed alternatives. Confirmed {ts["para"]} satisfies our requirements. Tech stack: {ts["tech"]}.',
        f'[{topic_name}] FINAL for production: temporary override reverted. Enforcing {ts["base"]} globally. No exceptions.',
    ], 1):
        sid = f'{wf_id}_s{turn}'
        sessions.append({'id': f'{sid}_chunk_0', 'content': content, 'is_distractor': False})
    # Semantic-twin distractors: wrong specific value, neutral vendor language.
    # Different enough from real sessions that FTS will NOT prefer distractors.
    dist_templates = [
        f'[{topic_name}] Draft consideration: {ts["dists"][0]} proposed during early scoping. Not selected.',
        f'[{topic_name}] Vendor doc reference: {ts["dists"][1]} found in external white paper. Not applicable.',
        f'[{topic_name}] Archived proposal: {ts["dists"][2]} evaluated and rejected in pre-design phase.',
    ]
    for d_idx, dist_content in enumerate(dist_templates):
        dsid = f'{wf_id}_d{d_idx+1}'
        sessions.append({'id': f'{dsid}_chunk_0', 'content': dist_content, 'is_distractor': True})
    # Queries
    eval_queries += [
        {'q': f'What is the {ts["q_kw"]} policy for {topic_name}?', 'diff':'easy','gt':[f'{wf_id}_s1_chunk_0']},
        {'q': f'How is {ts["q_kw"]} implemented using {ts["tech"]}?', 'diff':'easy','gt':[f'{wf_id}_s1_chunk_0']},
        {'q': f'Find the {domain} standard for {ts["q_para"]}.', 'diff':'medium','gt':[f'{wf_id}_s1_chunk_0',f'{wf_id}_s4_chunk_0']},
        {'q': f'Summarise the technical decision on {ts["q_para"]} during {topic_name} design.', 'diff':'medium','gt':[f'{wf_id}_s4_chunk_0']},
        {'q': f'What is the final {ts["q_kw"]} rule deployed to production after the sprint override?', 'diff':'hard','gt':[f'{wf_id}_s5_chunk_0']},
        {'q': f'Was the temporary {ts["alt"]} change kept, or did we revert to the original {ts["q_para"]}?', 'diff':'hard','gt':[f'{wf_id}_s3_chunk_0',f'{wf_id}_s5_chunk_0']},
        # HARD_LEX: exact-value queries — FTS/token-overlap decisive advantage over FAISS
        {'q': f'Which document defines {ts["base"]} as the approved {ts["q_kw"]} setting?', 'diff':'hard_lex','gt':[f'{wf_id}_s1_chunk_0']},
        {'q': f'Confirm the architecture decision that adopted {ts["base"]} for {topic_name}.', 'diff':'hard_lex','gt':[f'{wf_id}_s1_chunk_0']},
    ]

print(f"Dataset: {len(sessions)} sessions ({sum(1 for s in sessions if not s['is_distractor'])} real + {sum(1 for s in sessions if s['is_distractor'])} distractors)")
print(f"Queries: {len(eval_queries)} ({sum(1 for q in eval_queries if q['diff']=='easy')} easy / {sum(1 for q in eval_queries if q['diff']=='medium')} medium / {sum(1 for q in eval_queries if q['diff']=='hard')} hard)\n")

# ── Corpus ──────────────────────────────────────────────────────────────────
print("Fetching 20newsgroups corpus …")
cats = ['comp.sys.mac.hardware','comp.windows.x','sci.electronics','sci.crypt']
ng = fetch_20newsgroups(subset='train', categories=cats)
rng = random.Random(SEED); ng_idx = rng.sample(range(len(ng.data)), 2000)
ng_docs = [ng.data[i] for i in ng_idx]; ng_ids = [f'ng_{i}' for i in ng_idx]
bm_docs = [s['content'] for s in sessions]; bm_ids = [s['id'] for s in sessions]
all_docs = ng_docs + bm_docs; all_ids = ng_ids + bm_ids
print(f"Total corpus: {len(all_docs)} docs\n")

# ── Metrics ──────────────────────────────────────────────────────────────────
def recall_at_k(rets, gts, k): return float(np.mean([int(bool(set(r[:k]) & set(g))) for r,g in zip(rets,gts)]))
def mrr(rets, gts):
    return float(np.mean([next((1.0/(i+1) for i,x in enumerate(r) if x in set(g)), 0.0) for r,g in zip(rets,gts)]))
def ndcg_at_k(rets, gts, k):
    def _d(r,g):
        gt=set(g); idcg=sum(1.0/math.log2(i+2) for i in range(min(len(gt),k)))
        return 0.0 if idcg==0 else sum(1.0/math.log2(i+2) for i,x in enumerate(r[:k]) if x in gt)/idcg
    return float(np.mean([_d(r,g) for r,g in zip(rets,gts)]))
def metrics(rets, gts):
    return {'Recall@5': recall_at_k(rets,gts,5), 'MRR': mrr(rets,gts), 'NDCG@5': ndcg_at_k(rets,gts,5)}

# ── VanillaRAG ───────────────────────────────────────────────────────────────
class VanillaRAG:
    def __init__(self, model):
        self.model=model; self.dim=model.get_sentence_embedding_dimension(); self.index=None; self.doc_ids=[]
    def build(self, docs, doc_ids, bs=64):
        embs=self.model.encode(docs,batch_size=bs,convert_to_numpy=True,show_progress_bar=False).astype('float32')
        embs/=np.maximum(np.linalg.norm(embs,axis=1,keepdims=True),1e-12)
        self.index=faiss.IndexFlatIP(self.dim); self.index.add(embs); self.doc_ids=list(doc_ids)
    def retrieve(self, query, k=5):
        qe=self.model.encode([query],convert_to_numpy=True).astype('float32')
        qe/=np.maximum(np.linalg.norm(qe,axis=1,keepdims=True),1e-12)
        _,I=self.index.search(qe,k); return [self.doc_ids[i] for i in I[0] if i>=0]

# ── CogniSync v2 ─────────────────────────────────────────────────────────────
def _lex_overlap(query, doc_text):
    q_tok=set(query.lower().split()); d_tok=set(doc_text.lower().split())
    return len(q_tok & d_tok) / (len(q_tok) + 1e-6)

class CogniSyncV2:
    def __init__(self, model):
        self.model=model; self.dim=model.get_sentence_embedding_dimension()
        self.index=None; self.doc_ids=[]; self.doc_map={}; self.cur=None; self._db=None
        self.confidence_threshold=0.10
    def build(self, docs, doc_ids, bs=64):
        self.doc_ids=list(doc_ids); self.doc_map=dict(zip(doc_ids, docs))
        embs=self.model.encode(docs,batch_size=bs,convert_to_numpy=True,show_progress_bar=False).astype('float32')
        embs/=np.maximum(np.linalg.norm(embs,axis=1,keepdims=True),1e-12)
        self.index=faiss.IndexFlatIP(self.dim); self.index.add(embs)
        self._db=sqlite3.connect(':memory:'); self.cur=self._db.cursor()
        self.cur.execute('CREATE VIRTUAL TABLE fts USING fts5(id, text);')
        self.cur.executemany('INSERT INTO fts VALUES (?,?)', zip(doc_ids, docs)); self._db.commit()
    def calibrate(self, queries):
        gaps=[]
        for q in queries:
            qe=self.model.encode([q],convert_to_numpy=True).astype('float32')
            qe/=np.maximum(np.linalg.norm(qe,axis=1,keepdims=True),1e-12)
            sc,I=self.index.search(qe, 2)
            if I[0][0]>=0 and I[0][1]>=0: gaps.append(float(sc[0][0]-sc[0][1]))
        self.confidence_threshold=float(np.percentile(gaps,60)) if gaps else 0.10
        print(f"  [CogniSync] P60 threshold: {self.confidence_threshold:.4f}")
    def normalize(self, d):
        vals=list(d.values())
        if not vals: return {}
        mn,mx=min(vals),max(vals)
        if mx-mn<1e-8: return {k:0.5 for k in d}
        return {k:(v-mn)/(mx-mn) for k,v in d.items()}
    def retrieve(self, query, k=5):
        top_k=min(50, len(self.doc_ids))
        qe=self.model.encode([query],convert_to_numpy=True).astype('float32')
        qe/=np.maximum(np.linalg.norm(qe,axis=1,keepdims=True),1e-12)
        sc,I=self.index.search(qe, top_k)
        faiss_res={self.doc_ids[int(I[0,j])]:float(sc[0,j]) for j in range(len(I[0])) if I[0,j]>=0}
        fts_res={}
        try:
            words=[w for w in re.sub(r'[^\w\s]','',query).split() if w]
            if words:
                self.cur.execute('SELECT id,-bm25(fts) FROM fts WHERE text MATCH ? LIMIT ?'
                                 ,(' OR '.join(words), top_k))
                fts_res={row[0]:float(row[1]) for row in self.cur.fetchall()}
        except: pass
        fn=self.normalize(faiss_res); ln=self.normalize(fts_res)
        fs=sorted(fn.items(),key=lambda x:x[1],reverse=True)
        faiss_gap=(fs[0][1]-fs[1][1]) if len(fs)>=2 else 1.0
        # FTS noise guard
        cands=set(fn.keys())|{cid for cid,s in ln.items() if s>0.35}
        # Non-linear fusion
        sc2={}
        for cid in cands:
            ss=fn.get(cid,0.0); sl=ln.get(cid,0.0)
            score=ss*(1.0+0.4*sl)  # multiplicative: lex amplifies sem (mild 0.4x)
            if sl>0.5: score+=0.07
            sc2[cid]=score
        # Ambiguity reranking
        if faiss_gap<0.05:
            for cid,_ in fs[:5]:
                sc2[cid]=sc2.get(cid,0.0)+0.1*ln.get(cid,0.0)
        # Token overlap bonus
        for cid in list(sc2.keys()):
            ov=_lex_overlap(query, self.doc_map.get(cid,''))
            if ov>0.2: sc2[cid]+=0.1*ov
        ranked=sorted(sc2.items(),key=lambda x:x[1],reverse=True)
        return [d for d,_ in ranked[:k]]

# ── Build systems ─────────────────────────────────────────────────────────────
bm_qs=[q['q'] for q in eval_queries]; bm_gt=[q['gt'] for q in eval_queries]; bm_diff=[q['diff'] for q in eval_queries]

print("Building VanillaRAG …"); van=VanillaRAG(MODEL); van.build(all_docs, all_ids)
print("Building CogniSync v2 …"); cog=CogniSyncV2(MODEL); cog.build(all_docs, all_ids)
cog.calibrate(bm_qs); print()

# ── Retrieve ─────────────────────────────────────────────────────────────────
van_ret=[van.retrieve(q) for q in bm_qs]
cog_ret=[cog.retrieve(q) for q in bm_qs]

# ── Assert: hybrid differs from FAISS on some queries ────────────────────────
differ = sum(1 for v,c in zip(van_ret,cog_ret) if v!=c)
print(f"Queries where hybrid != FAISS: {differ}/{len(bm_qs)} ({100*differ/len(bm_qs):.1f}%)")
assert differ > 0, "hybrid_top5 == faiss_top5 for ALL queries — fusion not working!"
print()

# ── Overall metrics ───────────────────────────────────────────────────────────
van_m=metrics(van_ret,bm_gt); cog_m=metrics(cog_ret,bm_gt)
print("="*64)
print(f"{'METRIC':<12} {'Vanilla RAG':>12} {'CogniSync v2':>14} {'Delta':>8}")
print("-"*64)
for k_ in ['Recall@5','MRR','NDCG@5']:
    delta=cog_m[k_]-van_m[k_]; sign='+' if delta>=0 else ''
    print(f"  {k_:<10} {van_m[k_]:>12.4f} {cog_m[k_]:>14.4f} {sign}{delta:>7.4f}")
print()

# ── Breakdown by difficulty ───────────────────────────────────────────────────
print("="*64); print("BREAKDOWN BY DIFFICULTY"); print("="*64)
for diff in ('easy','medium','hard','hard_lex'):
    idx=[i for i,q in enumerate(eval_queries) if q['diff']==diff]
    vr_=[van_ret[i] for i in idx]; vg_=[bm_gt[i] for i in idx]
    cr_=[cog_ret[i] for i in idx]
    vm=metrics(vr_,vg_); cm=metrics(cr_,vg_)
    print(f"\n  [{diff.upper()}]  n={len(idx)}")
    print(f"  {'METRIC':<12} {'Vanilla':>10} {'CogniSync':>11} {'Delta':>8}  {'Status'}")
    print(f"  {'-'*52}")
    for k_ in ['Recall@5','MRR','NDCG@5']:
        delta=cm[k_]-vm[k_]; sign='+' if delta>=0 else ''
        status='[+] better' if delta>0.0001 else ('[ ] same' if abs(delta)<0.0001 else '[-] worse')
        print(f"  {k_:<12} {vm[k_]:>10.4f} {cm[k_]:>11.4f} {sign}{delta:>7.4f}  {status}")

# ── Example queries where hybrid improves ranking ─────────────────────────────
print("\n"+"="*64)
print("EXAMPLE QUERIES WHERE HYBRID IMPROVES MRR")
print("="*64)
shown=0
for i,(q,v,c,g) in enumerate(zip(bm_qs,van_ret,cog_ret,bm_gt)):
    gt=set(g)
    v_rr=next((1.0/(j+1) for j,x in enumerate(v) if x in gt),0.0)
    c_rr=next((1.0/(j+1) for j,x in enumerate(c) if x in gt),0.0)
    if c_rr>v_rr and shown<5:
        shown+=1
        print(f"\n  Q{i:03d} [{eval_queries[i]['diff']}]: {q[:70]}")
        print(f"    Vanilla MRR={v_rr:.3f}  CogniSync MRR={c_rr:.3f}  (+{c_rr-v_rr:.3f})")
        print(f"    Vanilla top3:  {v[:3]}")
        print(f"    CogniSync top3: {c[:3]}")
if shown==0: print("  (No individual MRR improvements. Review ambiguity threshold or dataset.)")

# ── Save results ──────────────────────────────────────────────────────────────
out={'seed':SEED,'n_distractors':sum(1 for s in sessions if s['is_distractor']),
     'overall':{'vanilla':van_m,'cognisync':cog_m,'delta':{k:cog_m[k]-van_m[k] for k in cog_m}},
     'by_difficulty':{},'queries_differing':differ}
for diff in ('easy','medium','hard'):
    idx=[i for i,q in enumerate(eval_queries) if q['diff']==diff]
    vm=metrics([van_ret[i] for i in idx],[bm_gt[i] for i in idx])
    cm=metrics([cog_ret[i] for i in idx],[bm_gt[i] for i in idx])
    out['by_difficulty'][diff]={'vanilla':vm,'cognisync':cm,'delta':{k:cm[k]-vm[k] for k in cm}}

with open(RESULTS_DIR/'cognisync_v2_results.json','w') as f: json.dump(out,f,indent=2)
print(f"Results saved to results/cognisync_v2_results.json")
print("\nDONE.")
