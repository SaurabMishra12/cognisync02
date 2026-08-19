# Analysis of 08-06results

Source folder: `C:\Users\msaur\OneDrive\Desktop\projectRL\08-06results`
Report generated against current on-disk files. Current `kaggle_latest_results.json`: 608121 bytes, last modified 2026-06-13 12:41:35.

## Executive Findings

- The folder changed during analysis: `kaggle_latest_results.json` is now a self-consistency result file with 5 groups of 10 samples each and no `stats` entries. The current report uses this current file state.
- Current `kaggle_latest_results.json` groups: `Self-Consistency_GSM8K`, `Self-Consistency_HOTPOTQA`, `Self-Consistency_MATH`, `Self-Consistency_TRUTHFULQA`, `Self-Consistency_MBPP`.
- Current self-consistency accuracies: GSM8K 90%, HOTPOTQA 40%, MATH 80%, TRUTHFULQA 80%, MBPP 0%.
- The latest ablation snapshot remains internally consistent in `ablation_arm11.json`: Arm_00_StaticRing = 60/100, Arm_01_PPOOnly = 66/100, Arm_10_SparseRing = 63/100, Arm_11_Full = 65/100.
- Factorial OLS betas implied by those four ablation accuracies are: intercept 0.60, sparsity +0.03, PPO +0.06, interaction -0.04.
- Transfer stats for AQUA and HOTPOTQA live in `phase2_interim.json`; they match recomputation using a Student t 95% CI over 3 seeds.
- `Transfer_GSM8K` has three raw seed streams but no stored aggregate stats in the current JSON files. Recomputed values are included below.
- FullComm/NoComm aggregate stats are not stored in the current JSON files, but raw streams exist. Recomputed one-run values are included below.
- `IB-Controller_gsm8k_stream.jsonl` contains only 2 records, so it looks incomplete.
- `exact_match` and `f1_score` are not interchangeable with `is_correct`; use `is_correct` as the primary accuracy column unless specifically debugging extraction.
- The `plots` directory contains no plot files.

## File Inventory

| Path | Kind | Size bytes | Last modified |
|---|---:|---:|---|
| `ablation_arm00.json` | file | 4069180 | 2026-06-13 08:04:46 |
| `ablation_arm01.json` | file | 820646 | 2026-06-13 11:16:02 |
| `ablation_arm10.json` | file | 2173842 | 2026-06-13 11:25:09 |
| `ablation_arm11.json` | file | 2982386 | 2026-06-13 11:25:25 |
| `aqua_pretrained.pt` | file | 582 | 2026-06-12 18:37:30 |
| `aqua_pretrained.pt.npz` | file | 155557 | 2026-06-12 18:37:30 |
| `continuous` | dir |  | 2026-06-13 11:01:53 |
| `continuous\Arm_01_PPOOnly_gsm8k_stream.jsonl` | file | 695945 | 2026-06-13 10:23:40 |
| `continuous\Arm_11_Full_gsm8k_stream.jsonl` | file | 688789 | 2026-06-13 11:07:57 |
| `continuous\IB-Controller_aqua_stream.jsonl` | file | 535427 | 2026-06-13 09:09:27 |
| `continuous\IB-Controller_gsm8k_stream.jsonl` | file | 11576 | 2026-06-12 16:17:13 |
| `continuous\IB-Controller_hotpotqa_stream.jsonl` | file | 777160 | 2026-06-13 09:01:44 |
| `continuous\Multi-Agent Debate_aqua_stream.jsonl` | file | 928401 | 2026-06-13 00:55:45 |
| `continuous\Multi-Agent Debate_hotpotqa_stream.jsonl` | file | 994278 | 2026-06-13 00:49:03 |
| `continuous\No Communication_aqua_stream.jsonl` | file | 935088 | 2026-06-13 00:56:27 |
| `continuous\No Communication_hotpotqa_stream.jsonl` | file | 1003753 | 2026-06-13 00:49:30 |
| `continuous\Train_Arm_01_PPOOnly_Epoch1_gsm8k_stream.jsonl` | file | 670362 | 2026-06-13 09:59:06 |
| `continuous\Train_Arm_01_PPOOnly_Epoch2_gsm8k_stream.jsonl` | file | 661307 | 2026-06-13 10:04:27 |
| `continuous\Train_Arm_01_PPOOnly_Epoch3_gsm8k_stream.jsonl` | file | 657666 | 2026-06-13 10:09:19 |
| `continuous\Train_Arm_01_PPOOnly_Epoch4_gsm8k_stream.jsonl` | file | 663042 | 2026-06-13 10:14:01 |
| `continuous\Train_Arm_01_PPOOnly_Epoch5_gsm8k_stream.jsonl` | file | 678543 | 2026-06-13 10:18:34 |
| `continuous\Train_Pretrain_AQUA_Epoch1_aqua_stream.jsonl` | file | 644769 | 2026-06-12 18:27:50 |
| `continuous\Train_Pretrain_AQUA_Epoch2_aqua_stream.jsonl` | file | 659719 | 2026-06-12 18:30:24 |
| `continuous\Train_Pretrain_AQUA_Epoch3_aqua_stream.jsonl` | file | 662384 | 2026-06-12 18:32:51 |
| `continuous\Train_Pretrain_AQUA_Epoch4_aqua_stream.jsonl` | file | 663029 | 2026-06-12 18:35:16 |
| `continuous\Train_Pretrain_AQUA_Epoch5_aqua_stream.jsonl` | file | 632581 | 2026-06-12 18:37:30 |
| `continuous\Train_Pretrain_GSM8K_Epoch1_gsm8k_stream.jsonl` | file | 737317 | 2026-06-12 17:33:47 |
| `continuous\Train_Pretrain_GSM8K_Epoch2_gsm8k_stream.jsonl` | file | 666206 | 2026-06-12 17:38:29 |
| `continuous\Train_Pretrain_GSM8K_Epoch3_gsm8k_stream.jsonl` | file | 674273 | 2026-06-12 17:42:52 |
| `continuous\Train_Pretrain_GSM8K_Epoch4_gsm8k_stream.jsonl` | file | 659733 | 2026-06-12 17:47:15 |
| `continuous\Train_Pretrain_GSM8K_Epoch5_gsm8k_stream.jsonl` | file | 647016 | 2026-06-12 17:51:29 |
| `continuous\Train_Pretrain_HOTPOTQA_Epoch1_hotpotqa_stream.jsonl` | file | 750477 | 2026-06-12 18:02:08 |
| `continuous\Train_Pretrain_HOTPOTQA_Epoch2_hotpotqa_stream.jsonl` | file | 738258 | 2026-06-12 18:06:24 |
| `continuous\Train_Pretrain_HOTPOTQA_Epoch3_hotpotqa_stream.jsonl` | file | 749001 | 2026-06-12 18:10:38 |
| `continuous\Train_Pretrain_HOTPOTQA_Epoch4_hotpotqa_stream.jsonl` | file | 754345 | 2026-06-12 18:14:50 |
| `continuous\Train_Pretrain_HOTPOTQA_Epoch5_hotpotqa_stream.jsonl` | file | 768297 | 2026-06-12 18:19:02 |
| `continuous\Train_Toy_GSM8K_Epoch1_gsm8k_stream.jsonl` | file | 310034 | 2026-06-12 17:10:47 |
| `continuous\Transfer_AQUA_seed0_aqua_stream.jsonl` | file | 1731238 | 2026-06-12 22:35:13 |
| `continuous\Transfer_AQUA_seed1_aqua_stream.jsonl` | file | 1745431 | 2026-06-12 22:43:16 |
| `continuous\Transfer_AQUA_seed2_aqua_stream.jsonl` | file | 1730854 | 2026-06-12 22:52:40 |
| `continuous\Transfer_GSM8K_seed0_gsm8k_stream.jsonl` | file | 2085921 | 2026-06-12 19:08:54 |
| `continuous\Transfer_GSM8K_seed1_gsm8k_stream.jsonl` | file | 2061472 | 2026-06-12 19:36:40 |
| `continuous\Transfer_GSM8K_seed2_gsm8k_stream.jsonl` | file | 2109592 | 2026-06-12 20:00:56 |
| `continuous\Transfer_HOTPOTQA_seed0_hotpotqa_stream.jsonl` | file | 2369491 | 2026-06-12 21:13:26 |
| `continuous\Transfer_HOTPOTQA_seed1_hotpotqa_stream.jsonl` | file | 2234238 | 2026-06-12 21:43:36 |
| `continuous\Transfer_HOTPOTQA_seed2_hotpotqa_stream.jsonl` | file | 2338129 | 2026-06-12 22:13:57 |
| `gsm8k_pretrained.pt` | file | 649 | 2026-06-12 17:51:29 |
| `gsm8k_pretrained.pt.npz` | file | 155557 | 2026-06-12 17:51:29 |
| `hotpotqa_pretrained.pt` | file | 710 | 2026-06-12 18:19:02 |
| `hotpotqa_pretrained.pt.npz` | file | 155557 | 2026-06-12 18:19:02 |
| `kaggle_latest_results.json` | file | 608121 | 2026-06-13 12:41:35 |
| `phase2_interim.json` | file | 1183 | 2026-06-13 11:11:42 |
| `plots` | dir |  | 2026-06-08 19:09:19 |

