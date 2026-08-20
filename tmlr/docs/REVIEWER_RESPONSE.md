# Every CIKM criticism, and where it is answered

Written as a working document for the resubmission, not as a rebuttal letter.
TMLR reviewers will not have seen the CIKM reviews; this exists so you can check
that nothing was dropped, and so Appendix A of the manuscript stays honest.

The reviews cluster into six issues. Five are addressed by new experiments; one
is addressed by removing a component.

---

## 1. The main comparison was unfair

> *R2:* "In Table 1, CogniSync includes cross-encoder reranking, while
> Hybrid_Naive does not; therefore the reported gain over Hybrid_Naive combines
> the effect of learned fusion, reranking, and possibly different scoring
> choices."
> *R4:* "The headline +2.80 pp over Dense is essentially the cross-encoder effect."
> *Metareview:* reason for rejection #2.

**This is correct and the claim is withdrawn.** NB1 replaces the comparison with
a grid: every first stage × every rerank budget ∈ {0, 50, 100}, so no system is
ever compared against one given less compute. The reader can read the reranker's
contribution and the fusion's contribution off separate axes.

The paper now says the reranker does the work, in the abstract, because it does.

**Where:** NB1 → `tab_main_retrieval.tex` → §4.1.

---

## 2. The evaluation protocol was not full-corpus retrieval

> *R1 Q1–Q2:* "How large are the candidate pools... Why is the full-corpus
> evaluation limited to 500 queries and a 100K-passage subset?"
> *R2:* "custom per-query candidate-pool reranking rather than full-corpus
> retrieval... the resulting MRR values are optimistic and not comparable."
> *Metareview:* reason #3.

**Also correct.** Candidate-pool MRR@5 = 0.887 is not comparable to anything, so
it is gone. Every retrieval number in the TMLR version comes from ranking a
complete BEIR corpus, scored with `pytrec_eval`, reported as nDCG@10 — the same
metric and implementation other BEIR papers use.

**One thing worth knowing before you resubmit.** The full-corpus experiment the
CIKM paper cited (MRR@10 0.9216 vs 0.9197) does not do what the paper says it
does. `calc_full_corpus_significance.py` in the repo uses a **fixed α = 0.6 and
no cross-encoder**, so it never evaluated CogniSync — it evaluated a static
hybrid. It also draws queries from the MS MARCO *train* split and appends their
positive passages to the index, which is why MRR@10 lands at 0.92 where the
literature reports ~0.33 for a MiniLM dense retriever on the real dev set. If a
TMLR reviewer opens that script, they will find this. Appendix A of the new
manuscript states it plainly, which is much better than having it discovered.

**Where:** NB1, `standard` tier (6 corpora, 272K docs) plus the optional
`msmarco` tier (full 8.84M corpus) → §3.4, §4.1.

---

## 3. Learned-alpha is not a contribution

> *R1:* "the Learned-Alpha Only variant performs worse than Dense... the main
> performance driver is the cross-encoder reranker."
> *R4:* "The new learned-alpha weight does not beat dense by the authors' own
> ablation, only repairs naive-RRF degradation."
> *Metareview:* reason #1 and #5.

**Correct, and this is where the reframe earns its keep.** The CIKM version
treated this as a limitation to be worded around. The TMLR version makes it the
result, by asking the question the reviewers implied but did not ask: *is
per-query weighting a bad idea, or a badly implemented one?*

NB2 answers it with an oracle that picks the best α per query in hindsight. Two
possible outcomes, both publishable:

- oracle ≫ fixed, learned ≈ fixed → the headroom is real and six cheap features
  cannot reach it. Report the bound and the identifiability analysis.
- oracle ≈ fixed → per-query weighting is worth nothing here, full stop.

The mechanism that explains it is the flatness of the α → nDCG curve: on most
queries, sweeping α across its whole range barely moves the metric, so α\* is
whichever grid point won a tie and the regression target is largely undefined.
A gradient-boosting model with 500 estimators does no better than the CIKM
random forest, which rules out capacity as the explanation.

