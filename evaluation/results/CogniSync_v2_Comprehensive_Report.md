# CogniSync v2 Evaluation - Comprehensive Results

## Run Metadata
- **run_id**: 20260420T202638Z
- **seed**: 42
- **n_gpus**: 2
- **faiss_gpu**: False
- **model**: all-MiniLM-L6-v2
- **batch**: 256
- **dataset_n**: 2000
- **platform**: kaggle-dual-t4
- **msmarco_n**: 2000
- **codesearch_n**: 2000
- **completed_at**: 2026-04-20T20:37:07.725197+00:00


## 1. Cross-Domain Retrieval Performance
|dataset|system|metric|mean|std|ci95_lo|ci95_hi|ci95_margin|n|
|---|---|---|---|---|---|---|---|---|
|MS-MARCO|dense|recall@1|0.344|0.47516|0.323175|0.364825|0.020825|2000|
|MS-MARCO|dense|recall@3|0.67|0.47033|0.649387|0.690613|0.020613|2000|
|MS-MARCO|dense|recall@5|0.832|0.37396|0.81561|0.84839|0.01639|2000|
|MS-MARCO|dense|mrr|0.5215|0.378568|0.504909|0.538091|0.016591|2000|
|MS-MARCO|dense|latency_ms|0.422939|0.207679|0.413837|0.432041|0.009102|2000|
|MS-MARCO|lexical|recall@1|0.2385|0.426273|0.219818|0.257182|0.018682|2000|
|MS-MARCO|lexical|recall@3|0.507|0.500076|0.485083|0.528917|0.021917|2000|
|MS-MARCO|lexical|recall@5|0.664|0.472457|0.643294|0.684706|0.020706|2000|
|MS-MARCO|lexical|mrr|0.389458|0.382672|0.372687|0.40623|0.016771|2000|
|MS-MARCO|lexical|latency_ms|99.277524|38.943073|97.570768|100.984279|1.706755|2000|
|MS-MARCO|hybrid|recall@1|0.304|0.460098|0.283835|0.324165|0.020165|2000|
|MS-MARCO|hybrid|recall@3|0.619|0.485754|0.597711|0.640289|0.021289|2000|
|MS-MARCO|hybrid|recall@5|0.783|0.412306|0.76493|0.80107|0.01807|2000|
|MS-MARCO|hybrid|mrr|0.476575|0.381903|0.459837|0.493313|0.016738|2000|
|MS-MARCO|hybrid|latency_ms|26.231167|0.852524|26.193804|26.268531|0.037364|2000|
|CodeSearchNet|dense|recall@1|0.87|0.336388|0.855257|0.884743|0.014743|2000|
|CodeSearchNet|dense|recall@3|0.9575|0.201777|0.948657|0.966343|0.008843|2000|
|CodeSearchNet|dense|recall@5|0.9745|0.157677|0.967589|0.981411|0.006911|2000|
|CodeSearchNet|dense|mrr|0.9141|0.233|0.903888|0.924312|0.010212|2000|
|CodeSearchNet|dense|latency_ms|2.914341|0.131509|2.908577|2.920104|0.005764|2000|
|CodeSearchNet|lexical|recall@1|0.9305|0.254366|0.919352|0.941648|0.011148|2000|
|CodeSearchNet|lexical|recall@3|0.987|0.113302|0.982034|0.991966|0.004966|2000|
|CodeSearchNet|lexical|recall@5|0.994|0.077246|0.990615|0.997385|0.003385|2000|
|CodeSearchNet|lexical|mrr|0.95865|0.156721|0.951781|0.965519|0.006869|2000|
|CodeSearchNet|lexical|latency_ms|177.401416|279.673859|165.144168|189.658663|12.257247|2000|
|CodeSearchNet|hybrid|recall@1|0.9075|0.289803|0.894799|0.920201|0.012701|2000|
|CodeSearchNet|hybrid|recall@3|0.981|0.136559|0.975015|0.986985|0.005985|2000|
|CodeSearchNet|hybrid|recall@5|0.9915|0.091826|0.987476|0.995524|0.004024|2000|
|CodeSearchNet|hybrid|mrr|0.943975|0.181934|0.936001|0.951949|0.007974|2000|
|CodeSearchNet|hybrid|latency_ms|48.82727|20.848975|47.913524|49.741017|0.913747|2000|


## 2. Episodic Memory Ablation
|mode|mrr_mean|recall5_mean|latency_ms|
|---|---|---|---|
|full|0.5189001|0.818|7.0518|
|no_consolidation|0.42083329999999997|0.728|27.20328|
|no_episodic|0.5434001|0.8539999999999999|0.2354|
|no_temporal|0.5189001|0.818|7.327299999999999|