## JSON Detailed Samples

| File | Group | N | Correct | Accuracy | EM mean | F1 mean | Tx tokens mean | Full tokens mean | Density mean | Formula mismatches |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `ablation_arm00.json` | `Arm_00_StaticRing` | 300 | 169 | 56.33% | 0.4000 | 0.4000 | 1807.7467 | 3020.9733 | 0.5000 | 2 |
| `ablation_arm01.json` | `Arm_00_StaticRing` | 100 | 60 | 60.00% | NA | NA | NA | NA | NA | NA |
| `ablation_arm01.json` | `Arm_01_PPOOnly` | 100 | 66 | 66.00% | 0.5100 | 0.5100 | 507.6500 | 822.2000 | 0.5372 | 0 |
| `ablation_arm10.json` | `Arm_00_StaticRing` | 100 | 60 | 60.00% | NA | NA | NA | NA | NA | NA |
| `ablation_arm10.json` | `Arm_01_PPOOnly` | 100 | 66 | 66.00% | 0.5100 | 0.5100 | 507.6500 | 822.2000 | 0.5372 | 0 |
| `ablation_arm10.json` | `Arm_10_SparseRing` | 100 | 63 | 63.00% | 0.4800 | 0.4800 | 1779.6400 | 2980.5600 | 0.5100 | 0 |
| `ablation_arm11.json` | `Arm_00_StaticRing` | 100 | 60 | 60.00% | NA | NA | NA | NA | NA | NA |
| `ablation_arm11.json` | `Arm_01_PPOOnly` | 100 | 66 | 66.00% | 0.5100 | 0.5100 | 507.6500 | 822.2000 | 0.5372 | 0 |
| `ablation_arm11.json` | `Arm_10_SparseRing` | 100 | 63 | 63.00% | 0.4800 | 0.4800 | 1779.6400 | 2980.5600 | 0.5100 | 0 |
| `ablation_arm11.json` | `Arm_11_Full` | 100 | 65 | 65.00% | 0.5000 | 0.5000 | 496.6600 | 822.2000 | 0.5119 | 1 |
| `kaggle_latest_results.json` | `Self-Consistency_GSM8K` | 10 | 9 | 90.00% | NA | NA | 1916.6000 | 3114.9000 | 0.5038 | 10 |
| `kaggle_latest_results.json` | `Self-Consistency_HOTPOTQA` | 10 | 4 | 40.00% | NA | NA | 1042.3000 | 1910.7000 | 0.5030 | 10 |
| `kaggle_latest_results.json` | `Self-Consistency_MATH` | 10 | 8 | 80.00% | NA | NA | 452.5000 | 840.3000 | 0.5092 | 9 |
| `kaggle_latest_results.json` | `Self-Consistency_TRUTHFULQA` | 10 | 8 | 80.00% | NA | NA | 597.4000 | 1162.2000 | 0.5065 | 9 |
| `kaggle_latest_results.json` | `Self-Consistency_MBPP` | 10 | 0 | 0.00% | NA | NA | 795.3000 | 1514.4000 | 0.5069 | 10 |

