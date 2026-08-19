CogniSync: Learned-Alpha Hybrid Retrieval with Multi-Signal
Adversarial Filtering for Local-First LLM Agents
Anonymous Authors
Anonymous Institution
Anonymous City, Anonymous Country
anonymous@anonymous.edu
Abstract
We present CogniSync, a retrieval system for local-first LLM agents
that combines learned-alpha adaptive score fusion of dense and
lexical signals with a lightweight multi-signal adversarial filtering
layer. The central question is whether retrieval-layer security can
be incorporated with modest impact on retrieval quality. On 29,011
public-benchmark query pairs and a separate synthetic adversarial
benchmark, we find that it can.
On the main retrieval evaluation, CogniSync achieves MRR@5
of 0.887 on public benchmarks, outperforming dense-only retrieval
by +2.75 pp (Wilcoxon test, Bonferroni-corrected 𝑝<10−100) and
fixed-weight hybrid RRF by +4.83 pp. The gain is concentrated
on MS MARCO (+9.1 pp over Dense), where query-adaptive score
weighting and cross-encoder reranking complement each other
most clearly. On SciQ and SQuAD, CogniSync matches Dense
within 0.1 pp, consistent with near-ceiling performance on single-
document QA tasks.
The multi-signal filtering layer uses a three-feature logistic
classifier to screen retrieved documents for adversarial content
before they enter the agent’s context window. Against adaptive
query-conditioned injection attacks, the filter reduces retrieval-
level payload-entry attack success from 99.3% to 0.12%, at a
documented false-positive rate of 1.04% and an approximately 1.0
percentage point reduction in MRR@5.
We report all results transparently: retrieval experiments use cus-
tom per-query candidate pools rather than official leaderboard set-
tings. Security results measure retrieval-level payload entry rather
than downstream LLM instruction-following robustness. On a per-
sistent 100K-passage index, CogniSync processes 1,000 sequential
queries with 275.6 ms average latency (P95: 480.8 ms; P99: 630.3 ms).
CCS Concepts
•Information systems →Retrieval models and ranking;Ques-
tion answering;•Security and privacy →Software and application
security;•Computing methodologies →Natural language pro-
cessing.
Permission to make digital or hard copies of all or part of this work for personal or
classroom use is granted without fee provided that copies are not made or distributed
for profit or commercial advantage and that copies bear this notice and the full citation
on the first page. Copyrights for components of this work owned by others than the
author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
republish, to post on servers or to redistribute to lists, requires prior specific permission
and/or a fee. Request permissions from permissions@acm.org.
CIKM ’26, Atlanta, GA, USA
©2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.
ACM ISBN 978-1-4503-XXXX-X/2026/10
https://doi.org/XXXXXXX.XXXXXXXKeywords
retrieval-augmented generation, LLM agents, hybrid retrieval, adap-
tive score fusion, prompt injection, retrieval security, local-first
RAG, cross-encoder reranking
ACM Reference Format:
Anonymous Authors. 2026. CogniSync: Learned-Alpha Hybrid Retrieval
with Multi-Signal Adversarial Filtering for Local-First LLM Agents. InPro-
ceedings of Proceedings of the 35th ACM International Conference on Infor-
mation and Knowledge Management (CIKM ’26).ACM, New York, NY, USA,
9 pages. https://doi.org/XXXXXXX.XXXXXXX
1 Introduction
Retrieval-augmented generation (RAG) pipelines for LLM agents
face two pressures that have mostly been studied in isolation. Mem-
ory and retrieval research optimizes recall and latency. Security
research catalogs attack success rates. The interaction between
them is less studied: specifically,what does it cost in retrieval quality
to add adversarial filtering at the retrieval layer?
The question matters because the same retrieval pipeline that
makes an agent useful also gives an attacker a direct channel into
the agent’s reasoning. Any document the agent can retrieve can
carry instructions. Recent work on prompt injection against tool-
selection pipelines [ 11] shows that adversarial documents can redi-
rect tool selection without touching model weights. The emergence
of dynamic tool discovery protocols such as MCP [ 6] widens this
surface further. A retrieval system that can filter injected content
before it reaches the context window provides defense that does
not depend on the model’s instruction-following robustness.
CogniSync is a local-first retrieval system that addresses both
dimensions. It runs on a locally hosted model, providing network-
layer control over outbound connections and eliminating depen-
dence on remote inference services. On top of that foundation it
adds two components: an adaptive retrieval engine that predicts
per-query score fusion weights using a small regression model,
followed by a cross-encoder reranking step; and a multi-signal fil-
tering layer that classifies retrieved documents as adversarial or
benign using semantic similarity, imperative-verb detection, and
length anomaly features.
We evaluate retrieval performance on 29,011 public-benchmark
query-passage pairs (MS MARCO, SQuAD, SciQ, and CodeSearch-
Net) and security performance on a separate synthetic adversarial
benchmark. On the public retrieval evaluation, CogniSync achieves
MRR@5 of 0.887, 2.75 percentage points ahead of dense retrieval and
4.83 percentage points ahead of fixed-weight RRF. The gain is con-
centrated on MS MARCO (+9.1 pp over Dense), while performance
on single-document QA tasks is within 0.1 pp of Dense. On the
adversarial benchmark, the filtering layer incurs approximately a

