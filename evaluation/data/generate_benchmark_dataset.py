"""
generate_benchmark_dataset.py
------------------------------
Generates the CogniSync Benchmark Dataset v1.0.

Structure
---------
20 multi-session developer workflows × 5 sessions each = 100 sessions.
200 evaluation queries, each with:
  - ground-truth session links
  - required constraints the retrieval system must recall
  - task_type label

All content is deterministically generated from seeds and templates so the
dataset is fully reproducible without any LLM API calls.

Output
------
  data/cognisync_benchmark.json   — the benchmark dataset
  data/README_dataset.md          — schema documentation (auto-generated)

Usage
-----
  python generate_benchmark_dataset.py
"""

import json
import random
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────

SEED = 42
random.seed(SEED)

N_WORKFLOWS = 20
SESSIONS_PER_WORKFLOW = 5
N_EVAL_QUERIES = 200          # 10 queries per workflow
CHUNK_WORDS_TARGET = 120      # approximate words per session chunk

OUTPUT_PATH = Path(__file__).parent / "cognisync_benchmark.json"
README_PATH = Path(__file__).parent / "README_dataset.md"

# ─────────────────────────────────────────────────────────
# Workflow Templates
# ─────────────────────────────────────────────────────────

WORKFLOW_TOPICS = [
    # (topic_id, name, domain)
    ("auth",        "JWT Authentication System",       "backend"),
    ("db_schema",   "Database Schema Design",          "backend"),
    ("microservice","Microservice Decomposition",      "architecture"),
    ("ci_cd",       "CI/CD Pipeline Configuration",   "devops"),
    ("monitoring",  "Observability Stack Setup",       "devops"),
    ("api_gateway", "API Gateway Rate Limiting",       "backend"),
    ("caching",     "Distributed Caching Strategy",   "backend"),
    ("frontend",    "React Component Architecture",   "frontend"),
    ("ml_pipeline", "ML Training Pipeline",           "mlops"),
    ("search",      "Elasticsearch Index Design",     "backend"),
    ("auth_oauth",  "OAuth2 / PKCE Flow",             "security"),
    ("logging",     "Structured Logging Standard",    "devops"),
    ("container",   "Docker Compose Orchestration",   "devops"),
    ("grpc",        "gRPC Service Contract",           "backend"),
    ("migration",   "Database Migration Strategy",    "backend"),
    ("rbac",        "Role-Based Access Control",       "security"),
    ("queue",       "Message Queue Architecture",      "backend"),
    ("cdn",         "CDN Cache Invalidation",          "frontend"),
    ("testing",     "Integration Test Strategy",       "qa"),
    ("secrets",     "Secrets Management Flow",         "security"),
]

# Session templates per turn
SESSION_TEMPLATES = [
    # Turn 1: define the constraint / decision
    "{topic_name}: Established core design decision — {constraint}. "
    "The system will use {tech_detail}. All future components must comply with this standard.",

    # Turn 2: implement first component using constraints
    "Implemented {component_a} following the {constraint} standard. "
    "Used {tech_detail} as the primary mechanism. Integration tests passed with 0 failures.",

    # Turn 3: encounter edge case
    "Discovered edge case in {component_a}: {edge_case}. "
    "Resolution: apply {constraint} with an additional {fix_detail}. Updated docs.",

    # Turn 4: extend to second component
    "Extended {constraint} compliance to {component_b}. "
    "Reused {tech_detail} adapter. Verified backward compatibility across all endpoints.",

    # Turn 5: finalize and document
    "Final architecture review complete. {constraint} enforced across {component_a} and {component_b}. "
    "{tech_detail} configuration locked. Added to project runbook.",
]