Full detailed ablation/stream record fields include: `agent_diversity`, `answer_entropy`, `average_delta_w`, `communication_density`, `compression_ratio`, `exact_match`, `f1_score`, `final_answer`, `final_answers`, `final_reasoning`, `generation_tokens`, `gold_answer`, `halt_round`, `information_retention`, `initial_answers`, `initial_correct`, `initial_majority_correct`, `initial_reasoning`, `is_correct`, `mode_distribution`, `n_active_edges`, `question`, `raw_communications`, `semantic_similarity`, `token_reduction`, `total_tokens_if_full`, `total_tokens_transmitted`, `weight_matrices`. Current self-consistency records use a smaller subset and omit `exact_match`, `f1_score`, and later semantic/compression diagnostic fields.

## Stored Stats Cross-check

| File | Stat | Stored acc mean | Stored acc sd | Stored acc 95CI | Recalc acc mean | Recalc acc sd | Recalc acc 95CI | Stored token mean | Stored token sd | Stored token 95CI | Recalc token mean | Recalc token sd | Recalc token 95CI |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `phase2_interim.json` | `Transfer_HOTPOTQA` | 0.3167 | 0.0426 | 0.1057 | 0.3167 | 0.0426 | 0.1057 | 473.1600 | 22.7164 | 56.4307 | 473.1600 | 22.7164 | 56.4307 |
| `phase2_interim.json` | `Transfer_AQUA` | 0.8622 | 0.0039 | 0.0098 | 0.8622 | 0.0039 | 0.0098 | 438.2323 | 8.7409 | 21.7136 | 438.2323 | 8.7409 | 21.7136 |

The 95% CI values use Student t with df=2 for the 3-seed aggregates, not the normal 1.96 multiplier.

## Factorial Ablation Check

| Quantity | Value | Check |
|---|---:|---|
| Intercept | 0.6000 | Arm_00 accuracy |
| beta_A_sparsity | 0.0300 | 0.63 - 0.60 |
| beta_B_ppo | 0.0600 | 0.66 - 0.60 |
| beta_AB_interaction | -0.0400 | 0.65 - 0.63 - 0.66 + 0.60 |

## Recomputed Aggregate Streams

| Experiment | Files | N per run | Correct per run | Accuracy values | Acc mean | Acc sd | Acc 95CI | Token values | Token mean | Token sd | Token 95CI |
|---|---|---:|---:|---|---:|---:|---:|---|---:|---:|---:|
| `Transfer_AQUA` | `Transfer_AQUA_seed0_aqua_stream.jsonl, Transfer_AQUA_seed1_aqua_stream.jsonl, Transfer_AQUA_seed2_aqua_stream.jsonl` | [254, 254, 254] | [218, 219, 220] | 85.83%, 86.22%, 86.61% | 86.22% | 0.39% | 0.98% | 431.5866, 448.1339, 434.9764 | 438.2323 | 8.7409 | 21.7136 |
| `Transfer_GSM8K` | `Transfer_GSM8K_seed0_gsm8k_stream.jsonl, Transfer_GSM8K_seed1_gsm8k_stream.jsonl, Transfer_GSM8K_seed2_gsm8k_stream.jsonl` | [300, 300, 300] | [159, 159, 169] | 53.00%, 53.00%, 56.33% | 54.11% | 1.92% | 4.78% | 493.2300, 483.1367, 506.6433 | 494.3367 | 11.7923 | 29.2938 |
| `Transfer_HOTPOTQA` | `Transfer_HOTPOTQA_seed0_hotpotqa_stream.jsonl, Transfer_HOTPOTQA_seed1_hotpotqa_stream.jsonl, Transfer_HOTPOTQA_seed2_hotpotqa_stream.jsonl` | [300, 300, 300] | [109, 92, 84] | 36.33%, 30.67%, 28.00% | 31.67% | 4.26% | 10.57% | 492.4767, 448.1333, 478.8700 | 473.1600 | 22.7164 | 56.4307 |
| `FullComm_AQUA` | `Multi-Agent Debate_aqua_stream.jsonl` | [762] | [663] | 87.01% | 87.01% | 0.00% | 0.00% | 789.2992 | 789.2992 | 0.0000 | 0.0000 |
| `NoComm_AQUA` | `No Communication_aqua_stream.jsonl` | [762] | [630] | 82.68% | 82.68% | 0.00% | 0.00% | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `FullComm_HOTPOTQA` | `Multi-Agent Debate_hotpotqa_stream.jsonl` | [900] | [306] | 34.00% | 34.00% | 0.00% | 0.00% | 2914.1289 | 2914.1289 | 0.0000 | 0.0000 |
| `NoComm_HOTPOTQA` | `No Communication_hotpotqa_stream.jsonl` | [900] | [270] | 30.00% | 30.00% | 0.00% | 0.00% | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

For one-file FullComm/NoComm rows, sd and CI are 0 because there is only one run; that should not be read as statistical certainty.

## Continuous Stream Summary