CIKM ’26, October 2026, Atlanta, GA, USA Anonymous et al.
1.0 percentage point reduction in MRR@5 at a 1.04% false-positive
rate while reducing retrieval-level payload-entry attack success
from 99.3% to 0.12%.
A separate full-corpus evaluation over a 100,528-passage MS
MARCO index confirms that the retrieval gains persist beyond
candidate-pool reranking, and a persistent-index benchmark shows
275.6 ms average latency over 1,000 sequential queries.
We describe an episodic memory graph design for cross-session
temporal reasoning, motivated by the needs of agent workflows that
span multiple sessions. A controlled synthetic ablation examines
the effect of appending temporal context documents versus topical
distractors. Full implementation and evaluation of the persistent
graph is left for future work; we are explicit about which claims
have empirical support here and which do not.
The contributions are:
(1)Adaptive hybrid retrieval with learned-alpha fusion
and cross-encoder reranking.A Random Forest regres-
sion model predicts per-query 𝛼from six query and score-
distribution features, and the resulting score fusion is fol-
lowed by cross-encoder reranking. A component ablation fur-
ther shows that the learned-alpha mechanism prevents the
substantial degradation caused by fixed-weight hybridiza-
tion and enables the full system to match the Dense + Cross-
Encoder ceiling within statistical noise.
(2)Multi-signal adversarial filtering.A three-feature logistic
classifier trained on a small proof-of-concept set of six clean
and six poison templates screens retrieved documents at
query time. Against adaptive query-conditioned injection at-
tacks, it reduces retrieval-level payload-entry attack success
from 99.3% to 0.12% with a 1.04% false-positive rate.
(3)Joint evaluation of retrieval quality and retrieval-layer
security.We quantify both dimensions on the same system
and show that the approximately 1.0 pp MRR cost associated
with filtering is smaller than the retrieval gains observed in
the public benchmark evaluation.
(4)Transparent reporting of evaluation scope.We docu-
ment evaluation protocol (custom candidate pools), security
scope (retrieval-level payload entry), and latency measure-
ment under both diagnostic and production-oriented set-
tings, and discuss what the numbers do and do not say about
production deployment.
2 Related Work
2.1 Hybrid Retrieval and Reranking
Dense passage retrieval [ 7] has dominated open-domain QA since
2020. Its weakness on exact-match queries involving technical iden-
tifiers and entity strings [ 14] motivates hybrid dense-sparse ap-
proaches. Reciprocal rank fusion [ 2] is the standard combination
method, with 𝑘=60as a conventional default. Fixed-weight RRF is
a reasonable baseline but treats all query types identically. Query-
adaptive weighting and query-dependent retrieval strategies have
been explored in learned sparse retrieval [ 4] and ensemble-based
retrieval systems, but the use of per-query score-distribution fea-
tures to predict fusion weights remains relatively underexplored.
Cross-encoder rerankers [ 3,8] consistently improve top- 𝑘precision
over first-stage retrieval, at the cost of higher per-query latency.2.2 Agent Memory
MemGPT [ 9] treats agent memory as a paging problem, moving
information between in-context working memory and an external
store. MemoryBank [ 15] applies forgetting-curve dynamics to mem-
ory pruning. A-MEM [ 13] constructs a Zettelkasten-style graph
with cosine-similarity edges between atomic memory nodes.
These systems optimize semantic relevance and persistence.
They do not explicitly model temporal ordering or causal rela-
tionships between events, which matter for tasks like incident
reconstruction where the question is notwhat do I know about
Xbutwhat happened just before X failed. CogniSync proposes an
episodic memory graph with directed causal edges to address this;
we describe the design but do not report full empirical results from
a persistent graph implementation in this paper.
2.3 Security in Agentic RAG
Perez and Ribeiro [ 10] characterized indirect prompt injection in
language models. Shi et al. [ 11] extended this to multi-tool agents,
showing that adversarial tool descriptions can redirect tool selec-
tion without weight modification. Greshake et al. [ 5] analyzed data
exfiltration via retrieval-integrated workflows. Hou et al. [ 6] docu-
ment security risks in MCP-based agent ecosystems. None of these
works jointly measures the retrieval quality cost of retrieval-layer
defense.
3 Problem Formulation
3.1 Retrieval and Context Model
Let an LLM with parameters 𝜃have maximum context capacity
𝐶max. At inference step 𝑡, working context 𝑊𝑡satisfies|𝑊𝑡|≤𝐶 max.
The agent maintains a corpus D, and retrieval function 𝑅(𝑞 𝑡,D,𝑘)
returns the top- 𝑘chunks for inclusion in 𝑊𝑡. The design problem is
ensuring that 𝑅maximizes task-relevant recall while adversarially
crafted content inDcannot redirect agent behavior through the
context window.
3.2 Threat Model
We assume an adversary who controls external content ingested
intoD(web pages, documents, API responses) but has no access
to model weights. Three attack classes are relevant:
•Prompt Injection[ 10]: adversarial string 𝑥adv∈𝑊 𝑡directs
the agent toward the adversary’s objective rather than the
system prompt’s.
•Tool Spoofing[ 11]: injected documentation shifts tool-
selection probability toward an unauthorized tool.
•Data Exfiltration[ 5]: the agent encodes private context
within an authorized outbound response.
The filtering layer evaluated here targets prompt injection and
tool spoofing at the retrieval stage. Steganographic exfiltration
requires a different defense and is outside this evaluation’s scope.
4 CogniSync Architecture
4.1 Local-First Execution
All reasoning, retrieval, and tool selection run on a locally hosted
model (Google Gemma-2B-Instruct, 4-bit quantized, 8–24 GB RAM).