# Constraint templates per topic
TOPIC_CONSTRAINTS = {
    "auth":         ("jwt_expiry_15min_refresh_rotation",   "HS256 JWT with 15-minute expiry and refresh-token rotation",      "PyJWT + Redis TTL",   "auth middleware", "token refresh service"),
    "db_schema":    ("snake_case_naming_uuid_pk",           "snake_case column naming with UUID primary keys",                 "Alembic + PostgreSQL","user_profile table", "audit_log table"),
    "microservice": ("domain_bounded_context_isolation",    "strict domain-bounded context isolation between services",        "gRPC + Protobuf",     "user-service",    "order-service"),
    "ci_cd":        ("branch_protection_main_staging",      "protect main and staging branches with required review gates",    "GitHub Actions",      "deploy workflow", "test pipeline"),
    "monitoring":   ("opentelemetry_traces_required",       "OpenTelemetry distributed tracing on all HTTP handlers",          "Jaeger + Prometheus", "api-service",     "worker-service"),
    "api_gateway":  ("rate_limit_100rpm_per_user",          "100 requests-per-minute rate limit keyed per authenticated user", "nginx + Lua",         "gateway config",  "upstream health check"),
    "caching":      ("cache_aside_redis_5min_ttl",          "cache-aside pattern with Redis and 5-minute TTL",                 "redis-py",            "product catalog", "search results cache"),
    "frontend":     ("atomic_design_storybook_required",    "Atomic Design with Storybook documentation for all components",   "React + Storybook",   "Button atom",     "UserCard molecule"),
    "ml_pipeline":  ("mlflow_experiment_tracking_required", "MLflow experiment tracking on every training run",               "MLflow + DVC",        "train.py",        "evaluate.py"),
    "search":       ("es_sharding_2_replicas_1",            "Elasticsearch index with 2 shards and 1 replica",                "elasticsearch-py",    "product index",   "log index"),
    "auth_oauth":   ("pkce_s256_required_no_implicit",      "PKCE S256 challenge required; implicit flow disabled",           "Authlib + FastAPI",   "authorization endpoint", "token endpoint"),
    "logging":      ("structured_json_logs_correlation_id", "structured JSON logs with correlation-id on every request",      "structlog",           "http middleware", "worker logger"),
    "container":    ("resource_limits_512m_1cpu",           "Docker resource limits: 512 MB RAM, 1 CPU per container",        "Docker Compose",      "web service",     "worker service"),
    "grpc":         ("proto3_required_backward_compat",     "Proto3 syntax with mandatory backward-compatible field additions","grpcio + buf",        "UserService",     "OrderService"),
    "migration":    ("reversible_migrations_only_down",     "all migrations must include a reversible down() method",         "Alembic",             "schema v2",       "schema v3"),
    "rbac":         ("least_privilege_role_scopes",         "least-privilege role scopes; no wildcard permissions",           "Casbin + FastAPI",    "admin role",      "viewer role"),
    "queue":        ("dlq_retry_3_exponential_backoff",     "dead-letter queue with 3 retries and exponential backoff",       "Celery + RabbitMQ",   "email tasks",     "report tasks"),
    "cdn":          ("cache_control_max_age_3600_immutable","Cache-Control: max-age=3600, immutable for versioned assets",    "CloudFront",          "static assets",   "API responses"),
    "testing":      ("contract_tests_pact_required",        "Pact contract tests required between all service boundaries",    "pact-python",         "consumer tests",  "provider tests"),
    "secrets":      ("vault_dynamic_db_credentials",        "HashiCorp Vault dynamic database credentials; no static secrets","hvac + psycopg2",     "db connection",   "service auth"),
}

EDGE_CASES = [
    "concurrent write conflict under high load",
    "token expiry race condition at network boundary",
    "schema migration failure rollback path",
    "cache stampede under cold-start conditions",
    "gRPC deadline propagation through nested calls",
    "OAuth code reuse attack window",
    "Redis eviction during peak traffic",
    "log correlation-id loss across async boundaries",
    "container OOM under memory pressure",
    "Proto field renaming breaking backward compat",
]

FIX_DETAILS = [
    "optimistic locking via version columns",
    "a 30-second clock-skew buffer on token validation",
    "atomic Alembic batch operations with savepoints",
    "distributed lock via Redis SETNX",
    "a gRPC timeout interceptor at each service boundary",
    "PKCE state validation on redirect",
    "a fallback to DB with async cache warming",
    "explicit context propagation via structlog contextvars",
    "a readiness probe with memory headroom check",
    "field aliases in the Protobuf descriptor",
]