| Stream | N | Correct | Accuracy | EM | F1 | Tx tokens | Full tokens | Gen tokens | Density | Halt mean | Formula mismatches | is_correct vs EM disagreements | Modes | Halt counts | Edge counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| `Arm_01_PPOOnly_gsm8k_stream.jsonl` | 100 | 66 | 66.00% | 0.5100 | 0.5100 | 507.6500 | 822.2000 | 4386.0400 | 0.5372 | 1.7000 | 0 | 15 | `{'PARTIAL': 510, 'FULL': 0}` | `{0: 15, 2: 85}` | `{0: 15, 6: 85}` |
| `Arm_11_Full_gsm8k_stream.jsonl` | 100 | 65 | 65.00% | 0.5000 | 0.5000 | 496.6600 | 822.2000 | 4380.5900 | 0.5119 | 1.7000 | 1 | 15 | `{'PARTIAL': 510, 'FULL': 0}` | `{0: 15, 2: 85}` | `{0: 15, 6: 85}` |
| `IB-Controller_aqua_stream.jsonl` | 100 | 88 | 88.00% | 0.0200 | 0.0200 | 40.9700 | 62.8800 | 2864.3000 | 0.0746 | 0.2400 | 6 | 86 | `{'PARTIAL': 72, 'FULL': 0}` | `{0: 88, 2: 12}` | `{0: 88, 6: 12}` |
| `IB-Controller_gsm8k_stream.jsonl` | 2 | 2 | 100.00% | 0.5000 | 0.5000 | 256.5000 | 503.0000 | 3287.5000 | 0.3107 | 1.0000 | 0 | 1 | `{'PARTIAL': 6, 'FULL': 0}` | `{0: 1, 2: 1}` | `{0: 1, 6: 1}` |
| `IB-Controller_hotpotqa_stream.jsonl` | 100 | 28 | 28.00% | 0.1900 | 0.3141 | 466.6600 | 764.4400 | 4816.3200 | 0.5463 | 1.7600 | 9 | 9 | `{'PARTIAL': 528, 'FULL': 0}` | `{0: 12, 2: 88}` | `{0: 12, 6: 88}` |
| `Multi-Agent Debate_aqua_stream.jsonl` | 762 | 663 | 87.01% | 0.0000 | 0.0000 | 789.2992 | 789.2992 | 5612.4291 | 0.1850 | 0.7402 | 0 | 663 | `{'PARTIAL': 0, 'FULL': 3384}` | `{0: 621, 4: 141}` | `{0: 621, 6: 141}` |
| `Multi-Agent Debate_hotpotqa_stream.jsonl` | 900 | 306 | 34.00% | 0.0000 | 0.0000 | 2914.1289 | 2914.1289 | 10888.9489 | 0.8811 | 2.6433 | 0 | 306 | `{'PARTIAL': 0, 'FULL': 14274}` | `{0: 107, 3: 793}` | `{0: 107, 6: 793}` |
| `No Communication_aqua_stream.jsonl` | 762 | 630 | 82.68% | 0.0000 | 0.0000 | 0.0000 | 14606.4094 | 2434.4016 | 0.0000 | 0.0000 | 762 | 630 | `{'PARTIAL': 0, 'FULL': 0}` | `{0: 762}` | `{0: 762}` |
| `No Communication_hotpotqa_stream.jsonl` | 900 | 270 | 30.00% | 0.0000 | 0.0000 | 0.0000 | 14905.3333 | 2484.2222 | 0.0000 | 0.0000 | 900 | 270 | `{'PARTIAL': 0, 'FULL': 0}` | `{0: 900}` | `{0: 900}` |
| `Train_Arm_01_PPOOnly_Epoch1_gsm8k_stream.jsonl` | 100 | 56 | 56.00% | 0.3600 | 0.3600 | 464.4700 | 825.3600 | 4279.4200 | 0.4561 | 1.6200 | 2 | 20 | `{'PARTIAL': 461, 'FULL': 29}` | `{0: 21, 2: 75, 3: 4}` | `{0: 21, 2: 3, 3: 9, 4: 7, 5: 13, 6: 47}` |
| `Train_Arm_01_PPOOnly_Epoch2_gsm8k_stream.jsonl` | 100 | 60 | 60.00% | 0.4000 | 0.4000 | 440.1600 | 767.9400 | 4172.3800 | 0.4622 | 1.5800 | 2 | 20 | `{'PARTIAL': 429, 'FULL': 30}` | `{0: 21, 2: 79}` | `{0: 21, 3: 4, 4: 14, 5: 20, 6: 41}` |
| `Train_Arm_01_PPOOnly_Epoch3_gsm8k_stream.jsonl` | 100 | 54 | 54.00% | 0.3400 | 0.3400 | 442.1100 | 767.9400 | 4183.4200 | 0.4706 | 1.5800 | 2 | 20 | `{'PARTIAL': 440, 'FULL': 20}` | `{0: 21, 2: 79}` | `{0: 21, 2: 1, 3: 2, 4: 13, 5: 28, 6: 35}` |
| `Train_Arm_01_PPOOnly_Epoch4_gsm8k_stream.jsonl` | 100 | 53 | 53.00% | 0.3300 | 0.3300 | 445.6700 | 767.9400 | 4183.0500 | 0.4763 | 1.5800 | 3 | 20 | `{'PARTIAL': 432, 'FULL': 29}` | `{0: 21, 2: 79}` | `{0: 21, 2: 1, 3: 2, 4: 9, 5: 33, 6: 34}` |
| `Train_Arm_01_PPOOnly_Epoch5_gsm8k_stream.jsonl` | 100 | 64 | 64.00% | 0.4400 | 0.4400 | 478.5200 | 767.9400 | 4208.8100 | 0.4719 | 1.5800 | 3 | 20 | `{'PARTIAL': 428, 'FULL': 32}` | `{0: 21, 2: 79}` | `{0: 21, 3: 4, 4: 12, 5: 23, 6: 40}` |
| `Train_Pretrain_AQUA_Epoch1_aqua_stream.jsonl` | 100 | 85 | 85.00% | 0.0500 | 0.0500 | 311.8200 | 575.5600 | 5528.7200 | 0.1087 | 0.7600 | 8 | 80 | `{'PARTIAL': 424, 'FULL': 22}` | `{0: 81, 4: 19}` | `{0: 81, 3: 1, 4: 3, 5: 4, 6: 11}` |
| `Train_Pretrain_AQUA_Epoch2_aqua_stream.jsonl` | 100 | 86 | 86.00% | 0.0600 | 0.0600 | 345.2600 | 599.9000 | 5523.1000 | 0.1218 | 0.7600 | 8 | 80 | `{'PARTIAL': 409, 'FULL': 33}` | `{0: 81, 4: 19}` | `{0: 81, 5: 4, 6: 15}` |
| `Train_Pretrain_AQUA_Epoch3_aqua_stream.jsonl` | 100 | 86 | 86.00% | 0.0600 | 0.0600 | 348.3700 | 550.7400 | 5587.5200 | 0.1154 | 0.7600 | 8 | 80 | `{'PARTIAL': 409, 'FULL': 29}` | `{0: 81, 4: 19}` | `{0: 81, 4: 3, 5: 7, 6: 9}` |
| `Train_Pretrain_AQUA_Epoch4_aqua_stream.jsonl` | 100 | 86 | 86.00% | 0.0600 | 0.0600 | 361.0100 | 591.7200 | 5548.2500 | 0.1067 | 0.7600 | 8 | 80 | `{'PARTIAL': 422, 'FULL': 20}` | `{0: 81, 4: 19}` | `{0: 81, 4: 3, 5: 4, 6: 12}` |
| `Train_Pretrain_AQUA_Epoch5_aqua_stream.jsonl` | 100 | 86 | 86.00% | 0.0600 | 0.0600 | 266.3800 | 495.1800 | 5550.5600 | 0.1181 | 0.7600 | 8 | 80 | `{'PARTIAL': 416, 'FULL': 23}` | `{0: 81, 4: 19}` | `{0: 81, 4: 1, 5: 4, 6: 14}` |
| `Train_Pretrain_GSM8K_Epoch1_gsm8k_stream.jsonl` | 100 | 58 | 58.00% | 0.4000 | 0.4000 | 627.0000 | 1067.8000 | 4985.1400 | 0.4719 | 1.8400 | 3 | 18 | `{'PARTIAL': 582, 'FULL': 49}` | `{0: 18, 2: 62, 3: 20}` | `{0: 18, 2: 1, 3: 5, 4: 18, 5: 27, 6: 31}` |
| `Train_Pretrain_GSM8K_Epoch2_gsm8k_stream.jsonl` | 100 | 59 | 59.00% | 0.4100 | 0.4100 | 473.9300 | 828.1400 | 4341.9800 | 0.4679 | 1.6800 | 3 | 18 | `{'PARTIAL': 471, 'FULL': 30}` | `{0: 18, 2: 78, 3: 4}` | `{0: 18, 3: 9, 4: 13, 5: 28, 6: 32}` |
| `Train_Pretrain_GSM8K_Epoch3_gsm8k_stream.jsonl` | 100 | 58 | 58.00% | 0.4000 | 0.4000 | 476.4000 | 780.7400 | 4254.6200 | 0.4688 | 1.6400 | 2 | 18 | `{'PARTIAL': 446, 'FULL': 36}` | `{0: 18, 2: 82}` | `{0: 18, 2: 1, 3: 4, 4: 21, 5: 27, 6: 29}` |
| `Train_Pretrain_GSM8K_Epoch4_gsm8k_stream.jsonl` | 100 | 54 | 54.00% | 0.3600 | 0.3600 | 446.0700 | 780.7400 | 4238.4100 | 0.4818 | 1.6400 | 3 | 18 | `{'PARTIAL': 432, 'FULL': 33}` | `{0: 18, 2: 82}` | `{0: 18, 3: 4, 4: 18, 5: 27, 6: 33}` |
| `Train_Pretrain_GSM8K_Epoch5_gsm8k_stream.jsonl` | 100 | 54 | 54.00% | 0.3600 | 0.3600 | 414.9700 | 780.7400 | 4199.2700 | 0.4613 | 1.6400 | 4 | 18 | `{'PARTIAL': 431, 'FULL': 35}` | `{0: 18, 2: 82}` | `{0: 18, 2: 1, 3: 10, 4: 16, 5: 31, 6: 24}` |
| `Train_Pretrain_HOTPOTQA_Epoch1_hotpotqa_stream.jsonl` | 100 | 40 | 40.00% | 0.3400 | 0.3899 | 421.0800 | 748.6200 | 4916.8800 | 0.5327 | 1.8000 | 13 | 6 | `{'PARTIAL': 479, 'FULL': 37}` | `{0: 10, 2: 90}` | `{0: 10, 2: 2, 3: 3, 4: 17, 5: 22, 6: 46}` |
| `Train_Pretrain_HOTPOTQA_Epoch2_hotpotqa_stream.jsonl` | 100 | 39 | 39.00% | 0.3300 | 0.3714 | 414.8300 | 748.6200 | 4935.3200 | 0.5101 | 1.8000 | 13 | 6 | `{'PARTIAL': 470, 'FULL': 44}` | `{0: 10, 2: 90}` | `{0: 10, 2: 2, 3: 6, 4: 12, 5: 40, 6: 30}` |
| `Train_Pretrain_HOTPOTQA_Epoch3_hotpotqa_stream.jsonl` | 100 | 44 | 44.00% | 0.3800 | 0.4289 | 435.6500 | 748.6200 | 4931.3200 | 0.5368 | 1.8000 | 13 | 6 | `{'PARTIAL': 484, 'FULL': 33}` | `{0: 10, 2: 90}` | `{0: 10, 2: 3, 3: 8, 4: 11, 5: 38, 6: 30}` |
| `Train_Pretrain_HOTPOTQA_Epoch4_hotpotqa_stream.jsonl` | 100 | 40 | 40.00% | 0.3400 | 0.4001 | 435.1700 | 748.6200 | 5045.4100 | 0.5315 | 1.8200 | 13 | 6 | `{'PARTIAL': 475, 'FULL': 53}` | `{0: 10, 2: 88, 3: 2}` | `{0: 10, 3: 6, 4: 11, 5: 38, 6: 35}` |
| `Train_Pretrain_HOTPOTQA_Epoch5_hotpotqa_stream.jsonl` | 100 | 41 | 41.00% | 0.3500 | 0.3936 | 459.2300 | 748.6200 | 5004.2800 | 0.5072 | 1.8100 | 13 | 6 | `{'PARTIAL': 473, 'FULL': 41}` | `{0: 10, 2: 89, 3: 1}` | `{0: 10, 2: 3, 3: 5, 4: 18, 5: 28, 6: 36}` |
| `Train_Toy_GSM8K_Epoch1_gsm8k_stream.jsonl` | 43 | 26 | 60.47% | 0.5116 | 0.5116 | 554.5581 | 928.7442 | 4505.7907 | 0.5338 | 1.8140 | 0 | 4 | `{'PARTIAL': 224, 'FULL': 9}` | `{0: 4, 2: 39}` | `{0: 4, 2: 1, 3: 3, 4: 2, 5: 5, 6: 28}` |
| `Transfer_AQUA_seed0_aqua_stream.jsonl` | 254 | 218 | 85.83% | 0.0669 | 0.0669 | 431.5866 | 714.5748 | 5376.2480 | 0.1160 | 0.7402 | 20 | 201 | `{'PARTIAL': 1128, 'FULL': 0}` | `{0: 207, 4: 47}` | `{0: 207, 6: 47}` |
| `Transfer_AQUA_seed1_aqua_stream.jsonl` | 254 | 219 | 86.22% | 0.0709 | 0.0709 | 448.1339 | 745.2126 | 5381.4764 | 0.1160 | 0.7402 | 20 | 201 | `{'PARTIAL': 1128, 'FULL': 0}` | `{0: 207, 4: 47}` | `{0: 207, 6: 47}` |
| `Transfer_AQUA_seed2_aqua_stream.jsonl` | 254 | 220 | 86.61% | 0.0748 | 0.0748 | 434.9764 | 711.5748 | 5406.7835 | 0.1160 | 0.7402 | 20 | 201 | `{'PARTIAL': 1128, 'FULL': 0}` | `{0: 207, 4: 47}` | `{0: 207, 6: 47}` |
| `Transfer_GSM8K_seed0_gsm8k_stream.jsonl` | 300 | 159 | 53.00% | 0.3533 | 0.3533 | 493.2300 | 826.3333 | 4338.5633 | 0.4937 | 1.6400 | 6 | 53 | `{'PARTIAL': 1476, 'FULL': 0}` | `{0: 54, 2: 246}` | `{0: 54, 6: 246}` |
| `Transfer_GSM8K_seed1_gsm8k_stream.jsonl` | 300 | 159 | 53.00% | 0.3400 | 0.3400 | 483.1367 | 806.6067 | 4299.1700 | 0.4876 | 1.6200 | 3 | 57 | `{'PARTIAL': 1458, 'FULL': 0}` | `{0: 57, 2: 243}` | `{0: 57, 6: 243}` |
| `Transfer_GSM8K_seed2_gsm8k_stream.jsonl` | 300 | 169 | 56.33% | 0.3800 | 0.3800 | 506.6433 | 830.4533 | 4324.5400 | 0.4899 | 1.6267 | 6 | 55 | `{'PARTIAL': 1464, 'FULL': 0}` | `{0: 56, 2: 244}` | `{0: 56, 6: 244}` |
| `Transfer_HOTPOTQA_seed0_hotpotqa_stream.jsonl` | 300 | 109 | 36.33% | 0.2900 | 0.4046 | 492.4767 | 790.8200 | 4716.5000 | 0.5440 | 1.7600 | 33 | 22 | `{'PARTIAL': 1584, 'FULL': 0}` | `{0: 36, 2: 264}` | `{0: 36, 6: 264}` |
| `Transfer_HOTPOTQA_seed1_hotpotqa_stream.jsonl` | 300 | 92 | 30.67% | 0.2333 | 0.3261 | 448.1333 | 719.4067 | 4935.5233 | 0.5337 | 1.7267 | 37 | 22 | `{'PARTIAL': 1554, 'FULL': 0}` | `{0: 41, 2: 259}` | `{0: 41, 6: 259}` |
| `Transfer_HOTPOTQA_seed2_hotpotqa_stream.jsonl` | 300 | 84 | 28.00% | 0.2333 | 0.3641 | 478.8700 | 772.4400 | 4960.5100 | 0.5562 | 1.8000 | 36 | 14 | `{'PARTIAL': 1620, 'FULL': 0}` | `{0: 30, 2: 270}` | `{0: 30, 6: 270}` |