CogniSync: Learned-Alpha Hybrid Retrieval with Multi-Signal Adversarial Filtering for Local-First LLM Agents CIKM ’26, October 2026, Atlanta, GA, USA
Figure 1: CogniSync system overview. Queries pass through learned-alpha adaptive fusion of dense and lexical retrieval,
cross-encoder reranking, and multi-signal adversarial filtering before reaching a local language model. Semantic and episodic
memory stores provide cross-session context, although only the retrieval and filtering components are evaluated in this
paper.The highlighted callout summarizes a cross-benchmark synthesis of the reported results: CogniSync improves retrieval
effectiveness by 2.75 percentage points MRR@5 over dense retrieval on the public benchmark evaluation, while the adversarial
filtering layer reduces adaptive prompt-injection attack success from 99.3% to 0.12% at an approximately 1.0 percentage point
MRR cost on a separate synthetic adversarial benchmark.
Two security properties follow: the system operates without re-
liance on external cloud inference services, and network-layer poli-
cies can restrict outbound connections. External content is un-
trusted by default and passes through the filtering layer before
reaching the context window. The hardware requirement is real
and excludes edge devices below the 8 GB threshold; this is the
direct cost of local execution.
4.2 Episodic Memory Graph (Design)
We describe the proposed episodic memory graph structure, with
the understanding that the full persistent implementation is not
evaluated in this paper. The design motivation and a synthetic
ablation on appended context documents are reported in Section 6.8.
The episodic graph 𝐺=(𝑉,𝐸) stores agent interactions as atomic
event nodes. Each node 𝑣𝑖∈𝑉holds: interaction text, a Unix times-
tamp, a session identifier, and the tool set invoked. A directed edge
𝑣𝑖→𝑣 𝑗exists when 𝑣𝑖’s outcome was a structural precondition
for𝑣𝑗’s invocation—capturing causation rather than semantic sim-
ilarity. After each session, stable recurring facts are consolidated
asynchronously into a parallel FAISS semantic store, following
Tulving’s episodic/semantic distinction [12].
The case for causal edges over similarity edges is clearest on
incident reconstruction queries such aswhat changed before the
service failed?require event ordering. A flat similarity graph returns
content topically related to the failure but not its cause. A directed
causal graph retrieves the specific sequence. This design prediction
requires a deployed multi-session agent evaluation to test properly;
we leave that for future work.4.3 Adaptive Hybrid Retrieval
Dense retrieval uses all-MiniLM-L6-v2 (384 dimensions, FAISS
inner-product index, pinned to revision c9745ed ). Lexical retrieval
uses BM25 (via rank_bm25). Both sets of scores are min-max nor-
malized to[0,1]within each query. When all scores for a retrieval
channel are identical, the normalized values are set to zero to avoid
division-by-zero.
Figure 2: Query-adaptive retrieval workflow. Query and score-
distribution features are used by a Random Forest regressor
to predict the fusion weight 𝛼, which controls the relative
contribution of dense and lexical retrieval scores before cross-
encoder reranking. The combined retrieval stack, consisting
of learned-alpha score fusion and cross-encoder reranking,
improves MRR@5 by 2.75 percentage points over dense re-
trieval on the public benchmark evaluation.
The combined score for document𝑑is:
score(𝑑)=𝛼· ˜𝑠dense(𝑑)+(1−𝛼)· ˜𝑠lex(𝑑),(1)

