# CogniSync Results Analysis for Publishability

Date: 2026-04-17

Scope:
- `faraday-server/results/*`
- `evaluation/results/*`
- `evaluation/build_neurips_notebook.py`
- `paper/cognisync_paper.tex`

This note analyzes the saved result artifacts. It does not rerun the benchmarks.

## Bottom Line

The current artifacts support a modest systems-and-safety paper much more strongly than a retrieval-SOTA paper.

What is genuinely strong:
- CogniSync beats all open-source memory baselines on aggregate retrieval.
- CogniSync matches Pinecone-sim retrieval quality while being much faster locally.
- Sanitization cuts leakage risk by 93-100% across the three attacks that were evaluated.
- Hybrid recall never falls below vanilla recall in the scalability study, even at 100k documents.

What is not yet strong enough for a NeurIPS/EMNLP main-track claim:
- The gain over Vanilla RAG is small: `+1.33` Recall@5 points, `+1.21` MRR points.
- On the workflow benchmark slice, CogniSync beats Vanilla RAG on only `1 / 50` queries at hit@5 and ties on the other `49`.
- Agent-task success is identical to Vanilla RAG.
- The ablation study shows `hybrid == faiss_only` on recall and MRR in the saved CSV.
- The retrieval benchmark only uses the first `50 / 160` workflow queries, covering only `7 / 20` workflows and `3 / 7` domains.
- The draft paper claims much larger numbers than the current saved results support.

## Strongest Publishable Results

### 1. Systems Pareto: local quality close to best baseline, cloud-free latency

From `faraday-server/results/retrieval_aggregated.csv`:

- CogniSync Recall@5: `79.47`
- Vanilla RAG Recall@5: `78.13`
- Pinecone (sim) Recall@5: `78.13`
- CogniSync latency: `28.73 ms`
- Pinecone (sim) latency: `223.36 ms`

Interpretation:
- CogniSync gains `+1.33` Recall@5 points over Vanilla RAG.
- CogniSync matches or exceeds the Pinecone-sim quality regime while running `7.77x` faster.
- This is a credible systems result even if the absolute accuracy gain is small.

### 2. Security story is stronger than the retrieval story

From `faraday-server/results/security_eval.csv`:

- Prompt injection leakage MRR: `0.90 -> 0.00` after sanitization (`100%` reduction)
- Tool spoofing leakage MRR: `1.00 -> 0.038` (`96.2%` reduction)
- Data exfiltration leakage MRR: `1.00 -> 0.070` (`93.0%` reduction)

Interpretation:
- The sanitization layer is the clearest headline result in the current artifacts.
- This is likely the strongest reviewer-facing contribution in the saved outputs.

### 3. Scalability is stable and non-regressive on recall

From `faraday-server/results/scalability_results.csv`:

- Mean hybrid recall gain over vanilla by scale:
  - `2k docs`: `+0.00` points
  - `10k docs`: `+1.67` points
  - `50k docs`: `+0.83` points
  - `100k docs`: `+0.83` points
- Mean hybrid latency:
  - `29.58 ms` at `2k`
  - `51.67 ms` at `100k`
- Mean hybrid p99 latency stays under `76 ms` even at `100k` docs.

Interpretation:
- The hybrid method scales reasonably well and does not lose recall against vanilla as corpus size grows.
- This supports a systems-efficiency claim.

## Hidden Patterns Reviewers Will Notice

### 1. The hybrid gain is sparse, not broad

Using `faraday-server/results/retrieval_per_query.csv`:

- On the workflow benchmark slice, hit@5 gain over Vanilla RAG appears on `1 / 50` queries.
- On the 20NG portion, hit@5 gain appears on only `6` query instances, with `1` loss.
- The overall statistical significance is coming from a small number of consistent wins, not broad per-query improvement.

Important implication:
- The honest claim is "small but consistent improvement" rather than "substantial accuracy lift."

### 2. Workflow benchmark saturation is hiding the weakness

The workflow benchmark slice is already near saturation:

- Vanilla RAG hit@5 on the workflow slice: `96.0%`
- CogniSync hit@5 on the workflow slice: `98.0%`

This means:
- There is very little room left for improvement.
- A stronger benchmark should stress conflict resolution, cross-session memory, and exact disambiguation harder than the current saved slice does.

### 3. The retrieval evaluation samples only the first 50 workflow queries

From `evaluation/build_neurips_notebook.py`, the retrieval benchmark uses:

- `queries = ng_q + bm_queries[:50]`

Consequences:
- Only `7 / 20` workflows are covered.
- Only `backend`, `devops`, and `architecture` domains appear.
- `security`, `frontend`, `mlops`, and `qa` are excluded from the retrieval benchmark slice.

This is a major evaluation-bias issue for a top-tier paper.