## Training Trends

- `Train_Arm_01_PPOOnly` GSM8K accuracy by epoch: 56%, 60%, 54%, 53%, 64%. Epoch 5 is best among those five.
- `Train_Pretrain_AQUA` accuracy by epoch: 85%, 86%, 86%, 86%, 86%. It stabilizes after epoch 2.
- `Train_Pretrain_GSM8K` accuracy by epoch: 58%, 59%, 58%, 54%, 54%. It declines after epoch 3.
- `Train_Pretrain_HOTPOTQA` accuracy by epoch: 40%, 39%, 44%, 40%, 41%. Epoch 3 is best.
- `Train_Toy_GSM8K_Epoch1` has only 43 records, 26 correct, 60.47% accuracy.

## Consistency Checks

| JSON file | Group | Stream | JSON N | Stream N | Exact matching records |
|---|---|---|---:|---:|---:|
| `ablation_arm11.json` | `Arm_01_PPOOnly` | `Arm_01_PPOOnly_gsm8k_stream.jsonl` | 100 | 100 | 100 |
| `ablation_arm11.json` | `Arm_11_Full` | `Arm_11_Full_gsm8k_stream.jsonl` | 100 | 100 | 100 |

Skipped expected cross-checks because the current JSON file no longer has those groups: `kaggle_latest_results.json` / `IB_Controller_HOTPOTQA`; `kaggle_latest_results.json` / `IB_Controller_AQUA`; `kaggle_latest_results.json` / `Arm_01_PPOOnly`; `kaggle_latest_results.json` / `Arm_11_Full`.