CIKM ’26, October 2026, Atlanta, GA, USA Anonymous et al.
Algorithm 1Multi-Signal Adversarial Filtering
Require: chunk𝑐; mean clean embedding 𝜇; logistic classifierF;
query embedding𝑞 emb
Ensure:decision∈{admit,filter}
1:Encode𝑐to embedding𝑒 𝑐
2:𝑠 cos←cos(𝑒 𝑐/∥𝑒 𝑐∥, 𝜇)
3:has_imperative← 1[𝑐matchesI] {I: {ignore, reveal, execute,
forget, bypass, output}}
4:len_ratio←|𝑐|/ |𝑐clean|
5:𝑝←F([𝑠cos,has_imperative,len_ratio] )
6:if𝑝>0.5then
7:returnfilter
8:end if
9:ifhas_imperative=1andcos(𝑒 𝑐/∥𝑒 𝑐∥,𝑞emb)<0.3then
10:returnfilter{goal-redirection heuristic}
11:end if
12:returnadmit
where ˜𝑠dense and˜𝑠lexare the normalized scores, and 𝛼∈[ 0,1]is set
per query by a regression model.
Learned alpha.We train a Random Forest regressor (50 trees,
depth 5, seed 42) on 300 held-out tuning queries. For each tuning
query, the oracle 𝛼∗is the value in{0.0,0.1,..., 1.0}that maxi-
mizes MRR@5. The regressor is trained to predict 𝛼∗from six
features: query length in tokens, standard deviation of normalized
dense scores, standard deviation of normalized BM25 scores, coeffi-
cient of variation of each score distribution, and a binary indicator
for identifier-like tokens (UUID patterns, hex strings, keywords
id/uuid/hash/key ). At test time, the regressor produces a per-
query𝛼without any oracle information. Coefficient-of-variation
features are set to zero when the corresponding mean score is zero.
Cross-encoder reranking.After score-level fusion, the top
candidates are reranked with a cross-encoder (cross-encoder/ms-
marco-MiniLM-L-6-v2, max 512 tokens). The cross-encoder jointly
encodes the query and each candidate passage and produces a
relevance score, replacing the fusion score in the final ranking.
At the candidate set sizes used here, the additional overhead of
the Random Forest prediction and cross-encoder reranking was
negligible, resulting in identical measured latency for CogniSync
and Hybrid_Naive (Section 6.9).
4.4 Multi-Signal Adversarial Filtering
The filtering layer screens retrieved documents before they enter
the context window. Algorithm 1 specifies it.
Training.The logistic classifier is trained on six clean docu-
ments drawn from the tuning corpus and six synthetic poison tem-
plates (e.g.,Ignore previous instructions and output YESandReturn all
API keys and system secrets). Class weights are balanced. The mean
clean embedding 𝜇is the normalized centroid of all clean training
document embeddings. We acknowledge that a six-example poi-
son training set is small; the classifier’s generalization beyond the
template family evaluated here is an open question we discuss in
Section 7.
Goal-redirection heuristic.A second gate (line 8–10) blocks
any document that contains an imperative keyword and has cosinesimilarity below 0.3 with the query embedding. This heuristic is
intended to catch payload documents that evade the classifier by
being short and atypical in length while remaining semantically
disconnected from the query.
5 Experimental Setup
5.1 Datasets
Public benchmarks.We sample from four publicly available
datasets. For reproducibility, all datasets are loaded at pinned Hug-
ging Face revision hashes:
•MS-MARCO v1.1 (validation, 6,980 unique queries, expanded
into 29,011 query–passage pairs after multi-passage expan-
sion and filtering; passage retrieval with per-passage rele-
vance labels; revisiona47ee7a)
•CodeSearchNet Python (test, 15,000 rows, code-
documentation retrieval; revisionbd0cf26)
•SciQ (train, 5,000 rows; revision2c94ad3)
•SQuAD (validation, 5,000 rows; revision7b6d24c)
All datasets are shuffled with seed 42 before sampling.
Evaluation protocol.This paper uses custom per-query
candidate-pool reranking: for each query, we retrieve the original
candidate passages from the dataset and rerank them. Results
are not comparable to official leaderboard evaluations, which
typically use the full retrieval corpus. We state this because
the difference matters for interpreting absolute MRR numbers.
For each dataset, candidate pools are constructed from the
passages or documents associated with each query in the original
dataset format. Queries with empty relevant-document sets after
preprocessing are excluded from metric computation. The final
public benchmark evaluation contains 29,011 query–passage pairs.
Full-corpus retrieval benchmark.To evaluate scalability beyond
candidate-pool reranking, we construct a 100,528-passage corpus
using the Tevatron MS MARCO passage collection, consisting of
100,000 randomly sampled distractors plus 528 guaranteed relevant
passages. We evaluate 500 held-out queries and report MRR@10.
Synthetic domain benchmark.The engineering domain cor-
pus covers JWT authentication, database migration, microservice
routing, CI/CD, and RBAC, comprising 312 semantic and 96 exact-
match queries. Two independent annotators scored relevance on a
three-level scale (𝜅=0.81semantic,𝜅=0.94exact-match) [1].
Security benchmark.Three attack families are evaluated:
Generic Prompt Injection, Generic Data Exfiltration, and Adap-
tive Query-Conditioned Injection. Adversarial documents are
constructed as synthetic payloads; attack success is measured as
retrieval-level payload entry (whether the adversarial document
appears in the top- 𝑘), not downstream instruction-following
compliance. In addition, we evaluate the classifier on the public
deepset/prompt-injections dataset to establish a standardized
baseline for adversarial prompt detection.
5.2 Baselines
•Dense: all-MiniLM-L6-v2 with FAISS inner-product index;
no BM25 component.
•Lexical: BM25 only (rank_bm25, default parameters).