**One finding you should be prepared for.** The released implementation contains
`if d_max > 0.85 or bm25_cv < 0.1: alpha = 1.0` — a hand-written rule that
discards the regressor's prediction and falls back to pure dense retrieval. Much
of what the paper attributed to "learned α preventing RRF degradation" is this
rule declining to fuse. NB1 ablates it as a separate row so the credit lands
where it belongs. Better to surface this yourself than to have a reviewer find
it in the artifact.

**Where:** NB2 → `tab_alpha_policies.tex`, `tab_alpha_predictability.tex`,
`fig_alpha_headroom.pdf` → §4.2–4.3.

---

## 4. The security evaluation was too synthetic

> *R1:* "trained on only six clean documents and six synthetic poison templates...
> The reported reduction from 99.3% to 0.12% may not generalize."
> *R1:* "An attacker can avoid explicit imperative keywords, use semantically
> query-relevant text, or distribute malicious instructions across multiple chunks."
> *R4:* "a synthetic attack built to always be retrieved, a classifier trained on
> six poison templates, an evadable imperative-keyword heuristic."
> *Metareview:* reason #4.

**Correct, and R1 essentially specified the experiment.** NB3 implements exactly
the three evasions R1 named, plus three more, as an attacker ladder:

| | Attacker | Evades |
|---|---|---|
| A0 | the six CIKM templates | — |
| A1 | CIKM's "adaptive" attack, reproduced | — |
| A2 | imperative-free paraphrase | the keyword feature (R1's first evasion) |
| A3 | semantic camouflage in real corpus text | the centroid + query-similarity features (R1's second) |
| A4 | length-matched to the clean corpus | the length feature |
| A5 | **black-box score-guided, 200 detector queries** | whatever it can find |
| A6 | payload split across *k* chunks | per-document detection (R1's third) |

Against six defenses, all held to the **same false-positive budget** — which
also resolves R2's observation that Table 7 reported FPR 1.04% and Table 9
reported 0.0% for the same system. There is now one calibration procedure and
every ASR names its operating point.

**On the 99.3% figure.** R4 called it self-referential and was right: the
"adaptive" payload was `<query terms> + "Ignore previous instructions"`, and a
document containing the query verbatim is retrieved essentially always. A1
reproduces it, and its undefended entry rate is printed next to every defended
number so the reader sees what the reduction is measured against. Keeping A1 in
the table alongside A5 is the clearest possible statement of what changed.

**The defense ladder also separates two defects the CIKM version conflated.** D1
is the six-example filter; D1b is the *same three features* trained on thousands
of real injection examples. If D1b does not close the gap, the problem is the
features, not the training set — and the fix is not more labels.

**Where:** NB3 → `tab_attack_defense.tex`, `tab_utility_cost.tex`,
`fig_attack_defense_matrix.pdf` → §5.

---

## 5. The metric measures the wrong thing

> *R1 Q5:* "the evaluation does not include a complete agent loop, downstream tool
> use, downstream instruction-following behavior."
> *R2:* "measures only whether the payload enters the retrieved set, not whether
> the downstream LLM follows it."
> *R4:* "a payload-entry metric that does not measure whether the agent acts on
> the document."

The CIKM paper conceded this in its limitations. NB4 measures it: a real local
instruct model reads the retrieved context, and we check whether it emits the
injected canary. The ratio — **compliance given entry** — is the factor by which
every payload-entry number in this literature must be discounted, and as far as
we can tell nobody has reported it.

Three additions beyond what was asked:

- **Tool selection.** The CIKM threat model listed tool spoofing and cited
  ToolHijacker, then never tested it. NB4 runs a tool-selection loop with
  injected tool documentation.
- **Position sensitivity.** Compliance as a function of where the poison sits in
  the context window. A security result measured only at rank 0 reports the
  hardest case.
- **Prompt hardening as a baseline.** Two sentences in the system prompt, costing
  nothing at retrieval time. If that suppresses more attacks than the filter
  does at 1% FPR, the paper should say so — and the useful question becomes
  whether filtering catches what prompting misses.

NB4 also **replays NB3's optimised A5 documents**, which is what proves the
adaptive attacker's evasion did not come at the cost of the payload ceasing to
work. Without that check, A5's evasion rate would be unfalsifiable.

**Where:** NB4 → `tab_behavioural_gap.tex`, `fig_behavioural_asr.pdf` → §6.

---

## 6. Episodic memory is not a contribution

> *R1 Q4:* "the actual persistent graph is not implemented or evaluated... feels
> more like a future-work idea than a contribution."
> *R4:* "The unimplemented episodic-memory section diminishes the contribution."
> *R2:* "Figure 1 includes semantic and episodic memory stores... which could
> mislead readers about the maturity of that component."
> *Metareview:* reason #5.

**Removed.** Not softened, not moved to an appendix — removed, along with the
+0.19 pp context-augmentation ablation and the memory stores in the architecture
figure. Three reviewers independently said it costs more than it adds, and
describing an unevaluated component alongside evaluated ones invites readers to
transfer confidence from one to the other. Related work notes the direction and
cites the prior systems; that is all.

If you want it back later, the way in is a real multi-session benchmark
(LoCoMo, LongMemEval), not a synthetic 500-query ablation.

---

## Also fixed, though nobody asked

**Latency.** R2 did not flag it, but the CIKM latency claim does not hold up.
`latency_amortized.py` builds its corpus by sampling from a 12-word vocabulary,
so BM25 sees nothing resembling a real posting-list structure, and the repo's
`latency_results.txt` records a 3,325 ms median where the paper claims 275.6 ms.
NB5 measures on real corpora in the configuration the quality results were
produced under, and reports **cross-encoder forward passes per query** alongside
wall clock — the only cost measure that transfers to another machine.

**Reproducibility.** R2 listed six underspecified details. All are now stated in
Appendix B and C of the manuscript and implemented in one place: candidate-pool
construction (gone — full corpus), the provenance of the α-fitting queries (3,000
MS MARCO train queries, applied zero-shot), the cross-encoder candidate count
(the grid axis), preprocessing rules, the attack-generation procedure (released
as a parquet), and the length-ratio feature definition.

**Determinism.** The attack generator used Python's `hash()` on strings, which is
randomised per process — the generated attack corpus differed on every run. Now
a content digest, so the corpus is byte-identical across runs and is released.

**Table consistency.** NB6 writes `claims.json` mapping every number to the
artifact that produced it, and audits the `.tex` against it. This is the
mechanism that would have caught Table 7 and Table 9 disagreeing.

**Statistics.** The CIKM version reported `p < 10^-100` for an effect of 0.028.
At n = 29,011 a paired test declares almost anything significant, which is not
informative. The TMLR version leads with paired-bootstrap effect sizes and 95%
intervals. (A related bug: the bootstrap implementation returned p = 0 for two
systems with *identical* per-query scores — relevant given the ablation's claim
that CogniSync and Dense+CE are statistically indistinguishable. Fixed, with a
regression test.)

---

## What to expect from TMLR

TMLR's criteria are narrower than CIKM's: claims supported by evidence, and some
subset of the audience would be interested. Novelty and state-of-the-art results
are explicitly **not** required. That is why this reframe works — the findings
that sank the CIKM submission are, stated honestly and bounded by measurement,
exactly the kind of thing TMLR publishes.

Likely reviewer pushback, and the answer:

- *"The negative results are not surprising."* The oracle bound and the
  compliance factor are quantitative, and neither has been reported before.
  Unsurprising and unmeasured are different things.
- *"Small models only."* Stated in Limitations, with the direction of the bias
  argued (larger models plausibly comply less, which makes the overstatement
  factor larger, not smaller).
- *"The adaptive attacker is weak."* Deliberately — it is stated as a lower
  bound on risk, not an estimate. A defense that fails against no-gradient,
  200-query hill climbing has not been shown robust by any stronger test.
- *"Which is the contribution, retrieval or security?"* The through-line is
  measurement protocol: matched budgets, matched operating points, and measuring
  the thing rather than its proxy. Keep §7's recommendations prominent.