| Snapshot A | Group A | Snapshot B | Group B | N A | N B | Exact matches |
|---|---|---|---|---:|---:|---:|
| `ablation_arm01.json` | `Arm_01_PPOOnly` | `ablation_arm10.json` | `Arm_01_PPOOnly` | 100 | 100 | 100 |
| `ablation_arm10.json` | `Arm_01_PPOOnly` | `ablation_arm11.json` | `Arm_01_PPOOnly` | 100 | 100 | 100 |
| `ablation_arm10.json` | `Arm_10_SparseRing` | `ablation_arm11.json` | `Arm_10_SparseRing` | 100 | 100 | 100 |

Arm_00 cross-checks:

| Check | Correct in ablation_arm00 slice | Matches with later 100-row boolean sequence |
|---|---:|---:|
| ablation_arm00 first 100 vs later bools | 58/100 | 56/100 |
| ablation_arm00 last 100 vs later bools | 51/100 | 45/100 |

The later 100-row Arm_00 boolean-only sequence is identical across `ablation_arm01.json`, `ablation_arm10.json`, and `ablation_arm11.json`, but it is not simply the first or last 100 rows of the 300-row `ablation_arm00.json`.

## Checkpoint Metadata

| File | Size | SHA256 | X thresholds | Y thresholds | Agent vars | Agent historical accuracy |
|---|---:|---|---|---|---|---|
| `aqua_pretrained.pt` | 582 | `f54a2042b17b2a6eabc56eba961f058853d0d752d13c12ab1a37b2b255fb9bb2` | `[0.5, 0.9, 0.99, 1.0]` | `[0.7383059418457648, 0.9719222462203023, 0.9719222462203023, 1.0]` | `{}` | `{0: 0.856, 1: 0.85, 2: 0.854}` |
| `gsm8k_pretrained.pt` | 649 | `7598acc4a43a704308f7dbeb7237e24cae771ff3a5b57006faa32277ff3f9233` | `[0.1, 0.5, 0.9, 0.94, 0.99, 1.0]` | `[0.13403880070546736, 0.13403880070546736, 0.8, 0.9413092550790068, 0.9413092550790068, 0.945054945054945]` | `{0: 0.40298970862282607, 1: 0.4881382201906898, 2: 0.28384741811933}` | `{0: 0.678, 1: 0.638, 2: 0.586}` |
| `hotpotqa_pretrained.pt` | 710 | `83b35e395bde70a597d731efce9778ec42c9c5c693652d7c7555aa112a57fed8` | `[0.5, 0.85, 0.86, 0.88, 0.9, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0]` | `[0.13983050847457623, 0.13983050847457623, 0.15384615384615385, 0.15384615384615385, 0.3613861386138614, 0.3613861386138614, 0.47058823529411764, 0.4842105263157895, 0.4842105263157895, 0.527027027027027, 0.6761133603238867, 0.9125]` | `{}` | `{0: 0.384, 1: 0.386, 2: 0.408}` |