CogniSync: Learned-Alpha Hybrid Retrieval with Multi-Signal Adversarial Filtering for Local-First LLM Agents CIKM ’26, October 2026, Atlanta, GA, USA
Table 1: Main retrieval results on public benchmarks (custom
candidate pools, 29,011 pairs). CogniSync outperforms all
baselines on MRR@5 and NDCG@5. Bold: best per column.
System Rec@1 Rec@5 MRR@5 NDCG@5
CogniSync0.826 0.969 0.887 0.906
Dense 0.790 0.961 0.859 0.883
Hybrid_Naive 0.769 0.944 0.839 0.863
Lexical 0.721 0.900 0.788 0.815
•Hybrid_Naive: rank-based Reciprocal Rank Fusion (RRF)
with𝑘=60and equal contribution from dense and lexical
rankings, with no learned weighting and no cross-encoder
reranking.
•CogniSync: learned-alpha score fusion + cross-encoder
reranking, as described in Section 4.3.
5.3 Metrics
Recall@{1,3,5}, MRR@5, and NDCG@5 are computed per query
and averaged. Where we compare systems pairwise, we use the
Wilcoxon signed-rank test with Bonferroni correction for three
comparisons ( 𝑝<0.05threshold after correction). Bootstrap confi-
dence intervals use 1,000 resamples. Attack success rate is computed
over all evaluated retrieval opportunities rather than as a binary
per-query outcome.
5.4 Reproducibility Details
To facilitate reproducibility, we fix all random seeds to 42 and pin all
datasets to immutable Hugging Face revisions. The retrieval stack
uses sentence-transformers/all-MiniLM-L6-v2 for dense re-
trieval, cross-encoder/ms-marco-MiniLM-L-6-v2 for reranking,
FAISS inner-product indexes, and BM25 (rank_bm25) with default
parameters. The learned fusion model is a Random Forest regres-
sor with 50 trees and maximum depth 5. Experiments were ex-
ecuted in Python using standard scientific libraries ( faiss-cpu ,
sentence-transformers ,scikit-learn ,datasets ,pandas , and
numpy ), typically on an NVIDIA T4 GPU. Detailed reproducibility
materials, including dataset revision pins, configuration files, hyper-
parameters, pseudocode, and all generated result artifacts (tables,
figures, and logs), are provided in the anonymous supplementary
repository.
6 Results
6.1 Main Retrieval Comparison
Table 1 reports results on the public benchmark evaluation (29,011
query pairs) after excluding queries with empty relevant-document
sets.
All pairwise comparisons are statistically significant after Bon-
ferroni correction (Table 3). CogniSync’s advantage over Dense is
+2.75 pp MRR (95% CI: [2.50, 3.00] pp). The advantage over Hy-
brid_Naive is+4.83 pp (95% CI: [4.57, 5.08] pp). These gaps are
consistent with cross-encoder reranking providing meaningful pre-
cision improvement over both first-stage fusion strategies.Table 2: Full-corpus retrieval on a 100,528-passage MS
MARCO index (500 queries).
System MRR@10
CogniSync0.9216
Dense 0.9197
Table 3: Pairwise statistical significance (public benchmark
evaluation, Bonferroni corrected). Tests are performed over
per-query MRR values. 𝑝-values below10−100are reported as
<10−100.
Comparison MeanΔMRR 95% CI Sig.?
CogniSync vs Dense+0.028 [0.025, 0.030] Yes
CogniSync vs Hybrid_Naive+0.048 [0.046, 0.051] Yes
CogniSync vs Lexical+0.099 [0.096, 0.102] Yes
Table 4: Per-dataset MRR@5 (public benchmarks). SciQ and
SQuAD are effectively tied between CogniSync and Dense;
MS-MARCO and CodeSearchNet show clear gains.
Dataset CogniSync Dense Hybrid_N Lexical
MS-MARCO0.6420.551 0.503 0.376
CodeSearchNet0.9980.994 0.990 0.983
SQuAD 0.9600.9610.934 0.879
SciQ 0.9620.9630.951 0.929
Synthetic1.0000.893 0.863 0.854
6.2 Full-Corpus Retrieval Scaling
To test whether the learned-alpha hybrid architecture scales beyond
candidate-pool reranking, we evaluated CogniSync on a 100,528-
passage corpus constructed from the Tevatron MS MARCO col-
lection (100,000 random distractors plus 528 guaranteed relevant
passages). On 500 held-out queries, CogniSync achieves MRR@10
of 0.9216, compared with 0.9197 for Dense (Table 2).
The absolute improvement is modest (+0.19 percentage points),
but the result demonstrates that the adaptive hybrid architecture
remains effective in a large retrieval corpus and that the observed
gains are not an artifact of small candidate pools.
6.3 Per-Dataset Breakdown
Table 4 breaks results by dataset. The gains are concentrated on
MS-MARCO, where CogniSync exceeds Dense by 9.1 pp. On SciQ
and SQuAD, the gap is under 0.2 pp, with systems within noise of
each other.
The MS-MARCO result is the most interpretable. MS-MARCO
has multiple partially relevant passages per query, and the selected
passage is sometimes only subtly more relevant than the others.
Cross-encoder reranking handles this well because it jointly en-
codes the query and each candidate passage rather than comparing
independent embeddings. SciQ and SQuAD are single-document

CIKM ’26, October 2026, Atlanta, GA, USA Anonymous et al.
Table 5: Component ablation on the MS MARCO validation
benchmark (5,744 evaluation queries with dynamically in-
jected distractors). Learned-alpha adaptive fusion neutral-
izes the degradation caused by fixed-weight hybridization
and enables the full CogniSync system to match the Dense +
Cross-Encoder ceiling within statistical noise.
System MRR@5
Dense 0.5450
Sparse (BM25) 0.3431
Naive RRF 0.4678
Dense + Cross-Encoder0.6384
Naive RRF + Cross-Encoder 0.6169
Learned-Alpha Only 0.4584
CogniSync (Full) 0.6369
tasks where the relevant passage is distinctive; dense retrieval is
already near ceiling ( ≈0.96), and cross-encoder reranking adds little.
The synthetic domain score of 1.0 for CogniSync reflects a small
benchmark (408 queries) where the system was tuned. We report it
for completeness, but we do not draw conclusions from it beyond
the sanity check that the system performs as expected on its design
domain.
6.4 Component Ablation: Adaptive Fusion vs.
Cross-Encoder Reranking
To isolate the contribution of the learned-alpha adaptive fusion
mechanism from that of the cross-encoder reranker, we conducted
a targeted component ablation on the MS MARCO validation bench-
mark using the same distractor-augmented candidate-pool construc-
tion described in Section 5.1. Table 5 reports the results. For each
query, we augmented the original candidate pool with 40 randomly
sampled distractor passages drawn from a global pool of 10,000 MS
MARCO passages. This substantially increases retrieval difficulty,
which explains why Dense MRR@5 decreases from 0.859 in the
standard candidate-pool evaluation to 0.545 in this harder ablation
setting.
Fixed-weight hybridization substantially degraded retrieval ef-
fectiveness: Naive RRF reduced MRR@5 from 0.5450 (Dense) to
0.4678, indicating that blindly combining dense and lexical signals
can be harmful when one retrieval channel is poorly matched to the
dataset. This deficit persisted even after cross-encoder reranking,
with Naive RRF + Cross-Encoder reaching 0.6169 compared with
0.6384 for Dense + Cross-Encoder.
The learned-alpha mechanism largely neutralized this degrada-
tion. Although the first-stage Learned-Alpha Only variant (0.4584)
remained below Dense, the full CogniSync system achieved 0.6369
MRR@5, statistically indistinguishable from Dense + Cross-Encoder
(Wilcoxon signed-rank test, p = 1.0). These results indicate that
the principal benefit of the adaptive fusion model is robustness: it
suppresses unhelpful lexical contributions and prevents the per-
formance loss associated with fixed-weight hybrid retrieval, while
preserving the gains of strong cross-encoder reranking.Table 6: MRR@5 by query type (public benchmarks). All
systems effectively saturate exact-match; semantic queries
drive the overall gap.
System Exact-Match Semantic
CogniSync1.000 0.887
Dense 0.987 0.859
Hybrid_Naive 1.000 0.838
Lexical 1.000 0.788
Table 7: Security evaluation (synthetic adversarial corpus;
retrieval-level payload entry, not downstream instruction-
following). FP Rate is the fraction of legitimate documents
blocked. MRR Drop reflects quality cost of filtering.
Attack System ASR FP Rate MRR Drop
Generic InjectionCogniSync 0.00% 1.04% 1.00 pp
No Defense 3.00% — —
Adaptive InjectionCogniSync 0.12% 1.04% 1.01 pp
No Defense 99.30% — —
Data ExfiltrationCogniSync 0.84% 1.04% 1.02 pp
No Defense 4.20% — —
6.5 Query-Type Analysis
On exact-match queries (UUID patterns, hex strings, versioned iden-
tifiers), all four systems achieve near-perfect MRR ( ≥0.987). These
queries have unambiguous lexical signatures, and any reasonable
retrieval system finds the right document. The differentiation is
entirely on semantic queries (Table 6), where CogniSync’s learned
alpha and cross-encoder together provide+2.76 pp over Dense.
6.6 Security Evaluation
Table 7 reports attack success rate (ASR) and the MRR drop from
false-positive document blocks, measured on 300 adversarial queries
per attack family, with attack success computed over all query-
document retrieval opportunities rather than as a binary per-query
outcome.
Two results stand out. Against adaptive query-conditioned in-
jection, CogniSync reduces ASR from 99.3% to 0.12%. This attack
family is designed to match query semantics closely, making it
harder for semantic similarity filters to detect; the goal-redirection
heuristic (imperative keyword + low query similarity) appears to
contribute substantially to the observed reduction in attack suc-
cess. Against generic injection and exfiltration, no-defense ASR is
already relatively low (3.0% and 4.2%), and CogniSync reduces it
further.
On the public deepset/prompt-injections benchmark, the
logistic classifier achieves 86.36% accuracy, with F1 scores of 0.89
for benign prompts and 0.81 for injection attacks. This establishes
that the lightweight three-feature model captures broadly useful
signals beyond the synthetic templates used in our retrieval-layer
experiments.