### 4. Gains are concentrated in lexical/entity-heavy cases

Qualitatively, the saved wins are mostly on metadata-heavy or exact-policy queries:

- 20NG wins cluster in `sci.crypt` and `sci.electronics`.
- No hit@5 gains appear in `comp.sys.mac.hardware` or `comp.windows.x`.
- The single workflow hit@5 rescue is:
  - `What is the rate limit policy for API Gateway Rate Limiting?`

What happened there:
- Vanilla retrieved a distractor-heavy top-5 and missed the policy source chunk.
- CogniSync swapped the correct policy chunk into the top-5 in all five seeds.

This supports a narrower claim:
- Hybrid lexical-semantic fusion helps exact policy recovery under distractor competition.

### 5. Ablation currently weakens the "hybrid retrieval" argument

From `faraday-server/results/ablation_results.csv`:

- `faiss_only` and `hybrid` have identical recall and MRR across the saved rows.
- `fts5_only` is `0.00` on recall and MRR in every saved row.

Implication:
- The current ablation file does not show that lexical retrieval materially contributes to the measured gains.
- Reviewers will likely ask why the main paper claims hybrid benefit if the ablation says the semantic branch is doing all the work.

### 6. Agent-task evaluation does not show superiority over Vanilla RAG

From `faraday-server/results/agent_task_aggregated.csv`:

- Macro success:
  - CogniSync: `93.75%`
  - Vanilla RAG: `93.75%`
- Macro MRR:
  - CogniSync: `77.56`
  - Vanilla RAG: `78.06`
- Cross-session MRR:
  - CogniSync: `73.92`
  - Vanilla RAG: `69.75`

Interpretation:
- The only encouraging signal is better cross-session ranking.
- But the success metric is saturated and does not separate the systems.
- This is not enough for a main empirical claim.

### 7. The security benchmark supports leakage prevention, not poisoning resistance

In the saved `security_eval.csv`:

- `poisoning_rate = 0.0` for every attack and condition.

Implication:
- The current benchmark validates leakage mitigation.
- It does not validate resistance to retrieval poisoning or context poisoning.

## Mismatch Between Draft Paper and Current Results

The draft paper (`paper/cognisync_paper.tex`) claims much larger numbers than the saved NeurIPS evaluation artifacts show, including:

- `97.33%` Recall@5 hybrid
- `0.34 ms` local retrieval latency
- `312.15 ms` cloud baseline

But the current saved results in `faraday-server/results` show:

- `79.47%` Recall@5 for CogniSync
- `28.73 ms` mean latency for CogniSync
- `223.36 ms` mean latency for Pinecone (sim)

This may be because the paper reflects an older benchmark, but as of the current artifacts:
- the draft and the saved evidence are not aligned,
- and reviewers will treat that as a credibility risk unless the paper is updated or the old benchmark is rerun and documented clearly.

## What Could Actually Be Published From These Results

### Best current angle

A systems/security paper with the following claim set:

- local-first memory gives competitive retrieval quality,
- local retrieval is far faster than managed-cloud access,
- safety sanitization dramatically reduces memory leakage risk,
- performance remains stable as memory size scales.

That is a more defensible framing than:
- "CogniSync is a much better retriever than dense baselines."

### Venue fit

Most plausible with current evidence:
- systems/workshop paper,
- MCP/agent memory workshop,
- security-for-agents workshop,
- benchmark/tooling or industry-style submission.

Not yet convincing for:
- NeurIPS main as a retrieval-method paper,
- EMNLP main as a retrieval or memory-modeling paper.

Possible after stronger reruns:
- NeurIPS Datasets and Benchmarks / workshop style venue,
- EMNLP Industry Track or Findings if the benchmark and security framing are strengthened.

## Highest-Leverage Next Experiments

1. Run retrieval on all `160` workflow queries, not `50`.
2. Cover all `20` workflows and all `7` domains in the reported retrieval table.
3. Build a harder benchmark where Vanilla RAG is not already at `96%` hit@5.
4. Redo ablations so the lexical contribution is actually visible.
5. Add a real cloud baseline, not only a simulated Pinecone baseline.
6. Make agent-task success non-saturated with harder multi-hop and cross-session tasks.
7. Add a real poisoning benchmark where poisoning rate is not identically zero.
8. Reconcile `paper/cognisync_paper.tex` with the current saved results before submission.

## Recommended Paper Reframe

If you want to keep moving with these exact artifacts, the safest central claim is:

> CogniSync is a local-first agent memory system that offers small but statistically consistent retrieval gains over strong local baselines, large latency savings over cloud-style retrieval, and substantial protection against leakage attacks.

That claim is consistent with the saved outputs.

The following central claim is not supported strongly enough by the current artifacts:

> CogniSync's hybrid retriever substantially outperforms semantic-only retrieval across the benchmark.