## 3. Long-Horizon Evaluation
|horizon|pct|step|mrr_mean|lat_mean|lat_p95|
|---|---|---|---|---|---|
|50.0|0.25|12.0|0.493056|7.4708|7.4708|
|50.0|0.5|25.0|0.591333|7.4708|7.4708|
|50.0|0.75|37.0|0.6|7.4708|7.4708|
|50.0|1.0|50.0|0.572|7.4708|7.4708|
|100.0|0.25|25.0|0.591333|7.4708|7.4708|
|100.0|0.5|50.0|0.572|7.4708|7.4708|
|100.0|0.75|75.0|0.524444|7.4708|7.4708|
|100.0|1.0|100.0|0.530167|7.4708|7.4708|
|200.0|0.25|50.0|0.572|7.4708|7.4708|
|200.0|0.5|100.0|0.530167|7.4708|7.4708|
|200.0|0.75|150.0|0.516|7.4708|7.4708|
|200.0|1.0|200.0|0.528|7.4708|7.4708|
|500.0|0.25|125.0|0.510933|7.4708|7.4708|
|500.0|0.5|250.0|0.516933|7.4708|7.4708|
|500.0|0.75|375.0|0.520133|7.4708|7.4708|
|500.0|1.0|500.0|0.5189|7.4708|7.4708|


## 4. Memory Quality
|index|Average|
|---|---|
|precision|0.1768|
|redundancy|0.17840691199999997|
|recall@5|0.818|
|mrr|0.5188999599999999|
|latency_ms|7.962800000000001|


## 5. Security Evaluation
|Metric|Value|
|---|---|
|Attack Success Rate|0.0%|
|Average MRR Delta (Poisoned - Clean)|0.0003|
|Clean MRR|0.5232|
|Poisoned MRR|0.5235|


## 6. Statistical Test Results
|dataset|system|metric|n|mean|std|ci95_lo|ci95_hi|ci95_margin|cohens_d_dense|cohens_d_lexical|wilcoxon_p_dense|wilcoxon_p_lexical|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|msmarco|dense|recall@1|2000|0.344|0.47516|0.323175|0.364825|0.020825|nan|nan|nan|nan|
|msmarco|lexical|recall@1|2000|0.2385|0.426273|0.219818|0.257182|0.018682|nan|nan|nan|nan|
|msmarco|hybrid|recall@1|2000|0.304|0.460098|0.283835|0.324165|0.020165|-0.0855|0.1477|1.7e-05|0.0|
|msmarco|dense|recall@3|2000|0.67|0.47033|0.649387|0.690613|0.020613|nan|nan|nan|nan|
|msmarco|lexical|recall@3|2000|0.507|0.500076|0.485083|0.528917|0.021917|nan|nan|nan|nan|
|msmarco|hybrid|recall@3|2000|0.619|0.485754|0.597711|0.640289|0.021289|-0.1067|0.2272|1e-06|0.0|
|msmarco|dense|recall@5|2000|0.832|0.37396|0.81561|0.84839|0.01639|nan|nan|nan|nan|
|msmarco|lexical|recall@5|2000|0.664|0.472457|0.643294|0.684706|0.020706|nan|nan|nan|nan|
|msmarco|hybrid|recall@5|2000|0.783|0.412306|0.76493|0.80107|0.01807|-0.1245|0.2684|0.0|0.0|
|msmarco|dense|mrr|2000|0.5215|0.378568|0.504909|0.538091|0.016591|nan|nan|nan|nan|
|msmarco|lexical|mrr|2000|0.389458|0.382672|0.372687|0.40623|0.016771|nan|nan|nan|nan|
|msmarco|hybrid|mrr|2000|0.476575|0.381903|0.459837|0.493313|0.016738|-0.1181|0.2279|0.0|0.0|
|codesearch|dense|recall@1|2000|0.87|0.336388|0.855257|0.884743|0.014743|nan|nan|nan|nan|
|codesearch|lexical|recall@1|2000|0.9305|0.254366|0.919352|0.941648|0.011148|nan|nan|nan|nan|
|codesearch|hybrid|recall@1|2000|0.9075|0.289803|0.894799|0.920201|0.012701|0.1194|-0.0844|0.0|0.000253|
|codesearch|dense|recall@3|2000|0.9575|0.201777|0.948657|0.966343|0.008843|nan|nan|nan|nan|
|codesearch|lexical|recall@3|2000|0.987|0.113302|0.982034|0.991966|0.004966|nan|nan|nan|nan|
|codesearch|hybrid|recall@3|2000|0.981|0.136559|0.975015|0.986985|0.005985|0.1364|-0.0478|0.0|0.018603|
|codesearch|dense|recall@5|2000|0.9745|0.157677|0.967589|0.981411|0.006911|nan|nan|nan|nan|
|codesearch|lexical|recall@5|2000|0.994|0.077246|0.990615|0.997385|0.003385|nan|nan|nan|nan|
|codesearch|hybrid|recall@5|2000|0.9915|0.091826|0.987476|0.995524|0.004024|0.1318|-0.0295|0.0|0.095581|
|codesearch|dense|mrr|2000|0.9141|0.233|0.903888|0.924312|0.010212|nan|nan|nan|nan|
|codesearch|lexical|mrr|2000|0.95865|0.156721|0.951781|0.965519|0.006869|nan|nan|nan|nan|
|codesearch|hybrid|mrr|2000|0.943975|0.181934|0.936001|0.951949|0.007974|0.1429|-0.0864|0.0|4.4e-05|


## 7. Hybrid Query Type Validation
|query_type|system|mrr|recall@5|latency_ms|
|---|---|---|---|---|
|exact|dense|0.5215|0.832|0.2739|
|exact|hybrid|0.47657499999999997|0.783|25.8647|
|exact|lexical|0.3894583333333333|0.664|99.3093562|