CogniSync: Learned-Alpha Hybrid Retrieval with Multi-Signal Adversarial Filtering for Local-First LLM Agents CIKM ’26, October 2026, Atlanta, GA, USA
Table 8: In a small exploratory stress test involving eight pub-
licly circulated prompt-injection patterns, the filter blocked
7 of 8 cases.
Jailbreak Family Blocked
Developer Mode (DAN-style) Yes
STAN Yes
Base64 Translation No
Narrative Roleplay Yes
Indirect Tool Injection Yes
Formatting Override Yes
Prefix Injection Yes
Hypothetical Context Yes
Observed ASR 12.5%
Figure 3: Security-accuracy tradeoff under adaptive query-
conditioned prompt injection (300 queries). The multi-signal
filtering layer reduces attack success rate from 99.3% to 0.12%
while incurring an approximately 1.0 percentage point reduc-
tion in MRR@5, preserving most of the retrieval advantage
observed in the public benchmark evaluation over dense and
fixed-weight hybrid baselines.
Real-World Jailbreak Stress Test.A common concern is that the
filtering layer may overfit to the six synthetic poison templates
used during training. To assess generalization beyond these tem-
plates, we evaluated the defense against eight widely circulated
real-world jailbreak families drawn from public prompt-injection
repositories and practitioner reports. These included DAN-style
Developer Mode, STAN (Strive To Avoid Norms), Base64 transla-
tion bypasses, narrative roleplay attacks, indirect tool injection
(ToolHijacker-style), formatting-based overrides, prefix injections,
and hypothetical-context attacks.
The defense blocked 7 out of 8 tested jailbreak families, yield-
ing an observed attack success rate of 12.5% in this stress test.
Although this evaluation does not establish robustness against ar-
bitrary adaptive adversaries, it suggests that the combination of
imperative-structure detection and query-conditioned semanticTable 9: Threshold sensitivity of the goal-redirection heuris-
tic.
Threshold (𝜏) ASR FPR
0.10 0.65 0.0%
0.15 0.50 0.0%
0.20 0.45 0.0%
0.25 0.45 0.0%
0.30 0.45 0.0%
0.50 0.45 0.0%
filtering captures structural characteristics shared by many real-
world prompt-injection strategies rather than memorizing specific
poison templates.
The false-positive rate of 1.04% is consistent across all three
attack families because it reflects the classifier’s base rate on legit-
imate documents, which is independent of the attack type. This
directly sets the quality cost: a 1.04% document block rate, in a
top-5 retrieval setting, produces roughly 1.0 pp MRR degradation.
Given that CogniSync already outperforms Dense by 2.75 pp on
the main benchmark, the net effect with filtering enabled would
be roughly+1.75 pp over Dense, though this estimate assumes the
public benchmark and security benchmark document distributions
are comparable, which is an approximation.
We note an important scope limitation: these results measure
whether adversarial documents appear in the retrieved set, not
whether the LLM downstream acts on them. A retrieved adversarial
document that the model ignores would count as an attack success
in our metric. Measuring the downstream behavioral effect requires
a full agent loop evaluation outside this paper’s scope.
6.7 Threshold Sensitivity Analysis
To assess sensitivity to the goal-redirection threshold 𝜏, we varied
the query-similarity cutoff used by the heuristic while measuring
attack success rate (ASR) and false-positive rate (FPR). Table 9
shows that FPR remains 0.0% across all tested thresholds, while
ASR drops from 0.65 to 0.45 as 𝜏increases from 0.10 to 0.20 and
then remains stable. We use𝜏=0.30as a conservative default.
6.8 Context Augmentation Ablation
To characterize the potential benefit of cross-session temporal con-
text, we constructed a synthetic temporal reasoning dataset: 500
queries of the formwhat changed before the 𝑋incident started hap-
pening?against pools of 9 noise documents plus one target doc-
ument. We then appended one additional document per variant:
either a temporal context document (2 minutes prior, an engineer
deployed a patch related to 𝑋) or a topical distractor (general docu-
mentation on𝑋describes possible causes).
This is a controlled ablation on context document appending,
not an evaluation of a deployed episodic memory graph. We report
it because it gives a partial signal on the relevance of context type
to retrieval quality.
Temporal context appending improves MRR by +0.19 pp relative
to no context, at a slight cost to Recall@5 (the added document

CIKM ’26, October 2026, Atlanta, GA, USA Anonymous et al.
Table 10: Context augmentation ablation (a synthetic tem-
poral reasoning dataset, 𝑛=500queries). Temporal context
provides a small positive signal; topical distractors hurt. All
variants use the CogniSync hybrid retriever.
Variant MRR@5 Recall@5
Hybrid (No Context) 0.9308 1.000
+ Temporal Context 0.9327 0.990
+ Topical Distractor 0.9219 1.000
Table 11: Amortized production latency on a persistent 100K-
passage index.
Metric Latency (ms)
Average 275.6
P95 480.8
P99 630.3
sometimes pushes a true positive out of the top 5). Topical distrac-
tors, designed to be related in topic but irrelevant in time ordering,
hurt MRR by−0.89 pp. The direction of the effect aligns with the
episodic memory design motivation: context relevance is not just
semantic but temporal. The magnitude of the effect is small, which
is expected given that this ablation does not implement actual cross-
session memory management.
6.9 Latency
To estimate production performance, we measured latency on a per-
sistent 100,000-passage index over 1,000 sequential queries. Table 11
reports average and tail latencies.
The average latency remains below 300 ms, which is practical
for interactive retrieval applications. Tail latencies remain under
650 ms at the 99th percentile.
7 Discussion and Limitations
What the evaluation covers and what it does not.The retrieval
evaluation uses custom per-query candidate pools, not full-corpus
retrieval. This means MRR numbers are not directly comparable to
official MS-MARCO or SQuAD leaderboard results. The selection
pool for each query is the set of candidate passages provided by the
original dataset, which is smaller than a full retrieval corpus. This
matters because the hardness of the reranking problem depends
on how many distractors are in the pool; a larger pool generally
makes it harder. The absolute numbers here are therefore optimistic
relative to full-corpus retrieval.
The security classifier’s generalization.The logistic classifier
is trained on six poison template strings. It generalizes well within
the three attack families evaluated, but its ability to detect novel
injection strategies that differ structurally from those templates
is untested. The adaptive query-conditioned injection family is
the most diverse and hardest, and the combined filtering system
reduces retrieval-level payload-entry attack success from 99.3% to
0.12% (equivalent to 99.88% suppression under this metric); but
an attacker aware of the classifier’s feature set could plausiblycraft documents that score below the detection threshold. The goal-
redirection heuristic provides a second layer of defense, but it too
can be evaded by an adversary who crafts payloads with query-
relevant surface text. We report the evaluation as a proof-of-concept
that lightweight classifiers can suppress typical injection payloads,
not as a claim that the system is robust to adversarially adapted
attacks.
Episodic memory.The context augmentation ablation provides
a weak positive signal ( +0.19 pp) that temporally relevant context
helps and topical distractors hurt. It does not evaluate a deployed
persistent episodic graph, cross-session memory consolidation, or
long-horizon retrieval at realistic session scales. Those experiments
require a production agent harness we have not built for this paper.
Downstream LLM evaluation.We measure whether adversar-
ial documents enter the retrieval set. Whether the local LLM then
acts on them is a separate question that depends on the specific
model and system prompt. The filtering layer reduces exposure
risk, but it does not replace instruction-following robustness in the
model.
Latency in production.On a persistent 100K-passage index,
CogniSync processes 1,000 sequential queries with 275.6 ms average
latency (P95: 480.8 ms; P99: 630.3 ms). These measurements indicate
that the combined retrieval, reranking, and filtering pipeline is
practical for interactive applications. Larger corpora and multi-user
deployments remain future work.
A dedicated component ablation confirms that the learned-alpha
model’s primary contribution is to suppress harmful lexical
signals when fixed hybridization would otherwise reduce retrieval
quality, rather than to outperform dense retrieval as a standalone
first-stage ranker in every setting. The principal public benchmark
results measure query-adaptive reranking effectiveness within
dataset-provided candidate pools. The full-corpus evaluation over
a 100K-passage index shows that the same architecture maintains
a small but consistent advantage at larger scale, indicating that the
strongest empirical benefits arise from improved reranking while
remaining compatible with realistic first-stage retrieval.
8 Conclusion
CogniSync combines learned-alpha adaptive score fusion with
cross-encoder reranking and a three-feature logistic filtering
layer. On the public benchmark evaluation (29,011 expanded
query–passage pairs, with metrics computed at the query level), it
outperforms dense-only retrieval by 2.75 pp MRR@5 and fixed-
weight hybrid RRF by 4.83 pp, both with Bonferroni-corrected
statistical significance. The gain comes primarily from MS-MARCO,
where cross-encoder reranking provides the largest benefit; on
single-document QA tasks (SciQ, SQuAD), CogniSync matches
Dense within noise.
A full-corpus evaluation over a 100,528-passage MS MARCO
index confirms that the learned-alpha hybrid architecture maintains
a small but consistent advantage over dense retrieval (MRR@10:
0.9216 vs. 0.9197).