# Eval query templates (require memory recall from earlier sessions)
QUERY_TEMPLATES = [
    ("api_integration",   "Implement {component_b} — make sure to apply the {constraint_key} standard defined earlier."),
    ("cross_session",     "We are adding a new {component_b}. What auth/configuration constraint was established in the prior session for {topic_name}?"),
    ("debugging",         "The {component_a} is failing after deployment. What is the canonical {constraint_key} fix we documented?"),
    ("code_generation",   "Generate a {component_a} stub that complies with {constraint_key} as agreed in our project runbook."),
    ("api_integration",   "The new service gateway needs to enforce {constraint_key}. Retrieve the configuration template from memory."),
    ("cross_session",     "Onboarding a new engineer to {topic_name}. Summarize the {constraint_key} decision made in Session 1."),
    ("debugging",         "Reproducing the {edge_case} incident. What resolution was documented for {topic_name}?"),
    ("code_generation",   "Scaffold a {component_b} module following the {constraint_key} conventions defined in this project."),
    ("api_integration",   "Extend {component_a} to support {component_b}. Recall the {tech_detail} adapter pattern we agreed on."),
    ("cross_session",     "Architecture review thread: confirm that {component_a} and {component_b} both comply with {constraint_key}."),
]


# ─────────────────────────────────────────────────────────
# Generation Logic
# ─────────────────────────────────────────────────────────

def make_chunk_id(session_id: str, chunk_idx: int) -> str:
    return f"{session_id}_chunk_{chunk_idx}"


def generate_session_content(turn: int, topic_id: str, workflow_idx: int) -> tuple[str, list[str]]:
    """Return (content_text, constraints_introduced)."""
    topic_name, constraint, tech_detail, component_a, component_b = TOPIC_CONSTRAINTS[topic_id][1:]
    constraint_key = TOPIC_CONSTRAINTS[topic_id][0]
    edge_case = EDGE_CASES[workflow_idx % len(EDGE_CASES)]
    fix_detail = FIX_DETAILS[workflow_idx % len(FIX_DETAILS)]

    template = SESSION_TEMPLATES[turn - 1]
    content = template.format(
        topic_name=topic_name,
        constraint=constraint,
        constraint_key=constraint_key,
        tech_detail=tech_detail,
        component_a=component_a,
        component_b=component_b,
        edge_case=edge_case,
        fix_detail=fix_detail,
    )
    constraints = [constraint_key] if turn == 1 else []
    return content, constraints


def generate_eval_query(query_idx: int, workflow_id: str, topic_id: str, workflow_idx: int) -> dict:
    """Generate one evaluation query for a workflow."""
    topic_name, constraint, tech_detail, component_a, component_b = TOPIC_CONSTRAINTS[topic_id][1:]
    constraint_key = TOPIC_CONSTRAINTS[topic_id][0]
    edge_case = EDGE_CASES[workflow_idx % len(EDGE_CASES)]

    q_template_idx = query_idx % len(QUERY_TEMPLATES)
    task_type, q_template = QUERY_TEMPLATES[q_template_idx]

    query_text = q_template.format(
        topic_name=topic_name,
        constraint=constraint,
        constraint_key=constraint_key,
        tech_detail=tech_detail,
        component_a=component_a,
        component_b=component_b,
        edge_case=edge_case,
    )

    # Ground truth: queries about constraint always require session 1
    required_session = f"{workflow_id}_s1"
    ground_truth_chunk = make_chunk_id(required_session, 0)

    # Debugging queries additionally require session 3 (edge case resolution)
    if task_type == "debugging":
        required_sessions = [required_session, f"{workflow_id}_s3"]
        ground_truth_chunks = [ground_truth_chunk, make_chunk_id(f"{workflow_id}_s3", 0)]
    else:
        required_sessions = [required_session]
        ground_truth_chunks = [ground_truth_chunk]

    return {
        "query_id": f"q{workflow_idx:02d}_{query_idx:02d}",
        "workflow_id": workflow_id,
        "query": query_text,
        "task_type": task_type,
        "required_sessions": required_sessions,
        "required_constraints": [constraint_key],
        "ground_truth_chunk_ids": ground_truth_chunks,
    }