All three `.pt` files contain a fitted scikit-learn isotonic regression calibrator (`_fitted=True`, `out_of_bounds=clip`, `_sklearn_version=1.9.0`).

## NPZ Model Arrays

| File | Array | Shape | Dtype | Min | Max | Mean | Std |
|---|---|---:|---|---:|---:|---:|---:|
| `aqua_pretrained.pt.npz` | `actor_W1` | `(20, 64)` | `float64` | -0.4714 | 0.5563 | -0.0082 | 0.1568 |
| `aqua_pretrained.pt.npz` | `actor_b1` | `(64,)` | `float64` | -0.0236 | 0.0369 | 0.0015 | 0.0119 |
| `aqua_pretrained.pt.npz` | `actor_W2` | `(64, 64)` | `float64` | -0.4257 | 0.4291 | -0.0006 | 0.1252 |
| `aqua_pretrained.pt.npz` | `actor_b2` | `(64,)` | `float64` | -0.0257 | 0.0408 | 0.0009 | 0.0125 |
| `aqua_pretrained.pt.npz` | `actor_W3` | `(64, 122)` | `float64` | -0.3952 | 0.3986 | -0.0001 | 0.1050 |
| `aqua_pretrained.pt.npz` | `actor_b3` | `(122,)` | `float64` | -0.0312 | 0.0409 | 0.0019 | 0.0133 |
| `aqua_pretrained.pt.npz` | `critic_W1` | `(20, 64)` | `float64` | -0.4541 | 0.4842 | 0.0029 | 0.1567 |
| `aqua_pretrained.pt.npz` | `critic_b1` | `(64,)` | `float64` | -0.0229 | 0.0437 | 0.0007 | 0.0128 |
| `aqua_pretrained.pt.npz` | `critic_W2` | `(64, 64)` | `float64` | -0.4934 | 0.4689 | -0.0016 | 0.1242 |
| `aqua_pretrained.pt.npz` | `critic_b2` | `(64,)` | `float64` | -0.0316 | 0.0203 | -0.0008 | 0.0110 |
| `aqua_pretrained.pt.npz` | `critic_W3` | `(64, 1)` | `float64` | -0.3365 | 0.4408 | -0.0195 | 0.1666 |
| `aqua_pretrained.pt.npz` | `critic_b3` | `(1,)` | `float64` | -0.0105 | -0.0105 | -0.0105 | 0.0000 |
| `aqua_pretrained.pt.npz` | `mean_dim` | `()` | `int64` | 61.0000 | 61.0000 | 61.0000 | 0.0000 |
| `aqua_pretrained.pt.npz` | `calibrator_fitted` | `()` | `bool` | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| `gsm8k_pretrained.pt.npz` | `actor_W1` | `(20, 64)` | `float64` | -0.4508 | 0.4927 | 0.0105 | 0.1542 |
| `gsm8k_pretrained.pt.npz` | `actor_b1` | `(64,)` | `float64` | -0.0320 | 0.0269 | 0.0000 | 0.0124 |
| `gsm8k_pretrained.pt.npz` | `actor_W2` | `(64, 64)` | `float64` | -0.3971 | 0.4982 | -0.0027 | 0.1255 |
| `gsm8k_pretrained.pt.npz` | `actor_b2` | `(64,)` | `float64` | -0.0191 | 0.0288 | 0.0009 | 0.0104 |
| `gsm8k_pretrained.pt.npz` | `actor_W3` | `(64, 122)` | `float64` | -0.4193 | 0.3556 | 0.0015 | 0.1046 |
| `gsm8k_pretrained.pt.npz` | `actor_b3` | `(122,)` | `float64` | -0.0431 | 0.0429 | 0.0016 | 0.0149 |
| `gsm8k_pretrained.pt.npz` | `critic_W1` | `(20, 64)` | `float64` | -0.5138 | 0.5025 | 0.0031 | 0.1560 |
| `gsm8k_pretrained.pt.npz` | `critic_b1` | `(64,)` | `float64` | -0.0281 | 0.0253 | -0.0019 | 0.0117 |
| `gsm8k_pretrained.pt.npz` | `critic_W2` | `(64, 64)` | `float64` | -0.4544 | 0.5591 | 0.0010 | 0.1258 |
| `gsm8k_pretrained.pt.npz` | `critic_b2` | `(64,)` | `float64` | -0.0240 | 0.0307 | -0.0015 | 0.0114 |
| `gsm8k_pretrained.pt.npz` | `critic_W3` | `(64, 1)` | `float64` | -0.3811 | 0.4671 | -0.0383 | 0.1815 |
| `gsm8k_pretrained.pt.npz` | `critic_b3` | `(1,)` | `float64` | 0.0069 | 0.0069 | 0.0069 | 0.0000 |
| `gsm8k_pretrained.pt.npz` | `mean_dim` | `()` | `int64` | 61.0000 | 61.0000 | 61.0000 | 0.0000 |
| `gsm8k_pretrained.pt.npz` | `calibrator_fitted` | `()` | `bool` | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| `hotpotqa_pretrained.pt.npz` | `actor_W1` | `(20, 64)` | `float64` | -0.5562 | 0.5163 | -0.0005 | 0.1552 |
| `hotpotqa_pretrained.pt.npz` | `actor_b1` | `(64,)` | `float64` | -0.0239 | 0.0216 | -0.0028 | 0.0087 |
| `hotpotqa_pretrained.pt.npz` | `actor_W2` | `(64, 64)` | `float64` | -0.4257 | 0.4543 | -0.0030 | 0.1267 |
| `hotpotqa_pretrained.pt.npz` | `actor_b2` | `(64,)` | `float64` | -0.0241 | 0.0245 | -0.0036 | 0.0084 |
| `hotpotqa_pretrained.pt.npz` | `actor_W3` | `(64, 122)` | `float64` | -0.4241 | 0.4061 | 0.0003 | 0.1036 |
| `hotpotqa_pretrained.pt.npz` | `actor_b3` | `(122,)` | `float64` | -0.0386 | 0.0404 | 0.0014 | 0.0147 |
| `hotpotqa_pretrained.pt.npz` | `critic_W1` | `(20, 64)` | `float64` | -0.5180 | 0.5075 | -0.0089 | 0.1584 |
| `hotpotqa_pretrained.pt.npz` | `critic_b1` | `(64,)` | `float64` | -0.0246 | 0.0326 | 0.0008 | 0.0104 |
| `hotpotqa_pretrained.pt.npz` | `critic_W2` | `(64, 64)` | `float64` | -0.4059 | 0.4943 | 0.0019 | 0.1259 |
| `hotpotqa_pretrained.pt.npz` | `critic_b2` | `(64,)` | `float64` | -0.0214 | 0.0378 | 0.0019 | 0.0127 |
| `hotpotqa_pretrained.pt.npz` | `critic_W3` | `(64, 1)` | `float64` | -0.3129 | 0.3855 | 0.0038 | 0.1698 |
| `hotpotqa_pretrained.pt.npz` | `critic_b3` | `(1,)` | `float64` | -0.0101 | -0.0101 | -0.0101 | 0.0000 |
| `hotpotqa_pretrained.pt.npz` | `mean_dim` | `()` | `int64` | 61.0000 | 61.0000 | 61.0000 | 0.0000 |
| `hotpotqa_pretrained.pt.npz` | `calibrator_fitted` | `()` | `bool` | 1.0000 | 1.0000 | 1.0000 | 0.0000 |

## Interpretation Notes

- Best ablation arm by latest 100-sample GSM8K ablation accuracy is `Arm_01_PPOOnly` at 66%, slightly above `Arm_11_Full` at 65%.
- The negative interaction term means combining sparsity and PPO underperformed the additive expectation by 4 percentage points on this latest ablation slice.
- Current self-consistency file is very small: 10 examples per dataset. Treat its 90/40/80/80/0 percentages as smoke-test scale rather than stable benchmarks.
- For AQUA raw streams, `IB_Controller_AQUA` on 100 rows reports 88% accuracy with very low transmitted-token cost, while the larger full/no-communication streams are 87.01% and 82.68% respectively.
- For HOTPOTQA raw streams, `IB_Controller_HOTPOTQA` is 28% on 100 rows; transfer mean is 31.67% across three 300-row seeds; full communication is 34% on one 900-row stream; no communication is 30% on one 900-row stream.
- For GSM8K transfer, mean accuracy over three 300-row streams is 54.11%; this is present in raw streams but absent from stored stats.
- All conclusions above come from raw JSON/JSONL/NPZ/PT artifacts; no plot image was available to verify visually.