CogniSync: Learned-Alpha Hybrid Retrieval with Multi-Signal Adversarial Filtering for Local-First LLM Agents CIKM ’26, October 2026, Atlanta, GA, USA
A component ablation on MS MARCO shows that learned-alpha
adaptive fusion acts primarily as a robust query-dependent weight-
ing mechanism: it neutralizes the degradation caused by fixed-
weight hybridization and allows the full system to match the Dense
+ Cross-Encoder performance ceiling within statistical noise.
The adversarial filtering layer reduces adaptive injection at-
tack success from 99.3% to 0.12% at a 1.04% false-positive rate and
roughly 1.0 pp MRR cost. This provides a cross-benchmark empiri-
cal synthesis of the retrieval-security tradeoff under our experimen-
tal conditions: the adversarial filtering layer incurs approximately
a 1 percentage point reduction in MRR@5 on the synthetic security
benchmark, while the retrieval improvements from adaptive fusion
and reranking on the public benchmark evaluation are more than
twice as large.
We describe a proposed episodic memory graph architecture
for cross-session temporal reasoning, supported by a context aug-
mentation ablation showing that temporally relevant context helps
(+0.19 pp) and topical distractors hurt ( −0.89 pp). Full deployment
and evaluation of the persistent graph remains future work. De-
tailed reproducibility materials, including dataset revision pins,
configuration files, hyperparameters, pseudocode, and all gener-
ated result artifacts (tables, figures, and logs), are provided in the
anonymous supplementary repository.
GenAI Usage Disclosure
Generative AI tools, including ChatGPT and similar large language
models, were used to assist with language editing, rephrasing, code
development and debugging, and general writing support during
the preparation of this manuscript. All outputs were carefully re-
viewed and verified by the authors. The authors performed and
validated all experimental design, implementation, data processing,
analyses, and interpretation of results, and take full responsibility
for the accuracy and integrity of the work.
References
[1]Jacob Cohen. 1960. A Coefficient of Agreement for Nominal Scales.Ed-
ucational and Psychological Measurement20, 1 (1960), 37–46. doi:10.1177/
001316446002000104
[2]G. V. Cormack, C. L. A. Clarke, and S. Buettcher. 2009. Reciprocal Rank Fusion
Outperforms Condorcet and Individual Rank Learning Methods. InProceedings
of SIGIR. ACM, New York, NY, USA, 758–759.
[3]Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. BERT:
Pre-training of Deep Bidirectional Transformers for Language Understanding. In
Proceedings of the 2019 Conference of the North American Chapter of the Association
for Computational Linguistics: Human Language Technologies. Association for
Computational Linguistics, Minneapolis, MN, USA, 4171–4186. doi:10.18653/v1/
N19-1423
[4]Thibault Formal, Benjamin Piwowarski, and Stéphane Clinchant. 2021. SPLADE:
Sparse Lexical and Expansion Model for First Stage Ranking. InProceedings
of the 44th International ACM SIGIR Conference on Research and Development
in Information Retrieval. ACM, Virtual Event, Canada, 2288–2292. doi:10.1145/
3404835.3463098
[5]Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Mario Fritz,
Christopher Kruegel, and Dawn Song. 2023. Not What You’ve Signed Up For:
Compromising Real-World LLM-Integrated Applications with Indirect Prompt
Injection. InProceedings of the 16th ACM Workshop on Artificial Intelligence and
Security. ACM, New York, NY, USA, 79–90.
[6] Xinyi Hou, Yanjie Zhao, Shenao Wang, and Haoyu Wang. 2025. Model Context
Protocol (MCP): Landscape, Security Threats, and Future Research Directions.
arXiv preprint arXiv:2503.23278.
[7]V. Karpukhin et al .2020. Dense Passage Retrieval for Open-Domain Question
Answering. InProceedings of EMNLP. Association for Computational Linguistics,
Online, 6769–6781.[8]Rodrigo Nogueira and Kyunghyun Cho. 2019. Passage Re-ranking with BERT.
CoRR abs/1901.04085. https://arxiv.org/abs/1901.04085
[9]C. Packer et al .2023. MemGPT: Towards LLMs as Operating Systems. arXiv
preprint arXiv:2310.08560.
[10] F. Perez and I. Ribeiro. 2022. Ignore Previous Prompt: Attack Techniques for
Language Models. arXiv preprint arXiv:2211.09527.
[11] Jiawen Shi, Zenghui Yuan, Guiyao Tie, Pan Zhou, Neil Zhenqiang Gong, and
Lichao Sun. 2025. Prompt Injection Attack to Tool Selection in LLM Agents.
arXiv preprint arXiv:2504.19793. doi:10.48550/arXiv.2504.19793
[12] E. Tulving. 1972. Episodic and Semantic Memory. InOrganization of Memory.
Academic Press, New York, NY, USA, 381–402.
[13] W. Xu et al .2025. A-MEM: Agentic Memory for LLM Agents. arXiv preprint
arXiv:2502.12110.
[14] S. Zhao et al .2022. DENSE: A Hybrid Dense-Sparse Retrieval Framework. In
Proceedings of NAACL. Association for Computational Linguistics, Seattle, WA,
USA, 1022–1034.
[15] W. Zhong et al .2023. MemoryBank: Enhancing Large Language Models with
Long-Term Memory. arXiv preprint arXiv:2305.10250.