def generate_dataset() -> dict:
    sessions = []
    eval_queries = []

    base_time = datetime(2025, 1, 1, 9, 0, 0)

    for wf_idx, (topic_id, topic_name, domain) in enumerate(WORKFLOW_TOPICS):
        workflow_id = f"wf{wf_idx + 1:02d}"

        for turn in range(1, SESSIONS_PER_WORKFLOW + 1):
            session_id = f"{workflow_id}_s{turn}"
            session_time = base_time + timedelta(days=wf_idx * 3, hours=(turn - 1) * 8)
            content, constraints = generate_session_content(turn, topic_id, wf_idx)

            chunk_id = make_chunk_id(session_id, 0)
            chunk_hash = hashlib.md5(content.encode()).hexdigest()[:8]

            sessions.append({
                "session_id": session_id,
                "workflow_id": workflow_id,
                "topic_id": topic_id,
                "topic_name": topic_name,
                "domain": domain,
                "turn": turn,
                "timestamp": session_time.isoformat(),
                "content": content,
                "word_count": len(content.split()),
                "tags": [topic_id, domain, f"turn_{turn}"],
                "constraints_introduced": constraints,
                "chunk_ids": [chunk_id],
                "chunk_hash": chunk_hash,
            })

        # Generate 10 evaluation queries per workflow
        for q_idx in range(10):
            query = generate_eval_query(q_idx, workflow_id, topic_id, wf_idx)
            eval_queries.append(query)

    return {
        "dataset_name": "CogniSync Benchmark",
        "version": "1.0.0",
        "description": (
            "A benchmark dataset for evaluating persistent agent memory systems. "
            "Contains 20 multi-session developer workflows, each with 5 sessions "
            "that introduce architectural constraints. 200 evaluation queries require "
            "recalling past decisions to succeed."
        ),
        "stats": {
            "n_workflows": N_WORKFLOWS,
            "n_sessions": len(sessions),
            "n_eval_queries": len(eval_queries),
            "task_types": list({q["task_type"] for q in eval_queries}),
            "domains": list({s["domain"] for s in sessions}),
            "seed": SEED,
            "generated_at": datetime.utcnow().isoformat() + "Z",
        },
        "sessions": sessions,
        "eval_queries": eval_queries,
    }


# ─────────────────────────────────────────────────────────
# README generation
# ─────────────────────────────────────────────────────────

README_TEMPLATE = """\
# CogniSync Benchmark Dataset v1.0

A reproducible benchmark for evaluating **persistent agent memory** systems.
Generated deterministically from `generate_benchmark_dataset.py` (seed={seed}).

## Statistics
| Field | Value |
|---|---|
| Workflows | {n_workflows} |
| Sessions | {n_sessions} |
| Eval Queries | {n_eval_queries} |
| Task Types | {task_types} |
| Domains | {domains} |

## Schema

### `sessions[]`
| Field | Type | Description |
|---|---|---|
| `session_id` | str | Unique ID, format `wfXX_sY` |
| `workflow_id` | str | Parent workflow, format `wfXX` |
| `topic_id` | str | Topic identifier (e.g. `auth`, `ci_cd`) |
| `topic_name` | str | Human-readable topic name |
| `domain` | str | Technical domain (backend, devops, ...) |
| `turn` | int | Session turn within workflow (1–5) |
| `timestamp` | str | ISO-8601 simulated timestamp |
| `content` | str | Full session text content |
| `word_count` | int | Word count of content |
| `tags` | list[str] | Topic, domain, and turn tags |
| `constraints_introduced` | list[str] | Constraints introduced in this session |
| `chunk_ids` | list[str] | Chunk IDs for retrieval evaluation |
| `chunk_hash` | str | MD5 hash prefix for dedup verification |

### `eval_queries[]`
| Field | Type | Description |
|---|---|---|
| `query_id` | str | Unique query ID, format `qXX_YY` |
| `workflow_id` | str | Parent workflow |
| `query` | str | Natural language query text |
| `task_type` | str | One of: api_integration, cross_session, debugging, code_generation |
| `required_sessions` | list[str] | Sessions the query requires memory of |
| `required_constraints` | list[str] | Constraints that must be recalled |
| `ground_truth_chunk_ids` | list[str] | Ground-truth chunks for Recall@K scoring |

## Evaluation Protocol
A retrieval system **succeeds** on a query if at least one `ground_truth_chunk_id`
appears in its Top-K results (`K ∈ {1, 3, 5, 10}`).

## Licence
CC BY 4.0 — free for research use with attribution.
"""


# ─────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating CogniSync Benchmark Dataset v1.0...")
    dataset = generate_dataset()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    stats = dataset["stats"]
    readme = README_TEMPLATE.format(
        seed=SEED,
        n_workflows=stats["n_workflows"],
        n_sessions=stats["n_sessions"],
        n_eval_queries=stats["n_eval_queries"],
        task_types=", ".join(sorted(stats["task_types"])),
        domains=", ".join(sorted(stats["domains"])),
    )
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"  ✅ Dataset  → {OUTPUT_PATH}")
    print(f"  ✅ README   → {README_PATH}")
    print(f"  Sessions: {stats['n_sessions']} | Queries: {stats['n_eval_queries']}")
