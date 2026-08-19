# FINAL MASTER RESULTS (CogniSync_RRF Architecture vFINAL)

This document contains the complete, unabridged results from every evaluation suite run on the finalized architecture (Cross-Encoder Reranking, Regression Alpha, Multi-Signal Security, Query-Aware Filtering).

---

## main_comparison_public_source_candidate_pool.csv

| System | Recall@1 | Recall@3 | Recall@5 | MRR@5 | NDCG@5 |
| --- | --- | --- | --- | --- | --- |
| CogniSync_RRF | 0.8260030518936655 | 0.9285048015695452 | 0.968748494131415 | 0.8869135717481843 | 0.9062385650897724 |
| Dense | 0.7902884383712525 | 0.9046954416640852 | 0.9608193072430844 | 0.8593616264528047 | 0.883361424469807 |
| Hybrid_Naive | 0.7690840877017864 | 0.8823036060533048 | 0.9439707890177722 | 0.838697093817047 | 0.8632907184946359 |
| Lexical | 0.7211762411225461 | 0.8261447469567113 | 0.8998829724985371 | 0.7884223086542984 | 0.8145211631620163 |

---

## statistical_significance_public_only.csv

| Comparison | n_pairs | Wilcoxon Statistic | Raw p-value | Bonferroni p-value | Mean MRR@5 Diff | All paired differences zero | Significant (adj. p<0.05) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CogniSync_RRF vs Dense | 29011 | 9616420.0 | 2.620929645169704e-116 | 7.862788935509111e-116 | 0.0275379741017774 | False | True |
| CogniSync_RRF vs Lexical | 29011 | 23401852.0 | 0.0 | 0.0 | 0.0986424689485597 | False | True |
| CogniSync_RRF vs Hybrid_Naive | 29011 | 12929463.5 | 5.8862690227966536e-282 | 1.765880706838996e-281 | 0.0482733560833247 | False | True |

---

## confidence_intervals_public_only.csv

| Comparison | n_pairs | Mean MRR@5 Diff | 95% CI |
| --- | --- | --- | --- |
| CogniSync_RRF - Dense | 29011 | 0.0275 | [0.0250, 0.0300] |
| CogniSync_RRF - Lexical | 29011 | 0.0986 | [0.0957, 0.1019] |
| CogniSync_RRF - Hybrid_Naive | 29011 | 0.0483 | [0.0457, 0.0508] |

---

## security_comparison.csv

| Evaluation_Group | System | Attack Type | Attack Family | Attack Success Rate | MRR@5 Drop | Docs_Blocked | Atk_Blocked | Relevant_Blocked | FP_Rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| security_synthetic | CogniSync_RRF_Defense | Adaptive Query-Conditioned Injection | adaptive | 0.0012 | 0.0100666666666666 | 2.7348 | 0.9988 | 0.0104 | 0.0104 |
| security_synthetic | CogniSync_RRF_Defense | Generic Data Exfiltration | generic | 0.0084 | 0.0102333333333333 | 2.5652 | 0.8292 | 0.0104 | 0.0104 |
| security_synthetic | CogniSync_RRF_Defense | Generic Prompt Injection | generic | 0.0 | 0.0100333333333333 | 2.736 | 1.0 | 0.0104 | 0.0104 |
| security_synthetic | No_Defense | Adaptive Query-Conditioned Injection | adaptive | 0.9932 | 0.2251133333333333 | 0.0 | 0.0 | 0.0 | 0.0 |
| security_synthetic | No_Defense | Generic Data Exfiltration | generic | 0.042 | -0.0044466666666666 | 0.0 | 0.0 | 0.0 | 0.0 |
| security_synthetic | No_Defense | Generic Prompt Injection | generic | 0.03 | -0.00418 | 0.0 | 0.0 | 0.0 | 0.0 |

---

## latency_vs_performance.csv

| System | MRR@5 | per_query_rebuild_latency_ms |
| --- | --- | --- |
| CogniSync_RRF | 0.8901280807945691 | 148.59654117825716 |
| Dense | 0.8603300672173361 | 98.55461752151992 |
| Hybrid_Naive | 0.8393973848777715 | 148.59654117825716 |
| Lexical | 0.790289714521397 | 10.950513057946656 |

---

## main_comparison_synthetic.csv

| System | Recall@1 | Recall@3 | Recall@5 | MRR@5 | NDCG@5 |
| --- | --- | --- | --- | --- | --- |
| CogniSync_RRF | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Dense | 0.8141176470588235 | 0.9823529411764704 | 1.0 | 0.8934313725490196 | 0.920622829075248 |
| Hybrid_Naive | 0.7282352941176471 | 1.0 | 1.0 | 0.8633333333333334 | 0.8990835930126128 |
| Lexical | 0.7141176470588235 | 1.0 | 1.0 | 0.8541176470588235 | 0.8921788044874027 |

---

## memoryarena_context_augmentation.csv

| Variant | MRR@5 | Recall@5 |
| --- | --- | --- |
| Hybrid (No Context) | 0.9308333333333334 | 1.0 |
| Hybrid + Appended Temporal Context | 0.9326666666666666 | 0.99 |
| Hybrid + Appended Topical Distractor | 0.9219 | 1.0 |

---

## per_dataset_metrics_final.csv

| Evaluation_Group | Dataset | System | MRR@5 | Recall@5 |
| --- | --- | --- | --- | --- |
| public_source_candidate_pool | code_search_net | CogniSync_RRF | 0.9982352941176472 | 0.9983529411764706 |
| public_source_candidate_pool | code_search_net | Dense | 0.9940954248366012 | 0.9981176470588236 |
| public_source_candidate_pool | code_search_net | Hybrid_Naive | 0.9902718954248366 | 0.9947450980392156 |
| public_source_candidate_pool | code_search_net | Lexical | 0.9833307189542484 | 0.987843137254902 |
| public_source_candidate_pool | ms_marco | CogniSync_RRF | 0.6423757575757576 | 0.926430303030303 |
| public_source_candidate_pool | ms_marco | Dense | 0.5509373737373737 | 0.8753555555555556 |
| public_source_candidate_pool | ms_marco | Hybrid_Naive | 0.5034282828282828 | 0.8394161616161616 |
| public_source_candidate_pool | ms_marco | Lexical | 0.3759696969696969 | 0.7195515151515152 |
| public_source_candidate_pool | sciq | CogniSync_RRF | 0.9621658339907092 | 0.9645017091769656 |
| public_source_candidate_pool | sciq | Dense | 0.9634893505127532 | 0.982645280042072 |
| public_source_candidate_pool | sciq | Hybrid_Naive | 0.9511175387851696 | 0.9679200631080724 |
| public_source_candidate_pool | sciq | Lexical | 0.928565167849943 | 0.951617144359716 |
| public_source_candidate_pool | squad | CogniSync_RRF | 0.9603019607843136 | 0.9658823529411764 |
| public_source_candidate_pool | squad | Dense | 0.9606901960784314 | 0.9952941176470588 |
| public_source_candidate_pool | squad | Hybrid_Naive | 0.934192156862745 | 0.9731764705882352 |
| public_source_candidate_pool | squad | Lexical | 0.8789372549019607 | 0.939764705882353 |
| synthetic_domain | synthetic_domain | CogniSync_RRF | 1.0 | 1.0 |
| synthetic_domain | synthetic_domain | Dense | 0.8934313725490196 | 1.0 |
| synthetic_domain | synthetic_domain | Hybrid_Naive | 0.8633333333333334 | 1.0 |
| synthetic_domain | synthetic_domain | Lexical | 0.8541176470588235 | 1.0 |

---

## query_type_comparison_public_source_candidate_pool.csv

| System | exact_match | semantic |
| --- | --- | --- |
| CogniSync_RRF | 1.0 | 0.8867654661382044 |
| Dense | 0.986842105263158 | 0.8591946694238612 |
| Hybrid_Naive | 1.0 | 0.8384858406571314 |
| Lexical | 1.0 | 0.7881452122465391 |

---

## context_ablation_final.csv

| Variant | MRR@5 | Recall@5 |
| --- | --- | --- |
| Dense + Appended Generic Context | 0.85309 | 0.96295 |
| Dense + Appended Topical Context | 0.8531566666666668 | 0.96295 |
| Dense + No Context | 0.8534299999999999 | 0.96315 |
| Hybrid + Appended Generic Context | 0.8387933333333333 | 0.9461166666666666 |
| Hybrid + Appended Topical Context | 0.83852 | 0.9457166666666666 |
| Hybrid + No Context | 0.8369533333333333 | 0.94495 |

---

## MASTER_RAW_EVAL_ALL_QUERIES.csv

*Skipped raw/master dump to preserve markdown readability. View CSV directly.*

---

## error_analysis_extended.csv

| query_id | Query | Dataset | Failure Type | Doc in Top-5 |
| --- | --- | --- | --- | --- |
| q_ec96373b313eb89b | definition of vitamin a | ms_marco | Ranking Error | 1 |
| q_836645d4f145d36e | how long does it take to refund on a credit card | ms_marco | Semantic Miss | 0 |
| q_dd570e2f6f9970ff | what is the statue of on the capitol building | ms_marco | Ranking Error | 1 |
| q_378412e3ec9bd065 | what is a depository receipt | ms_marco | Ranking Error | 1 |
| q_05ba8fb32611a0c7 | bona fide occupational qualification meaning | ms_marco | Ranking Error | 1 |
| q_fc2cda1a43e5df81 | what technology is used to detect earthquakes | ms_marco | Ranking Error | 1 |
| q_bc062a37ecd2a8d6 | does aspirin get rid of warts | ms_marco | Semantic Miss | 0 |
| q_2e14861492c3740b | The name of the scientist who coined the term cell for smallest living term | ms_marco | Ranking Error | 1 |
| q_363c431ead40cb4d | Time off in lieu of overtime meaning | ms_marco | Semantic Miss | 0 |
| q_656789d0747c4fb0 | age you can shoot at a firing range in usa | ms_marco | Ranking Error | 1 |
| q_db677a1db9caf62f | what accounting standards does the netherlands use? | ms_marco | Ranking Error | 1 |
| q_6b214bbe2e12bb44 | what does microscopic urinalysis tell you | ms_marco | Ranking Error | 1 |
| q_880c7acc86294908 | What, on the part of a teacher, can result in a decrease in student performance | squad | Semantic Miss | 0 |
| q_816a7892f7541e51 | what is the function of the epithelial tissue | ms_marco | Ranking Error | 1 |
| q_7c1f2a986033285e | the constitutional convention definition | ms_marco | Ranking Error | 1 |
| q_ff893b1ea76964d4 | cost to maintain a reining horse | ms_marco | Ranking Error | 1 |
| q_cb086a279418410c | what is the medication apo amitriptyline used for | ms_marco | Semantic Miss | 0 |
| q_d01ec70d31b04b69 | what does lesion on kidneys mean | ms_marco | Ranking Error | 1 |
| q_d5dec9ab69c03d9f | why did so many psychiatric hospitals close | ms_marco | Ranking Error | 1 |
| q_90dbbb9e695d3bf5 | Another name for the primary visual cortex is | ms_marco | Ranking Error | 1 |
| q_808fcbe4b2f69ab6 | bitumen temperature range | ms_marco | Ranking Error | 1 |
| q_46c5f0d401fed126 | where is kankerbos grown | ms_marco | Ranking Error | 1 |
| q_d0d7c09328354088 | what does the name macy mean | ms_marco | Ranking Error | 1 |
| q_59ea3d703a3b70a5 | what kind of jobs did the anglo saxons have | ms_marco | Semantic Miss | 0 |
| q_21a1c432bc19ebb5 | what are the ingredients in goat milk | ms_marco | Ranking Error | 1 |
| q_618dae44f0e724b9 | what is amyloplast | ms_marco | Ranking Error | 1 |
| q_e1365b8320765996 | What is contained within the polar body? | ms_marco | Semantic Miss | 0 |
| q_05c2cf72e5c4d02e | what degree do you need to be an energy engineer | ms_marco | Ranking Error | 1 |
| q_a8b1f4b82a3af53a | asbestos removal cost estimate | ms_marco | Ranking Error | 1 |
| q_fcc335b36a4cf70d | causes for kidney stones | ms_marco | Ranking Error | 1 |
| q_d2aa754251c32903 | how much to pay for drywall work | ms_marco | Semantic Miss | 0 |
| q_e72228341c2c9518 | what did aristotle believe earth was made of | ms_marco | Ranking Error | 1 |
| q_6c016a8d3f34c681 | what year did color television come out | ms_marco | Semantic Miss | 0 |
| q_afabb5e4bbae7b65 | twitter do tagged people see protected tweets? | ms_marco | Semantic Miss | 0 |
| q_d3988264105f7ba0 | what is a conjun | ms_marco | Ranking Error | 1 |
| q_34ce3730ee68f8b1 | derived trait definition | ms_marco | Ranking Error | 1 |
| q_0ab95112dbbbe455 | meaning of polemic | ms_marco | Ranking Error | 1 |
| q_9be93360fd111e7f | what are NK cells, scientific name | ms_marco | Ranking Error | 1 |
| q_83f7badc75ca029f | how long to cook lamb rack | ms_marco | Ranking Error | 1 |
| q_b2b4bd358a1e3806 | do you have to have a special license to be a plumber virginia | ms_marco | Ranking Error | 1 |
| q_c67d94ede9f53107 | any penalty for transferring roth ira? | ms_marco | Ranking Error | 1 |
| q_f92673d8477081a6 | manufacture uses of silicon dioxide | ms_marco | Ranking Error | 1 |
| q_6756238fedcfdeb3 | what is tcci indicator | ms_marco | Ranking Error | 1 |
| q_d258c9607393fbc3 | how many hours of college does it take to get an associates | ms_marco | Semantic Miss | 0 |
| q_76a5ec76391d72ec | what is a endometrial cyst | ms_marco | Ranking Error | 1 |
| q_00fc49704183db28 | what situations would you give a hypotonic solution? | ms_marco | Ranking Error | 1 |
| q_16a68230fce4ac98 | the cells of living things are composed of a substance called protoplasm | ms_marco | Semantic Miss | 0 |
| q_d19bc64aaedea77c | what is bid rigging in construction | ms_marco | Ranking Error | 1 |
| q_3d2f7311684ae8a1 | does eating when drunk sober you up | ms_marco | Ranking Error | 1 |
| q_d3444ca5d2303209 | what can you use limoncello for | ms_marco | Ranking Error | 1 |
| q_54b124d5ea9e2431 | what is the origin of the name cattermole? | ms_marco | Semantic Miss | 0 |
| q_e803fb6e63148b2d | can naproxen cause blood in urine | ms_marco | Ranking Error | 1 |
| q_98319a7d60af2c73 | what is the food like in greece | ms_marco | Ranking Error | 1 |
| q_f7fffef8ca187383 | In 2007, what was the high end of the salary range? | squad | Semantic Miss | 0 |
| q_69d3a3f3dc2e01dd | what is a phytate | ms_marco | Ranking Error | 1 |
| q_23461388ac2bdedd | is loss of hearing associated with old age | ms_marco | Ranking Error | 1 |
| q_20c20c53729487b3 | how much does a notary house call cost? | ms_marco | Ranking Error | 1 |
| q_257fd05527388f49 | cushing disease is caused by | ms_marco | Ranking Error | 1 |
| q_21e8cb10b59d0e81 | where is Cyt c found in the cell | ms_marco | Ranking Error | 1 |
| q_7afdb5b9b59b4bc2 | where does ermine come from | ms_marco | Ranking Error | 1 |
| q_42a8c3ac28b89334 | what is cbd good for | ms_marco | Ranking Error | 1 |
| q_297a47d76967eea9 | what is normal urine output per hour | ms_marco | Ranking Error | 1 |
| q_56abbaea6e81ff2b | what is hypoglycemia mean | ms_marco | Semantic Miss | 0 |
| q_41597f622b63f8cc | where is oregon located | ms_marco | Ranking Error | 1 |
| q_efcbcae82d204a0c | what type of lava comes out of a cinder cone volcano | ms_marco | Ranking Error | 1 |
| q_3acbb4cd019cf6b7 | what is the average time to cook a pork chops | ms_marco | Ranking Error | 1 |
| q_12df27f30dbd91d0 | is trimethylamine ionic | ms_marco | Ranking Error | 1 |
| q_4241d7486cdd51b5 | how was the first pacemaker made | ms_marco | Semantic Miss | 0 |
| q_2791cd7ec60f098e | what apps can i chromecast | ms_marco | Ranking Error | 1 |
| q_4031ee7fb40161d5 | what is a tawse | ms_marco | Ranking Error | 1 |
| q_b1aaeb4cfde07392 | nitrofurantoin dosage and duration for uti | ms_marco | Ranking Error | 1 |
| q_207c08155b8e8f78 | what are corals made of | ms_marco | Ranking Error | 1 |
| q_71a47eb481650fe0 | What kind of phenotype results in a case of incomplete dominance? | sciq | Semantic Miss | 0 |
| q_df65cf5a85c04619 | statistics on adopting a pet rather than buying | ms_marco | Ranking Error | 1 |
| q_4be537042ea72867 | what does a fractured vertebrae look like? | ms_marco | Ranking Error | 1 |
| q_e03109f443073cfb | how long for food to reach stomach | ms_marco | Ranking Error | 1 |
| q_88e3a96236f1e5af | how quickly can you get pregnant after the implant | ms_marco | Ranking Error | 1 |
| q_11ed145b91b35ebd | how to renew texas cna license | ms_marco | Ranking Error | 1 |
| q_ac280d5549c1e853 | what is normal range for triglycerides | ms_marco | Ranking Error | 1 |
| q_e298f035c9a72bea | how to start gypsophila elegans seeds | ms_marco | Ranking Error | 1 |
| q_f40ae5fafa366c63 | meaning of the name zoey | ms_marco | Ranking Error | 1 |
| q_dc9302356fa3abb1 | define radical chemistry | ms_marco | Ranking Error | 1 |
| q_237fbf49578419ff | how much does the masters payout winnings | ms_marco | Ranking Error | 1 |
| q_f74b3c1fa1ffce8b | dna condenses during what phase | ms_marco | Ranking Error | 1 |
| q_ce048a1b1b39f58f | the greatest relative pressure change in sea water takes place between _____ and _____ meters. | ms_marco | Ranking Error | 1 |
| q_570971b2a7e3e142 | how much does it cost to replace a shingle roof | ms_marco | Ranking Error | 1 |
| q_95c0eda4c36328e8 | what was the sherman antitrust act yahoo | ms_marco | Semantic Miss | 0 |
| q_e61966b7e8aa0901 | The continent with the largest population is __________. | ms_marco | Ranking Error | 1 |
| q_ae4a5043b97529a5 | how long does it take for knee ligaments to heal | ms_marco | Ranking Error | 1 |
| q_85b4f4a089acc120 | where do i see my medicare claims | ms_marco | Ranking Error | 1 |
| q_1552162d141bdc92 | what is a hip pointer | ms_marco | Ranking Error | 1 |
| q_efb6364f109a7fbb | what is the average cost per muscular disorder | ms_marco | Ranking Error | 1 |
| q_0abc42d0f69ebc8e | All chemical changes involve a transfer of what? | sciq | Semantic Miss | 0 |
| q_a053fa1f90e3d266 | which wave is considered a transverse wave? | ms_marco | Ranking Error | 1 |
| q_17ba147afd5e160f | normal wbc count range | ms_marco | Ranking Error | 1 |
| q_4fb6e8de02106d0d | where is madgaon | ms_marco | Ranking Error | 1 |
| q_f8593fbd8b661c54 | how long can a body be refrigerated before burial | ms_marco | Ranking Error | 1 |
| q_336c98a5461358b3 | what is canavan disease | ms_marco | Ranking Error | 1 |
| q_8f9c7c940faff335 | what time of day is the best time to take clear blue digital pregnancy test | ms_marco | Ranking Error | 1 |
| q_0ae35af2f76c9c3f | how tall does a child need to be for a booster seat | ms_marco | Ranking Error | 1 |
| q_ac033af54e6baf12 | how long can a house be pending | ms_marco | Ranking Error | 1 |
| q_72d79a84343d57a0 | what is the blastula | ms_marco | Ranking Error | 1 |
| q_055c3b6c2540a4e0 | have much protein should i take a day | ms_marco | Semantic Miss | 0 |
| q_39294a4d26491c35 | what type of duck is donald duck | ms_marco | Ranking Error | 1 |
| q_9fcdeb7e6eb930f8 | where is pain from gallbladder | ms_marco | Ranking Error | 1 |
| q_59c34e03a4b2974f | what is a loop current | ms_marco | Ranking Error | 1 |
| q_85923b8c8925b541 | types of inverted papilloma sinus | ms_marco | Ranking Error | 1 |
| q_d13a426a9efa1a14 | what is the role of the medial septum in the brain | ms_marco | Ranking Error | 1 |
| q_fb15ce6fe2cf8713 | strep throat contagious period | ms_marco | Ranking Error | 1 |
| q_778e5941aa965922 | is lupus curable | ms_marco | Ranking Error | 1 |
| q_d3c4bf78108508c4 | what is the meaning of Tachyglossus aculeatus | ms_marco | Ranking Error | 1 |
| q_9a2ccc324acfb32d | What are the two components of a mixture called? | sciq | Semantic Miss | 0 |
| q_8f8553fff2d7b2ab | what are coplanar circles | ms_marco | Ranking Error | 1 |
| q_9b23fdb0c702fdd8 | how long can cooked pork be frozen | ms_marco | Ranking Error | 1 |
| q_571c8898679e34c7 | what is the mountain range in european russia | ms_marco | Ranking Error | 1 |
| q_978f1bf2de308eb7 | define telecom international gateways | ms_marco | Ranking Error | 1 |
| q_572fbcff8f5b3a19 | what is gamification in marketing | ms_marco | Ranking Error | 1 |
| q_3d7352a53a067690 | what are the flavonoids | ms_marco | Ranking Error | 1 |
| q_8dce7e39f3f7e301 | where is cleethorpes | ms_marco | Ranking Error | 1 |
| q_1c473e52f4abdc22 | what causes canker sore | ms_marco | Ranking Error | 1 |
| q_75d421af731505ce | what is the usb for blue ray player | ms_marco | Ranking Error | 1 |
| q_52a015250a7a6641 | when did the provisional government fall | ms_marco | Ranking Error | 1 |
| q_a003c43f8b23ee81 | does poppy seed mean mustard seeds | ms_marco | Ranking Error | 1 |
| q_62fcba414e856a5a | cheese brain means | ms_marco | Semantic Miss | 0 |
| q_464e62002d262988 | does tremclad stop rust | ms_marco | Ranking Error | 1 |
| q_411884ae422fbf41 | adhira name meaning | ms_marco | Ranking Error | 1 |
| q_b825941bb2f93928 | what are the characteristics of hurricane | ms_marco | Semantic Miss | 0 |
| q_8c3bd8d19bf6ee3c | estimated cost to become a pharmacy technician | ms_marco | Ranking Error | 1 |
| q_c2066293f0aa10f8 | What spiritual significance does the ganges | ms_marco | Ranking Error | 1 |
| q_c46c807312818864 | who played batman | ms_marco | Ranking Error | 1 |
| q_26747896dea7c65b | how often should dogs urinate | ms_marco | Semantic Miss | 0 |
| q_6fa64535243875fb | how many years to become an accountant | ms_marco | Ranking Error | 1 |
| q_d27a1d6c77801cbd | is a pumice stone the best thing for cracked heels | ms_marco | Ranking Error | 1 |
| q_614943398116c0c2 | are fungi aquatic or terrestrial | ms_marco | Ranking Error | 1 |
| q_36f9a8ca23a47a0f | what good does bamboo symbolize | ms_marco | Ranking Error | 1 |
| q_cfae40f5c2b21bb9 | What part of the plant holds the plant upright? | sciq | Semantic Miss | 0 |
| q_8a2e6183698032d6 | how much digital perm cost | ms_marco | Ranking Error | 1 |
| q_5f0b69b5e42377c0 | Who hosts inside the actors studio | ms_marco | Ranking Error | 1 |
| q_fed3e55b0d2ae593 | what is a neutralization reaction | ms_marco | Ranking Error | 1 |
| q_98ff5526b495782e | what is the function of the lymphatic tissue that is observed throughout the digestive tract | ms_marco | Ranking Error | 1 |
| q_a710569d9f3620a6 | where is salalah | ms_marco | Ranking Error | 1 |
| q_cb08c7d431d6544f | What organ breaks down excess amino acids and toxins in the blood? | sciq | Semantic Miss | 0 |
| q_8207a4534a165f54 | define slogan | ms_marco | Ranking Error | 1 |
| q_6b067d5ec6fa6ba9 | Antibiotic drugs are usually effective in treating what kind of infections? | sciq | Semantic Miss | 0 |
| q_a132390908600290 | who wrote purple rain lyrics | ms_marco | Ranking Error | 1 |
| q_96c07ae7bf72ff75 | where does the name morag originate from | ms_marco | Ranking Error | 1 |
| q_523644a162ad0c7c | what is strategic initiative | ms_marco | Ranking Error | 1 |
| q_5602d128ec912b19 | how do you make graphs in excel | ms_marco | Ranking Error | 1 |
| q_d3439d77869356cc | is a savanna a biome | ms_marco | Semantic Miss | 0 |
| q_4c31df89f7c21c5f | how to get a real estate license in alabama | ms_marco | Ranking Error | 1 |
| q_06dd88e2b9a235e9 | what is RBC in blood test | ms_marco | Ranking Error | 1 |
| q_f184313d4498024e | what kind of economy does china have | ms_marco | Ranking Error | 1 |
| q_1b787a9b4e0fc98c | what is clitoridectomy | ms_marco | Ranking Error | 1 |
| q_5581d07642d05962 | what is manipuri language | ms_marco | Ranking Error | 1 |
| q_47a83a22b52920d3 | how long do you keep your baby in an infant car seat | ms_marco | Ranking Error | 1 |
| q_57573bce863d4e64 | what are the misc files on my phone | ms_marco | Ranking Error | 1 |
| q_9946df00f2942fff | what is dental dam used for | ms_marco | Ranking Error | 1 |
| q_406d8cdff527f7a1 | las olas florida zip code | ms_marco | Ranking Error | 1 |
| q_ed6544894003851a | where is majorca | ms_marco | Ranking Error | 1 |
| q_7a77d894f347f266 | who created the tesla car | ms_marco | Semantic Miss | 0 |
| q_b493f0ca19c44a05 | what are the functions of the neurotransmitters in the human brain | ms_marco | Ranking Error | 1 |
| q_eb8b17052e72070c | describe what happens in terms of electrons when lithium reacts with oxygen | ms_marco | Ranking Error | 1 |
| q_3f266aaca51857d7 | average precipitation in tropical seasonal forest | ms_marco | Ranking Error | 1 |
| q_17c1439e5b2c7126 | what year did the battle of gettysburg take place | ms_marco | Ranking Error | 1 |
| q_7a3efef58beffc82 | why does it say that JFK started affirmative action | ms_marco | Semantic Miss | 0 |
| q_b97c5bf8091b6d73 | what does an overactive immune system mean | ms_marco | Ranking Error | 1 |
| q_befd59457eae029b | sigmoidoscopy preparation | ms_marco | Ranking Error | 1 |
| q_c4236e227c1a5dde | is zirconium oxide toxic | ms_marco | Ranking Error | 1 |
| q_9111c2d8595610dc | larissa name meaning wikipedia | ms_marco | Ranking Error | 1 |
| q_87fa557035cec303 | average temperature in virginia in winter | ms_marco | Ranking Error | 1 |
| q_9ed839c4e343453e | where do joints occur | ms_marco | Ranking Error | 1 |
| q_93be9d7d5872fd09 | how much does it cost to patent an idea | ms_marco | Ranking Error | 1 |
| q_6a35c8c105d7b106 | name meaning of kaylyn | ms_marco | Ranking Error | 1 |
| q_2056128268c4b122 | proteins are synthesized (made) at what organelle in the cytosol | ms_marco | Ranking Error | 1 |
| q_5f5876700d40dc63 | psychology identification examples | ms_marco | Semantic Miss | 0 |
| q_1b5218663dd90e74 | how long to cook pork ribs in oven wrapped in foil to cook fast | ms_marco | Semantic Miss | 0 |
| q_d6710e26affbb06c | which kingdoms have a true nucleus | ms_marco | Ranking Error | 1 |
| q_fff581c4aec86f29 | tartrazine what is it | ms_marco | Ranking Error | 1 |
| q_aec96e539b419c64 | When were Photos First Taken | ms_marco | Ranking Error | 1 |
| q_db3cc280a6aa9bb1 | what age should a dog be spayed | ms_marco | Ranking Error | 1 |
| q_5babaa1a6741e898 | are drawings taxed? | ms_marco | Ranking Error | 1 |
| q_36a6c0d726aa6fec | what type of membrane secretes mucus | ms_marco | Ranking Error | 1 |
| q_49441d17ef1813d7 | what is the nearest point between vancouver island & the mainland | ms_marco | Ranking Error | 1 |
| q_5c65278b87084487 | what is panko made from | ms_marco | Ranking Error | 1 |
| q_18fbb246d391b28d | how long does it take sausages to cook | ms_marco | Ranking Error | 1 |
| q_9a5fc341c2645248 | what is the definition of the name norval | ms_marco | Ranking Error | 1 |
| q_1fe6b66ad4d24da9 | how to get index value of list in collection by passing a value in java | ms_marco | Ranking Error | 1 |
| q_932504b1cd9a7f90 | what made anzac cove so important | ms_marco | Ranking Error | 1 |
| q_568e8553cbd4dac1 | what is potassium nitrate found in | ms_marco | Ranking Error | 1 |
| q_3b670cdf8e77fdde | what makes you an independent student for financial aid | ms_marco | Semantic Miss | 0 |
| q_e1b7d8752199fd05 | how much do attorneys charge to register a trademark | ms_marco | Ranking Error | 1 |
| q_970f02e31e92bb26 | salary of a pilot english money | ms_marco | Ranking Error | 1 |
| q_74514b34da8e8956 | what are scientific uses for carbon | ms_marco | Ranking Error | 1 |
| q_4013375ccecfc03e | Boundary definition | ms_marco | Ranking Error | 1 |
| q_7d7a0596cffffe4e | Who did Emma Marry? | squad | Semantic Miss | 0 |
| q_c21e7cd0011a065b | each state is guaranteed how many representatives what is representation based on | ms_marco | Ranking Error | 1 |
| q_02192c19e389f6c7 | what is mercedes kompressor | ms_marco | Ranking Error | 1 |
| q_c1df520bb58ba838 | average cost for cement driveway and walkway | ms_marco | Ranking Error | 1 |
| q_f734e5cd46ca889e | define clostridium botulinum | ms_marco | Ranking Error | 1 |
| q_b39581ea99d198bf | average to get into harvard | ms_marco | Ranking Error | 1 |
| q_567fe1270c175426 | food borne diseases could be caused by consuming food which contains | ms_marco | Ranking Error | 1 |
| q_84a96b70ed7eeed2 | what determines social security disability | ms_marco | Ranking Error | 1 |
| q_15190176c1e1575e | what is rodelle vanilla | ms_marco | Ranking Error | 1 |
| q_23cc55ac05347d10 | organism that causes paralytic shellfish poisoning | ms_marco | Semantic Miss | 0 |
| q_04c5ef92b7cf722b | where is esophagus located | ms_marco | Ranking Error | 1 |
| q_1be2988f34d551e2 | what does eccentric mean in anatomy | ms_marco | Ranking Error | 1 |
| q_825860327b1f244d | does ketosis damage kidneys | ms_marco | Ranking Error | 1 |
| q_785ea76a0805bc8f | time and temperature to cook pork tenderloin | ms_marco | Ranking Error | 1 |
| q_4083d3c4d5b95254 | why is destination marketing important | ms_marco | Ranking Error | 1 |
| q_235ab84c29e85147 | how long does it take broken glass to decompose | ms_marco | Ranking Error | 1 |
| q_aaaec5322118093b | average cost for cat to be spayed | ms_marco | Ranking Error | 1 |
| q_d3939da53e19870f | female five weeks after birth height | ms_marco | Ranking Error | 1 |
| q_e050b3e754b6e562 | what is pans disease | ms_marco | Ranking Error | 1 |
| q_37d7eae33b5fb707 | what age do a babies need interaction with other babies | ms_marco | Ranking Error | 1 |
| q_b65fa1d54281db5c | what was tom roberts known for | ms_marco | Ranking Error | 1 |
| q_78cc516e6b44f317 | how much do hobby lobby employees make an hour | ms_marco | Ranking Error | 1 |
| q_835a707ccf89210e | what are ornamental plants | ms_marco | Ranking Error | 1 |
| q_b689794a01653177 | what is bluetooth smart | ms_marco | Ranking Error | 1 |
| q_f1ec39876863deb1 | what does potassium mean | ms_marco | Ranking Error | 1 |
| q_d03e9698fc3956a7 | how much does a afghan hound cost | ms_marco | Ranking Error | 1 |
| q_be69fc9deeaed959 | what is towie | ms_marco | Ranking Error | 1 |
| q_4effd757f3f7e9c7 | what are the uses for liquefied natural gas | ms_marco | Ranking Error | 1 |
| q_2d768fbd6d6791fe | what is a sensory homunculus | ms_marco | Ranking Error | 1 |
| q_8989f2ccef245eff | what is as good as a proton pump inhibitor | ms_marco | Ranking Error | 1 |
| q_81164a6625b02fda | where was zama located | ms_marco | Ranking Error | 1 |
| q_0a3c00c81d3dd6f3 | when did the triceratops appear in the fossil record | ms_marco | Ranking Error | 1 |
| q_c877a392abc35714 | what is a desert biome | ms_marco | Ranking Error | 1 |
| q_90b2581bc47dcf98 | why was the commission on civil rights created | ms_marco | Ranking Error | 1 |
| q_530511a905ef2b3b | How much resources were French placing in North America? | squad | Ranking Error | 1 |
| q_7c142b9ade634b99 | where do common spider crabs live | ms_marco | Ranking Error | 1 |
| q_097df1b4f8262a10 | why did charles bukowski write dirty realism' | ms_marco | Ranking Error | 1 |
| q_10c8859af431360d | what is chemical Glyphosate used for | ms_marco | Ranking Error | 1 |
| q_476fc10867e2ff54 | What was the name of Börte's second male child? | squad | Semantic Miss | 0 |
| q_bf020157be9c3a55 | dimensions of a square acre in feet | ms_marco | Ranking Error | 1 |
| q_2f3aba83d13b2d3e | what kind of tick has rocky mountain spotted fever | ms_marco | Ranking Error | 1 |
| q_75de50198a9cbd9a | what are cfl bulbs made of | ms_marco | Ranking Error | 1 |
| q_66b66f2226f146aa | does tadalista work | ms_marco | Ranking Error | 1 |
| q_b76438832cdbbe3d | lancelot definition | ms_marco | Ranking Error | 1 |
| q_790a6be9a4982146 | what legislation was passed due to civil rights movement | ms_marco | Ranking Error | 1 |
| q_16e217aa0a09154d | how to remove white rings from wooden furniture | ms_marco | Ranking Error | 1 |
| q_507d9d035572bd80 | what is the meaning of something inside so strong | ms_marco | Ranking Error | 1 |
| q_170c9370f1af49ce | meaning of LaBlanche name | ms_marco | Ranking Error | 1 |
| q_d50b2a725c8a928f | how to keep keyboard to bottom of screen of acer iconia | ms_marco | Ranking Error | 1 |
| q_ce0f3be3ae9005da | where is the volcano popocatepetl located in mexico | ms_marco | Ranking Error | 1 |
| q_b713a42868bcddfa | what is an accounting convention | ms_marco | Ranking Error | 1 |
| q_1cf438acbfdc0e2e | how long of not getting pregnant should you go to the doctor | ms_marco | Semantic Miss | 0 |
| q_c31b1c289495c1d1 | how to get loose motion | ms_marco | Semantic Miss | 0 |
| q_5cd46fdac8703435 | A polysaccharide that is used for storing energy in human muscle and liver cells is __________. | ms_marco | Ranking Error | 1 |
| q_86bc04d51049f05d | funding fee deductible | ms_marco | Semantic Miss | 0 |
| q_86eaf9ae547f6ab4 | What scale measures acidity? | sciq | Semantic Miss | 0 |
| q_be3b08938e477960 | what is causing school segregation | ms_marco | Ranking Error | 1 |
| q_29d54c33f50ca043 | tattoos cost average | ms_marco | Ranking Error | 1 |
| q_fdae0ecf4aca44cc | what was the number of prisoners in the dachau concentration camp | ms_marco | Ranking Error | 1 |
| q_99ad35823c86225b | what does filament do | ms_marco | Ranking Error | 1 |
| q_14c93ce02c62b2ea | how much per square foot to install acoustical ceiling | ms_marco | Ranking Error | 1 |
| q_ae5917a639185245 | song of joy meaning of name | ms_marco | Ranking Error | 1 |
| q_b278efdece2f5332 | what is food technology | ms_marco | Ranking Error | 1 |
| q_412058db320e0dee | what is bibingka | ms_marco | Ranking Error | 1 |
| q_1aaa4f938670b96e | what is a mcp disease | ms_marco | Ranking Error | 1 |
| q_de553eca9c602b61 | what is the thailand land like | ms_marco | Ranking Error | 1 |
| q_1716c6a0d9ef9cef | what is a trading symbol | ms_marco | Ranking Error | 1 |
| q_6a6f929b1f33e0ff | what is a rita municipality | ms_marco | Semantic Miss | 0 |
| q_24f1612d18289edb | what is the sed rate test | ms_marco | Ranking Error | 1 |
| q_bd9711589b21f6ac | where is marco island florida located | ms_marco | Ranking Error | 1 |
| q_4c8fc2c77ca0a741 | what is the form of the raven | ms_marco | Ranking Error | 1 |
| q_d365bacfabf684f8 | how long does it take the flu to show symptoms | ms_marco | Ranking Error | 1 |
| q_d8e4bfa91e064320 | what is meloxicam for | ms_marco | Ranking Error | 1 |
| q_af73f41a1f6e3c01 | what do I need to notify the social security about naturalization | ms_marco | Ranking Error | 1 |
| q_a3b50dcc98c303e7 | major landforms of the amazon rainforest | ms_marco | Ranking Error | 1 |
| q_8ae280bd9cca0697 | what is the saltatory conduction | ms_marco | Ranking Error | 1 |
| q_6cb80badc425c401 | what is copd disease | ms_marco | Ranking Error | 1 |
| q_0fb5d5c3d1b9a106 | how long does a dog bleed during a heat cycle | ms_marco | Ranking Error | 1 |
| q_4fb9c11a24e64d28 | what are the organs in the muscular system | ms_marco | Ranking Error | 1 |
| q_53650cef3d05c0d2 | what is iberian peninsula | ms_marco | Ranking Error | 1 |
| q_e1e1815fbb8a7582 | What is the name of the group that rats are apart of called? | sciq | Semantic Miss | 0 |
| q_3f9f8575ad3ca195 | meaning of the name darcy | ms_marco | Ranking Error | 1 |
| q_1a10773fd328066a | what is pycnogenol powder | ms_marco | Ranking Error | 1 |
| q_91185722c54daf23 | can you have two dhcp servers in the same site? | ms_marco | Ranking Error | 1 |
| q_3276b5f0c3eaa2cb | Liquid Measurements Metric | ms_marco | Ranking Error | 1 |
| q_789a587892ac539b | what does Claré means | ms_marco | Ranking Error | 1 |
| q_dfc509680964468a | what is dracaena plant | ms_marco | Semantic Miss | 0 |
| q_4c10eabb6c9df346 | What is the total number of codons? | sciq | Semantic Miss | 0 |
| q_05395fed99c8f352 | how long is a ladybug's life cycle | ms_marco | Ranking Error | 1 |
| q_d09f3bc56c860084 | are aries and cancer signs compatible | ms_marco | Ranking Error | 1 |
| q_b91b7f012dab436c | tsavorite meaning | ms_marco | Ranking Error | 1 |
| q_c670200e49b05938 | how to calculate spine of book | ms_marco | Semantic Miss | 0 |
| q_3983ef92910922b0 | can i sue the government in small claims court | ms_marco | Ranking Error | 1 |
| q_94536f6c5573b71d | how to get rid of grey hair naturally at home | ms_marco | Ranking Error | 1 |
| q_a4a5e73caa0efc85 | What was the last name of the designers of Newcastle's library? | squad | Semantic Miss | 0 |
| q_16c9379de46cd2ab | how long does pork last in fridge | ms_marco | Ranking Error | 1 |
| q_69b02210b11d324e | who does the dod oversee | ms_marco | Semantic Miss | 0 |
| q_2635994fdb22bf5e | what was the treaty of tordesillas | ms_marco | Ranking Error | 1 |
| q_b13e9cece590f08b | procedural committee definition | ms_marco | Ranking Error | 1 |
| q_9cad8e3f205db97b | where does translation of rna into proteins occur | ms_marco | Ranking Error | 1 |
| q_06769b02b93fcd0c | is sesame a legume | ms_marco | Ranking Error | 1 |
| q_e6a1c69b42767a26 | the brain is made up of about nerve cells | ms_marco | Semantic Miss | 0 |
| q_b7e93cff3f078689 | harmful effects of microorganisms to plants | ms_marco | Ranking Error | 1 |
| q_2f591f69aaee9fa2 | what part of the brain controls blinking | ms_marco | Ranking Error | 1 |
| q_4e554952e11a8e03 | Thesis, antithesis, synthesis is also known as | ms_marco | Ranking Error | 1 |
| q_1bfeb918ac3fa1ce | what is waste water plant effluent | ms_marco | Ranking Error | 1 |
| q_69fcd2d4d81078dd | is pleurisy contagious | ms_marco | Ranking Error | 1 |
| q_5bbba321156b7adc | do employer rrsp contributions count as income | ms_marco | Ranking Error | 1 |
| q_21009470ce4f401a | what is meter in literature | ms_marco | Ranking Error | 1 |
| q_b8c7f12ad96eb1a1 | what is thyroid eye disease | ms_marco | Ranking Error | 1 |
| q_17592502a69d9ee6 | what are phoenicians in ancient history | ms_marco | Ranking Error | 1 |
| q_ab0b6a10fe70abfc | total carbs per day | ms_marco | Ranking Error | 1 |
| q_ee0c6e26c1db3514 | how much does it cost to change a jetblue flight | ms_marco | Ranking Error | 1 |
| q_967b0081f01a9d83 | what is dimeric | ms_marco | Ranking Error | 1 |
| q_027eca3ae45d9b95 | what is balik ekmek | ms_marco | Ranking Error | 1 |
| q_53a8ad69c970173f | what are alcoholic spirits | ms_marco | Ranking Error | 1 |
| q_b638ae4d2fd15c35 | what is eskrima | ms_marco | Ranking Error | 1 |
| q_6d450e948e457702 | what is avionics | ms_marco | Ranking Error | 1 |
| q_cee0adcf807edb2a | average golden retriever weight | ms_marco | Ranking Error | 1 |
| q_0b8daf9b4b7e4cfb | what is a talus | ms_marco | Ranking Error | 1 |
| q_1dcf6f7908e1ac4b | how is the alveolar structure related to its function | ms_marco | Ranking Error | 1 |
| q_5a9fff773ce0164d | what do sensory nerves do | ms_marco | Ranking Error | 1 |
| q_a103e7fad1bb9ed9 | Is Polyvore a Store | ms_marco | Ranking Error | 1 |
| q_9eea092ef10ed7af | how much is a kitchen remodel | ms_marco | Ranking Error | 1 |
| q_afdd19c163bac126 | bad behaviour in schools statistics | ms_marco | Semantic Miss | 0 |
| q_8e2b77a98f07b0fe | what does multicast querier mean | ms_marco | Ranking Error | 1 |
| q_63360dc7317eee57 | organelle responsible for aerobic cellular respiration | ms_marco | Ranking Error | 1 |
| q_15e3acdeef77ccc2 | how is a cyclone measured | ms_marco | Semantic Miss | 0 |
| q_8423b48bc278d831 | can peanut butter cause migraines | ms_marco | Ranking Error | 1 |
| q_e44e6dcd9e91c62d | concrete cost per yard | ms_marco | Ranking Error | 1 |
| q_6daa3974c785cfc6 | how long does a cat pregnancy last | ms_marco | Ranking Error | 1 |
| q_b8b8430c30ce532c | average us employee salary | ms_marco | Ranking Error | 1 |
| q_72590c9334109e47 | what is antimony pentafluoride used for | ms_marco | Ranking Error | 1 |
| q_202a80fc5e418b55 | can too much orange juice make you sick | ms_marco | Ranking Error | 1 |
| q_e99131b128b06689 | what are geodes | ms_marco | Semantic Miss | 0 |
| q_9aa7aeeade10220f | what is the highest mountain of ireland | ms_marco | Ranking Error | 1 |
| q_c5a5e032760a0009 | how to get spin from a wedge shot | ms_marco | Ranking Error | 1 |
| q_91e6de00331b3a6d | temperature at which gasoline will ignite | ms_marco | Ranking Error | 1 |
| q_f36c15b458fa0f6c | why was archduke shot | ms_marco | Ranking Error | 1 |
| q_b3f529ba7b600a05 | types of technologies used in business | ms_marco | Ranking Error | 1 |
| q_696149f68d69c0bd | how much does a vic check cost | ms_marco | Ranking Error | 1 |
| q_9a07c1dfb1b63d15 | what materials is made of weathered rock | ms_marco | Ranking Error | 1 |
| q_0fff078ff3b5d6a5 | what colors does bougainvillea come in | ms_marco | Ranking Error | 1 |
| q_26f1d3c705fdd9cf | cost to attend GCSU | ms_marco | Ranking Error | 1 |
| q_b830755444d9704f | different types of helminth worms | ms_marco | Ranking Error | 1 |
| q_390b17eb88138960 | what is a mitral valve defect | ms_marco | Semantic Miss | 0 |
| q_1decf1a1d1fb04f9 | cost of gyprocking a house | ms_marco | Ranking Error | 1 |
| q_a76c35046673f1ac | what is parkerized finish | ms_marco | Ranking Error | 1 |
| q_4ca56d0c5f8d2ba3 | temp to bake boneless skinless chicken thighs | ms_marco | Ranking Error | 1 |
| q_94da50cdf720351c | what is the range for normal blood glucose levels | ms_marco | Ranking Error | 1 |
| q_31789a80f35d8821 | what is single malt whisky | ms_marco | Ranking Error | 1 |
| q_e933b84ce6038327 | where are puffins from | ms_marco | Ranking Error | 1 |
| q_635c1086443bf4bb | What fluid is most prevalent in your body? | sciq | Semantic Miss | 0 |
| q_3be6961fbc9f3454 | cystic fibrosis location of genetic cause | ms_marco | Ranking Error | 1 |
| q_a0743d004f40429b | what is a goddess | ms_marco | Ranking Error | 1 |
| q_2c500236e3b97bd5 | what are the causes of shortness of breath | ms_marco | Semantic Miss | 0 |
| q_86f4ae8ead58eac6 | what does an HR coordinator do | ms_marco | Ranking Error | 1 |
| q_bf8de9894e2f5da6 | fan motor cost for air conditioner | ms_marco | Ranking Error | 1 |
| q_a4153c0a9cd2d9af | normal range for triglycerides | ms_marco | Ranking Error | 1 |
| q_dabed742b8a0d9d9 | what are the colors of the Zantedeschia flower | ms_marco | Semantic Miss | 0 |
| q_28a1e6c01c3969bb | what are lacteals | ms_marco | Ranking Error | 1 |
| q_ede5f91f755cf918 | cost to drywall a room | ms_marco | Semantic Miss | 0 |
| q_4bc2f68df962642b | what happens to cookies with too much baking soda | ms_marco | Ranking Error | 1 |
| q_c666bdbf17762866 | what are the major organs in the respiratory system and their functions | ms_marco | Ranking Error | 1 |
| q_5f21402fae8b2865 | when was the rabbit first introduced to australia | ms_marco | Ranking Error | 1 |
| q_70c121a313996e58 | where does graphite come from | ms_marco | Ranking Error | 1 |
| q_ee4cc798d93f5ffe | Who was hired to be the deputy director of the Office of Manned Space Flight? | squad | Ranking Error | 1 |
| q_5d242a7cc8f21297 | what disease is classified hiv | ms_marco | Ranking Error | 1 |
| q_ed1cf2aab2ac16d5 | what is a moonroof | ms_marco | Ranking Error | 1 |
| q_2ef52faa35ff0c1e | how long chicken eggs incubate | ms_marco | Ranking Error | 1 |
| q_bbed692299607143 | Which type of livestock was the argricultural region known for? | squad | Semantic Miss | 0 |
| q_2864f799830ddf5e | what is pravastatin | ms_marco | Ranking Error | 1 |
| q_13fb4938c98c3c68 | where is benidorm the programme filmed | ms_marco | Ranking Error | 1 |
| q_3fc89d48281297f7 | what does soil pollution happen | ms_marco | Ranking Error | 1 |
| q_bd8534199c9b4616 | what do the kidneys do in the digestive system | ms_marco | Ranking Error | 1 |
| q_64101698c6f7d0b2 | dangers of taking wellbutrin | ms_marco | Ranking Error | 1 |
| q_6b911dcd47b595b3 | Who is most likely to be doing formal teaching? | squad | Semantic Miss | 0 |
| q_9a766a8d24a1e712 | where are most cnidarians found | ms_marco | Ranking Error | 1 |
| q_378ac62034502be4 | what are the organisms classified in the phylum chordata | ms_marco | Ranking Error | 1 |
| q_4ccbea6474a52317 | what are nerve reflexes | ms_marco | Semantic Miss | 0 |
| q_f500ad6fa8441ec8 | what tissues are plants covered in | ms_marco | Semantic Miss | 0 |
| q_c1c4232f2467c432 | what is moonshine made of | ms_marco | Ranking Error | 1 |
| q_632790c886b3ad1c | how long cook a baked potato in the oven | ms_marco | Ranking Error | 1 |
| q_e04e3d90e64e22a3 | what is nunavut | ms_marco | Ranking Error | 1 |
| q_dcd2788d1662aa3a | where can the opal stone be found | ms_marco | Ranking Error | 1 |
| q_924ef76ba3eed4fa | What happened to his lab? | squad | Semantic Miss | 0 |
| q_a079f5f91306f807 | what is a birthstone | ms_marco | Ranking Error | 1 |
| q_a05536c5adb58969 | how thick does concrete have to be for a driveway | ms_marco | Semantic Miss | 0 |
| q_e7fe814d7f1c5f15 | what will happen if i put egg in my hair | ms_marco | Ranking Error | 1 |
| q_f693eb84f2769951 | Fractures, rickets, and osteoarthritis all affect what part(s) of the body? | sciq | Semantic Miss | 0 |
| q_88b19efa7e12e210 | salary by job australia | ms_marco | Ranking Error | 1 |
| q_3fab03cc9c14950f | cost to put a child up for adoption | ms_marco | Ranking Error | 1 |
| q_af5c207bd570a9f0 | what do mri detect | ms_marco | Ranking Error | 1 |
| q_dff2b4cf53ac4b5d | why do cells need atp | ms_marco | Semantic Miss | 0 |
| q_e739b6c5e5e1c898 | what could you get with a&p plaid stamps | ms_marco | Ranking Error | 1 |
| q_64583d182596f6d0 | normal creatinine levels in urine | ms_marco | Ranking Error | 1 |
| q_5c7c2f6d1da944dc | calories in a medium pear | ms_marco | Ranking Error | 1 |
| q_a12319c29a32fe94 | what is the biggest rainforest in the world | ms_marco | Ranking Error | 1 |
| q_5d54deef57b02caa | What was Jacksonville referred to as after the consolidation? | squad | Ranking Error | 1 |
| q_f479f02866d0f18c | how long can pizza sit out for | ms_marco | Ranking Error | 1 |
| q_d79a3650ea4d5b4a | facade definition dictionary | ms_marco | Ranking Error | 1 |
| q_7b94230318b7b135 | who is the secretary of state on house of cards | ms_marco | Ranking Error | 1 |
| q_f591ff976308be36 | can leopard geckos dig | ms_marco | Ranking Error | 1 |
| q_bf1d2bda3b7c355a | jehoshaphat name meaning | ms_marco | Ranking Error | 1 |
| q_6f06e0b21ffddddc | What is another term for Tesla's visualization ability? | squad | Semantic Miss | 0 |
| q_ce39c62bea8a79b1 | how long should i keep insurance eobs | ms_marco | Ranking Error | 1 |
| q_efe6a11066ba8417 | where is a earthquake boundary located | ms_marco | Ranking Error | 1 |
| q_15f3d4e5ff4b222d | what are gelatin made of | ms_marco | Ranking Error | 1 |
| q_10abcaba5e88c045 | what does a radiology technician do | ms_marco | Ranking Error | 1 |
| q_92c243403431a8aa | how does the eighth amendment protect prisoners | ms_marco | Ranking Error | 1 |
| q_880aab9b11bd9eb1 | what is csal | ms_marco | Ranking Error | 1 |
| q_923d46d89bbb8275 | can i transplant a conifer tree | ms_marco | Ranking Error | 1 |
| q_b8090f6ee41063f2 | the average intake for carbohydrate daily | ms_marco | Ranking Error | 1 |
| q_1e1c76ade7dbe214 | causes of hepatitis c | ms_marco | Ranking Error | 1 |
| q_d9981b7bdc64f106 | oceanic crust made of | ms_marco | Ranking Error | 1 |
| q_576294885b390f63 | who sang always look on the bright side of life on as good as it gets | ms_marco | Semantic Miss | 0 |
| q_ace1e873e70f9e76 | is the temperate forest soil good | ms_marco | Ranking Error | 1 |
| q_92ceae5acf6d9b2a | chicken pox and incubation period | ms_marco | Ranking Error | 1 |
| q_74989ad155c06f42 | . | code_search_net | Semantic Miss | 0 |
| q_d2e2071d6baf3ec1 | what muscles does deadlift work | ms_marco | Ranking Error | 1 |
| q_0e6bb86d3d24a08f | what is a vitamin c deficiency | ms_marco | Ranking Error | 1 |
| q_a387393894aab360 | frequency modulation maximum deviation | ms_marco | Ranking Error | 1 |
| q_eaa95e1c66e39ac6 | similarities between due process and crime control models | ms_marco | Ranking Error | 1 |
| q_8c85c96cb3ddecf3 | what is bouldering | ms_marco | Ranking Error | 1 |
| q_b7e3103c122dc2ba | is influenza a contagious | ms_marco | Semantic Miss | 0 |
| q_7d2852d8042d1dcb | what liability does a ltd have | ms_marco | Ranking Error | 1 |
| q_351b469e81a9f435 | In what form is most of the earth's freshwater? | sciq | Semantic Miss | 0 |
| q_618244bed34155a0 | Who did Britain exploit in India? | squad | Semantic Miss | 0 |
| q_f8d1be456b37b907 | how long to cook eye round | ms_marco | Ranking Error | 1 |
| q_588029f2791b1c97 | how long does it take a butterfly to fly after hatching | ms_marco | Semantic Miss | 0 |
| q_5bde5931f4dc9a1b | what is lipoflavonoid used for | ms_marco | Ranking Error | 1 |
| q_70a5d7a5432f78c5 | types of wetland ecosystem | ms_marco | Ranking Error | 1 |
| q_8ca9d593b400112b | what is sulphur used for in terms of medicines | ms_marco | Ranking Error | 1 |
| q_3148ae8bc8671fef | what is anomie | ms_marco | Ranking Error | 1 |
| q_e0844e9aeca4e599 | Which bone is derived from the fusion of four very small coccygeal vertebrae? | sciq | Ranking Error | 1 |
| q_e4ba4078252c2c5b | how long for the citizenship process after fingerprints | ms_marco | Ranking Error | 1 |
| q_93ef36718b141952 | Create the distribution instance from a `params` vector. | code_search_net | Ranking Error | 1 |
| q_3215136495f152da | what direction does the spleen do | ms_marco | Ranking Error | 1 |
| q_c99d8424553762a1 | what are cyanobacteria | ms_marco | Ranking Error | 1 |
| q_fd1aefd765983b21 | pga tour texas open field | ms_marco | Semantic Miss | 0 |
| q_d3acc8cf08814ab5 | what distinguishes amino acids | ms_marco | Ranking Error | 1 |
| q_d4595fd045ce5ff5 | what types of materials make good conductors | ms_marco | Ranking Error | 1 |
| q_522d3250dfa243f3 | list of cancers for alcohol | ms_marco | Ranking Error | 1 |
| q_0bed1a4cc6d42344 | what is in a cell | ms_marco | Ranking Error | 1 |
| q_1289889f581c0f87 | what forms does carbon exist in | ms_marco | Ranking Error | 1 |
| q_a7c5cb5e22b141df | how much does it cost to install a garage door | ms_marco | Ranking Error | 1 |
| q_77714b55edf55ccc | what is in poultry seasoning | ms_marco | Ranking Error | 1 |
| q_a69e6913c5e51a6e | what is zana | ms_marco | Ranking Error | 1 |
| q_7348a81f3631a19b | what is tempeh made of | ms_marco | Semantic Miss | 0 |
| q_b2819d63bafcccc9 | what animal is ermine | ms_marco | Ranking Error | 1 |
| q_163742b3e874a986 | average cost of meal in paris | ms_marco | Ranking Error | 1 |
| q_461015d40153ed91 | bad gasoline how to clean carburetor | ms_marco | Ranking Error | 1 |
| q_c6f40d2ac6e7ba04 | what is woolworths known for | ms_marco | Ranking Error | 1 |
| q_19b4cf23ce1595e9 | what kind of wildlife is in Chili | ms_marco | Ranking Error | 1 |
| q_65626b628f325855 | gestation period horses and cows | ms_marco | Ranking Error | 1 |
| q_3f1835f5454b3479 | temp of pork or chicken | ms_marco | Ranking Error | 1 |
| q_147d49b5a2795365 | What is a stromule? | squad | Semantic Miss | 0 |
| q_ab0a2050a1064bb3 | what is garuda purana | ms_marco | Ranking Error | 1 |
| q_9229b3664fe560b5 | What did Tesla work on in 1888? | squad | Ranking Error | 1 |
| q_cfe41898bf41efd8 | where is aconcagua located | ms_marco | Ranking Error | 1 |
| q_0091b59e6d6b94b6 | main purpose of alienation and sedition act | ms_marco | Ranking Error | 1 |
| q_a0259e2760f7fd94 | is candida a bacterial infection | ms_marco | Ranking Error | 1 |
| q_753f619e1b3829a5 | cost of knee replacement after medicare | ms_marco | Ranking Error | 1 |
| q_3d1d0b34eec6030e | how long does it take to get a background check | ms_marco | Ranking Error | 1 |
| q_242638f0a2a1243e | what kind of climate do truffles grow in | ms_marco | Ranking Error | 1 |
| q_b8d8695194cec50e | definition of osseous | ms_marco | Ranking Error | 1 |
| q_431bc57bf393c1f5 | what does an hvac technician do | ms_marco | Ranking Error | 1 |
| q_a96b33f83d53fcb4 | antidepressants side effects table | ms_marco | Ranking Error | 1 |
| q_2c54279153115e89 | where does peppermint come from | ms_marco | Ranking Error | 1 |
| q_3374c722c2541003 | The scientific name of an organism includes the genus and species name | ms_marco | Ranking Error | 1 |
| q_f256bd69d658978c | average college tuition for private college | ms_marco | Ranking Error | 1 |
| q_39474e3c9375e13d | what types of bees pollinate | ms_marco | Ranking Error | 1 |
| q_40ba1eea6470f7a2 | how much do radio presenters earn | ms_marco | Ranking Error | 1 |
| q_32d13d08e0a1d440 | can libraries lend ebooks | ms_marco | Ranking Error | 1 |
| q_e3160e969709cc91 | do plants reduce carbon dioxide | ms_marco | Ranking Error | 1 |
| q_701010b8a1a83797 | what are allspice berries | ms_marco | Ranking Error | 1 |
| q_1b4733cdb5161967 | is europe a continent | ms_marco | Semantic Miss | 0 |
| q_d201ee6878f5f331 | how much can i sell my Golf cart for | ms_marco | Ranking Error | 1 |
| q_5417ac9f963c478f | how early can you start to have maternity benefit | ms_marco | Ranking Error | 1 |
| q_9611a200a13ff6fb | how soon is pregnancy detected in blood | ms_marco | Ranking Error | 1 |
| q_aed51a2c1d61c40d | how much is water per month in an apartment | ms_marco | Ranking Error | 1 |
| q_be839d1f50a98002 | what is hemoglobin | ms_marco | Semantic Miss | 0 |
| q_d96560ff23825f2a | how much do you make in a resort as a massage therapist | ms_marco | Ranking Error | 1 |
| q_e9792bc323308d51 | how often does sdi pay you | ms_marco | Ranking Error | 1 |
| q_f5e2242b71bf1e75 | how many years does it take studying to become an RN | ms_marco | Ranking Error | 1 |
| q_28ac50a922bf1049 | why do my joints hurt when i run | ms_marco | Semantic Miss | 0 |
| q_1ba8090724bd545d | what is the purpose of the indicator | ms_marco | Ranking Error | 1 |
| q_90f42f3df7fe0608 | how to get rid of bacne scars fast | ms_marco | Semantic Miss | 0 |
| q_e327a46bd8b6310f | when was the first harry potter books | ms_marco | Ranking Error | 1 |
| q_f120f150c1ac27b8 | what does androstenedione do | ms_marco | Ranking Error | 1 |
| q_e2b14f40588ca2a2 | how long do chickens live and lay eggs | ms_marco | Ranking Error | 1 |
| q_b36f470d3d75c10b | define agonist muscles | ms_marco | Ranking Error | 1 |
| q_aed2ff08619d112c | internal cost definition | ms_marco | Semantic Miss | 0 |
| q_c60a32749f86c402 | how do we know the mayans were influenced by the olmec | ms_marco | Ranking Error | 1 |
| q_91a73ea9dcbec46e | name the sphincters of the gastrointestinal tract in order | ms_marco | Ranking Error | 1 |
| q_2f1e4887a80a89cd | what is ferroelectric material | ms_marco | Ranking Error | 1 |
| q_e3c8a3b61faffccf | how many americans enrolled in medicare | ms_marco | Ranking Error | 1 |
| q_cafaf0f2565b927d | is cowan a common name | ms_marco | Ranking Error | 1 |
| q_ecca2358d7d2970a | best average temperature in toronto | ms_marco | Ranking Error | 1 |
| q_fe9ab49e1abacdeb | are chemical enzymes mostly made of proteins | ms_marco | Semantic Miss | 0 |
| q_e0da9bb38bd4dc2d | where does biomass energy come from | ms_marco | Ranking Error | 1 |
| q_ed16e3c70d490c17 | what is uncas jewelry | ms_marco | Ranking Error | 1 |
| q_f23b1df44230ebd2 | what does jelani mean in swahili | ms_marco | Ranking Error | 1 |
| q_0fc5449c768b50f3 | wikipedia is a crowdsourcing | ms_marco | Semantic Miss | 0 |
| q_4a0f24fd898b06dd | how has governor rick scott done since being elected? | ms_marco | Ranking Error | 1 |
| q_163ffc0c18843e01 | how to get dead lice eggs out of hair | ms_marco | Ranking Error | 1 |
| q_1a892ee1a8a542c3 | how tall is an average monkey | ms_marco | Ranking Error | 1 |
| q_38f5577c6e2e354f | name a food associated with mexico | ms_marco | Semantic Miss | 0 |
| q_2178cb789d51360f | how much does it cost to live in a nursing home | ms_marco | Ranking Error | 1 |
| q_60b378ecc4d54454 | what breed of pomeranian is boo | ms_marco | Ranking Error | 1 |
| q_a83d44ecfa9b303e | what is gottex | ms_marco | Ranking Error | 1 |
| q_46188df5e1a84e8c | The rising and sinking of these can cause precipitation? | sciq | Semantic Miss | 0 |
| q_36e4bc491f70d07a | benadryl dosage for dogs | ms_marco | Ranking Error | 1 |
| q_6cd21b9b3a92dc69 | how much should a party bus cost to hire | ms_marco | Ranking Error | 1 |
| q_a69996ccc4395002 | what is beta oxidation | ms_marco | Ranking Error | 1 |
| q_c45fbdc6499253eb | what is in azomite | ms_marco | Semantic Miss | 0 |
| q_e18d0d9a511fe856 | what is gaskin maneuver shoulder dystocia | ms_marco | Ranking Error | 1 |
| q_cf0d00674c012042 | what does hypotension mean | ms_marco | Ranking Error | 1 |
| q_cf573fe802cbd199 | what of the population is la pine oregon | ms_marco | Ranking Error | 1 |
| q_ef83303041ba2868 | where does the madagascar hissing cockroach live | ms_marco | Ranking Error | 1 |
| q_f7e3bc82113c45a9 | average salary for orthopedic pa in arizona | ms_marco | Ranking Error | 1 |
| q_87213a3da5e1522a | what is gas giants means | ms_marco | Ranking Error | 1 |
| q_4efefdb02b82a2de | executive committee exco definition | ms_marco | Semantic Miss | 0 |
| q_3d784859579fcd11 | what is glyceryl trinitrate spray used for | ms_marco | Ranking Error | 1 |
| q_7222d55dd3c4ce1b | can you borrow money from an ira | ms_marco | Ranking Error | 1 |
| q_0afc4ea3710ef105 | biblical meaning of the name jovan | ms_marco | Ranking Error | 1 |
| q_f6a1fe41813030ef | who is ulysses s grant | ms_marco | Ranking Error | 1 |
| q_7e2bc58c401a3778 | what river did the comanches hunt in | ms_marco | Ranking Error | 1 |
| q_eaad442a4740d292 | who discovered nitrogen | ms_marco | Ranking Error | 1 |
| q_65cee53d6d601d6d | how much does a pc computer cost | ms_marco | Ranking Error | 1 |
| q_b57c08d5a9c5d4ba | sugars are examples of what type of molecule | ms_marco | Ranking Error | 1 |
| q_6b1c972487a0a4cd | what area is considered east texas | ms_marco | Ranking Error | 1 |
| q_2a535fe9c595ef7d | what states do grizzly bears live in | ms_marco | Ranking Error | 1 |
| q_34b3524d7d629361 | diseases similar to rheumatoid arthritis | ms_marco | Ranking Error | 1 |
| q_09e4f0417425642c | how many miles is the grand canyon from las vegas | ms_marco | Ranking Error | 1 |
| q_9e1f9a413a8bf4ee | what was the pit in the globe theater | ms_marco | Ranking Error | 1 |
| q_c4b15a8b6e647dd2 | Who wrote the eulogy? | squad | Semantic Miss | 0 |
| q_098c0605c20228a5 | what are the average costs of a funeral | ms_marco | Ranking Error | 1 |
| q_f5b0fd22dbf975bf | what is an immunofixation test | ms_marco | Ranking Error | 1 |
| q_e1e545bf239d73f9 | what is an alias name vs preferred name | ms_marco | Ranking Error | 1 |
| q_bd2a32a4356903a8 | what is normal range for creatine | ms_marco | Semantic Miss | 0 |
| q_11553f921c02f5f3 | where is gerdau steel located | ms_marco | Ranking Error | 1 |
| q_3344b0dbc620d20a | what foods do you use capers in | ms_marco | Ranking Error | 1 |
| q_2358cc5e2561e937 | Who is the parent company of NDS? | squad | Semantic Miss | 0 |
| q_06f9a5aa0745baf5 | perirolandic cortex definition | ms_marco | Ranking Error | 1 |
| q_d5d6fc017fd6a108 | what is mycoplasma pneumoniae | ms_marco | Ranking Error | 1 |
| q_0f4f2661a90f9357 | what is pomodoro | ms_marco | Ranking Error | 1 |
| q_06ff0ccc30c11cc7 | model steam engine for marine | ms_marco | Ranking Error | 1 |
| q_eee4c790c5a51566 | what is a gossan | ms_marco | Ranking Error | 1 |
| q_152d42adc7085183 | what branch does spanish come from | ms_marco | Ranking Error | 1 |
| q_45c03205acf58d1c | does starving yourself cause your belly to bloat | ms_marco | Semantic Miss | 0 |
| q_717bb9ae54c92b3e | what county is berkeley ca | ms_marco | Ranking Error | 1 |
| q_56e036dcb5be3060 | what is gold formed in | ms_marco | Ranking Error | 1 |
| q_584a1b642893e140 | Who did he fire? | squad | Ranking Error | 1 |
| q_8537427920564159 | what is in tiger balm | ms_marco | Ranking Error | 1 |
| q_6761461bf3e3383d | how long does it take to fry a pork chop | ms_marco | Ranking Error | 1 |
| q_38bce51572af6e68 | sustainability is also referred to as | ms_marco | Ranking Error | 1 |
| q_331f156192493780 | define processed food | ms_marco | Ranking Error | 1 |
| q_22f7b6d5584f84d0 | what is in the subcutaneous layer of skin | ms_marco | Ranking Error | 1 |
| q_9a77a0b7158a9afc | what is multiplexed | ms_marco | Semantic Miss | 0 |
| q_43b983ec7e0db5cc | what causes infection around the heart | ms_marco | Ranking Error | 1 |
| q_6c4ed2e6d00c7a08 | What type of creature is a scallop? | sciq | Semantic Miss | 0 |
| q_41772d4d9ddcc6cd | how much does it cost to install central heat and air | ms_marco | Ranking Error | 1 |
| q_aa3e4b9445f85406 | are hives itchy | ms_marco | Ranking Error | 1 |
| q_e1a59dce5d3b3505 | how long to stay in oxford for | ms_marco | Ranking Error | 1 |
| q_e8b428ce56cc354b | average length of a golf course | ms_marco | Ranking Error | 1 |
| q_0628a3329350caca | tips for living with knee pain | ms_marco | Ranking Error | 1 |
| q_8c5d4288610fd8c5 | explain why italy was the birthplace of the renaissance | ms_marco | Semantic Miss | 0 |
| q_13c3b367a45f3c3f | what does leptin stimulate | ms_marco | Ranking Error | 1 |
| q_8a7579014b850c43 | arkansas dept of revenue mailing address | ms_marco | Ranking Error | 1 |
| q_8626bfa3a2f15067 | pavers per square foot cost | ms_marco | Ranking Error | 1 |
| q_d37e6b1280b6840a | what does a moth tattoo symbolize | ms_marco | Ranking Error | 1 |
| q_ab0ab571cb49e068 | is barcelona expensive | ms_marco | Ranking Error | 1 |
| q_a8e2d706d2e20c36 | cost to remove mold in home | ms_marco | Ranking Error | 1 |
| q_e2d0ad95d1d602db | how should a chiropractor dress | ms_marco | Ranking Error | 1 |
| q_21fa091d54cd330e | how long should you cook chicken for? | ms_marco | Ranking Error | 1 |
| q_36d3df440476093c | what is a drawout circuit breaker | ms_marco | Ranking Error | 1 |
| q_8cd31017a92a0db9 | standard abbreviation of liters per minute | ms_marco | Ranking Error | 1 |
| q_39fd3e880c6dddbb | the innermost wall of the uterus is called | ms_marco | Ranking Error | 1 |
| q_76141416eb09dbd9 | what form should vitamin a be in | ms_marco | Ranking Error | 1 |
| q_196ba439aa69a7e1 | the substance found in cells which hold the organelles is called | ms_marco | Semantic Miss | 0 |
| q_0a2bcb3467e50404 | is brown algae unicellular or multicellular | ms_marco | Ranking Error | 1 |
| q_1af359d958ebfa86 | are there nucleolus in plant cells | ms_marco | Ranking Error | 1 |
| q_cf5f5cb868aef2d2 | what is cost to stain a deck | ms_marco | Ranking Error | 1 |
| q_88ebdbae08c8a58f | where does lavender grow in the world | ms_marco | Ranking Error | 1 |
| q_0854e1b2329846d9 | cost of split system heating | ms_marco | Ranking Error | 1 |
| q_8412b3e8d1f5fe21 | what is a rosin | ms_marco | Ranking Error | 1 |
| q_fd7bee4d66187864 | how long does it take a dead ipod to charge | ms_marco | Ranking Error | 1 |
| q_de0f4710bef0e224 | is chobani publicly traded | ms_marco | Ranking Error | 1 |
| q_45680c3ef47583d6 | what is grewia asiatica | ms_marco | Ranking Error | 1 |
| q_99274b74fa7614fd | artridol what is | ms_marco | Ranking Error | 1 |
| q_e8f3c6895156047e | what is a PICO | ms_marco | Ranking Error | 1 |
| q_f75781a780ff0cef | is it safe to be induced at the hospital | ms_marco | Ranking Error | 1 |
| q_9dad2cea0eb4debc | how long does a steam burn take to heal | ms_marco | Ranking Error | 1 |
| q_afabf61197639c75 | how much does an acupuncturist earn in australia | ms_marco | Ranking Error | 1 |
| q_f899890e817bed84 | Who was Emma's brother? | squad | Semantic Miss | 0 |
| q_dad63d0f59e10f46 | potassium deficiency hereditary | ms_marco | Ranking Error | 1 |
| q_5fb4128865a639e5 | is there an age limit to play college sports | ms_marco | Ranking Error | 1 |
| q_d2e8d72b732ae426 | the meanings of vowel | ms_marco | Ranking Error | 1 |
| q_2d4172f3d1da9951 | how to add symbol to font | ms_marco | Ranking Error | 1 |
| q_bd5415f6aab35a05 | what is staph microbiology | ms_marco | Ranking Error | 1 |
| q_3463617dfa6de02a | dna definition bitesize | ms_marco | Ranking Error | 1 |
| q_4ebe06d256bf8183 | what are meristem cells | ms_marco | Ranking Error | 1 |
| q_6c69327bc4fedbe8 | what is buspirone used for | ms_marco | Ranking Error | 1 |
| q_1c1d87fd0070265a | how much is football retirement | ms_marco | Ranking Error | 1 |
| q_9e805d5789a88d5e | what is xylem and phloem | ms_marco | Ranking Error | 1 |
| q_9310889f0591cf64 | Ash that enters the air naturally as a result of a volcano eruption is classified as what kind of pollutant? | sciq | Semantic Miss | 0 |
| q_cb61f56645744a77 | is ginkgo biloba good for vertigo | ms_marco | Semantic Miss | 0 |
| q_5863aa186cf6e247 | how long to cook a whole turkey | ms_marco | Ranking Error | 1 |
| q_5bb7a108ffcb7dfe | how to be a radiologist | ms_marco | Ranking Error | 1 |
| q_3de54d722e181348 | what does te puni kokiri do | ms_marco | Ranking Error | 1 |
| q_42a2858469b59128 | cost for issuetrak | ms_marco | Semantic Miss | 0 |
| q_d5ca5e545fca6571 | when did gatorade come out | ms_marco | Ranking Error | 1 |
| q_e9b8b115df738201 | why is st helens called bay of fire | ms_marco | Ranking Error | 1 |
| q_877cfcd3598679cc | what is phosphate buffer | ms_marco | Ranking Error | 1 |
| q_f676f7fdbbbec776 | where does Sodium chloride come from | ms_marco | Ranking Error | 1 |
| q_f12c0723266606b5 | will a knock sensor cause a car to lose power | ms_marco | Ranking Error | 1 |
| q_956ef849c5c47fc6 | what is russia known for | ms_marco | Semantic Miss | 0 |
| q_4e5badbd889b6933 | what is hoarse | ms_marco | Ranking Error | 1 |
| q_11fa5bbcfc2781cf | when should cabbage seeds be planted | ms_marco | Ranking Error | 1 |
| q_3910ce88f9555601 | do you have to be smart to be an ultrasound tech | ms_marco | Ranking Error | 1 |
| q_606252ce09c84af6 | what does the enzyme alpha amylase do | ms_marco | Ranking Error | 1 |
| q_ee29d6c364634b81 | salary of import and export in usa | ms_marco | Ranking Error | 1 |
| q_69309b980dd9fcbe | what is chemotaxis | ms_marco | Ranking Error | 1 |
| q_eda13613bd4df609 | how do you calculate the percentage of freight on a shipment? | ms_marco | Ranking Error | 1 |
| q_1280b20419223df2 | cost of cartier lighter overhaul | ms_marco | Ranking Error | 1 |
| q_1c502a25fe6aa398 | how does ira work | ms_marco | Ranking Error | 1 |
| q_1cc987bc047deeb9 | cost to remove skin tags | ms_marco | Ranking Error | 1 |
| q_950c0c707e8ddb91 | what is wind mitigation | ms_marco | Ranking Error | 1 |
| q_d4ee8d86145d6a8d | how much does it cost to join the masters golf club | ms_marco | Ranking Error | 1 |
| q_b267df3ddd65f2f5 | when was mansa musa born | ms_marco | Ranking Error | 1 |
| q_548caa2c53a3d548 | average electricity bill per month | ms_marco | Ranking Error | 1 |
| q_371517da3fb57f59 | what does mange tout mean | ms_marco | Ranking Error | 1 |
| q_647ecb4d16c0b569 | is cystic fibrosis genetic | ms_marco | Ranking Error | 1 |
| q_edeb8142b5ee95f6 | what is the gulo gene | ms_marco | Ranking Error | 1 |
| q_5d2a0a35f76ac9a2 | does it hurt a baby to be born | ms_marco | Ranking Error | 1 |
| q_60f8860c1f8a1bad | what is nre account | ms_marco | Ranking Error | 1 |
| q_7714d12551090cb2 | what is map projection | ms_marco | Ranking Error | 1 |
| q_afa64e25cda0a8b0 | how long does it take to qualify for a home loan | ms_marco | Ranking Error | 1 |
| q_9ff42e631e0ff5d0 | how much does average canadian make | ms_marco | Ranking Error | 1 |
| q_aef185bf16ab22d9 | should i buy an extended warranty on a new car | ms_marco | Ranking Error | 1 |
| q_b229741bd4d707bf | average temperature in side turkey in may | ms_marco | Semantic Miss | 0 |
| q_1e1ac6bc7c047981 | what is prilocaine | ms_marco | Ranking Error | 1 |
| q_8cc39616456a7482 | what region is cambridge in | ms_marco | Ranking Error | 1 |
| q_cf9a5a082e5dd84b | average household electricity consumption ontario | ms_marco | Semantic Miss | 0 |
| q_937e4354d8bf45f9 | what is a sentient beings | ms_marco | Ranking Error | 1 |
| q_bb0769a8f7bb7adf | what is average cost for replacement windows | ms_marco | Ranking Error | 1 |
| q_4df9281ba5e6d223 | what is an mri | ms_marco | Ranking Error | 1 |
| q_781ac1145defe4e8 | cat repellent that is safe for dogs | ms_marco | Ranking Error | 1 |
| q_d898f63ef06b5b39 | what is slander law | ms_marco | Ranking Error | 1 |
| q_a2274b041eb981ec | how do i tie out my prior year retained earnings | ms_marco | Ranking Error | 1 |
| q_05fc52a30abb9c93 | wheel bearing replacement cost | ms_marco | Ranking Error | 1 |
| q_65530da25f837329 | meanings of the name lauren | ms_marco | Ranking Error | 1 |
| q_ee0abfef967b129c | average salary first year lawyer | ms_marco | Ranking Error | 1 |
| q_41fe202077973a42 | dna replication what is a replication fork | ms_marco | Ranking Error | 1 |
| q_da1f565fc63e2c45 | what is naive | ms_marco | Ranking Error | 1 |
| q_3428b66ed43d6d87 | where did Arabic come from | ms_marco | Ranking Error | 1 |
| q_258c4a1e0f08c495 | what is a girder | ms_marco | Ranking Error | 1 |
| q_3e9fa4539fc08103 | where did henry lawson grow up | ms_marco | Semantic Miss | 0 |
| q_905b9dc8a568f8a7 | average cost australian terrier | ms_marco | Ranking Error | 1 |
| q_68a485bdc099db72 | where are lungs located in your back | ms_marco | Ranking Error | 1 |
| q_26c2adf26c9b7bef | is a yucca moth a plant | ms_marco | Ranking Error | 1 |
| q_1fd60bb0bf8e534a | are possums nocturnal | ms_marco | Ranking Error | 1 |
| q_92b08f99a66adfb9 | what is celtic salt | ms_marco | Ranking Error | 1 |
| q_ff3c96041a6c8969 | quarterly state taxes virginia due date | ms_marco | Ranking Error | 1 |
| q_85b844660dd2c16b | what is a transistor composed of | ms_marco | Ranking Error | 1 |
| q_bc4faf27368b2793 | what nationality is jennifer lopez | ms_marco | Ranking Error | 1 |
| q_f18d5b8766539206 | what is a furuncle boil | ms_marco | Ranking Error | 1 |
| q_1c732aa2186eb00e | telecheck customer service phone number | ms_marco | Ranking Error | 1 |
| q_5dba40d6bbf2a440 | what is another name for skeletal muscle tissue | ms_marco | Ranking Error | 1 |
| q_67c495f9a517f706 | blanchard name meaning | ms_marco | Ranking Error | 1 |
| q_6f75064af75b1da2 | The average number of individuals per unit of area or volume is referred to as a population's what? | sciq | Ranking Error | 1 |
| q_818a1588f9a5fdc8 | where can koalas be found | ms_marco | Ranking Error | 1 |
| q_a8714a8d5ef80492 | average decor cost for wedding | ms_marco | Ranking Error | 1 |
| q_43b17e571c061361 | How much money was spent on other festivities in the Bay area to help celebrate the coming Super Bowl 50? | squad | Ranking Error | 1 |
| q_aae9de1397fcde48 | delta airlines cancellation fee | ms_marco | Ranking Error | 1 |
| q_435f67c17912aa84 | why is kodiak island historical | ms_marco | Ranking Error | 1 |
| q_094cd4c68cff2042 | factors that affect the cause of chickenpox | ms_marco | Ranking Error | 1 |
| q_60500c0bd3c06473 | what is the function of the orbicularis oculi | ms_marco | Ranking Error | 1 |
| q_030825fa13f0f01f | To where were the belongings taken? | squad | Semantic Miss | 0 |
| q_14e5398d624f147f | how long do chickens lay eggs | ms_marco | Ranking Error | 1 |
| q_dc322b4bdba22f39 | are quarks made of other particles | ms_marco | Ranking Error | 1 |
| q_8ccbccf0142ce615 | what is brooklands museum | ms_marco | Ranking Error | 1 |
| q_7df2f62ebd6cb502 | what minerals are in oatmeal | ms_marco | Ranking Error | 1 |
| q_5eeb3eab33b028e9 | what is meant by phonetics | ms_marco | Ranking Error | 1 |
| q_3dd88f6b81cda25b | Where does photosynthesis occur in plants? | sciq | Semantic Miss | 0 |
| q_2cd3b959e687e641 | what does pb mean | ms_marco | Ranking Error | 1 |
| q_53820005894d018c | what diabetes use for treatment options | ms_marco | Ranking Error | 1 |
| q_2bd3029ffb07ded1 | pronounce balance | ms_marco | Ranking Error | 1 |
| q_502befb3a3c76690 | size of the sun compared to earth | ms_marco | Ranking Error | 1 |
| q_0787ad822e84ebf2 | positive feedback homeostasis definition | ms_marco | Ranking Error | 1 |
| q_016d63d621007e13 | what is geritol | ms_marco | Ranking Error | 1 |
| q_a51b121daf103432 | cost of a electrician | ms_marco | Ranking Error | 1 |
| q_7c81fb73c1023860 | can rotation rack costco | ms_marco | Ranking Error | 1 |
| q_aa8b5f85c03e5dfc | what properties do lithium and francium have in common? | ms_marco | Ranking Error | 1 |
| q_c244265923cb4b90 | what does ankh symbol mean | ms_marco | Ranking Error | 1 |
| q_4611255b014f79f1 | can you purchase your own custom sports duvet cover | ms_marco | Ranking Error | 1 |
| q_6bea2bcb6077c1bc | how long to cook spaghetti squash in microwave | ms_marco | Ranking Error | 1 |
| q_4c7958e6d9d8457b | What is the name of the mineral that contains calcium, carbon and oxygen? | sciq | Semantic Miss | 0 |
| q_9f3837aeb33d629c | dna melting temperature | ms_marco | Ranking Error | 1 |
| q_eccdedddff2d148c | what is a cipher | ms_marco | Ranking Error | 1 |
| q_9106fcd51de1efc0 | policy analyst define | ms_marco | Ranking Error | 1 |
| q_7fdfcd894c0569ae | common extensor tendon origin and insertion | ms_marco | Ranking Error | 1 |
| q_de0e9b8b6692a746 | is it best to withdraw from college before being expelled | ms_marco | Ranking Error | 1 |
| q_3d915e627539644a | where are lipids digested | ms_marco | Semantic Miss | 0 |
| q_ed2e1b1d8f6d7e5e | why does a dog chew on a stick | ms_marco | Ranking Error | 1 |
| q_033d0bfefdecff00 | styx songs | ms_marco | Ranking Error | 1 |
| q_0af3fb1cb219d9ce | cost install inground pool | ms_marco | Ranking Error | 1 |
| q_b99136dc51c85ab2 | metastatic cancer lymph nodes symptoms | ms_marco | Ranking Error | 1 |
| q_57ae273c93a750d9 | what is mediterranean food | ms_marco | Ranking Error | 1 |
| q_15084a9d3edd41ee | where can i sell my baby stuff pensa | ms_marco | Ranking Error | 1 |
| q_9e2a025ca5dcc743 | average salary non invasive cardiologist | ms_marco | Ranking Error | 1 |
| q_2dce8604b0a3eacb | how long do beta fish live | ms_marco | Semantic Miss | 0 |
| q_9bda5dd6561db323 | how long does it take to recover from alcohol addiction | ms_marco | Ranking Error | 1 |
| q_2a87d726875f9df8 | what are ribosomes composed of | ms_marco | Ranking Error | 1 |
| q_babc28b0ec7b1f61 | Walmart hours silver city | ms_marco | Ranking Error | 1 |
| q_4503a5e321e34a60 | pnf stretching golgi tendon organ | ms_marco | Ranking Error | 1 |
| q_36c0f294ce10149b | cost of cremation cost of burial | ms_marco | Ranking Error | 1 |
| q_8d84961246347a4f | what are the different types of phenotypes | ms_marco | Ranking Error | 1 |
| q_0971c1890c186c0f | Recommended serving size of fish per person | ms_marco | Ranking Error | 1 |
| q_c604287848d5244e | how much do medical examiners make | ms_marco | Ranking Error | 1 |
| q_26cf80fc229f7678 | what is omics | ms_marco | Ranking Error | 1 |
| q_ec70dbd2cdad5fd1 | what is gme in dogs | ms_marco | Ranking Error | 1 |
| q_d4d54714ff20f58e | what should a normal heart rate be | ms_marco | Ranking Error | 1 |
| q_dd56cf9f6c9c710b | how many marijuana plants can you legally grow in riverside county california | ms_marco | Ranking Error | 1 |
| q_bd1a18d02f073017 | what is the emperor penguin habitat | ms_marco | Ranking Error | 1 |
| q_f88885deaa6b8f4b | similarities between humans and chimpanzees | ms_marco | Ranking Error | 1 |
| q_f880d5d9a8638907 | what is iron steel used for | ms_marco | Ranking Error | 1 |
| q_a0b5ad69d13ff0a9 | what medications are opiates | ms_marco | Ranking Error | 1 |
| q_c216130681baabab | what defines density | ms_marco | Ranking Error | 1 |
| q_d8f1ea6d187b1eb0 | what are the only multicellular protists | ms_marco | Ranking Error | 1 |
| q_e89cc468ffb87fdd | act psychology definition brentano | ms_marco | Ranking Error | 1 |
| q_31f6a52ea8452d27 | how long to cook a boneless lamb leg | ms_marco | Semantic Miss | 0 |
| q_42e324907cccea6b | shingles roofing cost | ms_marco | Ranking Error | 1 |
| q_3fdc2b84828f291d | what preacher's name is lester felty | ms_marco | Ranking Error | 1 |
| q_5b1045a20074cc64 | where does insulin come from | ms_marco | Ranking Error | 1 |
| q_2b7cf26a313bbd37 | define responsible government | ms_marco | Ranking Error | 1 |
| q_f81644cfc15dbdd2 | how long for a chicken to mature | ms_marco | Ranking Error | 1 |
| q_c6cd5ed06b8ea3b5 | which bonds are created during the formation of the primary structure of a protein? | ms_marco | Ranking Error | 1 |
| q_e3d5d3c5f3f747b3 | what language is spoken in switzerland | ms_marco | Semantic Miss | 0 |
| q_99215e400940faf0 | when was the walt disney company founded | ms_marco | Ranking Error | 1 |
| q_19eeca140a4c12f1 | what part of a vaccine stimulates an immune response | ms_marco | Ranking Error | 1 |
| q_0e766e305a8c27a6 | what is a characteristic of cellulose | ms_marco | Ranking Error | 1 |
| q_69f62d075aa5a324 | What does the kyoto protocol focus on controlling? | sciq | Semantic Miss | 0 |
| q_3b38c6827872ef13 | how long does a bad account stay on your credit report | ms_marco | Ranking Error | 1 |
| q_c57f12e5cefeffeb | what sport is good muscular endurance | ms_marco | Ranking Error | 1 |
| q_d1cb2ada1d53f68a | what geological processes is important in the formation of soil and sedimentary rock | ms_marco | Ranking Error | 1 |
| q_07326bd438ee3bdb | cost for total bath renovation | ms_marco | Ranking Error | 1 |
| q_1de301f606f8725f | salary it manager desktop support | ms_marco | Ranking Error | 1 |
| q_626bb44fea2a790d | personal service provider definition | ms_marco | Ranking Error | 1 |
| q_d0384942a6519f89 | average annual salary for a teacher | ms_marco | Ranking Error | 1 |
| q_23a1e830d6764651 | what continent is israel in | ms_marco | Semantic Miss | 0 |
| q_8c873ca8d616adbe | what is payee account | ms_marco | Ranking Error | 1 |
| q_23ab9013906e3763 | How many intercpetions did Newton have in Super Bowl 50? | squad | Semantic Miss | 0 |
| q_53e9a010ffb7dbff | calcitonin secreted by what cells | ms_marco | Ranking Error | 1 |
| q_ec5efaa3dc6ebddc | how much does laser treatment for broken capillaries cost | ms_marco | Ranking Error | 1 |
| q_06f7dd3793ba8c58 | why was san luis obispo built | ms_marco | Ranking Error | 1 |
| q_d6401936c5ef182a | what is an emg study | ms_marco | Ranking Error | 1 |
| q_e1f327581c2abb79 | what are exports of sweden | ms_marco | Ranking Error | 1 |
| q_76d6a6b858434523 | what is a winged lion called | ms_marco | Ranking Error | 1 |
| q_71f1f9fec0ee26ba | What will spores that eventually germinate develop into? | sciq | Semantic Miss | 0 |
| q_32921acfae355920 | can crohn's cause weight loss | ms_marco | Semantic Miss | 0 |
| q_c413822fbd4aec9f | A bicycle is an example of a compound machine made of many what? | sciq | Semantic Miss | 0 |
| q_a50849fa493b1cce | what is the name of the one that comes before undergraduate | ms_marco | Ranking Error | 1 |
| q_43ac8de0bf4bbf17 | what is soccer called in brazil | ms_marco | Ranking Error | 1 |
| q_4d1972d2aca863d2 | what does the nucleus basalis do | ms_marco | Semantic Miss | 0 |
| q_9a9b709f08b5692a | when was the first compass invented | ms_marco | Ranking Error | 1 |
| q_88f2f50e827a0982 | i never was a killing type lyrics | ms_marco | Ranking Error | 1 |
| q_cba2675041389cf4 | cost to reside a house in vinyl | ms_marco | Ranking Error | 1 |
| q_9108d03f34ea8d21 | Which is a nonvascular seedless plant? | ms_marco | Ranking Error | 1 |
| q_4c84a62c75846ef1 | what is intergovernmental relations | ms_marco | Semantic Miss | 0 |
| q_16a802b0080d1a15 | define malarkey | ms_marco | Ranking Error | 1 |
| q_49d6171d7eae82ef | Electromagnetic specturm is the full spectrum of raidant energy, which is energy emitted and transmitted as what? | sciq | Semantic Miss | 0 |
| q_6c50c0b484bd73f9 | word meaning predation | ms_marco | Ranking Error | 1 |
| q_89172f6030cafd4a | average square foot cost of modular home | ms_marco | Ranking Error | 1 |
| q_f2da55ac50b953b4 | How many chambers are in a reptiles heart? | sciq | Semantic Miss | 0 |
| q_ab7cb19631267c37 | what is fiber reinforced polymer | ms_marco | Ranking Error | 1 |
| q_1fb5287bedb34900 | causes of pain in elbow area | ms_marco | Ranking Error | 1 |
| q_99c5a9ced67bdcbe | difference between osteo and rheumatoid arthritis | ms_marco | Ranking Error | 1 |
| q_99a3ec924c0de097 | cost to store furniture | ms_marco | Semantic Miss | 0 |
| q_0cdff5bfd16bfd68 | parasympathetic division definition | ms_marco | Ranking Error | 1 |
| q_0e064ae9086d2707 | what is rootkit scan | ms_marco | Ranking Error | 1 |
| q_88ffb1810e511d4f | What is the name of the water body that is found to the east? | squad | Semantic Miss | 0 |
| q_f2812e7b0b16f3d8 | can you make money as a notary signing agent | ms_marco | Ranking Error | 1 |
| q_78993fa87e623164 | where is budapest located on a world map | ms_marco | Ranking Error | 1 |
| q_a8201d0ee3796c28 | how many calories do you burn in an insanity workout | ms_marco | Ranking Error | 1 |
| q_78f16ca80def2575 | why does my gas pedal keep sticking | ms_marco | Ranking Error | 1 |
| q_b8e0406f11b440b2 | cholesterol in shrimp good or bad | ms_marco | Ranking Error | 1 |
| q_350fedfe8b9a04fd | how do turkeys attract mates | ms_marco | Ranking Error | 1 |
| q_020e0bca3386d960 | what are the unique characteristics of kingdom fungi | ms_marco | Ranking Error | 1 |
| q_84b9e6d0bf9e1082 | docstring for main | code_search_net | Semantic Miss | 0 |
| q_10a52316bd0401a2 | causes of lymphopenia | ms_marco | Ranking Error | 1 |
| q_d83d4a8478e32a50 | what is a hamsa hand | ms_marco | Ranking Error | 1 |
| q_9fc83557dac58587 | The inside of a ctenophore is lined with what? | squad | Ranking Error | 1 |
| q_1ad9272e89b48e04 | what is cla | ms_marco | Ranking Error | 1 |
| q_d2e4104f952b3b13 | What is the balance for positive reinforcement? | squad | Semantic Miss | 0 |
| q_d1ec0b013578e85c | what is an object pronoun | ms_marco | Ranking Error | 1 |
| q_89aa2e8a57119947 | how do property managers charge | ms_marco | Semantic Miss | 0 |
| q_96177e1c9b154a04 | where is the three finger jack monument located | ms_marco | Ranking Error | 1 |
| q_4bb63c76c79e4fca | when did china become unified | ms_marco | Ranking Error | 1 |
| q_499e754e668633aa | what is a shanty town | ms_marco | Ranking Error | 1 |
| q_f609e4da9ef486aa | does peanuts cause arthritis | ms_marco | Ranking Error | 1 |
| q_80aefb3a0ce66af7 | define significant | ms_marco | Ranking Error | 1 |
| q_afe6e3a26fcd570f | ideal clone temp | ms_marco | Ranking Error | 1 |
| q_a55062683cc493e8 | when was the first picture of earth called earthrise taken | ms_marco | Ranking Error | 1 |
| q_fc9b9e5f21279c3f | what is a cluster headache | ms_marco | Ranking Error | 1 |
| q_c39858e391ecd6e0 | how do you say bounded | ms_marco | Ranking Error | 1 |
| q_5b973a8b6b6d4f87 | average age of women who get married | ms_marco | Ranking Error | 1 |
| q_d54b292254b71d83 | what is donburi | ms_marco | Ranking Error | 1 |
| q_05880927ea54a0c3 | what does a company treasurer do | ms_marco | Ranking Error | 1 |
| q_c2be7817975ba8ba | what is normal heartbeat | ms_marco | Ranking Error | 1 |
| q_858a23c471359108 | what province is paris in | ms_marco | Ranking Error | 1 |
| q_2ad4a53334c310c4 | how much protein should a woman have each day | ms_marco | Ranking Error | 1 |
| q_4ef5cf871ca970fd | how to set up printing to onenote | ms_marco | Ranking Error | 1 |
| q_3d574b56ab9c4b28 | what is public health model | ms_marco | Ranking Error | 1 |
| q_56cc6b5db5848eaf | swimming pool cost to build cost to fill in ground | ms_marco | Ranking Error | 1 |
| q_8d0d3b9823e6ab16 | when was delta airlines founded | ms_marco | Ranking Error | 1 |
| q_5d78de6d854592c7 | recommended pool temperature for lap swimming | ms_marco | Ranking Error | 1 |
| q_623b3eaa003dda15 | what is a state surveyor | ms_marco | Ranking Error | 1 |
| q_8a80feb50c3301f6 | can you buy a hat band to make a hat fit that is too small | ms_marco | Semantic Miss | 0 |
| q_aeb37952285c607f | The mars rover collected round clumps of crystals that, on earth, usually form in what? | sciq | Semantic Miss | 0 |
| q_79262451d9c2cc43 | what are the function of the lymphatic vessels | ms_marco | Ranking Error | 1 |
| q_cc842fabd2ff9c9b | how long do cardinal babies stay in nest | ms_marco | Ranking Error | 1 |
| q_d348f7b3229fce5e | A gene is usually __________. | ms_marco | Ranking Error | 1 |
| q_749987bc0434b4cc | how long do french lace hydrangea | ms_marco | Ranking Error | 1 |
| q_4d5389aea69da51a | what medications does lyrica interact with | ms_marco | Ranking Error | 1 |
| q_569a16254ab70ec7 | what is doxycycline | ms_marco | Ranking Error | 1 |
| q_069f8a2e1bee6677 | How long does it take to recover from a colonoscopy and endoscopy? | ms_marco | Ranking Error | 1 |
| q_c39d825faeb6804a | is spousal support in new york based on gross or net income | ms_marco | Ranking Error | 1 |
| q_b12eca3ebc2f8abb | pixelmon what level does pikachu evolve | ms_marco | Semantic Miss | 0 |
| q_a5bd8969ff5d2dbe | What do all respiratory diseases affect? | sciq | Semantic Miss | 0 |
| q_c4f0ec55b1e8982f | what is a mind muscle connection | ms_marco | Ranking Error | 1 |
| q_842140bf738be262 | length of time you have to wear a cast for a broken leg | ms_marco | Ranking Error | 1 |
| q_92bbec9b832df76a | where does chyme form in the stomach | ms_marco | Semantic Miss | 0 |
| q_d8343e11e714ecc5 | what kind of spectrums are there | ms_marco | Semantic Miss | 0 |
| q_001892ef7228da91 | what layer of the atmosphere does ozone depletion occur | ms_marco | Ranking Error | 1 |
| q_d8276fda9ea2aa4b | is honeydew healthy | ms_marco | Ranking Error | 1 |
| q_a1741181c3940224 | grassland ecosystem where in the world is it | ms_marco | Ranking Error | 1 |
| q_fbbd2cad193e0110 | how long to cook fresh fish in oven | ms_marco | Ranking Error | 1 |
| q_d4472c71bd2a91a4 | Alkynes are what type of compound? | sciq | Semantic Miss | 0 |
| q_4d1ecd93984b2b61 | what is an equalization rate | ms_marco | Ranking Error | 1 |
| q_37a240a67c44be0a | what is mediator software | ms_marco | Ranking Error | 1 |
| q_892d2ed66b19259e | who did the early christian persecution | ms_marco | Ranking Error | 1 |
| q_ee555265bb603e41 | what is the scientific word for sugar | ms_marco | Semantic Miss | 0 |
| q_c7049379ce0552a7 | Who was Ogedei's wife? | squad | Semantic Miss | 0 |
| q_bf02b3d9bfbc5c1e | benefits of drinking water on empty stomach in the morning | ms_marco | Ranking Error | 1 |
| q_6306ab220cdf29f8 | what foods grow well in italy | ms_marco | Ranking Error | 1 |
| q_426ef9b4923c4f02 | cost of cosmetic surgery for eyes | ms_marco | Ranking Error | 1 |
| q_44ed866c4ffa7e4e | average cost of child care in nevada | ms_marco | Ranking Error | 1 |
| q_f8a74d7935921637 | is genting highlands theme park open | ms_marco | Ranking Error | 1 |
| q_fe91fd4138564eee | definition of inseparable | ms_marco | Ranking Error | 1 |
| q_15f33de0cb7f5b13 | how much should a driveway cost | ms_marco | Ranking Error | 1 |
| q_f510ef802e9299e4 | life expectancy definition | ms_marco | Ranking Error | 1 |
| q_a4bc49c15557cebd | crossing over occurs when? | ms_marco | Ranking Error | 1 |
| q_34a79e83d127539a | what does your brain do | ms_marco | Ranking Error | 1 |
| q_1fd16190d16c9b22 | formula to find quarter from date | ms_marco | Ranking Error | 1 |
| q_a47cb3a2db426c0e | why is genetic engineering bad for humans | ms_marco | Ranking Error | 1 |
| q_b319027b387a3881 | where is tobacco mostly found | ms_marco | Ranking Error | 1 |
| q_b084cd84a29e92b4 | how young do babies start teething | ms_marco | Ranking Error | 1 |
| q_6155088867b5d410 | how to reduce pvc exposure | ms_marco | Ranking Error | 1 |
| q_75f2cd7c1a110e04 | bisque definition ceramics | ms_marco | Ranking Error | 1 |
| q_03e41014f448e743 | are oatcakes healthy | ms_marco | Ranking Error | 1 |
| q_68ab447530a9c611 | What Is Professional Indemnity | ms_marco | Ranking Error | 1 |
| q_479595c6ae85a1df | where is epinephrine produced | ms_marco | Ranking Error | 1 |
| q_14b34065dcba9d3b | meaning of name skippy | ms_marco | Ranking Error | 1 |
| q_334687991cb6bdff | how long does fresh steak keep in fridge | ms_marco | Ranking Error | 1 |
| q_e77a5be5901de8b8 | when did the new zealand flag come into being | ms_marco | Ranking Error | 1 |
| q_700ff9c5db07c38d | is campylobacter contagious | ms_marco | Ranking Error | 1 |
| q_2f63d77672a6c780 | how far from gold coast to noosa | ms_marco | Ranking Error | 1 |
| q_32f05ed8f71da48d | average cost of energy by state | ms_marco | Ranking Error | 1 |
| q_eb3ca1cf0f528d9a | When an atom gains or loses an electron it becames an? | sciq | Semantic Miss | 0 |
| q_98e769fcccd90d25 | what causes yersinia enterocolitica | ms_marco | Semantic Miss | 0 |
| q_4d856ab568631088 | what do elastic fibres do in arteries | ms_marco | Ranking Error | 1 |
| q_491083c3af995f8e | how much sugars per day | ms_marco | Ranking Error | 1 |
| q_73a8bf1fbb7a380b | What was Maxwell's job? | squad | Semantic Miss | 0 |
| q_c8578117dab05a8b | what is a purified phytochemical | ms_marco | Ranking Error | 1 |
| q_5012a50fe5175fec | what type of epithelium lines the esophagus | ms_marco | Ranking Error | 1 |
| q_291afdbda16f2feb | which chromosome is huntington's disease found on | ms_marco | Semantic Miss | 0 |
| q_cdf373ae2a3e8fe7 | who is giuseppe mercalli and charles richter | ms_marco | Ranking Error | 1 |
| q_0bd91fe6f9205c73 | cost of sim card | ms_marco | Ranking Error | 1 |
| q_f5595afafec9ce14 | how long does it take a belly button piercing to heal | ms_marco | Ranking Error | 1 |
| q_55c22f7cdbfc0187 | radiology salary per hour | ms_marco | Ranking Error | 1 |
| q_f91e43c3d9ec7f5c | who is the protagonist in lysistrata | ms_marco | Ranking Error | 1 |
| q_ab7d59f48c030053 | how much do you make with uber | ms_marco | Ranking Error | 1 |
| q_f29432a9884942a7 | consolute temperature meaning | ms_marco | Ranking Error | 1 |
| q_c27cf3a6b8bb9ed0 | coastal processes are located on what vertebrae | ms_marco | Semantic Miss | 0 |
| q_38251ad3f57ee899 | what year did miscegenation become unconstitutional | ms_marco | Ranking Error | 1 |
| q_e605f92610dde7af | when was the missouri compromise passed | ms_marco | Ranking Error | 1 |
| q_ffae9d69066e509e | subculture meaning | ms_marco | Semantic Miss | 0 |
| q_b9573774aa7618f6 | if someone is HIv positive does that mean they will die with aids | ms_marco | Ranking Error | 1 |
| q_b706c0f19da250e3 | One degree Celsius indicates the same temperature change as | ms_marco | Ranking Error | 1 |
| q_d2d0d1f884bddde4 | what is cell signaling and how does it occur | ms_marco | Ranking Error | 1 |
| q_09ea6d34f4956bd1 | how to put header on one page only | ms_marco | Ranking Error | 1 |
| q_3c77466c60e97c92 | what kind of volcano is paricutin | ms_marco | Ranking Error | 1 |
| q_36df3aa062ec5c56 | how much does dog hip dysplasia surgery cost | ms_marco | Ranking Error | 1 |
| q_9c9b21396c8fdb40 | grass temperature germination | ms_marco | Ranking Error | 1 |
| q_bcd264c0186b4c58 | flg mutation ethnicity | ms_marco | Ranking Error | 1 |
| q_026d692e64df6298 | why are chemical symbols important | ms_marco | Ranking Error | 1 |
| q_b50d54f529b8c35b | what is a verrine | ms_marco | Ranking Error | 1 |
| q_b3262fefb609c54b | What type of input is not required during passive transport? | sciq | Semantic Miss | 0 |
| q_51f9deaa05983a3f | what is involved in memory | ms_marco | Ranking Error | 1 |
| q_1ad7d1f5dd7768e2 | how much does it cost to get a real tattoo | ms_marco | Semantic Miss | 0 |
| q_8b6f295329b73d27 | what causes alkalosis | ms_marco | Ranking Error | 1 |
| q_2316754ec9975656 | What are the two types of cells? | sciq | Semantic Miss | 0 |
| q_93698b1a817fef96 | cost to remove and install concrete driveway | ms_marco | Ranking Error | 1 |
| q_e0ad5131b244671a | alko atc fitting cost | ms_marco | Ranking Error | 1 |
| q_b0cee537858cb755 | call apple support number | ms_marco | Semantic Miss | 0 |
| q_11f758da32f25386 | what does the caudate do | ms_marco | Ranking Error | 1 |
| q_4a65087f12d814a6 | how long does it take for my refund to process | ms_marco | Ranking Error | 1 |
| q_f698314566d3c591 | what makes it rococo style | ms_marco | Ranking Error | 1 |
| q_3415e83bc8bfc911 | what should the temp be inside a refrigerator | ms_marco | Ranking Error | 1 |
| q_e42b679077c23a3e | average salary of doctors in us | ms_marco | Ranking Error | 1 |
| q_0a7aa18568bf7636 | what explorer is an african gazelle named for | ms_marco | Ranking Error | 1 |
| q_ae7679b48cb6e809 | when is barley harvested in israel | ms_marco | Semantic Miss | 0 |
| q_e07d28e93e1c35b6 | doctor average salary | ms_marco | Ranking Error | 1 |
| q_4d486579c3b9e137 | how to measure oven temperature | ms_marco | Ranking Error | 1 |
| q_1782e48646504dbe | what is the largest organ in the body | ms_marco | Ranking Error | 1 |
| q_d33bf814086d59e6 | In what form is carbohydrate stored in the body | ms_marco | Semantic Miss | 0 |
| q_a38f5682c0cd89aa | is spotting a sign of pregnancy | ms_marco | Ranking Error | 1 |
| q_bf80062d1b84c904 | typical price per window | ms_marco | Ranking Error | 1 |
| q_513adcea8b553a5b | how thick does concrete need to be garden wall | ms_marco | Ranking Error | 1 |
| q_453a873f3b47dd0c | what is last name harjo from | ms_marco | Ranking Error | 1 |
| q_082238a93dc4a1c6 | how long is ferry from calais to dover | ms_marco | Ranking Error | 1 |
| q_036b5c327d93e49f | what is presorted standard mail | ms_marco | Ranking Error | 1 |
| q_1cf3cf64c83d6f09 | what is copper good for | ms_marco | Ranking Error | 1 |
| q_a70d64b517820973 | how much does it cost to clean an oven | ms_marco | Ranking Error | 1 |
| q_0d7fccc45a8df3a8 | what is a science scale | ms_marco | Ranking Error | 1 |
| q_f4c1ec6cd46d4f62 | how old does babies start teething | ms_marco | Ranking Error | 1 |
| q_8f7ef4e4db42ec56 | athena name meaning origin | ms_marco | Ranking Error | 1 |
| q_e02c31fb83e294b8 | cost to remove wisdom teeth without insurance | ms_marco | Ranking Error | 1 |
| q_2d2a017e43fa7dc2 | what is an oxalate | ms_marco | Ranking Error | 1 |
| q_a4fd5f4ce53699fc | does minoxidil work for women's hair loss | ms_marco | Ranking Error | 1 |
| q_f33bbf41b4a338c3 | what vegetation zone are pandas found | ms_marco | Ranking Error | 1 |
| q_e877f87b5157594b | oakwood university tuition cost | ms_marco | Ranking Error | 1 |
| q_1843ef0af70cd025 | how much to budget to eat per person at dollywood | ms_marco | Ranking Error | 1 |
| q_2c1cd02bcdd9e78d | what is soap saponification | ms_marco | Ranking Error | 1 |
| q_830f59d42ecbf613 | scurvy meaning | ms_marco | Ranking Error | 1 |
| q_4cdac130f0e814b9 | What can be the result of a change in an organization? | squad | Semantic Miss | 0 |
| q_32819c8d1275d883 | term meaning muscle pain | ms_marco | Ranking Error | 1 |
| q_a8663384a1b58b81 | what makes a lava lamp work | ms_marco | Semantic Miss | 0 |
| q_32b20955a25dfa5b | what muscles make up the muscular system | ms_marco | Ranking Error | 1 |
| q_99d94d1ce40464bb | temperature range in singapore | ms_marco | Ranking Error | 1 |
| q_8e131e7546f21557 | why is enzyme amylase affected by ph | ms_marco | Ranking Error | 1 |
| q_66ad2291a4365768 | difference between cooling fan and exhaust fan | ms_marco | Ranking Error | 1 |
| q_8bd95e5502a3e9b0 | what is a magnet? | ms_marco | Ranking Error | 1 |
| q_1bd1a2682f581006 | Because of the danger inherent in concentrated oxygen, what is a concern about keeping it? | squad | Semantic Miss | 0 |
| q_a661e1649875883f | how to measure for cement slab | ms_marco | Ranking Error | 1 |
| q_8e477764acf4ea4d | is spanish moss a lichen | ms_marco | Ranking Error | 1 |
| q_1cab99ed08de2c4a | definition of CEO | ms_marco | Ranking Error | 1 |
| q_119c9f39ac7d6104 | How long was each episode of Doctor Who? | squad | Ranking Error | 1 |
| q_bca15550b8d9f99d | cost of life in NYC | ms_marco | Ranking Error | 1 |
| q_1c4d80b5355a3a13 | what is crypton fabric | ms_marco | Ranking Error | 1 |
| q_f312ddb8b762d07f | causes of very yellow urine | ms_marco | Ranking Error | 1 |
| q_670f44b09ea1559b | what is the average cost of a funeral | ms_marco | Ranking Error | 1 |
| q_adf530c80954f891 | miana name meaning of name | ms_marco | Ranking Error | 1 |
| q_fa18232319bd28c0 | average cost to live in an apartment | ms_marco | Ranking Error | 1 |
| q_0de5cbafafbf32d9 | what material was used in hiroshima | ms_marco | Ranking Error | 1 |
| q_de7af35f91454725 | how does common descent applied to the evolution of cameras | ms_marco | Ranking Error | 1 |
| q_2cab9ffa4889eaaa | what temperature should underfloor heating be | ms_marco | Ranking Error | 1 |
| q_71866228e94b8ad4 | how to find someone ip on skype | ms_marco | Semantic Miss | 0 |
| q_9fd6e2b033b06923 | how much does it cost for a speech therapist | ms_marco | Ranking Error | 1 |
| q_5b1e50241272643b | benefits of eating protein for breakfast | ms_marco | Ranking Error | 1 |
| q_9f48c55e3580bd92 | what is pupil distance in eyeglass prescription | ms_marco | Ranking Error | 1 |
| q_af4b3adeae38735c | maximum handicap for for men | ms_marco | Ranking Error | 1 |
| q_f2ab764a57a8194c | average temperature of marine biome | ms_marco | Ranking Error | 1 |
| q_fa813bcde4ef78cc | cost of postage stamps | ms_marco | Semantic Miss | 0 |
| q_89baa44d916e3c76 | age at which an individual is classed as a minor and how this differs nationally | ms_marco | Ranking Error | 1 |
| q_a6be7e7c30a5d295 | importance of biochemical tests in identification of bacteria | ms_marco | Ranking Error | 1 |
| q_25276932a571b4ba | how long do you cook a crown roast of pork | ms_marco | Semantic Miss | 0 |
| q_862a3cc1c19cd1df | why was the separate amenities act passed | ms_marco | Ranking Error | 1 |
| q_10f97925fd3d9767 | what problems did the civil rights movement address | ms_marco | Ranking Error | 1 |
| q_8d7057db2458dfb2 | what is overpayment inequity | ms_marco | Semantic Miss | 0 |
| q_fcefe446cc6be0c8 | what symmetry means | ms_marco | Ranking Error | 1 |
| q_8fae0756eb72b5c3 | average cost for painting exterior of house | ms_marco | Ranking Error | 1 |
| q_d14b39a50bb75300 | definition of seiche | ms_marco | Ranking Error | 1 |
| q_7a1f071783489933 | is foxtail fern poisonous | ms_marco | Ranking Error | 1 |
| q_ed54713756bf0712 | xml interface definition | ms_marco | Ranking Error | 1 |
| q_bea67486ac446317 | the lowest whole number ratio of the elements in a compound is called the | ms_marco | Ranking Error | 1 |
| q_be5bfdea65bdf53f | vietnam size comparison to what us state | ms_marco | Ranking Error | 1 |
| q_3c61a761ac046003 | how long do black labs typically live | ms_marco | Ranking Error | 1 |
| q_c83d0c5e835a372b | what does inr measure? | ms_marco | Semantic Miss | 0 |
| q_87d30e70e90db865 | what is a commercial guaranty | ms_marco | Semantic Miss | 0 |
| q_c3e55e27917f5ae5 | what is the currency in ireland | ms_marco | Semantic Miss | 0 |
| q_c1fc6057a15ef7d5 | what kind of diversity is in grassland | ms_marco | Semantic Miss | 0 |
| q_8a3b3452f6e5999d | what type of barrier is mucus | ms_marco | Ranking Error | 1 |
| q_2af3e32e9ad98b5d | baking pork chops in convection oven how long at what temp | ms_marco | Ranking Error | 1 |
| q_f671f37c13c682c9 | vitamin and mineral content in fruits | ms_marco | Semantic Miss | 0 |
| q_4b42a280c4957da2 | can you cook a tri-tip in the oven | ms_marco | Ranking Error | 1 |
| q_6b95422a4d8e185e | how many carbs in plain baked potato | ms_marco | Ranking Error | 1 |
| q_b2e9e6050ff9d764 | does term life insurance increase | ms_marco | Ranking Error | 1 |
| q_4b8e5c04cc08cc5a | where is jekyll island located | ms_marco | Ranking Error | 1 |
| q_23387323f78a4d66 | how to update all figures in word | ms_marco | Semantic Miss | 0 |
| q_bf572b5f52449a35 | Some of the combs in the V&A collection of South East Asian art is made of what material? | squad | Ranking Error | 1 |
| q_f11041492b49a3d4 | What is the name of pluto's moon? | sciq | Semantic Miss | 0 |
| q_f19b8bbbdf5027e9 | what does wt mean in texting | ms_marco | Ranking Error | 1 |
| q_d79604daca55d646 | average cost to have someone build a website | ms_marco | Ranking Error | 1 |
| q_2b0feaf7f43b0a81 | cost per kwh in long beach ca | ms_marco | Ranking Error | 1 |
| q_82aaff3701cac6e2 | what characteristics of dna creates the genetic code | ms_marco | Ranking Error | 1 |
| q_a84a9cb03f7c413c | price to install an interior door | ms_marco | Ranking Error | 1 |
| q_661b5cb9502b2e60 | what is the strongest muscle in the body | ms_marco | Semantic Miss | 0 |
| q_08c433a9e70a2737 | Of what mathematical nature is the Basel problem? | squad | Semantic Miss | 0 |
| q_c7d63d2c20bd264f | how long is a hepatitis a vaccination good for | ms_marco | Ranking Error | 1 |
| q_17c482bf953479d0 | what is nitrofurantoin used for | ms_marco | Ranking Error | 1 |
| q_c18cd3246bbc36ad | oven temperature for sirloin tip roast | ms_marco | Ranking Error | 1 |
| q_b5385e22226da1ab | average yearly salary of a traveling nurse | ms_marco | Ranking Error | 1 |
| q_91b3fc3ecae23956 | what do you understand by the activation energy of a reaction and how does it relate to collision theory? | ms_marco | Ranking Error | 1 |
| q_b2fc0525a50dbc6a | how old do puppies have to be before they can hear | ms_marco | Ranking Error | 1 |
| q_9b795b8cf11bfe57 | cost to get passport | ms_marco | Ranking Error | 1 |
| q_92c5362e6461839a | ways to reduce emissions from cars | ms_marco | Ranking Error | 1 |
| q_5507a3d0b702ed9b | what is lodestar mean | ms_marco | Semantic Miss | 0 |
| q_0dfb036a17b5fc41 | is licorice a blood thinner | ms_marco | Ranking Error | 1 |
| q_cb90365c8ec8aa7d | how much does gutter guard cost | ms_marco | Semantic Miss | 0 |
| q_f5c4f2e2cd25a584 | average salary radiologist tennessee | ms_marco | Semantic Miss | 0 |
| q_69cfb4633f2d66a8 | average cost of auto insurance in florida | ms_marco | Ranking Error | 1 |
| q_7d4d22d38f63ee99 | how safe is salinas ca | ms_marco | Ranking Error | 1 |
| q_c8a74b5ca34cb9e7 | where are dromedary camels found | ms_marco | Ranking Error | 1 |
| q_ad700455dd573e10 | how much do associate corporate lawyers make | ms_marco | Ranking Error | 1 |
| q_03c0b046aa792450 | how do i check to see why the mic is not working | ms_marco | Ranking Error | 1 |
| q_91113ee2bc91a473 | typical renovation costs | ms_marco | Ranking Error | 1 |
| q_52f505fc4cb7b5d5 | is a multipolar neuron motor | ms_marco | Ranking Error | 1 |
| q_d68284b0fbe63c78 | how much is physician assistant program | ms_marco | Ranking Error | 1 |
| q_6ef2577ba864dca9 | what is mers servicer id | ms_marco | Ranking Error | 1 |
| q_aab4242734e6cacf | what does noblesse oblige mean | ms_marco | Ranking Error | 1 |
| q_504bf81ccb4db2f7 | habitat science definition | ms_marco | Ranking Error | 1 |
| q_7a2c1c1ef7cea638 | what is an unsaturated hydrocarbon | ms_marco | Ranking Error | 1 |
| q_14c5ba17eeca1cb0 | nys dba filing fee | ms_marco | Ranking Error | 1 |
| q_61eb686c30490ff2 | what is a reaction turbine | ms_marco | Ranking Error | 1 |
| q_1b21f0a60563a042 | brennan name meaning | ms_marco | Ranking Error | 1 |
| q_c755f538a14a9941 | what is the definition of the nile river valley | ms_marco | Ranking Error | 1 |
| q_c0a893bb3d71089b | what is fire blight | ms_marco | Ranking Error | 1 |
| q_590c7d7f5702684b | what is a novel | ms_marco | Ranking Error | 1 |
| q_306d4d3d72b731d7 | what does arbitration agreement means | ms_marco | Ranking Error | 1 |
| q_6287b15fd3f4bee3 | how long does the average cremation take | ms_marco | Semantic Miss | 0 |
| q_f6aeb115ee19478b | how to incubate guinea fowl eggs | ms_marco | Ranking Error | 1 |
| q_7b70206f584fcfc1 | what is the history name for carter | ms_marco | Ranking Error | 1 |
| q_a48834b1d8ba3923 | fluid of csf is derived from the bloodstream | ms_marco | Ranking Error | 1 |
| q_1fe7a9e918c61d6e | why chartered accountant is important | ms_marco | Ranking Error | 1 |
| q_aeefe137e96c5ba6 | what does a wellness check consist of | ms_marco | Ranking Error | 1 |
| q_07ec6d23f113ecb5 | What is the first stage of cellular respiration? | sciq | Ranking Error | 1 |
| q_af65462bcc74382f | what is the classification of krokodil | ms_marco | Ranking Error | 1 |
| q_db019a3f9e7b5fa8 | disease that opossum carry that are transmitted to dogs | ms_marco | Ranking Error | 1 |
| q_b55c0cee4574f550 | how long do house of representatives members serve | ms_marco | Ranking Error | 1 |
| q_995afedd9f3d69f0 | what are the lines on the forehead called | ms_marco | Ranking Error | 1 |
| q_984bfec90d417d7b | what is ractopamine | ms_marco | Ranking Error | 1 |
| q_d349b49f0acf3424 | polymerase chain reaction definition | ms_marco | Ranking Error | 1 |
| q_2314615faedd6f17 | how to get money to remodel my home | ms_marco | Ranking Error | 1 |
| q_235328810278f10a | what does the premotor area control | ms_marco | Ranking Error | 1 |
| q_1d0d3c20a8656109 | what carries coded information from the nucleus | ms_marco | Ranking Error | 1 |
| q_557a42a04d71e4cf | What does Kitab Rudjdjar mean in English? | squad | Semantic Miss | 0 |
| q_d531a253edefa6cc | what is goat | ms_marco | Ranking Error | 1 |
| q_7f3ec1d1e936983d | What system is responsible for defending your body against sickness? | sciq | Ranking Error | 1 |
| q_e78cf503c0908b75 | what does EPNS mean | ms_marco | Ranking Error | 1 |
| q_c0e8f0398c21cb3b | Save the original_value. | code_search_net | Semantic Miss | 0 |
| q_a5555aadd2ab605c | qualifications for becoming a registered nurse | ms_marco | Ranking Error | 1 |
| q_6bd19d54d1efc83f | where can I purchase alum from | ms_marco | Ranking Error | 1 |
| q_a0a2d0464c1fd57f | what are the best scales for body weight | ms_marco | Ranking Error | 1 |
| q_5e074fce376b82ad | name the power that interprets the laws and settles disputes between members of a society | ms_marco | Semantic Miss | 0 |
| q_7185554748efd126 | What is another term for rotors? | squad | Semantic Miss | 0 |
| q_81128032db69abf4 | grams in a tablespoon of sugar | ms_marco | Ranking Error | 1 |
| q_f7a8eb5b2a620bbf | Photosynthesis is initiated by what hitting plants? | sciq | Semantic Miss | 0 |
| q_2932e5d62a49886c | what dragonfly symbolizes | ms_marco | Ranking Error | 1 |
| q_da2de3d82695d05e | what is a cbr test | ms_marco | Semantic Miss | 0 |
| q_2f24e1f8ef2502c7 | what is rhetorical device | ms_marco | Ranking Error | 1 |
| q_60d7579b5e0a03dd | what is nasal stuffiness | ms_marco | Ranking Error | 1 |
| q_21426d23041360ec | what is a contingent liabilities | ms_marco | Ranking Error | 1 |
| q_62132bc159011c65 | how long do i have to charge a lawn mower battery before i can use it | ms_marco | Ranking Error | 1 |
| q_5d92580edc2f53cd | lorazepam dose for sleep | ms_marco | Ranking Error | 1 |
| q_1f173073daebb02a | is norvasc a blood thinner | ms_marco | Semantic Miss | 0 |
| q_d90d474016da142d | what is bidirectional SFP | ms_marco | Ranking Error | 1 |
| q_dd007543bf7f0176 | what is puush | ms_marco | Ranking Error | 1 |
| q_bc569b11cfa138b1 | how much cost appointment with small business coach | ms_marco | Ranking Error | 1 |
| q_ee41f52a866c5b08 | what is Serotonin syndrome | ms_marco | Ranking Error | 1 |
| q_1f27a22b2afe4ec9 | what are bunnies | ms_marco | Ranking Error | 1 |
| q_b360cff4a93557b7 | what muscles in activated during plank | ms_marco | Ranking Error | 1 |
| q_ff9747a76c9b59a8 | what is communism quizlet | ms_marco | Ranking Error | 1 |
| q_c71836c9840756ad | what is Diabetic microalbuminuria | ms_marco | Ranking Error | 1 |
| q_7aea4570a41aca44 | what is meant by reflection of the serous pericardium | ms_marco | Ranking Error | 1 |
| q_537d9b8467f96390 | how long does it take to take up a habit | ms_marco | Semantic Miss | 0 |
| q_cb6c3416efd38b44 | what is triple net rent mean | ms_marco | Ranking Error | 1 |
| q_176a46935c76a241 | what type of materials do you need to keep charges flowing? | ms_marco | Semantic Miss | 0 |
| q_e7e659396ca1f3ba | why is machu picchu fantastic | ms_marco | Semantic Miss | 0 |
| q_07e9c8ec44d89eaf | What do ferns use in place of seeds to reproduce? | sciq | Semantic Miss | 0 |
| q_1d371d4b988f2ec1 | what does magnetism affect | ms_marco | Ranking Error | 1 |
| q_828bfdd55205a928 | what is the cost of employment arbitration | ms_marco | Ranking Error | 1 |
| q_d9efa8ebc2799472 | what is the yearly pay for a civil engineer | ms_marco | Ranking Error | 1 |
| q_e4b8c33601080ead | should i apply the tb vaccine | ms_marco | Ranking Error | 1 |
| q_93ee64f1d98e9ad8 | what surface is indoor field hockey played on | ms_marco | Ranking Error | 1 |
| q_6343a21d5ccec1db | oil price per barrel history | ms_marco | Ranking Error | 1 |
| q_345c934971a38c2f | is the new york observer liberal or conservative | ms_marco | Semantic Miss | 0 |
| q_a993bc99b2bcd033 | what county is crawfordsville indiana in | ms_marco | Ranking Error | 1 |
| q_d4ecf5a6cbf7155a | what is in root beer | ms_marco | Ranking Error | 1 |
| q_3b610b6013eff740 | what year was the paperclip invented | ms_marco | Ranking Error | 1 |
| q_aab1037889d920fb | concrete resurfacing cost | ms_marco | Ranking Error | 1 |
| q_2d9c35334dd402c8 | what was the significance of the battle of the midway | ms_marco | Ranking Error | 1 |
| q_bd628e79ce41729d | word that means easily influenced | ms_marco | Ranking Error | 1 |
| q_7b600f56386662fb | how long to cook pork rib tips in oven | ms_marco | Semantic Miss | 0 |
| q_694583231931b8e2 | what is a flagstaff | ms_marco | Ranking Error | 1 |
| q_260999edf0afa95f | what makes a fossil an index fossil | ms_marco | Ranking Error | 1 |
| q_c7d6e338d022be88 | what are the main characteristics of the tropical savanna | ms_marco | Ranking Error | 1 |
| q_a69b03be8cdc1c13 | glycolysis definition as a pathway for atp | ms_marco | Ranking Error | 1 |
| q_937e7216dc8cc005 | difference between greek and roman culture | ms_marco | Ranking Error | 1 |
| q_aadcdde7a8c902f8 | what is ibm devops | ms_marco | Ranking Error | 1 |
| q_9e208f5b4a6bc014 | justdial coimbatore contact number | ms_marco | Semantic Miss | 0 |
| q_28a05a3c881b3b73 | uwe name meaning | ms_marco | Ranking Error | 1 |
| q_7a6dab083fb6c433 | diotrephes name meaning | ms_marco | Ranking Error | 1 |
| q_f6a19e19c4762255 | process of using dna to create rna | ms_marco | Ranking Error | 1 |
| q_e67aebd16c1f5dae | which minerals indicate the presence of oxygen | ms_marco | Ranking Error | 1 |
| q_2df7aae0b1cb714b | is dcpip harmful | ms_marco | Ranking Error | 1 |
| q_9a644e43a4979de3 | average household electricity usage | ms_marco | Ranking Error | 1 |
| q_58aeb052665320af | what do states have regarding whistleblower | ms_marco | Ranking Error | 1 |
| q_8a81be0bd6366f32 | is honey harmful | ms_marco | Ranking Error | 1 |
| q_62a7b1a40633ee48 | what is auricle | ms_marco | Ranking Error | 1 |
| q_2065686998622468 | average penile length yahoo | ms_marco | Ranking Error | 1 |
| q_8ba134df116a9c33 | flagler cost per credit hour | ms_marco | Ranking Error | 1 |
| q_24653a4e0ad0a4ec | where is chernobyl located | ms_marco | Ranking Error | 1 |
| q_7f6eae639d4014cb | what is inside jackfruit | ms_marco | Ranking Error | 1 |
| q_3445f3de512c48b7 | how much should a one month baby drink | ms_marco | Ranking Error | 1 |
| q_f98b0537825eae8f | how many credits for a degree | ms_marco | Semantic Miss | 0 |
| q_1fea73c2e8cdc372 | what does the name jasmin mean | ms_marco | Semantic Miss | 0 |
| q_b04b1645eebba77f | what is the definition of onomatopoeia | ms_marco | Ranking Error | 1 |
| q_bf85da45b93875f8 | What do ctenophore use to capture their prey? | squad | Ranking Error | 1 |
| q_aac44aa460ad19e5 | What type of text is the Quran? | squad | Semantic Miss | 0 |
| q_3e05a26caae7b072 | what is the average wage for housekeepers | ms_marco | Ranking Error | 1 |
| q_8248289fb3dc0bbd | different types of wines explained | ms_marco | Ranking Error | 1 |
| q_a63cd4bf8efa82bf | what category does liothyronine belong and what disease does it treat | ms_marco | Ranking Error | 1 |
| q_06f1360301b11b05 | are chickpeas a carbohydrate? | ms_marco | Semantic Miss | 0 |
| q_ae4c9f58a26a789f | how much do i pay for auditor | ms_marco | Ranking Error | 1 |
| q_b02ab8f50d02a768 | who was trek founded by | ms_marco | Ranking Error | 1 |
| q_ca5b12f6d9d59371 | definition of gene locus | ms_marco | Ranking Error | 1 |
| q_f4b569ce8a316417 | normal range of oxygen saturation for adults | ms_marco | Ranking Error | 1 |
| q_ad1d36419520e824 | where is woodbine georgia | ms_marco | Ranking Error | 1 |
| q_3f75becd91f00c21 | how contagious is a stomach flu | ms_marco | Ranking Error | 1 |
| q_6b31058356ca0652 | The visual cortex of the brain is located towards the: | ms_marco | Ranking Error | 1 |
| q_3dc1541118928325 | how long to cook pork chops in showtime rotisserie | ms_marco | Ranking Error | 1 |
| q_a08dbaa775093575 | where is the pcv valve located | ms_marco | Semantic Miss | 0 |
| q_ae0e8888508b3674 | how much exercise or physical activity should people do daily | ms_marco | Ranking Error | 1 |
| q_c36caec7d1086f0e | what is a bundle of neuronal processes | ms_marco | Ranking Error | 1 |
| q_0233ce9f1fa4888d | what is a hypo | ms_marco | Ranking Error | 1 |
| q_11e7b396cf12f795 | behavioral adaptations what resources do organisms need from their environment | ms_marco | Ranking Error | 1 |
| q_7d491d07919e7c66 | what is joconde cake | ms_marco | Ranking Error | 1 |
| q_1458960bf6bb09d5 | cost of pet insurance per month | ms_marco | Ranking Error | 1 |
| q_c0e0529e3ed1e01f | common causes of burning sensation in the tongue | ms_marco | Ranking Error | 1 |
| q_b14598501882c3cf | what is a desalination plant | ms_marco | Ranking Error | 1 |
| q_6d2c9e0932fc5df0 | what is pva used for | ms_marco | Ranking Error | 1 |
| q_8fb096e351bc6f03 | why is the united states considered a meritocracy | ms_marco | Ranking Error | 1 |
| q_0edd2f9e9878660d | how much is a meter stamp | ms_marco | Ranking Error | 1 |
| q_edb44a76e90e99b3 | what is sensory integration therapy | ms_marco | Ranking Error | 1 |
| q_ef7c2c027cab1097 | what is tco for software project | ms_marco | Ranking Error | 1 |
| q_8082287ab4180314 | when was the first computer built | ms_marco | Ranking Error | 1 |
| q_bd985092cf6507fb | what is venus known for | ms_marco | Semantic Miss | 0 |
| q_e8ac551daa5f0938 | What type of flower is sought on Midsummer's Eve? | squad | Semantic Miss | 0 |
| q_01a4c9aa3cf35ead | What is an example of a disease that affects the blood? | sciq | Semantic Miss | 0 |
| q_275fe0a7353730ef | was that midlife is affected biologically | ms_marco | Ranking Error | 1 |
| q_265849b65fdd733a | vitamin d in infants side effects | ms_marco | Ranking Error | 1 |
| q_317ddfe8a738e4ae | average velocity definition | ms_marco | Ranking Error | 1 |
| q_98acd9938ac8f31f | what level do you get a flying mount in wow | ms_marco | Ranking Error | 1 |
| q_1203bc4625ca8e0c | how much a home inspector make | ms_marco | Ranking Error | 1 |
| q_b8f444a62b91f019 | average weight age range baby boy | ms_marco | Ranking Error | 1 |
| q_ebf2de420f24edae | what is energy consumption intensity | ms_marco | Ranking Error | 1 |
| q_7147f68ba41395f3 | what evidence does dna show | ms_marco | Ranking Error | 1 |
| q_d9e8aebee3aa7725 | common sites of metastasis of ovarian cancer | ms_marco | Ranking Error | 1 |
| q_fcd5258c835ede47 | what does cmr stand for in business | ms_marco | Ranking Error | 1 |
| q_c0a52f488a8dfd2e | where do zebras live | ms_marco | Ranking Error | 1 |
| q_171d97b639d6fa25 | what tectonic plate is mount st helens on | ms_marco | Ranking Error | 1 |
| q_a86256cbe0a60711 | what course do you do to become a speech therapist | ms_marco | Ranking Error | 1 |
| q_60f4e493242fd3e9 | where puerto vallarta is located | ms_marco | Semantic Miss | 0 |
| q_d080956d104896a3 | temporal parietal damage | ms_marco | Ranking Error | 1 |
| q_11a71077361ace72 | what does clinical psychology mean | ms_marco | Ranking Error | 1 |
| q_c7c93cd392849ab3 | exilis cost | ms_marco | Ranking Error | 1 |
| q_97a55555b1ea5107 | what heath good does turmeric | ms_marco | Ranking Error | 1 |
| q_cc2b6bc0571ad320 | cost per class of university of chicago | ms_marco | Ranking Error | 1 |
| q_838d3241e932097b | terms used in a will | ms_marco | Ranking Error | 1 |
| q_370313a098d833f9 | average rainfall in bloemfontein | ms_marco | Ranking Error | 1 |
| q_e6095f0921901783 | what is deadline to file tax extension | ms_marco | Ranking Error | 1 |
| q_195744ea7d4e5277 | is contractor cost wages | ms_marco | Ranking Error | 1 |
| q_3c8cd927d486d17c | what to expect two weeks after knee replacement | ms_marco | Ranking Error | 1 |
| q_0b1ffdbc9c4c9f45 | how long is the seikan tunnel | ms_marco | Ranking Error | 1 |
| q_33a7a3a1ad574f2a | how many yards do i need for a baby blanket | ms_marco | Ranking Error | 1 |
| q_d089e4e37269ff14 | lab test what does bun mean | ms_marco | Semantic Miss | 0 |
| q_4b4e8dacd308a944 | Which gas is released by the group of archaea known as methanogens? | sciq | Semantic Miss | 0 |
| q_7bfe18f9ce8cc6bd | What types of teachers are retiring the most? | squad | Semantic Miss | 0 |
| q_bcae2c337fc8853f | what hormone does the pituitary gland produce in dogs | ms_marco | Ranking Error | 1 |
| q_bb36e45a26a9161a | first black woman to earn phd in astrophysics front yale | ms_marco | Ranking Error | 1 |
| q_89ec4706de0763b3 | what is the world's longest snake on record | ms_marco | Ranking Error | 1 |
| q_9b4e8c916a61a287 | what organs allow nutrients to be absorbed | ms_marco | Ranking Error | 1 |
| q_caa097627eb83f8a | what is polyurethane leather made of | ms_marco | Ranking Error | 1 |
| q_0442e6f437d120d8 | why do muslim men have beards | ms_marco | Ranking Error | 1 |
| q_f34f196edc47722f | What are the largest phylum of the animal kingdom? | sciq | Semantic Miss | 0 |
| q_596fc4e5a8589140 | what does S&M mean | ms_marco | Semantic Miss | 0 |
| q_06a2eee1b4f2ee7b | hepatitis definition | ms_marco | Semantic Miss | 0 |
| q_fae9196af6f08c87 | What type of movement is caused by erosion from direct gravity? | sciq | Semantic Miss | 0 |
| q_03e170fbb706b07a | where does Exocrine glands secrete their fluids | ms_marco | Ranking Error | 1 |
| q_0f99f55e5c046ac7 | what is limestone in chemistry | ms_marco | Semantic Miss | 0 |
| q_8cbabe0fd6630177 | what is a stalk of celery | ms_marco | Ranking Error | 1 |
| q_d3d8bcc7dacf9bb8 | cost of orthotics in ontario | ms_marco | Ranking Error | 1 |
| q_69bd69103763a1ab | the medial concavity of the kidney is called the | ms_marco | Semantic Miss | 0 |
| q_a37fd705bce73f50 | what is coal | ms_marco | Ranking Error | 1 |
| q_71ee0b07cfac5d91 | what is american shortening | ms_marco | Ranking Error | 1 |
| q_55d74b31b5925402 | What is the natural movement called within your intestines? | sciq | Semantic Miss | 0 |
| q_abf5280665899b4e | what breccia is used for | ms_marco | Ranking Error | 1 |
| q_31013f3c242d7897 | why are frequent monitoring of diabetes important | ms_marco | Ranking Error | 1 |
| q_8be3869ae3faa8f2 | where in california is the naval base north island | ms_marco | Ranking Error | 1 |
| q_a21d3267d5c03b46 | what is river rocks | ms_marco | Semantic Miss | 0 |
| q_8e2c53439a936859 | town where ruins of machu picchu are located on which continent | ms_marco | Ranking Error | 1 |
| q_f909ab4e708f32bf | how long do teams have to draft in the nfl | ms_marco | Semantic Miss | 0 |
| q_95201d437e97f4a1 | indira name meaning | ms_marco | Ranking Error | 1 |
| q_e64b96b302e006e8 | why was berlin airlift needed | ms_marco | Ranking Error | 1 |
| q_551dae60314f3fe4 | clenbuterol how long to see results | ms_marco | Semantic Miss | 0 |
| q_86d15c4daaa0f2c4 | what are economic impacts of geothermal energy | ms_marco | Ranking Error | 1 |
| q_01bf9fb20275e6cb | how to request for approval email for data card | ms_marco | Ranking Error | 1 |
| q_e6511f393e8fae13 | what should normal diabetes glucose levels be | ms_marco | Ranking Error | 1 |
| q_9662ede8fe929f8a | when does implantation in pregnancy occur | ms_marco | Ranking Error | 1 |
| q_0ba114e1b87458cd | how long do fresh hen eggs keep outside fridge | ms_marco | Semantic Miss | 0 |
| q_838a994da51071af | what is the equation for calculating density | ms_marco | Ranking Error | 1 |
| q_20fb2f1d2c3b76a3 | what is a ancient religion | ms_marco | Ranking Error | 1 |
| q_c838a4cd3cbbccdb | typical payroll cost for a small firm | ms_marco | Ranking Error | 1 |
| q_359fb3d374c97fba | cost of clock spring repair | ms_marco | Ranking Error | 1 |
| q_65ee6ddb1fa45850 | what does incited mean | ms_marco | Ranking Error | 1 |
| q_52311e259475cf80 | political system that divides power between a central government | ms_marco | Ranking Error | 1 |
| q_dac7be52b34ab118 | what is granisetron hcl used for | ms_marco | Ranking Error | 1 |
| q_664267f34b7a153b | average cost of heat pump system and installation | ms_marco | Ranking Error | 1 |
| q_84179c2be90481f1 | kratom definition | ms_marco | Ranking Error | 1 |
| q_791bc40df12a83d4 | definition of law of attraction | ms_marco | Ranking Error | 1 |
| q_e4c1e1c46b59ee7e | where do auroras occur | ms_marco | Ranking Error | 1 |
| q_5544ef86f6b64fba | what is a certified ehr system | ms_marco | Ranking Error | 1 |
| q_018e3a21bebe30c8 | which types of waves are absorbed by the atmosphere | ms_marco | Ranking Error | 1 |
| q_76c356617fc60ee0 | what is nrf2 activator | ms_marco | Ranking Error | 1 |
| q_1b4cc5fcdae6edf5 | what is bilirubin function | ms_marco | Ranking Error | 1 |
| q_4244f617e8854943 | can a pinched nerve feel like a heart attack | ms_marco | Ranking Error | 1 |
| q_f8e17a33edc13703 | what kind of landform is toronto | ms_marco | Semantic Miss | 0 |
| q_ddddc214a0401345 | can you tile over control joints | ms_marco | Ranking Error | 1 |
| q_77959b26a4330e07 | common hog diseases | ms_marco | Ranking Error | 1 |
| q_3244119ac87181ee | Other theories of the word's origin can be generally classed as what? | squad | Semantic Miss | 0 |
| q_be2439dadbdee18e | what is the origin of the name quirino | ms_marco | Ranking Error | 1 |
| q_e3a72825533e4ccd | where is duck dynasty filmed | ms_marco | Ranking Error | 1 |
| q_a373c8c8690b434a | benign tumor of mesenchymal origin | ms_marco | Ranking Error | 1 |
| q_e82c39156ef91717 | barite is in what mineral group | ms_marco | Ranking Error | 1 |
| q_85d3c62d7b6a1072 | what movement does the cerebrum control | ms_marco | Ranking Error | 1 |
| q_f8afd967f8acf070 | what is geoengineering chemtrails | ms_marco | Ranking Error | 1 |
| q_fd843d1b18eee83e | what Pokémon is a moth | ms_marco | Ranking Error | 1 |
| q_8352468c38d1071d | average temp of a taiga | ms_marco | Ranking Error | 1 |
| q_980ca4213e33adae | what is made at the lhc | ms_marco | Ranking Error | 1 |
| q_004a53be2dfe0601 | oldest president to be elected | ms_marco | Ranking Error | 1 |
| q_ef8fbf2bde3ebf3c | neonatal nurse salary how much will they make | ms_marco | Ranking Error | 1 |
| q_38d0041efe1a3a94 | what food is iodine found in | ms_marco | Ranking Error | 1 |
| q_c158585671f769f2 | all of the hobbit movies | ms_marco | Semantic Miss | 0 |
| q_b481efdf8a55a0de | Motor neurons are considered to be what type of neurons | ms_marco | Ranking Error | 1 |
| q_6388439723f2d401 | Chewing insects such as dragonflies and grasshoppers have how many sets of jaws? | sciq | Semantic Miss | 0 |
| q_3064d661094964be | can you hatch quails in an incubator | ms_marco | Ranking Error | 1 |
| q_07252a11edea5a32 | what is the average salary for a project manager in construction | ms_marco | Ranking Error | 1 |
| q_cdb3ae19f91e9367 | When does a baby double in length and triple in weight? | sciq | Semantic Miss | 0 |
| q_9f4478c4745f56ec | where do palm trees originate | ms_marco | Ranking Error | 1 |
| q_093c7670b6143235 | worst types of brain damage | ms_marco | Ranking Error | 1 |
| q_e531d772ec509c37 | return loss definition | ms_marco | Ranking Error | 1 |
| q_b901e4717817bfe1 | who sang the disco song Take me to a higher place | ms_marco | Ranking Error | 1 |
| q_01f7831e5f859864 | delusions definition schizophrenia | ms_marco | Ranking Error | 1 |
| q_6d503ec712bfa6c5 | which is a predetermined reimbursement methodology | ms_marco | Ranking Error | 1 |
| q_bac248a07fd53292 | how many pounds of coffee are roasted during small batch roasting | ms_marco | Ranking Error | 1 |
| q_039e5fb174ce8b7f | constricts blood vessels definition | ms_marco | Ranking Error | 1 |
| q_c1d9f960acf219ea | how much can i expect to pay for carpet? | ms_marco | Ranking Error | 1 |
| q_4287a1dfa55453c6 | what moss is antibacterial, native american | ms_marco | Ranking Error | 1 |
| q_cfda6ea3c127d030 | how much is m&s prosecco | ms_marco | Ranking Error | 1 |
| q_e73b15685445bdfd | is pertussis a communicable disease | ms_marco | Ranking Error | 1 |
| q_dfda5ff4ee3f6d71 | how long does an occupational therapist go to school | ms_marco | Ranking Error | 1 |
| q_6bf786c5f1ecf95f | what is the meaning of election | ms_marco | Ranking Error | 1 |
| q_a042ba4f2287a776 | Who actually won the prize? | squad | Semantic Miss | 0 |
| q_12e9e63ef965132d | cholera infantum definition | ms_marco | Ranking Error | 1 |
| q_1e49fdf2f391ca4c | what is the average cost to have a tree removed | ms_marco | Semantic Miss | 0 |
| q_e79094188531cf04 | what is the average cost of a full time nanny | ms_marco | Ranking Error | 1 |
| q_61b86a979b596091 | What type of mammals are humans? | sciq | Semantic Miss | 0 |
| q_6114045eb53c2181 | who did belgium give power over in | ms_marco | Semantic Miss | 0 |
| q_5257ea09d4734dcb | what is spinosad | ms_marco | Ranking Error | 1 |
| q_458393047ccbeb61 | where do catfish live in ponds | ms_marco | Ranking Error | 1 |
| q_59d50063d8967760 | how long does an irs audit take | ms_marco | Ranking Error | 1 |
| q_0617322dcf52dd2d | how much weight can an egg hold | ms_marco | Ranking Error | 1 |
| q_fe65afb8224f4df9 | don bradman where was he born | ms_marco | Ranking Error | 1 |
| q_7f3b7554bc47e509 | what is adobo chicken | ms_marco | Ranking Error | 1 |
| q_55f3695607c7f58c | what is hydroquinone | ms_marco | Ranking Error | 1 |
| q_948c5785a116f7e8 | how to conclude a long essay | ms_marco | Ranking Error | 1 |
| q_e06cc2606bd1d86c | how to do photogenic smile | ms_marco | Ranking Error | 1 |
| q_fba8bbfbc3412ed7 | salary texas university | ms_marco | Ranking Error | 1 |
| q_f72fa3b4ff5deeb8 | which opioids is an agonist and antagonist | ms_marco | Ranking Error | 1 |
| q_d8abe04c7ef4d3f7 | where on the foot represents the lymph nodes | ms_marco | Ranking Error | 1 |
| q_ea4188b095cf3814 | what does dysentery mean | ms_marco | Ranking Error | 1 |
| q_a76c3a74fb69318f | how much energy does an air conditioner use per hour | ms_marco | Ranking Error | 1 |
| q_bfbfe49e29d81e73 | why do they call it rubbing alcohol | ms_marco | Ranking Error | 1 |
| q_8496c1cd4a88e1ab | do black holes grow | ms_marco | Ranking Error | 1 |
| q_0992f5dc513cbd29 | what is a catalase positive result | ms_marco | Ranking Error | 1 |
| q_643f198ab9608dba | what is neuromuscular therapy | ms_marco | Ranking Error | 1 |
| q_a73f49d982d55d06 | definition of prothrombin gene mutation | ms_marco | Ranking Error | 1 |
| q_78f05274da76e7fd | where does the bilby live | ms_marco | Ranking Error | 1 |
| q_9ae1636bcd6f343c | what causes the chemical reaction of carbonated water | ms_marco | Ranking Error | 1 |
| q_d1a9a955bde086b4 | pitambari name meaning | ms_marco | Ranking Error | 1 |
| q_617eac3f6627bfc3 | what is the origin of the name Belgae | ms_marco | Ranking Error | 1 |
| q_273e3ec14639861f | is yellow loosestrife invasive | ms_marco | Semantic Miss | 0 |
| q_11524b3c9c39cdcf | what proteins are directly affected by ADH | ms_marco | Ranking Error | 1 |
| q_1d5dcd9fa12a21bd | what is the max deduction for charitable donations | ms_marco | Ranking Error | 1 |
| q_45766b213029536b | what is dipladenia plant | ms_marco | Ranking Error | 1 |
| q_13c65abbb53cc32e | what does pityriasis alba look like | ms_marco | Ranking Error | 1 |
| q_fd120e3a35924df3 | does greek yogurt contain probiotics | ms_marco | Ranking Error | 1 |
| q_12f0fd05a7ba5cff | average cost attorney to prepare deed | ms_marco | Ranking Error | 1 |
| q_5616bd32d77b1b56 | what biome is the hoh rainforest | ms_marco | Ranking Error | 1 |
| q_72048e3c7dec4af8 | can polycrylic be used over oil based stain | ms_marco | Ranking Error | 1 |
| q_b4944c4bc02fc2fe | what class of drugs is gabapentin | ms_marco | Ranking Error | 1 |
| q_6f87e0b1ed34f2fd | usda pork loin temperature | ms_marco | Ranking Error | 1 |
| q_d0c86d0936219a9c | is charles lubbe banting a qualified doctor | ms_marco | Ranking Error | 1 |
| q_613b3d1d3c27d1f9 | what show is on at the bellagio las vegas | ms_marco | Ranking Error | 1 |
| q_fb65a665bdf8980f | did the Equal rights amendment ever get passed | ms_marco | Ranking Error | 1 |
| q_15aff93aee00ba0c | average salary for financial analyst | ms_marco | Ranking Error | 1 |
| q_56d4c520060be2ca | meaning of gloom | ms_marco | Ranking Error | 1 |
| q_acd669475edebc1a | what age can my puppy go on a walk | ms_marco | Ranking Error | 1 |
| q_fc8d28f8a01a579c | how much money do you get as a mechanical engineer | ms_marco | Ranking Error | 1 |
| q_290acf0647f1b970 | what helps with mood swings during pms | ms_marco | Ranking Error | 1 |
| q_a58661b06f0912b8 | causes of sensitive skin | ms_marco | Ranking Error | 1 |
| q_a8581f96f8b19db1 | what are the adaptation of a cassowary | ms_marco | Ranking Error | 1 |
| q_2c354254673de24d | what types of movements are observed in transport of bedload | ms_marco | Ranking Error | 1 |
| q_9e5d464544d60a5f | sachin cast tamil | ms_marco | Ranking Error | 1 |
| q_f5a5c068d3643245 | why did ancient rome build aqueducts | ms_marco | Ranking Error | 1 |
| q_fa8efd8ae82ef27b | difference between grams and grams force | ms_marco | Ranking Error | 1 |
| q_3f05c4ac190472bf | how to care for indoor potted basil plant | ms_marco | Ranking Error | 1 |
| q_825d3f1a87824900 | what is the average cost of a condo in miami | ms_marco | Ranking Error | 1 |
| q_e4ae3b12648a4177 | why is linen used | ms_marco | Ranking Error | 1 |
| q_4abf8c90b426c0bf | salary of civil engineering technician | ms_marco | Ranking Error | 1 |
| q_2a1119e4bef8f90f | where does the word clew come from | ms_marco | Ranking Error | 1 |
| q_2a28411d439e11c6 | what is considered a raised temperature | ms_marco | Ranking Error | 1 |
| q_c505b24e40ae6568 | which of the following endocrine glands is located in the neck | ms_marco | Ranking Error | 1 |
| q_2492b068e5521c38 | what is a pear shaped diamond called | ms_marco | Ranking Error | 1 |
| q_d6e2e0a77d046eb5 | australian carpenter salary range | ms_marco | Ranking Error | 1 |
| q_b0b724c82da3d82d | vaginoplasty cost | ms_marco | Ranking Error | 1 |
| q_fd49bea23defe14d | how long is cooked chicken good for in fridge | ms_marco | Ranking Error | 1 |
| q_a10aab0d10d682cd | what fault is near ecuador | ms_marco | Ranking Error | 1 |
| q_3df3ec103e9220fa | cost of milk production in india | ms_marco | Ranking Error | 1 |
| q_2356f89a214037dd | what is an erv | ms_marco | Ranking Error | 1 |
| q_b1c206d4edc8b6bd | how close can you plant poplar trees | ms_marco | Ranking Error | 1 |
| q_6ddd65f67bb2ff43 | why did they invent the telephone | ms_marco | Ranking Error | 1 |
| q_bf1abb89f5b8346d | what is a pole hem on a flag | ms_marco | Ranking Error | 1 |
| q_791517b04cc07025 | types of precancerous skin cancer | ms_marco | Ranking Error | 1 |
| q_dd2ba0b35bae827d | average lifespan of builder grade carpet | ms_marco | Ranking Error | 1 |
| q_fde3766fc80f13e5 | what sports do sri lanka play | ms_marco | Ranking Error | 1 |
| q_4d344568a1a8b2e9 | what is a boutique owner called | ms_marco | Ranking Error | 1 |
| q_3b364fbe891f73a4 | what was the manifesto of surrealism | ms_marco | Ranking Error | 1 |
| q_3436d11b956961eb | how many types of nucleotides are in dna and how do they differ | ms_marco | Semantic Miss | 0 |
| q_3c5147e044b8d154 | is there a way to find the owner of a cell phone number | ms_marco | Ranking Error | 1 |
| q_67efed161b611f7a | how to become a parole officer | ms_marco | Ranking Error | 1 |
| q_9b799cea73398ad5 | what stone to use for a walkway | ms_marco | Ranking Error | 1 |
| q_198b3328ac2c407f | can other fish be placed with bala sharks | ms_marco | Ranking Error | 1 |
| q_456b9863d310e178 | what is fluorspar | ms_marco | Ranking Error | 1 |
| q_381e9c52e0141d25 | what is travel retail industry | ms_marco | Ranking Error | 1 |
| q_7685289463622991 | what does virtue means | ms_marco | Semantic Miss | 0 |
| q_ec3fc62304689322 | medication percodan what condition | ms_marco | Ranking Error | 1 |
| q_a11c9360157c054e | how to like a page on facebook without friends seeing it | ms_marco | Ranking Error | 1 |
| q_239d12319a74647f | does cerebrospinal fluid contain white blood cells | ms_marco | Semantic Miss | 0 |
| q_29b2bc2ce6c220a8 | why is it necessary that we have a transport system in the human body | ms_marco | Ranking Error | 1 |
| q_7ce5327bbbae2d4f | is english a nationality | ms_marco | Ranking Error | 1 |
| q_4336edef89b70dc4 | What is another word for diatom? | squad | Semantic Miss | 0 |
| q_c65495430896e380 | what is blood occult mean | ms_marco | Ranking Error | 1 |
| q_6134e058a61406f7 | how big is a nanometer | ms_marco | Ranking Error | 1 |
| q_4488ea9974639edb | what vitamins are good for splitting nails | ms_marco | Ranking Error | 1 |
| q_86b7c4f0ee017fc3 | what species are jaguars | ms_marco | Ranking Error | 1 |
| q_3ccb983ed14a57bf | how much does it cost to run a street light | ms_marco | Ranking Error | 1 |
| q_4bf9b70cf78a179c | how long does it take an lcl sprain to heal | ms_marco | Ranking Error | 1 |
| q_ef80889c26fe0ce6 | what kingdom are plants in | ms_marco | Ranking Error | 1 |
| q_b868958e4b070102 | gene family definition | ms_marco | Ranking Error | 1 |
| q_aa98f72f7536337e | who is the deputy taoiseach | ms_marco | Semantic Miss | 0 |
| q_cb2cb8a4a15b1fdd | what is the minimum temperature for an office environment | ms_marco | Ranking Error | 1 |
| q_ec3d04007c993641 | how long to grill thin steak | ms_marco | Ranking Error | 1 |
| q_2412282b20f55921 | what is personality disorder traits | ms_marco | Ranking Error | 1 |
| q_57672028d024324a | What is the edcuation system currently? | squad | Ranking Error | 1 |
| q_e6c47780bf514095 | does magnetic flux produce a current | ms_marco | Ranking Error | 1 |
| q_865327d906b7b393 | shoulder replacement how long driving | ms_marco | Ranking Error | 1 |
| q_c53ba5670ebee729 | how much time is needed to digest food for hours take | ms_marco | Ranking Error | 1 |
| q_0e31fd8eebd4ec0b | how to be invulnerable in life | ms_marco | Ranking Error | 1 |
| q_34f2a5b8c96991d0 | average cost to lay carpet | ms_marco | Ranking Error | 1 |
| q_488f70a4bf41ebf2 | can thrush comes through kissing | ms_marco | Ranking Error | 1 |
| q_17b84bf46daf3ff3 | what is duration risk | ms_marco | Ranking Error | 1 |
| q_1de53d06a39662c1 | what is kosher gelatin | ms_marco | Ranking Error | 1 |
| q_e14c271af413201e | statistics on energy consumption in the united states | ms_marco | Ranking Error | 1 |
| q_0e5a062bce9505f1 | is there a medication called pileri? | ms_marco | Semantic Miss | 0 |
| q_ee82e272710a3611 | what causes pressure on the groin in women | ms_marco | Ranking Error | 1 |
| q_45d5ff0f58c474f7 | what is electric charge physics | ms_marco | Ranking Error | 1 |
| q_59800557ec4050da | The motion of stars in galaxies imply that there is about 10 times as much what as in the luminous objects we can see? | sciq | Semantic Miss | 0 |
| q_81f2d9791a875c94 | define adaptive immunity | ms_marco | Ranking Error | 1 |
| q_265b485cee9055b8 | what is the correct name for the eardrum | ms_marco | Ranking Error | 1 |
| q_7b69b8d4b71150b1 | what was the formation of the united nations | ms_marco | Ranking Error | 1 |
| q_025c5696fe7c7455 | prion disease definition | ms_marco | Ranking Error | 1 |
| q_92bdf15d033f730f | where would peasants live | ms_marco | Ranking Error | 1 |
| q_58cb0c3570ea4672 | what is a borough | ms_marco | Semantic Miss | 0 |
| q_92e84dbf8e75f75e | where can stem cells be found in human body | ms_marco | Ranking Error | 1 |
| q_0e6c4a40c95b7e58 | In US dollars what is the most money ever paid for a bluefin tuna in Japan | ms_marco | Ranking Error | 1 |
| q_1b963797ae09b9b8 | cultural intrusion definition | ms_marco | Ranking Error | 1 |
| q_799a681b83cbf5e3 | shorter university tuition cost | ms_marco | Ranking Error | 1 |
| q_e6f7f19379094d82 | what does ach manager mean | ms_marco | Semantic Miss | 0 |
| q_f67a240e6efc4611 | what benefited from reconstruction finance corporation created by president hoover who benefited from this program | ms_marco | Ranking Error | 1 |
| q_f762078c74b6d002 | meaning name darren | ms_marco | Ranking Error | 1 |
| q_137095b940bde925 | are there inherited ira early withdrawal penalties | ms_marco | Ranking Error | 1 |
| q_c79d0213f4d7775a | how is employment range for ekg technician | ms_marco | Ranking Error | 1 |
| q_3b7e563cbe676452 | what are symptoms of pancreatitis | ms_marco | Ranking Error | 1 |
| q_6d1c6a40f25aea5e | legal age a child can stay home alone in louisiana | ms_marco | Ranking Error | 1 |
| q_7465922dde365bcf | what types of volcanic rock are found at divergent plate boundaries | ms_marco | Ranking Error | 1 |
| q_b3a2500697cc7741 | salary for associates degree | ms_marco | Ranking Error | 1 |
| q_bd5d9eacf81d6c8f | what is a unicorn | ms_marco | Ranking Error | 1 |
| q_0ff2137829595b1a | When did Zhenjin die? | squad | Semantic Miss | 0 |
| q_bc26254e48d0b3a4 | how many ml equals an ounce | ms_marco | Ranking Error | 1 |
| q_21503eded5ecba10 | psyllium husk fiber | ms_marco | Ranking Error | 1 |
| q_f696c05e31f71bc7 | what does phosphate do for grass | ms_marco | Ranking Error | 1 |
| q_e491dd191595d07e | what is vzw airwaves | ms_marco | Ranking Error | 1 |
| q_ad495d4873f78610 | how to invest ira roth | ms_marco | Semantic Miss | 0 |
| q_9a0e1c5175896bcb | michael chiklis played in what shows | ms_marco | Ranking Error | 1 |
| q_fea5358a436bc6a2 | how long does it take a baby tortoise to grow | ms_marco | Ranking Error | 1 |
| q_bc831496da7baf33 | what are bacterial virulence factors | ms_marco | Ranking Error | 1 |
| q_e2664b4940ac658c | how long does a ctc check take | ms_marco | Semantic Miss | 0 |
| q_e973d8aac3f4d9b2 | where is ilwaco washington | ms_marco | Ranking Error | 1 |
| q_600cd3a78ba97dde | how much does it cost for someone to put up a retaining wall | ms_marco | Ranking Error | 1 |
| q_31370518463294ae | what foods do weevils get into | ms_marco | Ranking Error | 1 |
| q_990aea73cb543583 | how much does Pharmacy Technician make | ms_marco | Ranking Error | 1 |
| q_4d358f11e992cc89 | biological therapy definition | ms_marco | Ranking Error | 1 |
| q_9117e1fa6b6cb3b2 | what size is mercury | ms_marco | Semantic Miss | 0 |
| q_8f09af111c160c6b | how many people get aids a year | ms_marco | Ranking Error | 1 |
| q_3b3005064b17b893 | what is e dispar | ms_marco | Ranking Error | 1 |
| q_49ff156447c69c3e | what is sap in business | ms_marco | Ranking Error | 1 |
| q_3aada57c9e4593a2 | which kind of minerals are most common on earth | ms_marco | Ranking Error | 1 |
| q_c262b8fc93ef14b5 | what is zinc oxide used for | ms_marco | Ranking Error | 1 |
| q_e1461f6945d0705c | what causes enlarged thyroid in neck | ms_marco | Ranking Error | 1 |
| q_4edaeb1dddab1e9c | bhavin name meaning | ms_marco | Ranking Error | 1 |
| q_f37fae0c84a66488 | average price of a kayak pool | ms_marco | Ranking Error | 1 |
| q_58e37ba3fd084738 | what hormone is responsible for decreasing blood glucose levels | ms_marco | Ranking Error | 1 |
| q_691cc52250de0a17 | what group does the squirrel monkey belong to | ms_marco | Ranking Error | 1 |
| q_301d5019fd0e7302 | what organism is Saimiri boliviensis boliviensis | ms_marco | Ranking Error | 1 |
| q_8913677d83f1e660 | what is foh manager | ms_marco | Ranking Error | 1 |
| q_b1299452d9064132 | what is cloudfront | ms_marco | Ranking Error | 1 |
| q_81d20b444b2a4408 | how much money does a dental assistant make a year | ms_marco | Ranking Error | 1 |
| q_0fd3de164d4181d0 | what kind of lavender is the most fragrant | ms_marco | Ranking Error | 1 |
| q_acfb59c8c9d7f5e0 | what is a turducken | ms_marco | Ranking Error | 1 |
| q_361b16c9067c5762 | how long do pickled eggs last in fridge | ms_marco | Ranking Error | 1 |
| q_95efa2fb3967baa1 | what is the difference between sms and mms | ms_marco | Ranking Error | 1 |
| q_391014049fbaada2 | colonoscopy procedure how long does it take | ms_marco | Ranking Error | 1 |
| q_fe8017553cbf0a23 | the name tayla meanings | ms_marco | Ranking Error | 1 |
| q_b894a3b9c3834bf0 | What are injectors used to supply? | squad | Semantic Miss | 0 |
| q_865a2ee1dc7b24ee | what is omentum | ms_marco | Ranking Error | 1 |
| q_4152d4357076fffe | what is mexican accordion music called | ms_marco | Ranking Error | 1 |
| q_29d088a8ffc95b19 | what does a transportation coordinator do | ms_marco | Ranking Error | 1 |
| q_bf92cb53e0fa8ce8 | what does azra mean in arabic | ms_marco | Ranking Error | 1 |
| q_6abe5be80de6bfce | How many volumes are contained in the library? | squad | Semantic Miss | 0 |
| q_b44f9f4382c22c91 | openreach customer service number | ms_marco | Ranking Error | 1 |
| q_007a3570a25768b9 | meaning of name teia | ms_marco | Ranking Error | 1 |
| q_6e18065fd530c7d1 | what is a normal amount of steps per day | ms_marco | Ranking Error | 1 |
| q_3f7e4fdea0906d0b | what is protected extensible authentication protocol | ms_marco | Ranking Error | 1 |
| q_7e2fa3435fc38f5d | temp settings for baking a chicken | ms_marco | Semantic Miss | 0 |
| q_deac9c9756692142 | what causes discoloration of toenails | ms_marco | Ranking Error | 1 |
| q_80129bb8ac95e029 | what size is the human eyeball | ms_marco | Ranking Error | 1 |
| q_223e0e277c2844b5 | what kind of symmetry do grasshoppers have | ms_marco | Ranking Error | 1 |
| q_ba6b153d0a1c1ed8 | how much do marketers earn | ms_marco | Ranking Error | 1 |
| q_ec73552b1c718e84 | what does corporate governance include | ms_marco | Semantic Miss | 0 |
| q_91f5d0903bbc88c8 | when do you take cold eeze | ms_marco | Ranking Error | 1 |
| q_ea5f300174c4d027 | what does a naturopath do | ms_marco | Semantic Miss | 0 |
| q_271f7a2e222994a3 | what are intermediate rocks | ms_marco | Semantic Miss | 0 |
| q_5dd6298a10947cb2 | how long does it take to get medical assistant online | ms_marco | Ranking Error | 1 |
| q_c89ae4f5f3b3e181 | what is a paralegal degree | ms_marco | Ranking Error | 1 |
| q_503166a31bef4189 | where is abruzzo italy | ms_marco | Semantic Miss | 0 |
| q_d2da77582fe31396 | what does agalychnis mean | ms_marco | Ranking Error | 1 |
| q_6f3ff3565286ecc2 | how much space do you need above a refrigerator | ms_marco | Ranking Error | 1 |
| q_48fdafa9fb97376a | cost to obtain private pilots license | ms_marco | Ranking Error | 1 |
| q_4a58d6117d88528c | what does a wolf spider look like | ms_marco | Ranking Error | 1 |
| q_65b99c7a9314762a | what does clustering mean | ms_marco | Ranking Error | 1 |
| q_ad5ba9e5de877a59 | how to improve iq | ms_marco | Ranking Error | 1 |
| q_602f6ba933b62456 | the molten rock that flows from a volcano is called what | ms_marco | Ranking Error | 1 |
| q_b0d0a37d011b0bf7 | what structure do traditional turkey music use? | ms_marco | Ranking Error | 1 |
| q_72eee26ebfe2e5a7 | starting salary for dialysis nurse | ms_marco | Ranking Error | 1 |
| q_6de1208d5e396e75 | normal pulse rate in adults | ms_marco | Ranking Error | 1 |
| q_fb72a9e40d1aaa2d | what does salinity mean | ms_marco | Ranking Error | 1 |
| q_a1c24c4dd4695523 | how long will food keep in the upright freezer without power | ms_marco | Ranking Error | 1 |
| q_43aed692dcf95efe | how long to cook brisket in oven | ms_marco | Ranking Error | 1 |
| q_c6863f192ecee191 | how long will soup keep in the fridge | ms_marco | Ranking Error | 1 |
| q_c252881073119ca0 | how long does geese eggs take to hatch | ms_marco | Ranking Error | 1 |
| q_4791331efe259bfa | what are the types of creatinine kinase | ms_marco | Semantic Miss | 0 |
| q_16b09a79860eef6e | zygomaticus muscles definition | ms_marco | Ranking Error | 1 |
| q_967fb0d2824b6728 | what is microscopic colitis disease | ms_marco | Ranking Error | 1 |
| q_c0f1e7ac126f81df | how much is greek theatre parking | ms_marco | Ranking Error | 1 |
| q_f6f4a7299d55b6d0 | are mastiffs dangerous | ms_marco | Ranking Error | 1 |
| q_02ee536929d1378c | what are the types of parvo? | ms_marco | Semantic Miss | 0 |
| q_280e4fd14538c2d1 | does medicaid pay for dentures | ms_marco | Ranking Error | 1 |
| q_06a6a662ecda1751 | how much should i pay for a will | ms_marco | Ranking Error | 1 |
| q_8b7fb9aea7b0afc5 | In which year was the Salting Bequest? | squad | Ranking Error | 1 |
| q_d9b0051c5458982c | does late payments affect your credit score | ms_marco | Semantic Miss | 0 |
| q_fca86fa2616b578a | the top leader in that's running for president | ms_marco | Ranking Error | 1 |
| q_6900afc2fdf20a9c | how much humidity do chicken eggs need | ms_marco | Ranking Error | 1 |
| q_fed2ffa5428f44fa | what kind of dog does jennifer aniston have | ms_marco | Ranking Error | 1 |
| q_25876236ce8ec358 | what is a routed network | ms_marco | Ranking Error | 1 |
| q_b989f1912853483a | which hormone is responsible for eating | ms_marco | Ranking Error | 1 |
| q_94e1b212b39f7caa | definition of muscle pain | ms_marco | Ranking Error | 1 |
| q_45c66f71b11948bd | what constitutes a scientific name | ms_marco | Semantic Miss | 0 |
| q_f662b89f1e80b141 | define causality | ms_marco | Ranking Error | 1 |
| q_e2f51e625096c277 | cozumel weather in february | ms_marco | Ranking Error | 1 |
| q_44aedae3a10512f3 | what system are affected by heart diseases | ms_marco | Ranking Error | 1 |
| q_3ca1dc99d90d178d | what does a trapeze artist wear | ms_marco | Ranking Error | 1 |
| q_5b14d0f832bf245a | relative humidity vs absolute humidity | ms_marco | Ranking Error | 1 |
| q_51329a2294634669 | what does MENSA mean | ms_marco | Ranking Error | 1 |
| q_a7ea92ff92d448c3 | cost of fence installation | ms_marco | Ranking Error | 1 |
| q_9226e20267cfe13c | types of toxins produced by snakes | ms_marco | Ranking Error | 1 |
| q_efd48d6ccbcd534f | what are some perpetual resources | ms_marco | Ranking Error | 1 |
| q_a1f09ab1be308664 | best over the counter pain meds for arthritis | ms_marco | Ranking Error | 1 |
| q_b7f4ab722290ac95 | foods that are bad for gout | ms_marco | Ranking Error | 1 |
| q_2f06294880a8d8c8 | how is the great barrier reef managed | ms_marco | Semantic Miss | 0 |
| q_e82a0d12ea7772e1 | the delicate layer of the meninges closely applied to the brain is | ms_marco | Ranking Error | 1 |
| q_5274a4db0c9b6d2e | what nutrients does a teenager need | ms_marco | Semantic Miss | 0 |
| q_f080f26f9050e325 | when were airbags developed | ms_marco | Semantic Miss | 0 |
| q_9cab19bfb1abb287 | how many degrees fahrenheit for child fever | ms_marco | Ranking Error | 1 |
| q_379ec40b6982d02a | what is contribution contribution | ms_marco | Ranking Error | 1 |
| q_ef5bf467dc27af5d | why is the river severn called the river severn | ms_marco | Semantic Miss | 0 |
| q_676fd2c7abb05851 | what is an endowment plan | ms_marco | Ranking Error | 1 |
| q_d07c4a35af9180c1 | how long does a roast chicken last in the refrigerator | ms_marco | Semantic Miss | 0 |
| q_10f2a7e5a6021528 | how long does it take a baby duck to hatch | ms_marco | Ranking Error | 1 |
| q_a5965c67d90b75ae | do you need power meter for your road bike | ms_marco | Ranking Error | 1 |
| q_40070248971a1c95 | where is gallaudet university located | ms_marco | Ranking Error | 1 |
| q_1e5df2c2b30ef756 | what does secretions mean | ms_marco | Ranking Error | 1 |
| q_cbb3472606b592cf | what is dk | ms_marco | Ranking Error | 1 |
| q_af8a8394438bdc66 | hydronic heating cost | ms_marco | Ranking Error | 1 |
| q_51f1ce75ce93c889 | how i can make money fast | ms_marco | Ranking Error | 1 |
| q_62ce4a803e729701 | why was the heian period given its name | ms_marco | Ranking Error | 1 |
| q_bf0720a9cb798633 | what is a two digit numbers | ms_marco | Ranking Error | 1 |
| q_6b3bc4a05593313f | what is an average amount to spend on health insurance a month | ms_marco | Ranking Error | 1 |
| q_f8b0a54d69c3cf5b | is protaras in larnaca | ms_marco | Ranking Error | 1 |
| q_1a175909ae3a814d | where was chayanne born | ms_marco | Ranking Error | 1 |
| q_0d844fe3382981c4 | what kind of mining is bentonite | ms_marco | Ranking Error | 1 |
| q_d995105152893cfd | dog gestation period | ms_marco | Ranking Error | 1 |
| q_fa0f94289aafeff4 | what is destination imagination | ms_marco | Ranking Error | 1 |
| q_50c2d5295d993ccd | how long can you keep chicken cutlets in the freezer | ms_marco | Ranking Error | 1 |
| q_f4506271d6b90120 | food that arizona is known for | ms_marco | Ranking Error | 1 |
| q_7f9095ad288e5975 | typical underwriting fee | ms_marco | Ranking Error | 1 |
| q_c5e61540af22843d | who was in the limo when jfk was shot | ms_marco | Ranking Error | 1 |
| q_e69c896199fb8e93 | what bacteria causes osteomyelitis | ms_marco | Ranking Error | 1 |
| q_a1cea5315b148227 | where in the brain are eye movements controlled | ms_marco | Ranking Error | 1 |
| q_c2657ca27c72c3d4 | what does hip do | ms_marco | Ranking Error | 1 |
| q_daea9d858a25f34b | what kind of disorder is adhd | ms_marco | Ranking Error | 1 |
| q_ffd06f946ac08dc4 | What are the names of the salivary glands located anterior to the ear | ms_marco | Ranking Error | 1 |
| q_36fd09e76a107cb1 | how can you become a faster reader | ms_marco | Ranking Error | 1 |
| q_984088097c6931ee | what is barramundi | ms_marco | Ranking Error | 1 |
| q_08b69617dc9cba84 | average cost for cal lutheran university | ms_marco | Semantic Miss | 0 |
| q_9908843f2aa4f143 | how to use movie maker | ms_marco | Ranking Error | 1 |
| q_59c931e7971b56a0 | what was the goal of the prohibition movement | ms_marco | Ranking Error | 1 |
| q_15212b9c162bee09 | how to get through the Earth's crust | ms_marco | Ranking Error | 1 |
| q_16daeb3dcadc47df | Test WiFi Signal Strength | ms_marco | Ranking Error | 1 |
| q_dddf3999f73bbec2 | what causes a hoarse voice | ms_marco | Ranking Error | 1 |
| q_8059c8193c828a55 | push definition | ms_marco | Ranking Error | 1 |
| q_8981812ece310919 | what vitamins are in fresh pineapple | ms_marco | Ranking Error | 1 |
| q_066f89516ad8df05 | is myalgia contagious | ms_marco | Ranking Error | 1 |
| q_fe5ab39568af46cf | meaning of the name ethan | ms_marco | Ranking Error | 1 |
| q_87112b22a855ada8 | does tesla negotiate price | ms_marco | Ranking Error | 1 |
| q_5dceea50e5dbc892 | Where did Tesla work in 1888? | squad | Ranking Error | 1 |
| q_d85d638016c1fc76 | what is the average attention span of a child | ms_marco | Ranking Error | 1 |
| q_9f9cb7666eae8dd1 | can quadratic equation be used without b | ms_marco | Ranking Error | 1 |
| q_5b628194ae7eca1d | what creates earthquakes | ms_marco | Semantic Miss | 0 |
| q_f9d31c6d514ee0ba | do earnings in a roth ira get taxed | ms_marco | Ranking Error | 1 |
| q_cac1a13ffa016cb7 | what is a desert rose | ms_marco | Ranking Error | 1 |
| q_4cb0c2e1b018301a | types of onions names | ms_marco | Ranking Error | 1 |
| q_365cc7cbcfbdf848 | genus name for algae | ms_marco | Ranking Error | 1 |
| q_5d1e2890c956a509 | tsh blood test normal range | ms_marco | Ranking Error | 1 |
| q_351d910832f84e37 | what is rhodium plate | ms_marco | Semantic Miss | 0 |
| q_517d9a1aee8d8faf | what is plexus for | ms_marco | Ranking Error | 1 |
| q_5b81bf59cdbf4e40 | what particles make up a proton | ms_marco | Ranking Error | 1 |
| q_01f56e80c6f2bb2b | what is the fee for return receipt for usps mail | ms_marco | Ranking Error | 1 |
| q_d8e0a5db53a39b98 | what continent is australia | ms_marco | Ranking Error | 1 |
| q_fd4dbaa564d3c0ab | what does a tectonic plate do | ms_marco | Ranking Error | 1 |
| q_d83a80f3c8238dfa | what is mojo mean | ms_marco | Ranking Error | 1 |
| q_f0088e3090f9b327 | how to estimate what my business is worth | ms_marco | Ranking Error | 1 |
| q_60276382d2e45c60 | what is mousseline buttercream | ms_marco | Ranking Error | 1 |
| q_c83bc67fe085e153 | who made the enigma machine | ms_marco | Ranking Error | 1 |
| q_7ad3f38e66198402 | what were yorkshire terriers bred for | ms_marco | Ranking Error | 1 |
| q_0075e454d8d94583 | what kinds of food it bad for the heart | ms_marco | Ranking Error | 1 |
| q_9df7c45b7dddf1b0 | where does the southern accent come from | ms_marco | Ranking Error | 1 |
| q_3849a0c983b24ba8 | how long does a college lacrosse game last | ms_marco | Ranking Error | 1 |
| q_bac05ea87c1f9825 | how to marinate steak for grilling | ms_marco | Ranking Error | 1 |
| q_6f701d1fa3645a77 | career in sonography salary | ms_marco | Ranking Error | 1 |
| q_4dd3bd4693433d6d | Who officially opened the V&A? | squad | Ranking Error | 1 |
| q_9a4cb3d31d901b53 | osceola indiana raceway is in what county | ms_marco | Ranking Error | 1 |
| q_47d53afc850866bb | new driveway cost | ms_marco | Ranking Error | 1 |
| q_94a1962e20e12280 | what are the uses of radon | ms_marco | Ranking Error | 1 |
| q_b11a03943e015c45 | where and who does gray wolf find its food | ms_marco | Ranking Error | 1 |
| q_05471359d57756e0 | What is the name of San Francisco's stadium when looked at as a possibility for Super Bowl 50? | squad | Semantic Miss | 0 |
| q_4d86e7fb3081ebf1 | what is carbon hydroxide | ms_marco | Ranking Error | 1 |
| q_ec5d378755b76471 | what kind of romex for outlets | ms_marco | Ranking Error | 1 |
| q_f1d9aecff9819052 | what is an algebraic expression | ms_marco | Ranking Error | 1 |
| q_070104e2cf60cd1d | how long is cooked shrimp good for in refrigerator | ms_marco | Ranking Error | 1 |
| q_74f10035d121b6eb | average temperature in vero beach florida in june | ms_marco | Ranking Error | 1 |
| q_f13c9261348344b3 | requirements for being a correctional officer | ms_marco | Semantic Miss | 0 |
| q_61edaa50683486fc | meanings of armenian name marianna | ms_marco | Ranking Error | 1 |
| q_7ab03c02643be828 | age of earth bible | ms_marco | Ranking Error | 1 |
| q_0fc2dd0c48c3625d | who invented cotton candy | ms_marco | Semantic Miss | 0 |
| q_082acbc1ef964f30 | steam cleaning carpet pesticides | ms_marco | Ranking Error | 1 |
| q_a516c310cd0a2fef | average cost to polish concrete per square meter | ms_marco | Ranking Error | 1 |
| q_7cfbdec812a4d48d | is palawan dangerous | ms_marco | Ranking Error | 1 |
| q_7fa86557c4840c1f | Water infiltrates the ground because soil and rock may have air spaces between the grains. these pores, or tiny holes, result in the rock's what? | sciq | Semantic Miss | 0 |
| q_ee62795f0f9cdd17 | what is dhcp relay | ms_marco | Ranking Error | 1 |
| q_0bdd8a593600871a | who is the grantor of trust | ms_marco | Ranking Error | 1 |
| q_ea71699e020382ea | what cow does water buffalo resemble | ms_marco | Ranking Error | 1 |
| q_4558ea1730d342a1 | in what type of blood vessels are materials exchanged with the body cells | ms_marco | Ranking Error | 1 |
| q_e20e26ddb108db21 | who invented induced currents | ms_marco | Ranking Error | 1 |
| q_40fa7480674d4f92 | what is sitz bath | ms_marco | Ranking Error | 1 |
| q_57f6e6f38cb97c7d | what structure is modified in crayfish | ms_marco | Ranking Error | 1 |
| q_27f6f110c7bc5b31 | what is benzedrine | ms_marco | Ranking Error | 1 |
| q_b74c36a025f58348 | Staph infection is it contagious | ms_marco | Ranking Error | 1 |
| q_12faa5b8814623a1 | how long will homemade vegetable soup keep in the fridge | ms_marco | Ranking Error | 1 |
| q_4cf4351d4b6ff4bc | is larnaca in ayia napa | ms_marco | Ranking Error | 1 |
| q_978ff5e2dbca2aa6 | where do pumice stones originate | ms_marco | Ranking Error | 1 |
| q_e889f9f6a1c41a6c | how long does it take for a female dog to heal after spaying | ms_marco | Ranking Error | 1 |
| q_8d6c2773bb1096a5 | what type of tissue is the wall of the heart made of | ms_marco | Ranking Error | 1 |
| q_83a6d9461f49e827 | what is the average pay for a hotel manager | ms_marco | Ranking Error | 1 |
| q_e72c47aed3b5afca | what is the maximum amount of credit from residential energy credit | ms_marco | Semantic Miss | 0 |
| q_31c487175d60e2d5 | how much money do we spend because of obesity | ms_marco | Semantic Miss | 0 |
| q_bc8e0d18cfb0df8d | what is the average cost of cataract surgery in illinois | ms_marco | Ranking Error | 1 |
| q_d3b6097e5c82238c | how long can vegetarian chili stay in the fridge | ms_marco | Semantic Miss | 0 |
| q_1d6f49aa6a3531d3 | where does the horse originated from | ms_marco | Ranking Error | 1 |
| q_059767e0d2e38371 | how long it can take to get tax refund back | ms_marco | Ranking Error | 1 |
| q_6d552dca253d9f56 | what can you do if your employer fails to pay you | ms_marco | Ranking Error | 1 |
| q_3324286efe5a2207 | What natural destructive element cuts away at rock forming river valleys? | sciq | Semantic Miss | 0 |
| q_e8b8b3a330f57c58 | osteoarthritis usually is caused by | ms_marco | Ranking Error | 1 |
| q_f68f9a6316de7ba6 | how much does it cost for a crown without insurance | ms_marco | Ranking Error | 1 |
| q_cc043153f1f744d7 | do I need flood insurance | ms_marco | Ranking Error | 1 |
| q_16aa25f23380f894 | requirements for cosmetology instructor license in california | ms_marco | Ranking Error | 1 |
| q_b2c50d0a944fc33f | what does carino mean | ms_marco | Ranking Error | 1 |
| q_f7d46ddd6acccdf4 | writing numbers in expanded form examples | ms_marco | Ranking Error | 1 |
| q_db986748fd309ea7 | what type of archetypal hero is luke skywalker | ms_marco | Ranking Error | 1 |
| q_b4e9f8f4f844133b | list of foods that are starches | ms_marco | Ranking Error | 1 |
| q_54e1bd006b6f061a | what are schizophrenic hallucinations | ms_marco | Ranking Error | 1 |
| q_9d9ef07e6b05228a | nc jury duty age limit | ms_marco | Ranking Error | 1 |
| q_0569ea6fab69c230 | what are phenotypes | ms_marco | Semantic Miss | 0 |
| q_06c9bced5352a716 | what food has vitamin e | ms_marco | Ranking Error | 1 |
| q_6b3bdb3ac908ebd4 | what are the short branched extensions on a nerve called | ms_marco | Ranking Error | 1 |
| q_ea87b0ea34b1dc50 | what are legumes examples | ms_marco | Ranking Error | 1 |
| q_c918a507479252fe | spinal reflex definition | ms_marco | Ranking Error | 1 |
| q_b7736515c0f3b020 | how did the great depression affect germany | ms_marco | Semantic Miss | 0 |
| q_fcbc5d6787bc5fc4 | average dental implant cost | ms_marco | Ranking Error | 1 |
| q_5aa167b13ddd1f1e | what is chiropractic therapy | ms_marco | Ranking Error | 1 |
| q_54bd52122c5fa15b | what is tbt | ms_marco | Semantic Miss | 0 |
| q_626a5151d9d30df2 | what does conjunctivitis mean | ms_marco | Ranking Error | 1 |
| q_a6bba4de84bc26b4 | what are canadian lynx babies called | ms_marco | Ranking Error | 1 |
| q_ff414d5df7f1d778 | how to get from stuttgart to munich | ms_marco | Ranking Error | 1 |
| q_8ef3870f783fefb9 | what is education credentials meaning | ms_marco | Ranking Error | 1 |
| q_36914a7f83829971 | what is a pterodactyl dinosaur | ms_marco | Ranking Error | 1 |
| q_ec15527f3a7a4a31 | what does caloric testing show | ms_marco | Ranking Error | 1 |
| q_b37b6cf19e706c43 | how long does caffeine stay in your system for | ms_marco | Ranking Error | 1 |
| q_78e9a92da7e808d7 | can you deduct mileage on a rental car | ms_marco | Ranking Error | 1 |
| q_193ed4dc229b817f | what does foreign language mean | ms_marco | Ranking Error | 1 |
| q_bdde2ccb016bb2b8 | what does hydrogen mean | ms_marco | Ranking Error | 1 |
| q_09ad609f744c3cbb | what is papaver somniferum | ms_marco | Ranking Error | 1 |
| q_d9f6dd46fb3d611f | what is the bride entrance called | ms_marco | Ranking Error | 1 |
| q_11e4433a8b936a72 | major depressive disorder definition psychology | ms_marco | Ranking Error | 1 |
| q_b0b7b28b79a809d6 | can you make an ira contribution to a sep | ms_marco | Semantic Miss | 0 |
| q_3ba2b0df1853d2ae | do annelids have body segmentation | ms_marco | Ranking Error | 1 |
| q_95a117fadab69088 | what kind of volcano is yellowstone | ms_marco | Ranking Error | 1 |
| q_b4debf6dfdf1dfc4 | what is a powwow | ms_marco | Ranking Error | 1 |
| q_bddce7362ef80d6b | Create a tree.Alt | code_search_net | Semantic Miss | 0 |
| q_8c3771af2156b269 | what does a feather tattoo mean | ms_marco | Ranking Error | 1 |
| q_c749892de29c40ad | what is melaleuca products | ms_marco | Ranking Error | 1 |
| q_df6beef7c04ddbd3 | what are hotspots | ms_marco | Ranking Error | 1 |
| q_4a281662cd77094f | can child transfer tuition to parent | ms_marco | Ranking Error | 1 |
| q_274672a731de8c05 | how much does it cost to take a tenant to small claims court | ms_marco | Ranking Error | 1 |
| q_8f123b21aefb5607 | what does a thaad battery | ms_marco | Semantic Miss | 0 |
| q_192d61793b9e2ca8 | where is maldon salt from | ms_marco | Ranking Error | 1 |
| q_25478ce475a91dc7 | what type of blood cells does hiv attack | ms_marco | Semantic Miss | 0 |
| q_d49630a4427bebf9 | what is tympanic membrane | ms_marco | Ranking Error | 1 |
| q_46aab62abf49cc73 | espionage act definition us history | ms_marco | Semantic Miss | 0 |
| q_aed94e2be98e17d7 | what process produces zygotes what cells join or fuse | ms_marco | Ranking Error | 1 |
| q_0e2dc015cd35ac7f | What replaced the Sky+Box? | squad | Semantic Miss | 0 |
| q_bd7514e56f26222f | what does wheatgrass do | ms_marco | Semantic Miss | 0 |
| q_16211dfd0efc7f0e | are capillaries all throughout the body | ms_marco | Ranking Error | 1 |
| q_cc6e9a12ad4d7465 | shedding tissues (carbuncles) in eye | ms_marco | Ranking Error | 1 |
| q_6946e216e0f93534 | is the levator palpebrae superioris an extraocular muscle | ms_marco | Ranking Error | 1 |
| q_b3db01162a8fd3b1 | What is a hermaphrodite? | squad | Semantic Miss | 0 |
| q_2b7853a0cca14435 | haneefa name meaning in urdu | ms_marco | Ranking Error | 1 |
| q_5ebba86a0461303e | when was fontana dam built | ms_marco | Ranking Error | 1 |
| q_b8db4aed11f09862 | what is tomato rasam | ms_marco | Ranking Error | 1 |
| q_711e1535716638c9 | how long does a hep a vaccine last | ms_marco | Ranking Error | 1 |
| q_c141cae54ab5294c | what term is tranquility | ms_marco | Ranking Error | 1 |
| q_60525f42aaf1a964 | which fungi has flagellated spores | ms_marco | Ranking Error | 1 |
| q_702c92fb0372426e | how far is kangaroo island from adelaide | ms_marco | Ranking Error | 1 |
| q_788737da6db56412 | nerve disease caused by nutrient deficiencies | ms_marco | Ranking Error | 1 |
| q_2508257d099333a1 | what does catfishing mean | ms_marco | Ranking Error | 1 |
| q_87b6dcee630d7b4f | where does the coral snake live | ms_marco | Ranking Error | 1 |
| q_7c6464633b960f65 | buddhist symbol aum | ms_marco | Ranking Error | 1 |
| q_87b0e5a18cb65a55 | what is chamoy | ms_marco | Ranking Error | 1 |
| q_0a7b76a3e3a9c0a9 | top reasons for having pain in left heart | ms_marco | Ranking Error | 1 |
| q_a740a39ecfda1bbe | can i use email money transfer to send money to account in us | ms_marco | Ranking Error | 1 |
| q_c8c4cbe1a1381e88 | infection of respiratory tract caused by fungus | ms_marco | Ranking Error | 1 |
| q_2d443e10020450b3 | what does it cost to repair a rotator cuff tear? | ms_marco | Ranking Error | 1 |
| q_69398c19b294d5fe | does sore throat usually mean a cold | ms_marco | Ranking Error | 1 |
| q_c293e1e49f8efa01 | the other side lyrics evanescence | ms_marco | Ranking Error | 1 |
| q_66b0efe3c1bbac42 | what degree for patent law | ms_marco | Ranking Error | 1 |
| q_fffe928cec106ca4 | do planks work abs | ms_marco | Ranking Error | 1 |
| q_345b64f68f3b46f5 | did deaths by alcohol decreased during prohibition | ms_marco | Ranking Error | 1 |
| q_c8e9f3f33e2481ad | is detachment a symptom of anxiety | ms_marco | Ranking Error | 1 |
| q_5abed5b99d80179e | how long does it take to receive a package from japan to us | ms_marco | Ranking Error | 1 |
| q_85538c99a3f81e19 | where does bachata originate from | ms_marco | Ranking Error | 1 |
| q_0f712ef0524a0657 | what type of government did the phoenicians have | ms_marco | Ranking Error | 1 |
| q_92a55ac06daa038f | What is the only planet that is known to support life? | sciq | Semantic Miss | 0 |
| q_51e169b2e62044ff | how long do i cook boneless lamb leg | ms_marco | Ranking Error | 1 |
| q_82f2304a3d48f5b7 | what is the relation between annular pancreas and polyhydramnios | ms_marco | Ranking Error | 1 |
| q_3ce7e2ba88b63088 | rights based theory definition | ms_marco | Ranking Error | 1 |
| q_d130aeb2e2de17f2 | age recommendation for shingles shot | ms_marco | Ranking Error | 1 |
| q_4d2d4b1d66e6916f | what does the nucleus need to function | ms_marco | Ranking Error | 1 |
| q_c8e3928ca3698b7e | standard deduction for dependent | ms_marco | Ranking Error | 1 |
| q_4e32d3807c043a55 | what is an inguinal hernia how is it usually repaired | ms_marco | Ranking Error | 1 |
| q_91b44d5c14dbfb48 | when did married women get the right to own their own money | ms_marco | Ranking Error | 1 |
| q_73f3ef1d98103654 | where do bees usually live | ms_marco | Ranking Error | 1 |
| q_e728528c395b2e42 | what color is our blood | ms_marco | Ranking Error | 1 |
| q_00109567fd530123 | which neuron secretes neurotransmitters in light | ms_marco | Ranking Error | 1 |
| q_5c67de76fcb7ac8c | mean gene definition | ms_marco | Ranking Error | 1 |
| q_ed3b2d7131658a78 | poems punctuation rules | ms_marco | Ranking Error | 1 |
| q_ad7e73a96398c3a1 | how much does it cost to have a small tree removed | ms_marco | Ranking Error | 1 |
| q_655cf38b5c86ec52 | what is a variation definition | ms_marco | Ranking Error | 1 |
| q_8edbc7d814d923cc | what is echinacea angustifolia root | ms_marco | Ranking Error | 1 |
| q_a7510adbefcb4b79 | which type of blood vessel usually carries oxygen-rich blood | ms_marco | Ranking Error | 1 |
| q_0c964051d2c87b55 | where does lactase come from | ms_marco | Ranking Error | 1 |
| q_24121657f8d563c8 | transcription translation definition | ms_marco | Ranking Error | 1 |
| q_7af51babae00e6dd | definition of querulous? | ms_marco | Ranking Error | 1 |
| q_0b91aa0bf114c08b | What is the touch response in plants called? | sciq | Semantic Miss | 0 |
| q_39fe1f23d472ed56 | When was the Latin version of the word Norman first recorded? | squad | Semantic Miss | 0 |
| q_b9b03aa0a9f0e72e | how to mute on conference call | ms_marco | Ranking Error | 1 |
| q_4a7ff30ed2ac84d5 | klonopin normal dose | ms_marco | Ranking Error | 1 |
| q_42e7e03e2fe5108f | factory reset galaxy s3 | ms_marco | Ranking Error | 1 |
| q_043b06e37fb2c27a | should you rely on a compliance officer | ms_marco | Semantic Miss | 0 |
| q_510a454d7e4f1cba | what age are ira rmds mandatory | ms_marco | Ranking Error | 1 |
| q_d50f6e0cb9c048bc | could chlamydia be cured but have pid | ms_marco | Ranking Error | 1 |
| q_c2b7ff8955994205 | on average how long does first labour last from start to finish | ms_marco | Ranking Error | 1 |
| q_b0f0962a913dd06f | what is a microarray | ms_marco | Ranking Error | 1 |
| q_798a5d69532390f5 | typical balloon mortgage terms | ms_marco | Ranking Error | 1 |
| q_b6c13f9959aaa682 | is typhus contagious | ms_marco | Ranking Error | 1 |
| q_f1f9b2d811116b75 | what constitutes a persistent blood blister | ms_marco | Ranking Error | 1 |
| q_13ac889424267116 | how long does it take irs refund to be sent after return is approved | ms_marco | Semantic Miss | 0 |
| q_b2eff207e0e4d0b0 | what are the three types of vertebrae | ms_marco | Ranking Error | 1 |
| q_d258bec09dfb4315 | Who was Genghis's 3rd son? | squad | Semantic Miss | 0 |
| q_810c7f34f05f0f46 | what is combustion in chemistry | ms_marco | Ranking Error | 1 |
| q_1f268da41e05b0d7 | What color is phycoerytherin? | squad | Semantic Miss | 0 |
| q_f5a7d78238702243 | what kind of lake is lake simcoe | ms_marco | Semantic Miss | 0 |
| q_472b3f27efcec97e | how long does it take to recover from knee arthroscopy | ms_marco | Ranking Error | 1 |
| q_c622ee7b3f625ff7 | how did nafta affect united states | ms_marco | Semantic Miss | 0 |
| q_41406f4e278df2cd | rice phylum name | ms_marco | Ranking Error | 1 |
| q_de50691afc2e3ff0 | what is a methane hydrate | ms_marco | Ranking Error | 1 |
| q_176e70d569c7332b | how much does it cost for a hog roast | ms_marco | Ranking Error | 1 |
| q_20923a34e7d32847 | cast of the adventures of superman | ms_marco | Ranking Error | 1 |
| q_e9abc83331bc6807 | what is a pinecone | ms_marco | Ranking Error | 1 |
| q_4dbc0387e9319821 | does whole life insurance expire at a certain age | ms_marco | Ranking Error | 1 |
| q_7f92bd436ed188b7 | define angina pain | ms_marco | Ranking Error | 1 |
| q_3f6e567c06e2a7f8 | Like other bryophytes, moss plants spend most of their life cycle as what? | sciq | Semantic Miss | 0 |
| q_65a276c6bafeedfb | what is ceres | ms_marco | Semantic Miss | 0 |
| q_a6e92226ba5fd3c5 | rf cavity system | ms_marco | Semantic Miss | 0 |
| q_83d59f16275def75 | how do you know if a stamp is a forever stamp | ms_marco | Semantic Miss | 0 |
| q_aed65362304363f5 | At what point is water on the ph scale? | sciq | Semantic Miss | 0 |
| q_aa452636b4d9bccd | how many human organs are there | ms_marco | Ranking Error | 1 |
| q_4a7e7d89664a4a55 | do you need to fast for a lipid profile test | ms_marco | Semantic Miss | 0 |
| q_7952b5c2f612a106 | what is austenitic and martensitic | ms_marco | Ranking Error | 1 |
| q_c1e285685995ba24 | Where can you find more information on a country's practices? | squad | Semantic Miss | 0 |
| q_73f100c547e2619d | What is QED short for? | squad | Semantic Miss | 0 |
| q_b8b0ca7fff549bc6 | The nuclear envelope is a double-layered plasma membrane like the cell membrane, although without what? | sciq | Semantic Miss | 0 |
| q_357d1939f2d6eb1a | what situation caused the magna carta to be created | ms_marco | Ranking Error | 1 |
| q_02e75d15089fa5dc | the structure where urine is formed is the | ms_marco | Ranking Error | 1 |
| q_498304d49c820afd | how do you open a .paf file | ms_marco | Semantic Miss | 0 |
| q_43049b8a8d79c30a | how long is raw pork good for in the fridge | ms_marco | Ranking Error | 1 |
| q_4aac9ba3c1e91a63 | what features are found in theropods | ms_marco | Ranking Error | 1 |
| q_e210f922df355b78 | In Latin America what is the most revered skin color? | squad | Ranking Error | 1 |
| q_6022e8a4ff3f7652 | what is micronized progesterone | ms_marco | Ranking Error | 1 |
| q_4030a1c3e8827a7f | average salary for hgv driver | ms_marco | Ranking Error | 1 |
| q_a485195e836b29e7 | how many times are you supposed to be able to bench press your weight | ms_marco | Ranking Error | 1 |
| q_38683af63b09b69a | gestation period for wild rabbits | ms_marco | Ranking Error | 1 |
| q_ca1b8e65411a60ff | are polyunsaturated fats good | ms_marco | Ranking Error | 1 |
| q_59973303571af892 | who can prescribe in australia | ms_marco | Ranking Error | 1 |
| q_035846c697c2f95e | the are a series of fibrous connective tissue membranes covering | ms_marco | Ranking Error | 1 |
| q_a8fc4d7d455d6923 | where is rocky point located | ms_marco | Ranking Error | 1 |
| q_125fb07319e6e894 | what album is enter sandman on by metallica | ms_marco | Ranking Error | 1 |
| q_070da9d49b817f4f | what does trade name dba mean | ms_marco | Semantic Miss | 0 |
| q_34ff831827166f16 | how long can a body survive without food and water | ms_marco | Ranking Error | 1 |
| q_f2d90fb579b41271 | botox for men how much cost | ms_marco | Ranking Error | 1 |
| q_39965d461ad1b98c | how long does it take to walk a mile on average | ms_marco | Ranking Error | 1 |
| q_fd150ed5a369f2fa | average temperature august in new york | ms_marco | Ranking Error | 1 |
| q_295e2ec22bb568ce | in which order do baby teeth fall out | ms_marco | Ranking Error | 1 |
| q_55ff23cd7cb4fdf9 | what does malana | ms_marco | Ranking Error | 1 |
| q_15fa74bfa6b22b44 | what are the three types of meteoroids/asteroids. | ms_marco | Ranking Error | 1 |
| q_6cfcef038a0fcd88 | what does the enterogastric reflex accomplish | ms_marco | Ranking Error | 1 |
| q_9cf034f4222c9e75 | how long are the longest axons in humans | ms_marco | Ranking Error | 1 |
| q_551cd78e7dcf76a3 | what is mean of levorg' | ms_marco | Ranking Error | 1 |
| q_6306de89a9ef82be | what is conservation of chromosome number called | ms_marco | Ranking Error | 1 |
| q_acb2f684c5b5585d | what is markup language | ms_marco | Ranking Error | 1 |
| q_95770c173e87c26b | how to select an object without selecting is manually using vba | ms_marco | Ranking Error | 1 |
| q_3c224f7132d03444 | how long should i cook a roast beef in the oven | ms_marco | Ranking Error | 1 |
| q_4ed8dc1242839536 | cost to install chandelier | ms_marco | Ranking Error | 1 |
| q_3100a0b5c6556ec0 | per diem deduction | ms_marco | Semantic Miss | 0 |
| q_d8f515c6a8332621 | when were telegraph were discovered | ms_marco | Ranking Error | 1 |
| q_8877c93395779bbf | what is aneurysm caused by | ms_marco | Ranking Error | 1 |
| q_a1378b7d184170b0 | what does dsu switching stand for | ms_marco | Ranking Error | 1 |
| q_bd8b8ea7636dd4c1 | what is pericycle in plants | ms_marco | Ranking Error | 1 |
| q_94669ae8f14a5f4e | a contagious skin infection caused by fungi is | ms_marco | Ranking Error | 1 |
| q_7c92852857061ba8 | is donner pass open | ms_marco | Ranking Error | 1 |
| q_a661f203ba12d840 | what are the letters in algebra called | ms_marco | Ranking Error | 1 |
| q_c034ce55169d9d4a | oy gevalt meaning | ms_marco | Ranking Error | 1 |
| q_0555f7645a8bed8e | is the water meter next to the shut off valve | ms_marco | Ranking Error | 1 |
| q_54e661d660d0c381 | What is the name of the stadium where Super Bowl 50 was played? | squad | Semantic Miss | 0 |
| q_71ff5607fbca5094 | what age can a yorkie breed | ms_marco | Ranking Error | 1 |
| q_6d6b67f423a70270 | define gene mutation | ms_marco | Ranking Error | 1 |
| q_98a35d307dbaf602 | average cost of paving driveway | ms_marco | Ranking Error | 1 |
| q_85288ca9574bc60a | What is a main duty of the GPhC? | squad | Semantic Miss | 0 |
| q_5a0a48c1871bd4e9 | How many people, at most, have died of plague in Baghdad? | squad | Semantic Miss | 0 |
| q_76eeeb333f14fcc0 | who wrote the james bond theme tune | ms_marco | Ranking Error | 1 |
| q_d9b26788cb76e30c | on what month was mother's day was supposed to be celebrated | ms_marco | Ranking Error | 1 |
| q_02fe9f2e72f0f4eb | Does pressure increase or decrease when gas particles heat up? | sciq | Semantic Miss | 0 |
| q_9dba7b4b1757355e | how long do you cook asparagus in the oven | ms_marco | Ranking Error | 1 |
| q_c64d4699ca86eb80 | is gelatin made with pork | ms_marco | Ranking Error | 1 |
| q_aa34e38228d03bd7 | how to rename devices in google | ms_marco | Ranking Error | 1 |
| q_8a218fcb1004f809 | what is eva material | ms_marco | Ranking Error | 1 |
| q_c357a4abaa3b3e31 | how much does a plumber charge to replace faucet | ms_marco | Ranking Error | 1 |
| q_0a2759270f4adb13 | desert description biome | ms_marco | Ranking Error | 1 |
| q_a6b41681e05b0446 | different types of gruyere cheese | ms_marco | Ranking Error | 1 |
| q_e6a83ef401994717 | can i rinse out my dishwasher | ms_marco | Ranking Error | 1 |
| q_1537e73955a637c9 | who or what influenced shel silverstein | ms_marco | Ranking Error | 1 |
| q_32aa3c229be5e471 | what makes a prokaryote and eukaryote difference | ms_marco | Semantic Miss | 0 |
| q_29a22e0756c3ed2d | what age do you become a teenager | ms_marco | Ranking Error | 1 |
| q_84870d8f937ccd71 | what Kombucha is good for | ms_marco | Ranking Error | 1 |
| q_e2461d9cf5b839ca | What are the three most common elements in the air we breathe? | sciq | Semantic Miss | 0 |
| q_f536f2bffe710082 | troubleshooting definition | ms_marco | Ranking Error | 1 |
| q_5405c45460de31c1 | what is the difference turmeric root from ginger root | ms_marco | Ranking Error | 1 |
| q_c6b99cbfb19c3521 | how long for pain medication to work | ms_marco | Ranking Error | 1 |
| q_087189dc1faabebd | what is flaxseed | ms_marco | Ranking Error | 1 |
| q_a67d14ea7aa54cab | what is codeine | ms_marco | Ranking Error | 1 |
| q_c3eab1c434f589d0 | qualitative forecasting definition | ms_marco | Ranking Error | 1 |
| q_f37b9f14d913a839 | How many of Jacksonville's city residents are younger than 18? | squad | Semantic Miss | 0 |
| q_78d69ef49e940b27 | the plural form of ulna is | ms_marco | Ranking Error | 1 |
| q_af95741d6fa41dfc | mesentery definition | ms_marco | Semantic Miss | 0 |
| q_71a5da1f8014bea5 | how to remove duplicate pictures from computer | ms_marco | Ranking Error | 1 |
| q_01eb22863744728f | cost to spread mulch per yard | ms_marco | Ranking Error | 1 |
| q_c580ffb37e3618b3 | how long does it take for stool sample results to come back H.Pylori | ms_marco | Semantic Miss | 0 |
| q_59ebb22e531b8dbd | what impact did the harlem renaissance have on american society | ms_marco | Ranking Error | 1 |
| q_37cc61f96d34cd37 | where cancun is located | ms_marco | Ranking Error | 1 |
| q_10fab83afae2bb05 | what is clove spice | ms_marco | Ranking Error | 1 |
| q_9404e01da8db092b | can metamorphic rock be used to make pottery | ms_marco | Semantic Miss | 0 |
| q_854a764c18345ce5 | how big is neptune | ms_marco | Ranking Error | 1 |
| q_94c308075e51c6db | common causes for bladder infections | ms_marco | Ranking Error | 1 |
| q_8ca2fa4c51ea5e29 | what is artane medication used for | ms_marco | Ranking Error | 1 |
| q_cf14443808a394fd | what is aice diploma | ms_marco | Ranking Error | 1 |
| q_c4893b97b024f93d | What type of resource is water power? | sciq | Semantic Miss | 0 |
| q_2943ce8cc2fa5843 | what are the a distinguishing characteristic between fats and oils | ms_marco | Ranking Error | 1 |
| q_5cc8902309f93395 | age you can leave a child home alone | ms_marco | Semantic Miss | 0 |
| q_e7e74eb55cf59b46 | What type of chemicals do ants communicate with? | sciq | Semantic Miss | 0 |
| q_62e26b84182a9806 | what type grease is required for a centrifuge bearing | ms_marco | Ranking Error | 1 |
| q_889e8c9e0a4787e6 | What term best describes southern California's collection of landscapes? | squad | Semantic Miss | 0 |
| q_24ed8508670d7980 | meaning of constitution | ms_marco | Ranking Error | 1 |
| q_7912327dfc7df787 | cost to replace check valve on well pump | ms_marco | Ranking Error | 1 |
| q_5037ea445898aa22 | what is quinine good for | ms_marco | Semantic Miss | 0 |
| q_ab3527022d23715c | calcium score test cost | ms_marco | Ranking Error | 1 |
| q_1fa2b21473ce97ac | how do i compute the cost of goods sold | ms_marco | Ranking Error | 1 |
| q_3bf03f1f141d5464 | how much do church workers make | ms_marco | Ranking Error | 1 |
| q_d6936721a09d87ff | what is the main goal of any business | ms_marco | Semantic Miss | 0 |
| q_e1681f252733584d | what does means prostate | ms_marco | Ranking Error | 1 |
| q_18c9084efe8f8aee | inflamed bowel disease | ms_marco | Ranking Error | 1 |
| q_3db9c5e430169a34 | how many years do you need followup appointments for womb cancer | ms_marco | Ranking Error | 1 |
| q_6d7ac98598b0af1f | what temperature to cook roast lamb | ms_marco | Ranking Error | 1 |
| q_825ad0b329c822f0 | what is cns toxicity | ms_marco | Ranking Error | 1 |
| q_768a1138a6d4a527 | what phylum are there | ms_marco | Ranking Error | 1 |
| q_f683b457162ab98c | diabetes mellitus definition medical | ms_marco | Ranking Error | 1 |
| q_f393c3e54210d504 | list of foods for mediterranean diet | ms_marco | Ranking Error | 1 |
| q_c6970fb300ae7130 | what is normal retirement age | ms_marco | Ranking Error | 1 |
| q_3942e325935cb163 | is there an airport at uluru | ms_marco | Ranking Error | 1 |
| q_6edf974143c987c9 | how long does it take to grow long hair | ms_marco | Ranking Error | 1 |
| q_7f7991fd58faef3d | where i can send my tax amended | ms_marco | Ranking Error | 1 |
| q_32a9a8b79a7a5c90 | why is immune rejection an example of a healthy immune system | ms_marco | Ranking Error | 1 |
| q_d57bc42788e1ed96 | what does häagen-dazs mean | ms_marco | Ranking Error | 1 |
| q_d1b4791ec4ff2f10 | cost for admission to disneyland | ms_marco | Ranking Error | 1 |
| q_9a4fef4d80d05b36 | what is mahlab made from | ms_marco | Ranking Error | 1 |
| q_9230fac945851663 | how much does a facial cost in dallas | ms_marco | Ranking Error | 1 |
| q_99d3a74e4a687275 | where are centipedes found | ms_marco | Ranking Error | 1 |
| q_6466a44fe3e0a7d7 | What did Luther call these donations? | squad | Ranking Error | 1 |
| q_421b05f1128a9711 | where is dallas located in usa | ms_marco | Ranking Error | 1 |
| q_3410d831e63c7ad9 | where is amherstburg located | ms_marco | Ranking Error | 1 |
| q_a60a63b0baf2cb46 | what kind of complaints does the bbb handle | ms_marco | Ranking Error | 1 |
| q_ff8cf5d0d9551269 | What does the UN want to stabilize? | squad | Semantic Miss | 0 |
| q_014464a6eb38999c | when to claim parent as dependent | ms_marco | Ranking Error | 1 |
| q_87307f9488b5030c | average height for black male | ms_marco | Ranking Error | 1 |
| q_b44e1dd439a91aa5 | What do industries use water to generate? | sciq | Semantic Miss | 0 |
| q_6e2100ca50151750 | what is a critical habitat | ms_marco | Ranking Error | 1 |
| q_5209958d2915bedd | what is a blood plum | ms_marco | Ranking Error | 1 |
| q_5db7349811d6e104 | Bones are part of which body system? | sciq | Semantic Miss | 0 |
| q_61e3dcb8bab13a76 | Leaves respond to these environmental stimuli by producing less what? | sciq | Semantic Miss | 0 |
| q_e9279a60aa7062d9 | what does bullous emphysema suggest | ms_marco | Semantic Miss | 0 |
| q_e910ac2ad77bd8bd | When did O2 begin to acculturate in the atmosphere? | squad | Semantic Miss | 0 |
| q_8584e55e7da5fd2f | can you freeze your social security earnings | ms_marco | Ranking Error | 1 |
| q_46f9490fc7694b43 | how much does a garage concrete slab cost | ms_marco | Ranking Error | 1 |
| q_f7949b625ee231e1 | what are nephrons | ms_marco | Ranking Error | 1 |
| q_50a0eb5e922d2e93 | is enterococcus part of strep | ms_marco | Ranking Error | 1 |
| q_2244dac0ba4a8c5e | what is the use of bt spray for plants | ms_marco | Semantic Miss | 0 |
| q_e5204501388fc3d4 | how much do you get paid for being a riding instructor | ms_marco | Ranking Error | 1 |
| q_3614543e22504cf7 | how much should you get paid for dog walking | ms_marco | Ranking Error | 1 |
| q_cdc5d84f0e230fda | What country is this statistic for? | squad | Semantic Miss | 0 |
| q_578d93bb22547e06 | What is 'grey literature'? | squad | Semantic Miss | 0 |
| q_46a512db7f4cd26a | why did congress object to the league of nations | ms_marco | Ranking Error | 1 |
| q_a805193fa6760151 | irritable bowel syndrome is it contagious | ms_marco | Ranking Error | 1 |
| q_2dd36a480d679112 | epsilon delta definition of limit examples | ms_marco | Semantic Miss | 0 |
| q_8b99bc61b3365850 | what event created the invention of morse code | ms_marco | Semantic Miss | 0 |
| q_1a3961b2dd6a91bb | what does effexor do | ms_marco | Ranking Error | 1 |
| q_25c7dea7f278d6c3 | what is a molar root canal | ms_marco | Semantic Miss | 0 |
| q_a4c13958acecdb85 | average salary for draughtsman | ms_marco | Ranking Error | 1 |
| q_64350a2078ad7e52 | how long does it take to receive student loan | ms_marco | Ranking Error | 1 |
| q_4db6d8b96e2ec906 | What were X-rays known as at the time? | squad | Semantic Miss | 0 |
| q_734568ccae0abf96 | what does bms mean in texting | ms_marco | Ranking Error | 1 |
| q_aec79e6058d099b4 | What does ctenophora mean in Greek? | squad | Semantic Miss | 0 |
| q_0d7fec8af8c0fa3b | subaru impreza mileage per gallon | ms_marco | Ranking Error | 1 |
| q_e3a80089b0092138 | A paragraph explaining dna and what is does | ms_marco | Ranking Error | 1 |
| q_e084425d4e74a9b4 | cost of a single tooth repair (cavity)? | ms_marco | Ranking Error | 1 |
| q_e50c9c34a7c4d1e7 | what is resilience | ms_marco | Semantic Miss | 0 |
| q_31ca868af169c47d | how to remove mobogenie adware on android phone | ms_marco | Ranking Error | 1 |
| q_76c4376e202b56c7 | who originally wrote last kiss | ms_marco | Semantic Miss | 0 |
| q_2c4d9d786b79852d | what is saltpeter | ms_marco | Ranking Error | 1 |
| q_340e11f011cb3e60 | how much does a doctor's office visit cost without insurance | ms_marco | Ranking Error | 1 |
| q_36478b5d18a05e14 | what company does allergan owns | ms_marco | Ranking Error | 1 |
| q_57cf7edab0afae8c | what is the structure of carbon | ms_marco | Ranking Error | 1 |
| q_c3e98eb28f12c57b | jenny craig cost per week | ms_marco | Ranking Error | 1 |
| q_035b6d8729a5b1cf | how long does it take for food to pass | ms_marco | Ranking Error | 1 |
| q_38f599df36626c1d | body systems affected by kidney stones | ms_marco | Ranking Error | 1 |
| q_c69f25f681053ccc | what minerals are carbonate | ms_marco | Semantic Miss | 0 |
| q_4d2ce2c10c330f2a | how to cook eye of round beef | ms_marco | Ranking Error | 1 |
| q_cb4aa3a1c27126f9 | cost to carpet your home | ms_marco | Ranking Error | 1 |
| q_db665f9e5b937c4c | where is aspergillus found | ms_marco | Ranking Error | 1 |
| q_1cb8fdd1bf5c8364 | how much do waiters make | ms_marco | Ranking Error | 1 |
| q_3354df8d9caa55b1 | What is used to decide a teacher's salary? | squad | Semantic Miss | 0 |
| q_38f4262109f4b4ed | what is chartered financial analyst | ms_marco | Ranking Error | 1 |
| q_8251b5f78f02aeb0 | What two country's referendums curtailed a constitution for Europe? | squad | Semantic Miss | 0 |
| q_ff2fe315316ea2a0 | average temperature hanoi | ms_marco | Ranking Error | 1 |
| q_608d50a4a736700c | electrical engineer vs electronics engineer | ms_marco | Ranking Error | 1 |
| q_00aab6720c959232 | what region of the world is france in | ms_marco | Ranking Error | 1 |
| q_4d4795e99925bb61 | what are proteins used for | ms_marco | Ranking Error | 1 |
| q_c0e7c9e5cd9598c1 | Where is the Apostles located? | squad | Semantic Miss | 0 |
| q_fda8287d7314218c | what can cause shrinking testicles | ms_marco | Ranking Error | 1 |
| q_5e01fa1f91577b88 | hardwood flooring installation labor cost | ms_marco | Ranking Error | 1 |
| q_1eb9af91a82de721 | what language in austria | ms_marco | Ranking Error | 1 |
| q_3b5f6c27d88a6642 | what are intercostal muscles | ms_marco | Ranking Error | 1 |
| q_fd9aa6d7cd89e148 | what was the battle of the lone pine | ms_marco | Semantic Miss | 0 |
| q_71ea9204c2a3ef47 | can i play games without nvidia drivers installed | ms_marco | Ranking Error | 1 |
| q_1c8333b9dc575e10 | standardization definition in chemistry | ms_marco | Ranking Error | 1 |
| q_b2956198223d7655 | how much social security is deducted from my paycheck | ms_marco | Ranking Error | 1 |
| q_5945037c90444742 | definition of scavenger for kids | ms_marco | Ranking Error | 1 |
| q_7617c4ccee4aabab | what year did the constitutional convention meet | ms_marco | Ranking Error | 1 |
| q_2234711fc13822c6 | what was the reason for the berlin airlift quizlet | ms_marco | Ranking Error | 1 |
| q_1c71629dc5019467 | What are the primary causes of bone fractures? | sciq | Semantic Miss | 0 |
| q_b92fa2a6dc672909 | The existence of (virtual) photons is possible only by virtue of the heisenberg uncertainty principle and can travel an unlimited distance, so the range ofthe electromagnetic for is what? | sciq | Semantic Miss | 0 |
| q_7b37ed7f7f0320ba | What was the name of Westinghouse's company? | squad | Semantic Miss | 0 |
| q_5921f0fd2d9c0f56 | how long does ground beef stay good for frozen | ms_marco | Ranking Error | 1 |
| q_59c8613fa1f997c9 | what is the scientific name of beetle species | ms_marco | Ranking Error | 1 |
| q_7f43eba4acfeacee | what is the average starting salary for chemical engineers | ms_marco | Ranking Error | 1 |
| q_ce76041b95991aa3 | how much does a pilot earn | ms_marco | Ranking Error | 1 |
| q_b14e5d940b43ea7f | What did European empires rely on to supply them with resources? | squad | Semantic Miss | 0 |
| q_7d0352c464ec03ab | what type of cancer causes thrush in adults | ms_marco | Ranking Error | 1 |
| q_e186a0634d507c21 | who was king arthur's sister | ms_marco | Ranking Error | 1 |
| q_66659ff0b742beeb | what temp is beef well done | ms_marco | Ranking Error | 1 |
| q_892a1b4a9bae3826 | price per square foot for log homes | ms_marco | Ranking Error | 1 |
| q_df9472cacbc016ba | what was the plan of d day | ms_marco | Ranking Error | 1 |
| q_97c1c6462e00091d | where does seaweed grow | ms_marco | Ranking Error | 1 |
| q_e3038accac27be69 | what does a moist productive cough indicate | ms_marco | Ranking Error | 1 |
| q_500827bc56413d2e | how long does a std test take to come back | ms_marco | Ranking Error | 1 |
| q_3f758eb339e49949 | can you legally get married in the bahamas | ms_marco | Ranking Error | 1 |
| q_381fd5f35d6a2448 | what is the meaning of mayur | ms_marco | Ranking Error | 1 |
| q_d5f69822cc8c908c | There are two of what type of institution in Newcastle? | squad | Semantic Miss | 0 |
| q_2064ccc48f334783 | are neurons true cells | ms_marco | Ranking Error | 1 |
| q_5b4db7b4dbba9ef3 | how much it costs to make game of thrones | ms_marco | Ranking Error | 1 |
| q_d4bff5bc19b869f7 | how old do you have to be to have ebay | ms_marco | Ranking Error | 1 |
| q_e053a204c5641f07 | What is lava called before it reaches the surface of the earth? | sciq | Semantic Miss | 0 |
| q_0961963745e678b7 | does chemical digestion occur in the pancreas | ms_marco | Ranking Error | 1 |
| q_f7e2066c4a14b5e9 | normal level for cholesterol | ms_marco | Ranking Error | 1 |
| q_182b6fa35f776cb9 | what is tomato pomace | ms_marco | Ranking Error | 1 |
| q_8acc8fd582d36b2c | what nationality is dilma rousseff | ms_marco | Semantic Miss | 0 |
| q_2eb4f359e8c2c2cd | what was the main goal of the military reconstruction act | ms_marco | Semantic Miss | 0 |
| q_69727a34212a77d5 | average temperature in singapore in june | ms_marco | Ranking Error | 1 |
| q_794d16578179695c | what company owns naturipe farms | ms_marco | Ranking Error | 1 |
| q_f47e981bba3b4d5e | what is cued articulation | ms_marco | Ranking Error | 1 |
| q_f91fc99eab02d425 | what is ring fencing | ms_marco | Ranking Error | 1 |
| q_f452cf3a5c935653 | What does the human heart do? | sciq | Ranking Error | 1 |
| q_2612e2983bc77234 | is cumene a monomer | ms_marco | Ranking Error | 1 |
| q_f6dfefa9f036628c | what is sulfites in food | ms_marco | Ranking Error | 1 |
| q_60310639a8f51a50 | how long do i have to pay my credit card | ms_marco | Ranking Error | 1 |
| q_a484a1c3a5e2a56f | is lyrica a narcotic | ms_marco | Ranking Error | 1 |
| q_34cfc60ab00b52e4 | how much nicotine is considered a lethal dose for humans | ms_marco | Ranking Error | 1 |
| q_bd47707498b8ea8d | can you borrow money against a roth ira | ms_marco | Semantic Miss | 0 |
| q_8c498cf71d91e9a5 | when to check blood sugar non insulin | ms_marco | Ranking Error | 1 |
| q_79842b331615f93f | where is hull | ms_marco | Ranking Error | 1 |
| q_e77950b7b509b719 | what are antioxidants in food | ms_marco | Ranking Error | 1 |
| q_5c2cbe1cce6518c3 | what are organic molecules digested by | ms_marco | Ranking Error | 1 |
| q_fc4d621131a815f2 | does lowes install sheds | ms_marco | Ranking Error | 1 |
| q_03e77148a409be3f | how to cook marinated beef ribs | ms_marco | Ranking Error | 1 |
| q_b87ff59a5a530ae4 | what does the yin yang mean | ms_marco | Ranking Error | 1 |
| q_7823339b77b4ba31 | What is the meaning of the song purple rain? | ms_marco | Ranking Error | 1 |
| q_3907dbca127ade05 | dna is contained in what structure in prokaryotes and eukaryotes | ms_marco | Ranking Error | 1 |
| q_f8c2caafabe7385e | cost attend yale | ms_marco | Ranking Error | 1 |
| q_a84ed38c48088f51 | when can i separate my hostas | ms_marco | Ranking Error | 1 |
| q_4d9a7e8c8242d858 | how to connect car charger to car | ms_marco | Ranking Error | 1 |
| q_22898de9144cf05a | The republic was also known as a socialist government. | ms_marco | Semantic Miss | 0 |
| q_4465cb6a1fcbf816 | how do you find out your std results | ms_marco | Ranking Error | 1 |
| q_0b17907383ff2e13 | continental volcanic arcs are associated with the | ms_marco | Ranking Error | 1 |
| q_1666eea593010cf2 | what are baby sparrows called | ms_marco | Semantic Miss | 0 |
| q_bd9a9db75f999da6 | what biome is the netherlands in | ms_marco | Ranking Error | 1 |
| q_f3424baec5b93f34 | how much to replace master cylinder | ms_marco | Ranking Error | 1 |
| q_43e9942fbff02b8d | what amount magnesium blood level is normal | ms_marco | Ranking Error | 1 |
| q_597029124d0b048b | what makes a shirt flannel | ms_marco | Ranking Error | 1 |
| q_f966e26fb8cfb0e1 | what is a cost centers | ms_marco | Ranking Error | 1 |
| q_1fc70dc65355005d | how do you get to aran islands | ms_marco | Ranking Error | 1 |
| q_415334287355578a | what are the adaptations of a maned wolf | ms_marco | Ranking Error | 1 |
| q_fb4f545e6cc99111 | why are phospholipids important in cell membranes | ms_marco | Semantic Miss | 0 |
| q_0f12e2b672aaeab9 | gmu cost per credit | ms_marco | Ranking Error | 1 |
| q_217b642521efc6d7 | what are the predators of the gulper eel | ms_marco | Ranking Error | 1 |
| q_dd4267ef02711905 | average act score for a freshman | ms_marco | Ranking Error | 1 |
| q_3900c96a37750b13 | can albuterol be used an advair inhaler | ms_marco | Ranking Error | 1 |
| q_2d4cf7c63a6fff8c | what does the imeche do | ms_marco | Ranking Error | 1 |
| q_9d213ee2ec0d9a75 | what bug bite causes small blisters | ms_marco | Semantic Miss | 0 |
| q_461c9c8f3b9d790c | what causes very foul smelling stools | ms_marco | Semantic Miss | 0 |
| q_49833de39622d540 | what temperature should it be to plant grass seeds | ms_marco | Ranking Error | 1 |
| q_3be63df65bd21157 | do female serial killers exist | ms_marco | Ranking Error | 1 |
| q_0729adf1902306c9 | what are the bacterial cells organisms | ms_marco | Ranking Error | 1 |
| q_835d716cece44a70 | what is a Otorhinolaryngology | ms_marco | Semantic Miss | 0 |
| q_139e6ed444cb9dbf | incubation period for viral pneumonia | ms_marco | Ranking Error | 1 |
| q_cceb4f9b62c1c6aa | holds an organism's hereditary information | ms_marco | Ranking Error | 1 |
| q_1c70e4fed24b6bca | Parse the data. | code_search_net | Semantic Miss | 0 |
| q_2bcff97d77e98096 | description of the different types of radiation | ms_marco | Ranking Error | 1 |
| q_2f2d0b91d4a255cd | what is schnapps | ms_marco | Ranking Error | 1 |
| q_00c59daa5fca9aa8 | why did only miriam get leprosy | ms_marco | Ranking Error | 1 |
| q_bffa602043c30b18 | what is the carbohydrates that is your body primary source of energy | ms_marco | Ranking Error | 1 |
| q_d3f4cb3e5134d8cb | is tobacco considered a controlled substance | ms_marco | Ranking Error | 1 |
| q_3af7ec26b65ff87a | erythroid tissue definition | ms_marco | Ranking Error | 1 |
| q_ccc5d6d49b948ac3 | who money is worth the most | ms_marco | Ranking Error | 1 |
| q_76c8e48e588e563c | how did the twelfth amendment change the electoral college? | ms_marco | Ranking Error | 1 |
| q_e579d723a6ea2344 | What is a defining feature of deformed sedimentary rocks? | sciq | Semantic Miss | 0 |
| q_da3493f0e6dcbf7e | distance between canmore, alberta and banff (town) miles and time | ms_marco | Ranking Error | 1 |
| q_ff4ce74a915a8f19 | what is needed twic | ms_marco | Ranking Error | 1 |
| q_afe601392c60813b | what is STC rating | ms_marco | Ranking Error | 1 |
| q_9109bd33fc2795fb | how can infertility be treated | ms_marco | Ranking Error | 1 |
| q_beb60a396b4861b7 | what is the income limit to get food stamps | ms_marco | Ranking Error | 1 |
| q_1929fb3bc2950bab | how much does an lpn make an hour in illinois | ms_marco | Ranking Error | 1 |
| q_b343ff6bd1281e55 | what classification is lanoxin | ms_marco | Ranking Error | 1 |
| q_e1deab66ff476eeb | gluconeogenesis meaning | ms_marco | Ranking Error | 1 |
| q_558bfc23346797e7 | good sources of vitamin a | ms_marco | Ranking Error | 1 |
| q_356fc5c063447dd4 | how long does it take for a loaf of bread to thaw | ms_marco | Ranking Error | 1 |
| q_b314842a5be38826 | what is a adenomatous polyp in colon | ms_marco | Ranking Error | 1 |
| q_0e9635b23e2c9948 | how to turn screen on iphone 6 plus | ms_marco | Ranking Error | 1 |
| q_86a0ddb2564c5ca2 | what kind of government is the us | ms_marco | Semantic Miss | 0 |
| q_813ec9a902cd89c1 | what is a habitat of a wolf | ms_marco | Ranking Error | 1 |
| q_d74ce7b2e7f7dcea | is rheumatoid arthritis different from arthritis | ms_marco | Ranking Error | 1 |
| q_2eaf878f3829f6a0 | how much liquid does an evod hold | ms_marco | Ranking Error | 1 |
| q_fe623484311b8872 | what age do baby teeth come out | ms_marco | Ranking Error | 1 |
| q_0d14f64c9bfc9d7d | what type of political system does the us have | ms_marco | Ranking Error | 1 |
| q_366b754acdf0fefe | prefab homes average cost | ms_marco | Ranking Error | 1 |
| q_b6cca0be82a9ba48 | what is an inherited disorder | ms_marco | Semantic Miss | 0 |
| q_2eac657faa61ba45 | Limestone is insoluble in water, so what can dissolve it? | sciq | Semantic Miss | 0 |
| q_a42ea3fa4ec2033b | what are american kestrel adaptations | ms_marco | Semantic Miss | 0 |
| q_68c326b02baab600 | how many calories in honey | ms_marco | Ranking Error | 1 |
| q_9367146a93f306da | what is taurine made of | ms_marco | Ranking Error | 1 |
| q_367802a906f0c111 | best time to visit denmark | ms_marco | Ranking Error | 1 |
| q_aedb44dddc5bf58e | what cells are found within the epithelium lines of trachea quizlet | ms_marco | Ranking Error | 1 |
| q_ec880802816a531b | how to auto power off pc | ms_marco | Ranking Error | 1 |
| q_e45db701c93aa7fd | what proteins in gluten cause coeliac disease | ms_marco | Ranking Error | 1 |
| q_29bb98a3225ddd5c | what does the name cierra mean | ms_marco | Ranking Error | 1 |
| q_c52ee51be0c03476 | can a person with a criminal record travel | ms_marco | Ranking Error | 1 |
| q_4e7f529937c30517 | what color is azurite | ms_marco | Ranking Error | 1 |
| q_56f445ab525bd0a9 | mediterranean diet what type of residents are on this food | ms_marco | Ranking Error | 1 |
| q_e3dcbb1eb1a1e39c | what is a phosphodiester bonds. | ms_marco | Ranking Error | 1 |
| q_6472c812bbd2caaf | the part in the lungs where oxygen enters the bloodstream are | ms_marco | Ranking Error | 1 |
| q_f7a9a5f683efea54 | how many astronomical units away is alpha centauri | ms_marco | Semantic Miss | 0 |
| q_919dce5b3dfc7ee0 | what are symptoms for chlamydia | ms_marco | Ranking Error | 1 |
| q_36ba8bdad8fed8cb | what is macrovision | ms_marco | Ranking Error | 1 |
| q_4ae543cc46519b1b | average digital pulse rate of horse | ms_marco | Ranking Error | 1 |
| q_4845c12064d33f8a | lowest theoretical temperature | ms_marco | Ranking Error | 1 |
| q_cc130bf80f4ccdc9 | how much did the first electric sewing machine cost | ms_marco | Ranking Error | 1 |
| q_6413a93b8d0099c3 | what type of government does slovakia have | ms_marco | Ranking Error | 1 |
| q_551ecfb386975a8b | average fee for paying up mortgage | ms_marco | Semantic Miss | 0 |
| q_0adec3b5effce546 | what is a aboriginal boomerang used for | ms_marco | Ranking Error | 1 |
| q_df08a0abf27b3849 | advantages caused by the trans- saharan trade routes | ms_marco | Ranking Error | 1 |
| q_6e7ae3e70587f6b5 | how long is a whole watermelon good for in the fridge | ms_marco | Ranking Error | 1 |
| q_5a565c94a1dde725 | how long will fresh asparagus last in fridge | ms_marco | Ranking Error | 1 |
| q_5e4229ac0c383ac5 | what is ernest hilgard best known for | ms_marco | Ranking Error | 1 |
| q_9aa28fc4aeff91d1 | meaning of protagonist | ms_marco | Semantic Miss | 0 |
| q_f78c9612c26d18a2 | Who fumbled the ball on 3rd-and-9? | squad | Ranking Error | 1 |
| q_d4289a4f02258eb2 | Colonies were a sign of what amongst European countries? | squad | Semantic Miss | 0 |
| q_245ca810f29ad59d | jeweler salary pay scale | ms_marco | Ranking Error | 1 |
| q_22538a1275be425f | what is jcaho | ms_marco | Ranking Error | 1 |
| q_9b50e3efcc119200 | what laws or acts did jfk pass | ms_marco | Ranking Error | 1 |
| q_4d42fe798c6d040e | what is a characteristic of influenza? | ms_marco | Ranking Error | 1 |
| q_28584dfd1e7bf0fc | is vanuatu in fiji | ms_marco | Semantic Miss | 0 |
| q_24cd1f948a61fb6f | coventry council senior social workers salary | ms_marco | Ranking Error | 1 |
| q_67e52b242c693c4c | life vs death cost | ms_marco | Ranking Error | 1 |
| q_449c6c45103ba630 | what was the first battle that the union won | ms_marco | Ranking Error | 1 |
| q_4f2cfb3e701250f2 | what is the longest professional baseball game ever played | ms_marco | Ranking Error | 1 |
| q_10276b2758a468a1 | what is the meaning of herniated | ms_marco | Ranking Error | 1 |
| q_53517ebefd94a958 | a list of vitamins and minerals and what they do | ms_marco | Ranking Error | 1 |
| q_1b316443c94fdd9d | what is the antagonist in muscles | ms_marco | Ranking Error | 1 |
| q_914e0b78b7fa2738 | peripheral nervous is part of what system | ms_marco | Ranking Error | 1 |
| q_715d124f078f3570 | what geological event occurs at a transform boundary | ms_marco | Ranking Error | 1 |
| q_e355d0c216dfe804 | What is another word for saturated hydrocarbons? | sciq | Semantic Miss | 0 |
| q_ed2a48b92ac6b216 | what is a geographic description | ms_marco | Ranking Error | 1 |
| q_0cbc4895b45a8c21 | sudden weight loss medical term | ms_marco | Ranking Error | 1 |
| q_358d90702c35ab04 | how often does medicare pay for mammograms | ms_marco | Ranking Error | 1 |
| q_13feb6dc09dfb1ad | average cost of credit repair services | ms_marco | Ranking Error | 1 |
| q_214a4f36f16ba5f2 | what is wheatgrass | ms_marco | Ranking Error | 1 |
| q_36e221b52b90b92b | what type of muscle is responsible for contractions of the digestive tract and arteries | ms_marco | Ranking Error | 1 |
| q_292b7fb73ce701f6 | when was abraham lincoln elected president of the united states | ms_marco | Ranking Error | 1 |
| q_f12ea12f31dec77b | where does white truffle grow | ms_marco | Ranking Error | 1 |
| q_7ce9c207bde6ef27 | what is impressionistic writing | ms_marco | Ranking Error | 1 |
| q_0b07cca2db2edb96 | What is the translation of Siebengebirge? | squad | Semantic Miss | 0 |
| q_54dc7103b87daddb | what is a locus biology | ms_marco | Ranking Error | 1 |
| q_7ee595d0cfefc386 | what is chipotle chili powder | ms_marco | Ranking Error | 1 |
| q_f46d0c4b4fdf0f8f | what was the lend-lease act | ms_marco | Ranking Error | 1 |
| q_56c501d42cde592d | weighted average method of inventory valuation | ms_marco | Ranking Error | 1 |
| q_ef1b9e351ef6f801 | what is the meaning of anonymity | ms_marco | Ranking Error | 1 |
| q_304b98295f0978bc | when can i sell a stock and still get dividend td | ms_marco | Ranking Error | 1 |
| q_f81a677ed43c15bf | where is the good english spoken in dubai | ms_marco | Semantic Miss | 0 |
| q_9dd1842ae876624b | How many centimeters are in a meter? | sciq | Semantic Miss | 0 |
| q_5022e6a6cd3853d0 | convert stone to lb | ms_marco | Ranking Error | 1 |
| q_38b4641b8be31741 | what makes up the asthenosphere | ms_marco | Ranking Error | 1 |
| q_09c87810e0733b3a | what is a pom? | ms_marco | Ranking Error | 1 |
| q_7219468abccfd92d | how to stop boxbe | ms_marco | Ranking Error | 1 |
| q_2368d3e58ba778fc | can a man live on avocado | ms_marco | Ranking Error | 1 |
| q_11a9c2e143dd010e | is mold a carcinogen | ms_marco | Ranking Error | 1 |
| q_96c466c2db23f6b0 | what is phosphorus good for | ms_marco | Semantic Miss | 0 |
| q_bc355ca1cbde6c96 | how are seafloor volcanoes formed | ms_marco | Ranking Error | 1 |
| q_cf29bcedbfe0b015 | what stone is made of cement | ms_marco | Ranking Error | 1 |
| q_31f53e78f724e3c1 | lvac membership cost | ms_marco | Ranking Error | 1 |
| q_5f5b5b34bfa86233 | how long do mallard ducks sit on eggs | ms_marco | Ranking Error | 1 |
| q_541ac98584c84ee0 | what is a BN | ms_marco | Ranking Error | 1 |
| q_5e162d7b9332670b | average human body temperature | ms_marco | Ranking Error | 1 |
| q_d1c6b17162c7eb26 | annual temperature in poland | ms_marco | Ranking Error | 1 |
| q_a3f8d568ec376f66 | when was pompeia born | ms_marco | Ranking Error | 1 |
| q_ae23eb568690ff2f | why was the treaty of nanjing unequal | ms_marco | Ranking Error | 1 |
| q_29d89bbd286d0c26 | What do we call the empire that Genghis Khan founded? | squad | Semantic Miss | 0 |
| q_7c91bbb878f9625d | what is masteron | ms_marco | Ranking Error | 1 |
| q_61b9e29b6dcf42e9 | What element makes up the majority of coal? | sciq | Semantic Miss | 0 |
| q_13463c1b62433f8a | when was the cannon invented | ms_marco | Ranking Error | 1 |
| q_31fa331d80c68b0e | definition of horderves | ms_marco | Ranking Error | 1 |
| q_5730eef132aaf02b | how much money do the dancing with the stars contestants make | ms_marco | Ranking Error | 1 |
| q_6cfc98206167c4b1 | bu measurement conversion in kg | ms_marco | Ranking Error | 1 |
| q_2472d2416ebbf988 | what landforms do divergent boundaries form | ms_marco | Ranking Error | 1 |
| q_bcd75c9c7ac29bf9 | what to use in power washer to clean the side of house without harming my garden | ms_marco | Ranking Error | 1 |
| q_b2a40ddbfe035fc6 | how fast can a giraffe run in mph | ms_marco | Ranking Error | 1 |
| q_ec3df96bccc0a842 | What kind of weathering is abrasion? | sciq | Semantic Miss | 0 |
| q_b6ba5c34a76c645d | is georgia hilly | ms_marco | Ranking Error | 1 |
| q_56e991ef51adfe4a | how old should goats be to neuter | ms_marco | Ranking Error | 1 |
| q_32d0566b99f3078e | germany uses strikes called blitzkrieg | ms_marco | Ranking Error | 1 |
| q_0adf4803d4442477 | what is marketing myopia | ms_marco | Ranking Error | 1 |
| q_f4ccb157fd120018 | what is reverse osmosis desalination process | ms_marco | Ranking Error | 1 |
| q_5d276059790143d7 | dental hygienist salary alberta | ms_marco | Ranking Error | 1 |
| q_3c1f25e7f53d6397 | what is the maximum age for life insurance | ms_marco | Ranking Error | 1 |
| q_73009622d6e369db | how to cut seed potatoes to plant | ms_marco | Ranking Error | 1 |
| q_00fe75e86ada2fbf | salary nhl players | ms_marco | Ranking Error | 1 |
| q_262b6cd4408729bd | where is property brothers filmed | ms_marco | Ranking Error | 1 |
| q_11f24f76f5f67394 | what disease does entamoeba histolytica cause | ms_marco | Ranking Error | 1 |
| q_b64b309cbea65908 | what is average psa level by age | ms_marco | Ranking Error | 1 |
| q_5f001b3d06499272 | where is sinus located | ms_marco | Ranking Error | 1 |
| q_cd45c73a28024846 | who played frasier on tv series | ms_marco | Ranking Error | 1 |
| q_32bd34e68b367ac6 | why is it not recommended that consumers acquire debts | ms_marco | Ranking Error | 1 |
| q_d6f8ce1e48483fc0 | what is marl material | ms_marco | Ranking Error | 1 |
| q_0f456c879d1229d1 | what is the difference between scripting language and programming language | ms_marco | Ranking Error | 1 |
| q_291e7f1380e0d4f5 | how long will chorizo keep in the fridge | ms_marco | Ranking Error | 1 |
| q_3b7515a8a7d1c2f5 | after tooth extraction upto how long does pain remains | ms_marco | Ranking Error | 1 |
| q_0f9a21798f74d08c | what is a producer gas | ms_marco | Ranking Error | 1 |
| q_36c44921713044bf | how long can someone last without food or fluids | ms_marco | Ranking Error | 1 |
| q_d7f011ef2999aca4 | why did we start saying burn the midnight oil | ms_marco | Ranking Error | 1 |
| q_a32c59d2bb7b2731 | what language do they speak in kazakhstan | ms_marco | Ranking Error | 1 |
| q_c32b8915d8fa9dca | how much does a successful neurosurgeon make per year | ms_marco | Ranking Error | 1 |
| q_0497634e709beb9e | what is granulated sugar? | ms_marco | Ranking Error | 1 |
| q_66d63e313b694519 | What is Tesla's home country? | squad | Semantic Miss | 0 |
| q_e4093911d781e051 | taiga temperature and precipitation | ms_marco | Ranking Error | 1 |
| q_9a8442ff285d2e21 | what are donairs | ms_marco | Ranking Error | 1 |
| q_4152004f0591be8d | what is normal oxygen levels | ms_marco | Ranking Error | 1 |
| q_99c734a8b27d7efc | what does the zoroastrianism symbol represent | ms_marco | Ranking Error | 1 |
| q_4b93e0dfe826281d | what do you understand by fiscal policy | ms_marco | Ranking Error | 1 |
| q_67efb1e086fad419 | Who was famous for disobedience against a tax collector? | squad | Ranking Error | 1 |
| q_d5554606b1bb64f6 | salary or wage for a medical office assistant | ms_marco | Ranking Error | 1 |
| q_d11ce30a535577d6 | what does widely patent mean | ms_marco | Ranking Error | 1 |
| q_24e962ab96ac24eb | what is the biggest breed of horse | ms_marco | Semantic Miss | 0 |
| q_af44d9d188a402c3 | pharmacist tech salary | ms_marco | Ranking Error | 1 |
| q_bcc378d89b844434 | how to get photos from phone to computer | ms_marco | Ranking Error | 1 |
| q_f8efccb7f7013c34 | how to help riften skyrim | ms_marco | Ranking Error | 1 |
| q_12d4d660c37beca3 | how much do tuna fishers first mates make | ms_marco | Ranking Error | 1 |
| q_7290e7f3e70c4c0a | how long does a torn shoulder tendon take to heal | ms_marco | Ranking Error | 1 |
| q_f0dcae9e22046ad8 | ethnicity of the name wiser | ms_marco | Ranking Error | 1 |
| q_0c0260bba0326072 | what does plasmodium cause | ms_marco | Ranking Error | 1 |
| q_08b267d1722669b0 | what separates culture from civilization | ms_marco | Ranking Error | 1 |
| q_feeb7b2fe270eae3 | how much flaxseed per day | ms_marco | Ranking Error | 1 |
| q_e7ca641d4769e39e | cost accounting salary houston | ms_marco | Semantic Miss | 0 |
| q_b3fe40712b04f064 | What kind of fertilization do birds have? | sciq | Semantic Miss | 0 |
| q_1ba9080850e80738 | ending sentence with preposition example | ms_marco | Ranking Error | 1 |
| q_cca61a9211c3f22d | how much does an average kitchen cabinet refacing cost | ms_marco | Ranking Error | 1 |
| q_2603691dd0036655 | What is a mutation? | sciq | Semantic Miss | 0 |
| q_68675aef9a9d34c2 | what is a construction company | ms_marco | Ranking Error | 1 |
| q_4b9e54e30baf8bbb | what is mucuna pruriens | ms_marco | Ranking Error | 1 |
| q_7a223749dee92a4b | what makes corned beef corned | ms_marco | Ranking Error | 1 |
| q_334f22fa2162e779 | avg lifespan for rabbits | ms_marco | Semantic Miss | 0 |
| q_a4c150fb1ddeeca0 | what tissue is the heart made out of | ms_marco | Semantic Miss | 0 |
| q_458d6a4b2a0ccc84 | how much did goldman sachs pay hillary clinton | ms_marco | Ranking Error | 1 |
| q_5f1ab9d0d89589ad | what is syncope | ms_marco | Ranking Error | 1 |
| q_eb985f5f53623e4d | How Much Does IVF Cost | ms_marco | Ranking Error | 1 |
| q_9d197eac4c2b1995 | chemicals produced in plants that are characterized by their ability to induce cell elongation and cell division in stems | ms_marco | Semantic Miss | 0 |
| q_6d0b987e0a640569 | Decision tree is an example of what type of measure? | squad | Semantic Miss | 0 |
| q_72aff9f234b4b83f | male name meaning healer | ms_marco | Ranking Error | 1 |
| q_2f92ae909c9a0b1e | did the railroad invention have an impact on the world | ms_marco | Ranking Error | 1 |
| q_46aac0cd10c91565 | where in a muscle cell is calcium stored | ms_marco | Ranking Error | 1 |
| q_7afefd907b3b73ba | whittaker classification genus species variety | ms_marco | Ranking Error | 1 |
| q_bd5c714fb4caa012 | significance of the golden gate bridge | ms_marco | Semantic Miss | 0 |
| q_d45672b1d616d77f | what are other names for color blindness | ms_marco | Ranking Error | 1 |
| q_2df065b3c39b3c75 | what does NT mean | ms_marco | Ranking Error | 1 |
| q_f42463324a23f655 | what is the cerebellum known as | ms_marco | Ranking Error | 1 |
| q_9cd57115c69eb4f4 | how to pack a kitchen for a move | ms_marco | Ranking Error | 1 |
| q_cf18e0d0cc2f6634 | does castor oil grow eyebrow hair | ms_marco | Ranking Error | 1 |
| q_72cbee5ec4899934 | what language is spoken in singapore | ms_marco | Ranking Error | 1 |
| q_9eb6dc5f0153c149 | how to remove a locked door handle without the key | ms_marco | Ranking Error | 1 |
| q_c396cfcc20ee5d64 | what do the arteries do in the respiratory system | ms_marco | Ranking Error | 1 |
| q_37fe084ec376e81b | what is a semitone | ms_marco | Ranking Error | 1 |
| q_9eb385f3a451f78e | warning signs of someone contemplating suicide | ms_marco | Ranking Error | 1 |
| q_e5b9695db7543433 | how much does it cost to replace struts and shocks | ms_marco | Ranking Error | 1 |
| q_3f8acbd55c68ca9b | how to calculate %w/w of a liquid | ms_marco | Ranking Error | 1 |
| q_21357402249160e2 | what breed is the american pitbull | ms_marco | Ranking Error | 1 |
| q_d0e735d88d63d0ad | what causes purple urine | ms_marco | Ranking Error | 1 |
| q_2856a4c0bab5d61d | is fountain grass perennial | ms_marco | Ranking Error | 1 |
| q_a9959444c29da033 | what to do in chamonix in summer | ms_marco | Ranking Error | 1 |
| q_4d8f1696c2fbeb07 | how much to get a dent pulled out | ms_marco | Ranking Error | 1 |
| q_a0518d63742e58f5 | what stops r on mexican riviera cruise? | ms_marco | Ranking Error | 1 |
| q_b9aeaa83c776d48c | is maltitol natural | ms_marco | Ranking Error | 1 |
| q_941a97a0a896680f | What sometimes follows moving chloroplasts? | squad | Semantic Miss | 0 |
| q_a98935f3f6b6d6d0 | what does astaxanthin do for skin | ms_marco | Ranking Error | 1 |
| q_7a0712cff530d8d9 | What nationality is the name Lamendola | ms_marco | Semantic Miss | 0 |
| q_902cec8dc43f19d2 | who discovered the structure of dna the story | ms_marco | Ranking Error | 1 |
| q_b1292cef5f773b5d | can a mid level see new patients per medicare guidelines | ms_marco | Semantic Miss | 0 |
| q_c632b72ff10065b6 | What goal do many of these protests have? | squad | Semantic Miss | 0 |
| q_4562b06b01f5d42f | cost of garage door openers installed | ms_marco | Ranking Error | 1 |
| q_ef3b10fbd09093bd | What is the standard measurement for mass? | sciq | Ranking Error | 1 |
| q_86f3aa7c7a2f2dec | airport near providence ri | ms_marco | Ranking Error | 1 |
| q_5ce0c944e89c6ed7 | how do I remove microsoft office trial | ms_marco | Ranking Error | 1 |
| q_07dc8ab3f3ece3e8 | which layer of the earth is made mostly of granite and rocks | ms_marco | Ranking Error | 1 |
| q_496f267da4c2342d | what is dhcp reservation used for | ms_marco | Ranking Error | 1 |
| q_3c4a51c4c02c01e7 | is saffron poisonous | ms_marco | Ranking Error | 1 |
| q_a333b8a27920a042 | what is a bant deck mtg | ms_marco | Ranking Error | 1 |
| q_2b0f2c7537c961db | how much does assisted living facilities in manchester nj cost | ms_marco | Ranking Error | 1 |
| q_2247260ea087afa0 | if quantity demanded goes down what happens to total revenue | ms_marco | Ranking Error | 1 |
| q_adad3855ecbbbfcb | which statement best describes the concept of binding price ceiling | ms_marco | Semantic Miss | 0 |
| q_9993e063121d3531 | what is the currency in haiti | ms_marco | Ranking Error | 1 |
| q_b2ab0b9c70c1c7a5 | where did ansel adams live | ms_marco | Semantic Miss | 0 |
| q_e87687339c332d6c | SNP definition | ms_marco | Ranking Error | 1 |
| q_ad32d0832fbebe24 | what is slander or libel | ms_marco | Ranking Error | 1 |
| q_38d6701a6df8be67 | is orchid a angiosperm | ms_marco | Ranking Error | 1 |
| q_eaf9adf04b1e3d81 | between which two plates are the himalayan mountains forming | ms_marco | Ranking Error | 1 |
| q_656fa55d3dc42c90 | Who conceptualized the piston? | squad | Semantic Miss | 0 |
| q_49f5ec76b826f0d2 | initialize the app | code_search_net | Semantic Miss | 0 |
| q_342dd3a11522fab4 | average salary for bank president | ms_marco | Ranking Error | 1 |
| q_c4a0535628b0a30f | how to close a recessionary gap by fiscal policy | ms_marco | Ranking Error | 1 |
| q_1294a2c16e81a522 | what is ioffer website | ms_marco | Ranking Error | 1 |
| q_8407c0359ecaa5e5 | Transport of nutrients and regulation of body temperature through fluid flow are characteristics of which bodily system? | sciq | Semantic Miss | 0 |
| q_7dda0cd213f2d3e9 | what is cumulative standard normal distribution | ms_marco | Ranking Error | 1 |
| q_608591b5df7f2104 | replacing permanent resident card canada | ms_marco | Semantic Miss | 0 |
| q_a192517095154571 | what is sarin | ms_marco | Ranking Error | 1 |
| q_4339968ed1e6def2 | are squamous epithelial cells cancerous | ms_marco | Ranking Error | 1 |
| q_1406c8514f79a3b6 | where was will rogers born | ms_marco | Ranking Error | 1 |
| q_086092426c7a440c | democratic convention define majority | ms_marco | Ranking Error | 1 |
| q_0b42075a53e8ce84 | where was the Pantheon built | ms_marco | Ranking Error | 1 |
| q_0377b00f5e683454 | metabolic causes of ataxia | ms_marco | Ranking Error | 1 |
| q_774e41994a519b73 | what is a long term problem for patients with emphysema | ms_marco | Ranking Error | 1 |
| q_224781cd2d600507 | how to keep ants out of grass | ms_marco | Ranking Error | 1 |
| q_b8b19b8bd0934c16 | average cost of sweater | ms_marco | Ranking Error | 1 |
| q_0cdd0745bc980b6c | what age is parental responsibility | ms_marco | Ranking Error | 1 |
| q_eb86ded08496633f | how long do you cook a boiled egg | ms_marco | Ranking Error | 1 |
| q_df2671a58a073acf | what is the one part of a nucleotide that differs | ms_marco | Ranking Error | 1 |
| q_035132ce71e58668 | where does spaghetti originate from | ms_marco | Ranking Error | 1 |
| q_c5899502f77099f6 | what is the thyroid responsible for | ms_marco | Ranking Error | 1 |
| q_ed75f3c10de74c9e | what kind of food is served at a luau | ms_marco | Ranking Error | 1 |
| q_40221c70cc8556d4 | where was steven spielberg born | ms_marco | Ranking Error | 1 |
| q_cd14b70706ee399d | who plays which characters in hamilton | ms_marco | Ranking Error | 1 |
| q_e7e797f3ad1539ae | what type of pathogen is ebola | ms_marco | Ranking Error | 1 |
| q_0f48fee56bcfef0c | A rug by which Russian-born British designer is included in the V&A collection? | squad | Ranking Error | 1 |
| q_f1e775f85ec70531 | how much should a kitten drink | ms_marco | Semantic Miss | 0 |
| q_6bff56a9ae5f6d95 | does using a proxy server hide from your isp? | ms_marco | Ranking Error | 1 |
| q_19ac8fd6286d3bdf | can you cable a mimosa tree | ms_marco | Ranking Error | 1 |
| q_abbe6bb71375425b | do ford vehicles have wifi | ms_marco | Ranking Error | 1 |
| q_a8cf4a9b2f656060 | who was budding inventor | ms_marco | Ranking Error | 1 |
| q_3db22958f11b466d | what eukaryotic cell structure contains DNA | ms_marco | Ranking Error | 1 |
| q_ea520b8eab8304b8 | insoluble fiber foods | ms_marco | Semantic Miss | 0 |
| q_2b4328134fe4ea93 | how much should i pay for carpet cleaning | ms_marco | Ranking Error | 1 |
| q_bdc75d3c3c6e7565 | what do the gonadal veins drain | ms_marco | Ranking Error | 1 |
| q_942ec47d6bd4026c | who sang it's a new day originally | ms_marco | Ranking Error | 1 |
| q_36c2e17915b92f0b | what is the average cost of replacement windows installed | ms_marco | Ranking Error | 1 |
| q_c73e757e955ed4b7 | what specific tasks do paramedics do | ms_marco | Ranking Error | 1 |
| q_410576747223f7f8 | how to find serial number on dell | ms_marco | Ranking Error | 1 |
| q_b3d615c88c44c914 | what genre is twisted metal | ms_marco | Ranking Error | 1 |
| q_eebb067e3f737c0d | average carbs per day female | ms_marco | Semantic Miss | 0 |
| q_66aff557dbebff39 | how much to charge for architectural rendering | ms_marco | Semantic Miss | 0 |
| q_aa11811f9c8a1a2c | what is the system that makes up your body | ms_marco | Ranking Error | 1 |
| q_ddcc10aa0d270f2c | foods to avoid during implantation | ms_marco | Ranking Error | 1 |
| q_5c1fbf7288ceda14 | . | code_search_net | Semantic Miss | 0 |
| q_96fddaf107fd4935 | what does contemporaneous mean | ms_marco | Ranking Error | 1 |
| q_2dc86fc71a65b557 | what is detachment | ms_marco | Ranking Error | 1 |
| q_0409803fda66cbbb | how long to cook a boiled egg | ms_marco | Ranking Error | 1 |
| q_77e1508c34e138c1 | what does the name lathan mean | ms_marco | Ranking Error | 1 |
| q_c03e969d7209a441 | What was the protest in Antigone about? | squad | Semantic Miss | 0 |
| q_87d6fe93017eccd8 | what is the significance of the fact that the human trachea is reinforced | ms_marco | Ranking Error | 1 |
| q_4919a8791c5607e0 | what is a grocery store | ms_marco | Ranking Error | 1 |
| q_675b482790788dcd | what are chiefdoms | ms_marco | Ranking Error | 1 |
| q_77393ca36fb30a74 | fluid reabsorption is isotonic | ms_marco | Ranking Error | 1 |
| q_f8724479835cc8cc | what is cilia function | ms_marco | Ranking Error | 1 |
| q_fbf1ef584014be3e | how long to keep financial records irs | ms_marco | Ranking Error | 1 |
| q_e4b11d3d2c5aa419 | what is nco content | ms_marco | Ranking Error | 1 |
| q_08cad17db3af8c66 | how does benedict's solution work | ms_marco | Ranking Error | 1 |
| q_a79c920f42319558 | host of the first season of american idol | ms_marco | Ranking Error | 1 |
| q_5a37be22d5e862df | What can lead to higher wages for members of labor organizations? | squad | Ranking Error | 1 |
| q_4846bc6e0f32e872 | what did the intolerable acts do | ms_marco | Ranking Error | 1 |
| q_1d97cf94d559a20b | can you opt to tax part of a building | ms_marco | Ranking Error | 1 |
| q_ec4b55f86a31fa43 | temperature to incubate turkey eggs | ms_marco | Semantic Miss | 0 |
| q_539327baa9ecca6a | when are babies supposed to stand with help | ms_marco | Ranking Error | 1 |
| q_a1bde0f9b79b766e | what are glycolipids | ms_marco | Ranking Error | 1 |
| q_dd9cab904aa11885 | what is the compound needed for photosynthesis | ms_marco | Ranking Error | 1 |
| q_ba584979d86470b3 | is there spirulina in algae | ms_marco | Ranking Error | 1 |
| q_72d2eab2148d759c | how long to hatch duck eggs | ms_marco | Ranking Error | 1 |
| q_04e068d13dc44b2d | how fast does bamboo grow in a day | ms_marco | Ranking Error | 1 |
| q_7b64b69bf749cb39 | what is degenerative scoliosis | ms_marco | Ranking Error | 1 |
| q_684c75249d771f35 | what kind of government does japan have | ms_marco | Ranking Error | 1 |
| q_0e9cac58528a5777 | definition of motion rate | ms_marco | Ranking Error | 1 |
| q_37f70eb1f69a54f2 | with open("brandon_testing/test_"+str(time.clock())+".csv","w") as f:
	writer = csv.writer(f,delimiter=",")
	for row in fin:
	    writer.writerow(row) | code_search_net | Semantic Miss | 0 |
| q_89f80a82e2707ca8 | what are human tissues | ms_marco | Ranking Error | 1 |
| q_54a240909cc30a28 | earth temperature range | ms_marco | Ranking Error | 1 |
| q_7fc06f1a539a4725 | common source of adenovirus | ms_marco | Ranking Error | 1 |
| q_7146c1caa3289107 | What characteristic of oxygen makes it necessary to life? | squad | Ranking Error | 1 |
| q_9f82ad2865a89bf5 | what foods are cruciferous foods | ms_marco | Ranking Error | 1 |
| q_62ec245e80c09632 | (internal) | code_search_net | Semantic Miss | 0 |
| q_70bf08342501eb29 | different types of salivary glands | ms_marco | Ranking Error | 1 |
| q_0e5e99f3f6f27acb | how long does it take to get passport renewed | ms_marco | Ranking Error | 1 |
| q_e9cad5ed8e40e626 | how long does a gas water heater take to heat up | ms_marco | Ranking Error | 1 |
| q_7ff8b0114814ec56 | what is vestibular rehabilitation | ms_marco | Ranking Error | 1 |
| q_f1f2295eb4eee7d7 | inflammation around the heart medical term | ms_marco | Semantic Miss | 0 |
| q_d6df27fb7912b131 | how long to steam asparagus in microwave | ms_marco | Ranking Error | 1 |
| q_30140cc9946ed353 | what is the yearly salary of a boat builder? | ms_marco | Ranking Error | 1 |
| q_7fe37e5e1ee6f948 | what organelle stores calcium | ms_marco | Ranking Error | 1 |
| q_2c0787e6fef49c18 | granite countertops cost per square foot installed | ms_marco | Ranking Error | 1 |
| q_2e4390db9e34cb09 | what nutrient is important in the transport of oxygen in blood and in muscle tissue | ms_marco | Semantic Miss | 0 |
| q_5dba661751891c3f | How much does a Probationer earn, initially? | squad | Semantic Miss | 0 |
| q_3a68dd91057aad69 | why is crude oil separated into | ms_marco | Ranking Error | 1 |
| q_4db98166bb68de4c | Who started rumors in 2008 that ABC would sell its ten owned-and-operated stations? | squad | Ranking Error | 1 |
| q_06276aaa54a7ee72 | how much does it cost to geld a donkey | ms_marco | Ranking Error | 1 |
| q_e424f4c69f3c0144 | average temp budapest october | ms_marco | Ranking Error | 1 |
| q_5217bda6e6d08e2b | what is an inflamed esophagus | ms_marco | Ranking Error | 1 |
| q_29b73586c3eb9013 | how to add a picture when creating an event on facebook | ms_marco | Ranking Error | 1 |
| q_4656e5e7da14d46d | different names for sugars | ms_marco | Ranking Error | 1 |
| q_66ebba0b9dbaa47c | how much should home appraisal cost | ms_marco | Ranking Error | 1 |
| q_9a030add1da1970d | is isobutylene recyclable | ms_marco | Ranking Error | 1 |
| q_080ced6c880e3540 | what is curcumin good for | ms_marco | Ranking Error | 1 |
| q_9153e5b2b667b7d0 | What was put on pylons for Super Bowl 50? | squad | Ranking Error | 1 |
| q_8bf6867939d5e8a8 | dissociative identity disorder meaning | ms_marco | Ranking Error | 1 |
| q_19dc1e43c4209c5d | what causes arteries to harden | ms_marco | Semantic Miss | 0 |
| q_5ef0cf5952fa84e0 | what is flagella | ms_marco | Ranking Error | 1 |
| q_69469f92f1abd160 | what is maleate | ms_marco | Ranking Error | 1 |
| q_82f0c741efbcf20d | calligrapher definition | ms_marco | Ranking Error | 1 |
| q_c0e557a82729bff7 | what is dietary fiber | ms_marco | Ranking Error | 1 |
| q_aed88f938436b29c | what is the foramen ovale | ms_marco | Ranking Error | 1 |
| q_5459a8c87af95a71 | who can notarize | ms_marco | Ranking Error | 1 |
| q_3eb3b0175917b38c | Where is the river Danube and where is its source and length | ms_marco | Ranking Error | 1 |
| q_088dbca5be5d7d6d | what is a siren mermaid | ms_marco | Ranking Error | 1 |
| q_5b5d7a18940e437c | how much ntuc membership fee | ms_marco | Ranking Error | 1 |
| q_fb62c874e6c1eec1 | definition occupational therapy | ms_marco | Ranking Error | 1 |
| q_8f61fed07800bc04 | meaning of kiersten name | ms_marco | Ranking Error | 1 |
| q_9811067c6b683092 | how does temperature vary with altitude in earth's atmosphere | ms_marco | Ranking Error | 1 |
| q_d097521ec8c42a46 | what is an animal called that eats other animals its own kind | ms_marco | Ranking Error | 1 |
| q_b3c50a158ac950f3 | what was the name of the operation of the invasion of poland | ms_marco | Ranking Error | 1 |
| q_76735d9735340db8 | definition of IBR disease | ms_marco | Ranking Error | 1 |
| q_fcd22c36b657f3f8 | where is ramada shoal bay | ms_marco | Ranking Error | 1 |
| q_451b5f3666963afd | what does a adjective mean | ms_marco | Ranking Error | 1 |
| q_2ec6ec3b165fc822 | what gland secretes a substance that regulates glucose | ms_marco | Semantic Miss | 0 |
| q_c03ce9ee981dc99d | driver side window motor replacement cost | ms_marco | Ranking Error | 1 |
| q_df7817309cef4a90 | Where did he live while he was looking good? | squad | Semantic Miss | 0 |
| q_97c40d3a97318db6 | snake goddess meaning | ms_marco | Ranking Error | 1 |
| q_8044b68646d40143 | does the coast guard have free housing | ms_marco | Ranking Error | 1 |
| q_69a283956df6a642 | how does laser measure distance | ms_marco | Ranking Error | 1 |
| q_b398bc550d6422ab | what is occupational therapist | ms_marco | Ranking Error | 1 |
| q_ff71d4ec82d27e74 | The migration of what familiar coastal landform involves saltation and gravity? | sciq | Semantic Miss | 0 |
| q_b08ecabf186540f8 | is there something called a recorder but looks like a flute | ms_marco | Ranking Error | 1 |
| q_837b2a0c6bb087b8 | what does epinephrine do to peripheral vessels | ms_marco | Ranking Error | 1 |
| q_9c13420a713c4809 | what are gaba receptors for | ms_marco | Ranking Error | 1 |
| q_09bfff3c38649cf0 | how long does it take to do an access course | ms_marco | Ranking Error | 1 |
| q_da5b1794848bf9cd | fertilization occurs when which cells unite | ms_marco | Ranking Error | 1 |
| q_f66300a3b32d5f0c | how much does a tuxedo cost to rent | ms_marco | Ranking Error | 1 |
| q_24456e3ef1c0ebfb | does visio require office | ms_marco | Ranking Error | 1 |
| q_ea5597dd11f8d8e5 | what causes overactive nerves | ms_marco | Semantic Miss | 0 |
| q_2f78fbd744a8d470 | What is CSNET | squad | Semantic Miss | 0 |
| q_603a55ddc4599e1c | When was this proclamation issued? | squad | Semantic Miss | 0 |
| q_4e798a3b77801cc9 | why is this reaction called a hydrolytic reaction | ms_marco | Ranking Error | 1 |
| q_221dcb356e77466b | what conditions do viruses need to grow | ms_marco | Ranking Error | 1 |
| q_3161d5b2b42e11f6 | what type of volcano is mount vesuvius | ms_marco | Ranking Error | 1 |
| q_392ab1eefa464ebc | building an extension cost | ms_marco | Ranking Error | 1 |
| q_ffa5d15893f487bc | what is a constructive trustee | ms_marco | Ranking Error | 1 |
| q_2d7c329b2ad0fa6b | Where can the Treatise be found? | squad | Semantic Miss | 0 |
| q_bf03e18d20184998 | why does dissolved oxygen decrease as temperature increases | ms_marco | Ranking Error | 1 |
| q_1d7905e43e5c8baa | what does depictions mean | ms_marco | Ranking Error | 1 |
| q_1d067946c14ab54e | chemoreceptor reflex definition | ms_marco | Ranking Error | 1 |
| q_d0ad52e065d6baa7 | should people with mental illnesses be in a relationship | ms_marco | Ranking Error | 1 |
| q_12e42fc0e2558136 | what is knee arthroplasty cause | ms_marco | Ranking Error | 1 |
| q_b23341c54421fc24 | where does author's name go in a citation for a website | ms_marco | Ranking Error | 1 |
| q_df0e062eef233044 | how much does a turf field cost to install | ms_marco | Ranking Error | 1 |
| q_f9b26e5c8272b835 | what tissues are in the diaphragm respiratory system | ms_marco | Ranking Error | 1 |
| q_21e31f4e3b29509f | replacing insulation under mobile home | ms_marco | Ranking Error | 1 |
| q_7aca8c5d014d4367 | describe igneous rocks | ms_marco | Ranking Error | 1 |
| q_9d34f3c28b9bad93 | what is quilting | ms_marco | Ranking Error | 1 |
| q_535435fafb26ba5c | what does the peripheral nervous system do | ms_marco | Ranking Error | 1 |
| q_0c613a9867679b3a | what super score do you need vanderbilt | ms_marco | Ranking Error | 1 |
| q_c2d5d30c50978609 | standard deduction if someone can claim you as a dependent | ms_marco | Ranking Error | 1 |
| q_0363751a4945719f | research study protocol meaning | ms_marco | Ranking Error | 1 |
| q_a0933f030c1c3596 | what colours represent what emotions | ms_marco | Ranking Error | 1 |
| q_131589687d7859b8 | how much is an mep paid | ms_marco | Ranking Error | 1 |
| q_d9dc4a018c5d7e0b | average salary of nasl soccer player | ms_marco | Ranking Error | 1 |
| q_1847858d6c2dd571 | how far from a fence should you plant a tree | ms_marco | Ranking Error | 1 |
| q_fdd40bbed493e051 | why does facebook ask for your email password on sign up | ms_marco | Ranking Error | 1 |
| q_b4023c603bc2df8f | litotes definition and examples | ms_marco | Ranking Error | 1 |
| q_f3162fc4bcb5fed4 | how important was the issue of slavery in the constitution quizlet | ms_marco | Semantic Miss | 0 |
| q_77c1b33afa3baf96 | what temperature is a roast done | ms_marco | Ranking Error | 1 |
| q_a1b08e35a4ffc78d | what is the classification of flatworms | ms_marco | Ranking Error | 1 |
| q_8a40c54344fb277c | why is hydroxychloroquine prescribed for lupus | ms_marco | Ranking Error | 1 |
| q_42866abe72a1b4c7 | cooking time for a leg of lamb per kg | ms_marco | Ranking Error | 1 |
| q_885d846718973bb6 | cost of whatsapp call | ms_marco | Ranking Error | 1 |
| q_b493bd46f078802b | what side do you wear someone else's medals | ms_marco | Ranking Error | 1 |
| q_1c1a4ea30fb2f7fb | when filling a job application and it asks salary what does it mean | ms_marco | Semantic Miss | 0 |
| q_da56d8862c769743 | what is seedling | ms_marco | Ranking Error | 1 |
| q_7448ef8249b1c02b | can alcohol cause psychosis | ms_marco | Semantic Miss | 0 |
| q_48dcbd65ed0b3cf1 | what kind of tea do they drink in india | ms_marco | Ranking Error | 1 |
| q_9b24e4e32329fbba | how do strong bases burn skin | ms_marco | Ranking Error | 1 |
| q_a43089af4700a69f | How was this possible | squad | Ranking Error | 1 |
| q_127e439e5d045c04 | What is the replication fork? Why is it called a “fork”? | ms_marco | Ranking Error | 1 |
| q_8798861cd2bb1664 | What is the most common cause of lung cancer? | sciq | Semantic Miss | 0 |
| q_f49400f582ed0040 | what causes stye | ms_marco | Ranking Error | 1 |
| q_cb6ce3b13adafc7b | how do i open pictures in windows media player | ms_marco | Ranking Error | 1 |
| q_d044940e96285771 | what temperature do you keep baby quail | ms_marco | Ranking Error | 1 |
| q_159e15ea8baccbd3 | how much salary translator | ms_marco | Ranking Error | 1 |
| q_a756e384dc1cab8c | explain the dawes act | ms_marco | Ranking Error | 1 |
| q_ffacba68a7a57cce | linguistic authenticity definition | ms_marco | Ranking Error | 1 |
| q_f1c4c99e52e0497a | baby name lina pronunciation | ms_marco | Ranking Error | 1 |
| q_d6a70bb2da0a6600 | how long does a respiratory infection last | ms_marco | Ranking Error | 1 |
| q_d086561d8c5a9811 | cost of marble countertops | ms_marco | Semantic Miss | 0 |
| q_0641f88c959c6768 | where was the waltons filmed | ms_marco | Ranking Error | 1 |
| q_a62822e9ce4e546a | where is the okefenokee swamp located | ms_marco | Ranking Error | 1 |
| q_02320d85c8e6bb86 | cardioversion definition | ms_marco | Ranking Error | 1 |
| q_07756d2e5a64f91b | how much does it cost to get a cat declawed | ms_marco | Ranking Error | 1 |
| q_a0a1423b1a050fad | what is the average cost of a vet visit for a dog | ms_marco | Ranking Error | 1 |
| q_b1890e199c01bef8 | what causes overactive nerve pain | ms_marco | Ranking Error | 1 |
| q_b0325205e6164656 | what is iguana | ms_marco | Ranking Error | 1 |
| q_0979ecfeb475cbf2 | what are dust diseases | ms_marco | Ranking Error | 1 |
| q_2c0bd917853bee3f | what are cracklins | ms_marco | Ranking Error | 1 |
| q_4ce4e9faf49c477d | where to buy vivosmart hr activity tracker | ms_marco | Semantic Miss | 0 |
| q_6cd1af782cbbe88f | how much is a superintendent salary in new york | ms_marco | Ranking Error | 1 |
| q_96fd750f5f412d8a | What US war has a large amount of Civil Disobedients? | squad | Semantic Miss | 0 |
| q_628dbfe3786cba57 | best coolant stop leak | ms_marco | Ranking Error | 1 |
| q_f97139147cfda6e1 | define human behaviour | ms_marco | Ranking Error | 1 |
| q_67aa9423afe78ee6 | what is the primary function of the thyroid hormones quizlet | ms_marco | Semantic Miss | 0 |
| q_83e8c4e8cea4be51 | cost of catering services for a wedding | ms_marco | Ranking Error | 1 |
| q_bdcd6994573ca721 | how did russia own alaska | ms_marco | Semantic Miss | 0 |
| q_ee1bf5cf3e2b9a63 | which is better tuna or salmon | ms_marco | Ranking Error | 1 |
| q_bce19d50da62fe59 | how much do you pay for a dog | ms_marco | Ranking Error | 1 |
| q_b5068ec3b24b9969 | what is the meaning of demetri | ms_marco | Ranking Error | 1 |
| q_b440732193b3e86e | what is masterbatch | ms_marco | Ranking Error | 1 |
| q_22c0d1d41c1162b5 | what are the four types of dissociative disorders | ms_marco | Ranking Error | 1 |
| q_1bdf44eff46b9a85 | how old is mattie jackson | ms_marco | Ranking Error | 1 |
| q_0dca935d7fcc3423 | what tyt means | ms_marco | Ranking Error | 1 |
| q_3492624fac3dd302 | what type of bond does a janitorial service need | ms_marco | Ranking Error | 1 |
| q_e12b3eb006d03f2d | what is trap | ms_marco | Ranking Error | 1 |
| q_9e1846267397245c | . | code_search_net | Semantic Miss | 0 |
| q_fc7a96a79331561a | what do transcription factors do in eukaryotic cells | ms_marco | Ranking Error | 1 |
| q_301b2f59f6877a49 | recommended dose for ondansetron | ms_marco | Ranking Error | 1 |
| q_3822f31038cc77b6 | how fattening is honey | ms_marco | Ranking Error | 1 |
| q_15aabfb43d49f4ea | explain diversity in your own words | ms_marco | Ranking Error | 1 |
| q_ac6a5ecbfe96b9e9 | average cost to install architectural shingles | ms_marco | Ranking Error | 1 |
| q_c97f3eab01a0a402 | Where was Tesla's new lab? | squad | Ranking Error | 1 |
| q_7d0d80ba45aaf477 | where was horse whisperer filmed | ms_marco | Ranking Error | 1 |
| q_6c1733f37bfa0bf0 | What do beroids typically eat? | squad | Semantic Miss | 0 |
| q_d969b539ca9584c5 | why is brassica rapa a good model organism | ms_marco | Ranking Error | 1 |
| q_73823efc58425bd0 | tiles installation cost estimate | ms_marco | Semantic Miss | 0 |
| q_69b2e4c525678d61 | is portugal a republic | ms_marco | Ranking Error | 1 |
| q_848f42602d3d133d | what are bibliography of different viruses | ms_marco | Ranking Error | 1 |
| q_057e405729bf2a26 | what process does human cells use to generate more atp | ms_marco | Ranking Error | 1 |
| q_99c567e995847fb2 | is a castor beans venomous | ms_marco | Ranking Error | 1 |
| q_9f81ac9304c30c4b | what is a basilar migraine | ms_marco | Ranking Error | 1 |
| q_855f00dd6c1b79a1 | what are the sensory receptor for balance name | ms_marco | Semantic Miss | 0 |
| q_cea4cfba45501ff5 | Who lost to the Broncos in the AFC Championship? | squad | Ranking Error | 1 |
| q_cc074d6293524a15 | meaning of eagles | ms_marco | Ranking Error | 1 |
| q_1a2c35e404da6dd8 | what is the thoracic vena cava also called | ms_marco | Semantic Miss | 0 |
| q_f08a0a2da7bc4461 | how many years do i need to wear my retainer | ms_marco | Ranking Error | 1 |
| q_f43c951b8b9de17d | what is a vaccination | ms_marco | Ranking Error | 1 |
| q_23fb72f55220df72 | is vetch edible | ms_marco | Ranking Error | 1 |
| q_c6ed9fde1eecc0ea | describe where the river tillingbourne is | ms_marco | Ranking Error | 1 |
| q_6a2e06a2ca7da50e | CCAC tuition and fees | ms_marco | Ranking Error | 1 |
| q_c1cf9e12039c03bf | what kind of infections does a z pack treat | ms_marco | Semantic Miss | 0 |
| q_f7c4610908c15431 | how to prevent recurrence of pinworms | ms_marco | Ranking Error | 1 |
| q_7de7be48b86f11cc | definition of an electron | ms_marco | Ranking Error | 1 |
| q_f18c1605d0032299 | what is the function of salivary amylase | ms_marco | Ranking Error | 1 |
| q_8749ed035f8732ae | where does the gulf stream flow | ms_marco | Semantic Miss | 0 |
| q_bc6c93ad98eab34a | what is aboriginal ochre | ms_marco | Ranking Error | 1 |
| q_26d1fdce113e785e | average cost of bills per month | ms_marco | Ranking Error | 1 |
| q_0d1268e5e1d30279 | router for wireless internet connection walmart | ms_marco | Ranking Error | 1 |
| q_cd703eff1adc98a9 | what is bupropion used to treat | ms_marco | Semantic Miss | 0 |
| q_a70867075a1aba05 | what pressure is the eye of the hurricane | ms_marco | Ranking Error | 1 |
| q_1278c83c0f653270 | what is lagna in astrology | ms_marco | Ranking Error | 1 |
| q_9a1e6ed8ebfe40a0 | what kind of ulcers are caused by stress | ms_marco | Semantic Miss | 0 |
| q_498fece285cdcbde | difference between plant air and instrument air | ms_marco | Ranking Error | 1 |
| q_e277fb92dc47ea21 | what level is hnd qualification | ms_marco | Ranking Error | 1 |
| q_14683a3bb05360b8 | where does the optic nerve end | ms_marco | Ranking Error | 1 |
| q_1b4608ece6c078a7 | how much does a log cabin home cost to build | ms_marco | Ranking Error | 1 |
| q_b43feeea253f44bf | what happened to shergar | ms_marco | Ranking Error | 1 |
| q_81f1437802166dc1 | can a baby be born HIV positive and then be HIV negative | ms_marco | Ranking Error | 1 |
| q_25e95723b1397cd7 | which kingdom contain all unicellular organisms | ms_marco | Ranking Error | 1 |
| q_16595e2b05b1a626 | where is greece | ms_marco | Semantic Miss | 0 |
| q_8b926d134791c7bd | what is the condition called in which the cells persist in stratum corneum layer of skin | ms_marco | Ranking Error | 1 |
| q_60f94760a5efce2f | how much does a pack of printing paper weigh | ms_marco | Semantic Miss | 0 |
| q_11d202f341a355ef | what is the purpose of peroxidase used in elisa | ms_marco | Semantic Miss | 0 |
| q_5f9ada671030e992 | how to take resting pulse rate | ms_marco | Semantic Miss | 0 |
| q_7fac1679753026bd | how much money do first round nfl draft picks make | ms_marco | Ranking Error | 1 |
| q_3853e77af2900377 | are koalas bears vicious | ms_marco | Ranking Error | 1 |
| q_2b6829ffb9e882ef | temperature to cook pork chops | ms_marco | Ranking Error | 1 |
| q_df5a93b63abde084 | can a leader call a nation to prayer | ms_marco | Semantic Miss | 0 |
| q_9f4c6c35dab39e82 | What is the calculation that determines what a batters average is | ms_marco | Ranking Error | 1 |
| q_eeaebb380661ddb1 | what does sherm mean | ms_marco | Ranking Error | 1 |
| q_658920ba403d1c07 | what are berms | ms_marco | Semantic Miss | 0 |
| q_a3b0be72aa527169 | beef tenderloin internal temperature | ms_marco | Ranking Error | 1 |
| q_c9887cfed1fcb0c9 | what bacteria does doxycycline treat | ms_marco | Ranking Error | 1 |
| q_3c1273d18fa63f8e | where in the body is urea excreted | ms_marco | Ranking Error | 1 |
| q_59d529cf6be5e8fe | what unit of wavelength is a de broglie | ms_marco | Ranking Error | 1 |
| q_6adc29aea4a49981 | how to invest in bitcoin | ms_marco | Ranking Error | 1 |
| q_fa2b5c52607b387c | are upper respiratory infections contagious in dogs | ms_marco | Semantic Miss | 0 |
| q_4dfa2e2d143b7813 | what actor played moses | ms_marco | Semantic Miss | 0 |
| q_ca8a23c90caab754 | where is dilley texas | ms_marco | Ranking Error | 1 |
| q_add383f68d092194 | what are b complex vitamins good for | ms_marco | Ranking Error | 1 |
| q_05b240f56fcda055 | is protease the same as pepsin | ms_marco | Ranking Error | 1 |
| q_8f76721fa68d507e | WHat states do alligators live in | ms_marco | Ranking Error | 1 |
| q_87aa27098043056c | state the names of two scientists who helped develop the periodic table | ms_marco | Ranking Error | 1 |
| q_e92d25bb3c232281 | where are the leeward islands located | ms_marco | Ranking Error | 1 |
| q_9904d34f7c8a9a5b | what is sinus tract | ms_marco | Ranking Error | 1 |
| q_72bea26561e92362 | what is the name of a four sided shape | ms_marco | Ranking Error | 1 |
| q_a77f42adf2823d43 | tuition cost at university of iowa | ms_marco | Ranking Error | 1 |
| q_7b3d57846bac36bf | what are bairdi crab | ms_marco | Ranking Error | 1 |
| q_e4151c38d71768b7 | when did renaissance start | ms_marco | Ranking Error | 1 |
| q_5dca4f45bc906a06 | what time was treaty of versailles signed at | ms_marco | Ranking Error | 1 |
| q_a09cf56d3fce4c0b | what is beltane celebration | ms_marco | Semantic Miss | 0 |
| q_93c51d2c402d831e | what are young rabbits called | ms_marco | Ranking Error | 1 |
| q_f8dbefbadcf00bd8 | what is location based marketing | ms_marco | Ranking Error | 1 |
| q_c9ad5d2c04375328 | how to change credit card limit uob | ms_marco | Ranking Error | 1 |
| q_fc2006904bcff60a | how many types of slugs are there | ms_marco | Ranking Error | 1 |
| q_027c02117b6e5857 | how much does a wedding blessing cost | ms_marco | Ranking Error | 1 |
| q_2895f72faf6f95f2 | what is a certified nurse midwife | ms_marco | Ranking Error | 1 |
| q_ac05dde4f98f43d7 | when was john o'sullivan born | ms_marco | Ranking Error | 1 |
| q_ec7f093de1d35edf | meaning of the name kayla | ms_marco | Ranking Error | 1 |
| q_af01b94bcd3fd896 | what is ethnography pdf | ms_marco | Ranking Error | 1 |
| q_f024d600fce79b56 | what is the difference between business and first class on american airlines | ms_marco | Ranking Error | 1 |
| q_b9086f050f46bc70 | Name a text that might be used by a religious teacher to teach. | squad | Semantic Miss | 0 |
| q_bf077bde18f155f4 | meaning of the name lindze | ms_marco | Semantic Miss | 0 |
| q_eb5291f7ad92393e | can ira's be gifted to charity | ms_marco | Ranking Error | 1 |
| q_b5f89d5efb093fd2 | is up to his ears | ms_marco | Ranking Error | 1 |
| q_16a397c3394b5c22 | what does a rash around your ankles mean | ms_marco | Ranking Error | 1 |
| q_74a69b0f09176fad | can you get a universal garage door opener | ms_marco | Ranking Error | 1 |
| q_68348582fedc0e56 | how much urine in a day is normal | ms_marco | Ranking Error | 1 |
| q_0fde8eb71941a97e | is dna backbone basic | ms_marco | Ranking Error | 1 |
| q_e13bf6f7af0f0a9b | meaning of lyme disease | ms_marco | Ranking Error | 1 |
| q_18219e53ef4b18eb | disruptive dysfunctional mood disorder | ms_marco | Ranking Error | 1 |
| q_8434cf994be35bc0 | are fish considered a meat | ms_marco | Ranking Error | 1 |
| q_c2b2dd80ba2455f6 | cost of installing backup sump pump | ms_marco | Ranking Error | 1 |
| q_8a5408ca5796968f | how many immigrants are allowed in the us each year | ms_marco | Ranking Error | 1 |
| q_0e5630baa901ff7c | what is the organism that causes strep throat quizlet | ms_marco | Ranking Error | 1 |
| q_d6ef112e03cdee17 | how much weight does a shipping container hold | ms_marco | Ranking Error | 1 |
| q_7ea57301f71aae52 | what is emotive words used for | ms_marco | Ranking Error | 1 |
| q_445af5a9887650df | where do you go to apply for a mortgage | ms_marco | Ranking Error | 1 |
| q_c1181b3aab1e015b | where is georgia usa | ms_marco | Ranking Error | 1 |
| q_741917c25f334ad7 | what is purinethol | ms_marco | Ranking Error | 1 |
| q_05771c643d2cb884 | What year was Temüjin, who became Genghis Khan, likely born? | squad | Semantic Miss | 0 |
| q_cfc564fead4caf61 | what is the salary working at disability teacher | ms_marco | Ranking Error | 1 |
| q_d3f3d974ec4ab676 | what is a parole officer | ms_marco | Ranking Error | 1 |
| q_b7323b0af0a40ab8 | selu annual cost of housing | ms_marco | Ranking Error | 1 |
| q_8e4839fcdd144cb8 | process of clotting blood | ms_marco | Ranking Error | 1 |
| q_a48f3e5ef030e71b | what is genetic diversity within a species | ms_marco | Ranking Error | 1 |
| q_76e28a9cccf0cc99 | what were the frontier wars | ms_marco | Ranking Error | 1 |
| q_80a41fba9f1d3b5b | how much force can human withstand | ms_marco | Ranking Error | 1 |
| q_228e8612ab7f1259 | what is pos system in hotels | ms_marco | Ranking Error | 1 |
| q_ff79ef1b3c9fdc7b | financing campaign definition | ms_marco | Ranking Error | 1 |
| q_babfd8438db627c8 | what is fibrin fibrous tissue | ms_marco | Ranking Error | 1 |
| q_bf14a9aedf244bd8 | what is a takht sikhism | ms_marco | Semantic Miss | 0 |
| q_4838312d3f89255f | what causes cyclones | ms_marco | Ranking Error | 1 |
| q_bda3cdd79fa10180 | what foods are typically eaten in ecuador | ms_marco | Ranking Error | 1 |
| q_2a4e021dc28599f9 | what is aion | ms_marco | Ranking Error | 1 |
| q_12a2178d46b3d884 | what is a whey | ms_marco | Ranking Error | 1 |
| q_de35cc7fed332522 | what diseases does dandelion cure | ms_marco | Ranking Error | 1 |
| q_f3cf435c81b89c76 | cost of partial dentures | ms_marco | Ranking Error | 1 |
| q_1061478eb9a0e139 | net worth of pat sajak | ms_marco | Ranking Error | 1 |
| q_8733543e98b83886 | cost to install super sliding patio door | ms_marco | Ranking Error | 1 |
| q_f1127b3e6e8fdc54 | what is the earliest type of computer | ms_marco | Ranking Error | 1 |
| q_08e95bd14bc1da85 | what servos in flyzone beaver? | ms_marco | Ranking Error | 1 |
| q_c46e1a87398fd9d2 | Save the weights of the trainable variables, each one in a different file in output_path. | code_search_net | Ranking Error | 1 |
| q_e49e0bc25a08eb78 | What are the two main components in a battery? | sciq | Semantic Miss | 0 |
| q_e6569658849f3908 | mova what is inside | ms_marco | Ranking Error | 1 |
| q_d17526c29c3bfce5 | what symbolizes strength | ms_marco | Ranking Error | 1 |
| q_86c327b49f1ffdb0 | era amendment what it says | ms_marco | Ranking Error | 1 |
| q_e12048b2cde6463c | meaning dream of man lying in pool of blood | ms_marco | Ranking Error | 1 |
| q_8ceb425fe54bfd7e | is hymenolepis a protozoan | ms_marco | Ranking Error | 1 |
| q_31c42279eb5e3afc | what is sonnet | ms_marco | Ranking Error | 1 |
| q_458b7d8fd4f23785 | what chemical is in sparklers | ms_marco | Ranking Error | 1 |
| q_e98cb661b3c9523e | Init client | code_search_net | Semantic Miss | 0 |
| q_047e52366b06cdb7 | how long to boil ribs before grilling | ms_marco | Ranking Error | 1 |
| q_e1f2236c08787da7 | where does the lateral cutaneous nerve of the arm come from | ms_marco | Ranking Error | 1 |
| q_a44343c4d934d4a9 | purpose of encumbrance accounting | ms_marco | Ranking Error | 1 |
| q_551bf73d2648a92e | is gallbladder a bile duct | ms_marco | Ranking Error | 1 |
| q_872555d3e6fd3cd3 | what are signs of liver problems from alcohol | ms_marco | Ranking Error | 1 |
| q_dd1d5dd6a9098f45 | what is the difference between dental hygienist and dental assistant salaries | ms_marco | Ranking Error | 1 |
| q_7496935ddc1337c4 | who wrote a dog of flanders crossword | ms_marco | Ranking Error | 1 |
| q_9a4de105c395f25b | what is capocollo | ms_marco | Ranking Error | 1 |
| q_c420f186d43b8c7c | what industry is intel corporation | ms_marco | Ranking Error | 1 |
| q_14d642b749d4e0a9 | how many years do you sleep in a lifetime | ms_marco | Ranking Error | 1 |
| q_2c787e06d59d5e4a | should we do space exploration | ms_marco | Semantic Miss | 0 |
| q_03d1be6eace55c80 | what was the weimar republic what happened | ms_marco | Ranking Error | 1 |
| q_6979b85fd7876d70 | what is identity management system | ms_marco | Ranking Error | 1 |
| q_cda309d76b738e5e | gas plant operator salary | ms_marco | Ranking Error | 1 |
| q_4d2a5bc677b81619 | how much does it cost to rebook a skills test | ms_marco | Ranking Error | 1 |
| q_245736f64ff768ae | What difficulties was Shirly having? | squad | Semantic Miss | 0 |
| q_e6bdfe5ee6ae5577 | what is jujitsu | ms_marco | Ranking Error | 1 |
| q_d912e3b4d770c19f | what is a lease disposition fee | ms_marco | Ranking Error | 1 |
| q_8176bb932848d690 | is twenty one pilots christian | ms_marco | Ranking Error | 1 |
| q_a22d364915e44cfd | biological definition TRAITS | ms_marco | Ranking Error | 1 |
| q_36887afe790edd34 | Main method | code_search_net | Semantic Miss | 0 |
| q_aaef141298c29853 | how much schooling to be an orthopedic surgeon | ms_marco | Ranking Error | 1 |
| q_86cfc92d78076970 | what function does the thyroid have | ms_marco | Ranking Error | 1 |
| q_5aadf471492628fc | how long do cupcakes stay fresh | ms_marco | Ranking Error | 1 |
| q_4ffb50bf2a880480 | Survivial is at the heart of what concept for workers? | squad | Ranking Error | 1 |
| q_19d4b9ab75727396 | recommended dosage of paracetamol | ms_marco | Ranking Error | 1 |
| q_0dee72e6bd2e8248 | what type of barrier isolates gene pools | ms_marco | Ranking Error | 1 |
| q_e6a38788be20a9c2 | why was shays rebellion necessary | ms_marco | Ranking Error | 1 |
| q_bf0b736aaaa7727b | what is habu sake | ms_marco | Ranking Error | 1 |
| q_93ee1e87f178139b | where is the coywolf habitat | ms_marco | Ranking Error | 1 |
| q_8ab191abbd569174 | how long to cook lamb chops in nuwave oven | ms_marco | Ranking Error | 1 |
| q_16495c0e4bf43787 | what is a credit tenant | ms_marco | Ranking Error | 1 |
| q_9aefa3fcf6d95115 | how do you hard cook an egg | ms_marco | Semantic Miss | 0 |
| q_dc6edcf6d8ccb266 | how long do wild baby bunnies nurse | ms_marco | Ranking Error | 1 |
| q_d4942fba157a5a34 | cost of neograft | ms_marco | Ranking Error | 1 |
| q_5bccde080484303a | is there a net torque on the loop of wire from the magnetic field | ms_marco | Ranking Error | 1 |
| q_cbeb10d8eafbb8ad | platinum cost of production per ounce | ms_marco | Ranking Error | 1 |
| q_6238f9047a9f0464 | what does norwegian anretning meaning | ms_marco | Ranking Error | 1 |
| q_1b5d2cde50e7df32 | what is regurgitation through damaged valve | ms_marco | Ranking Error | 1 |
| q_47b266cfadd337a9 | how fast should my pulse be | ms_marco | Ranking Error | 1 |
| q_2172e678b4108314 | which organelle provides energy for translation | ms_marco | Ranking Error | 1 |
| q_133e6774e200c58d | cost of prolotherapy injections | ms_marco | Ranking Error | 1 |
| q_b8146e3ea2ae77a5 | what makes antibodies | ms_marco | Ranking Error | 1 |
| q_44ff702dc67fa1df | what is promethazine hydrochloride and codeine phosphate syrup | ms_marco | Ranking Error | 1 |
| q_56c18c25131a334f | when was the classical period of greek coins | ms_marco | Ranking Error | 1 |
| q_9db82c7c6cdb977a | meaning of quarrying | ms_marco | Ranking Error | 1 |
| q_eaab64d26d9a190f | how much is aaa per month | ms_marco | Ranking Error | 1 |
| q_c415a232b49ae4a3 | how to register more devices on now tv | ms_marco | Ranking Error | 1 |
| q_a07329eb28117284 | how long do a person earn uif | ms_marco | Ranking Error | 1 |
| q_ce7a6ab8dfd36ff1 | what are coordinately controlled genes | ms_marco | Ranking Error | 1 |
| q_17b5e668021ce345 | is it normal for babies to wake a lot at night | ms_marco | Ranking Error | 1 |
| q_3a34bd9e085db1b7 | Which blood vessels is oxygen transferred through? | sciq | Semantic Miss | 0 |
| q_a8e3427185a94eb7 | why do we have different time zones | ms_marco | Ranking Error | 1 |
| q_0638950b90098baa | what causes nodes | ms_marco | Ranking Error | 1 |
| q_bf282de441d111a5 | Why is the statement doubtful in the eyes of scholars? | squad | Semantic Miss | 0 |
| q_1d2b456741f0740d | standard speeding fines | ms_marco | Ranking Error | 1 |
| q_13891fbb61b05405 | when did the grand canyon form | ms_marco | Ranking Error | 1 |
| q_f54c170aee31c969 | what does the trinity symbol mean | ms_marco | Ranking Error | 1 |
| q_3b3c0ae3f3e7d55e | what medication is used for excessive sweating | ms_marco | Ranking Error | 1 |
| q_51304afade0fdabc | What is the force pushing a rocket called? | sciq | Semantic Miss | 0 |
| q_bdea7a9da2dd7f23 | what is essid | ms_marco | Ranking Error | 1 |
| q_a855570482606a81 | identify three types of kidney disorders | ms_marco | Ranking Error | 1 |
| q_b33eaf86f6bc1e4d | cost of implant tooth | ms_marco | Ranking Error | 1 |
| q_bc3376e6612f3e2a | adjectival modifier definition | ms_marco | Semantic Miss | 0 |
| q_d689fa0592d9b405 | tainted blood scandal canada compensation | ms_marco | Ranking Error | 1 |
| q_fdffee1bdf757398 | how are world heritage sites chosen | ms_marco | Semantic Miss | 0 |
| q_961d21b7c2202c0b | how to use a push mower | ms_marco | Ranking Error | 1 |
| q_24c694e620b82be6 | Who assembles the authors' contributions? | squad | Semantic Miss | 0 |
| q_b46fc695820d474b | if i'm married can i claim our kids turbotax | ms_marco | Semantic Miss | 0 |
| q_6ea1b79df904cfe2 | what ethnicity is the last name moody | ms_marco | Ranking Error | 1 |
| q_a81c3ba561e3d076 | resting metabolic rate is often measured instead of bmr because | ms_marco | Ranking Error | 1 |
| q_2b0db52620fcdcdc | cost to fix chimney cap | ms_marco | Semantic Miss | 0 |
| q_919351518b521259 | how long does a knee replacement surgery take to recover from | ms_marco | Semantic Miss | 0 |
| q_523efea4da9be6f6 | what kind of paint to use on glass | ms_marco | Ranking Error | 1 |
| q_dc0e55947ae99e5f | the effects of ozone depletion | ms_marco | Ranking Error | 1 |
| q_11015c8aacca84f1 | definition of life sciences | ms_marco | Ranking Error | 1 |
| q_abe7dcd024da3751 | what bachelor degrees can get you into law | ms_marco | Ranking Error | 1 |
| q_bc6ac3c99629ba68 | price for speeding ticket | ms_marco | Ranking Error | 1 |
| q_b467388cddfbece4 | what biological factors determine an individual's telomere length | ms_marco | Ranking Error | 1 |
| q_1777f9a56116e5b7 | what do dynamic routing protocols do | ms_marco | Ranking Error | 1 |
| q_3177fb4fc01c547b | does aecom pay interns | ms_marco | Ranking Error | 1 |
| q_bfaeb450726ce815 | lowest viable body temperature | ms_marco | Ranking Error | 1 |
| q_1368f716ad8f0d44 | how long does it take to become an acupuncturist | ms_marco | Semantic Miss | 0 |
| q_302741bc7daf9616 | what is maximum security prison | ms_marco | Ranking Error | 1 |
| q_8a33e7871173d1ee | food that contains toxins | ms_marco | Ranking Error | 1 |
| q_0f671925258160cb | standard deviation of probability distribution | ms_marco | Ranking Error | 1 |
| q_df8210b31a1dded1 | what is a normal fever temperature for adults | ms_marco | Ranking Error | 1 |
| q_f0e7fbb68d92ae66 | what is a coatimundi | ms_marco | Ranking Error | 1 |
| q_a4ee6a4f69c6609b | why was graphene aerogel created | ms_marco | Ranking Error | 1 |
| q_5edff287f3ed7be8 | is chlorpyrifos systemic | ms_marco | Semantic Miss | 0 |
| q_4a4854046199520c | what does a lambda sensor do | ms_marco | Ranking Error | 1 |
| q_5d47750a64147f0b | What is caused by atoms or ions when they share or transfer valance electrons? | sciq | Semantic Miss | 0 |
| q_cc5fdb44a79557ad | how much do network architects make | ms_marco | Ranking Error | 1 |
| q_5f45a4507dc57037 | cost to build garage office | ms_marco | Ranking Error | 1 |
| q_7f231d6e986f5e6c | macrovascular complications definition | ms_marco | Ranking Error | 1 |
| q_150ce353a80d61c0 | essential oil that start with rose | ms_marco | Ranking Error | 1 |
| q_83cbeb3884dc5273 | where is the alveoli located and what is its function | ms_marco | Ranking Error | 1 |
| q_7628e0fdae25850c | what does vinegar consist of | ms_marco | Ranking Error | 1 |
| q_b5f6d72a9d9b4395 | carbs in a medium potato | ms_marco | Ranking Error | 1 |
| q_5384bf2e8b3aa923 | how to cook a lamb chop in the oven | ms_marco | Ranking Error | 1 |
| q_532a610ba0ae2c44 | how long is the average nfl career | ms_marco | Semantic Miss | 0 |
| q_46cf3ca338530244 | how to start okra indoors | ms_marco | Semantic Miss | 0 |
| q_3f6bb8a8a62a5e71 | reupholstery cost | ms_marco | Ranking Error | 1 |
| q_034f9f1726b35d68 | where is the rocky mountains located on a map | ms_marco | Ranking Error | 1 |
| q_662e6e670722c078 | how to roast a small prime rib roast | ms_marco | Ranking Error | 1 |
| q_977a00135c82f741 | where is haleakala on the islands | ms_marco | Ranking Error | 1 |
| q_6fae7020789f98d3 | what does a cortisol test show | ms_marco | Ranking Error | 1 |
| q_0907104e0cbdab9d | how much does it cost to rent a dance hall | ms_marco | Ranking Error | 1 |
| q_a77297971994801c | does ringworm itch | ms_marco | Ranking Error | 1 |
| q_f4ddeda8f6d4460a | what is seafood mix | ms_marco | Ranking Error | 1 |
| q_ab9479689e2cc36f | when was navex global founded | ms_marco | Ranking Error | 1 |
| q_4f35f20487308e92 | average cost to open a day care | ms_marco | Semantic Miss | 0 |
| q_24bd99f2a92b9f66 | what foods are magnesium in | ms_marco | Ranking Error | 1 |
| q_d5df7f6feec7a2f5 | what is vietnamese food | ms_marco | Ranking Error | 1 |
| q_5b3ba4afdae35aeb | sensorineural hearing loss diagnosis code | ms_marco | Ranking Error | 1 |
| q_be5a266a842fe7ae | order of magnitude estimate definition | ms_marco | Ranking Error | 1 |
| q_79ca9a7dee1c3335 | what is an example of a psychological need | ms_marco | Ranking Error | 1 |
| q_d4118741e38ba677 | how long does it take for a swallow to build a nest | ms_marco | Ranking Error | 1 |
| q_f571c2bf4feea6be | what causes shingles disease | ms_marco | Semantic Miss | 0 |
| q_8a161fd061886d70 | UTEP tuition and fees | ms_marco | Semantic Miss | 0 |
| q_b499401069782fb6 | Who did the Super Bowl 50 National Anthem? | squad | Semantic Miss | 0 |
| q_8c55b2a1fb2de94f | does a dark floor make a room smaller | ms_marco | Ranking Error | 1 |
| q_82f39cde9cb7dbbe | what was a weakness of the bill of rights | ms_marco | Ranking Error | 1 |
| q_17ab4d0595ec3f06 | how long does dental implant process take | ms_marco | Ranking Error | 1 |
| q_a974da45092e9e4a | In which type of reaction are compounds formed? | sciq | Semantic Miss | 0 |
| q_cf0d1bfbb02371f0 | what kind of cactus do i have | ms_marco | Ranking Error | 1 |
| q_e34505173d5e6537 | narcolepsy symptoms | ms_marco | Ranking Error | 1 |
| q_2cdbd1471e91a035 | where is fitzrovia | ms_marco | Ranking Error | 1 |
| q_bce8c7b5d8af1338 | what is antidiuretic hormone and its function | ms_marco | Ranking Error | 1 |
| q_4f0380f3b3cd8fb2 | what is voluntary repo | ms_marco | Ranking Error | 1 |
| q_eafea479fecc2fe0 | can you get pta degree online | ms_marco | Ranking Error | 1 |
| q_3fd90b37ef1707c6 | What did the acronym AAP stand for? | squad | Semantic Miss | 0 |
| q_56a941d900dd09e4 | What type of reproduction produces offspring from a single parent that share the exact same genetic material as the parent? | sciq | Ranking Error | 1 |
| q_054d236cc41ea475 | average price of home in san antonio | ms_marco | Ranking Error | 1 |
| q_7677fe3feff77643 | what is dolomitic lime used for | ms_marco | Ranking Error | 1 |
| q_adf5e84287c8d96e | what is mass and heat balance | ms_marco | Ranking Error | 1 |
| q_9268647dcf110a8e | how to reset fuel filter light on toyota hilux | ms_marco | Ranking Error | 1 |
| q_1b6a9d24b70cbe74 | how many calories should a person consume in a day | ms_marco | Semantic Miss | 0 |
| q_5cfe3b0d4dc13bbd | What is the largest taxonomic rank? | sciq | Semantic Miss | 0 |
| q_7474137d8a50f689 | what does the empire state building have | ms_marco | Ranking Error | 1 |
| q_b62ae5c63e87de45 | how to install cat back exhaust | ms_marco | Ranking Error | 1 |
| q_32ee7eb722c67b5e | disadvantages of north during civil war | ms_marco | Ranking Error | 1 |
| q_5f349fe97f7e92e2 | calories and carbs in one sweet potato | ms_marco | Ranking Error | 1 |
| q_826fbd7e88fcdd07 | what is a hummingbird moth | ms_marco | Ranking Error | 1 |
| q_710be48400ce4ca4 | what is whistler village | ms_marco | Semantic Miss | 0 |
| q_01adeb4a1409fbb2 | what is biodegrade mean | ms_marco | Ranking Error | 1 |
| q_3435fb38b6b4f3b7 | how long does a felony conviction stay on your record in california | ms_marco | Ranking Error | 1 |
| q_ed490f6d6ab98179 | difference between emancipation proclamation and thirteenth amendment | ms_marco | Semantic Miss | 0 |
| q_68ac6caf4c42dd45 | what creates carbon monoxide in a home | ms_marco | Ranking Error | 1 |
| q_76a3f2c0acc65707 | What do you have to do for a horse daily | ms_marco | Ranking Error | 1 |
| q_c4b5dd9e9d0c5791 | symptoms of meningitis | ms_marco | Ranking Error | 1 |
| q_19658d821d12ef83 | what is perlite made of? | ms_marco | Ranking Error | 1 |
| q_9ef469644e40de84 | What is the estimate for the amount of tree species in the amazon tropical rain forest? | squad | Ranking Error | 1 |
| q_31ee5dc211ae3265 | what is charcoal canister | ms_marco | Ranking Error | 1 |
| q_98ccf4ac65409427 | The DNA in eukaryotes is found in: | ms_marco | Ranking Error | 1 |
| q_bfd9e60dea6ecf85 | what is mesothelioma cancer | ms_marco | Ranking Error | 1 |
| q_95bc90713946bd1f | arthritis caused by ulcerative colitis | ms_marco | Ranking Error | 1 |
| q_2910619588289308 | what body system does an insulin pump help with | ms_marco | Ranking Error | 1 |
| q_7f6289f6802e3130 | are hybrid seeds a gmo | ms_marco | Ranking Error | 1 |
| q_79b18d87a7f5de5e | political party which opposed expansion | ms_marco | Ranking Error | 1 |
| q_e503310070b728f9 | what does mutated will mean | ms_marco | Ranking Error | 1 |
| q_9bbbd8a2968feb5f | bad effect of watching tv | ms_marco | Ranking Error | 1 |
| q_cf463887724cb325 | average salary for rn in florida | ms_marco | Ranking Error | 1 |
| q_9d4cda3bf0a5ce8c | what does a negative oxidase test mean | ms_marco | Ranking Error | 1 |
| q_4c2c1642df2c277f | average price per acre | ms_marco | Ranking Error | 1 |
| q_6b4ee1b9be213b06 | what do the aegean civilizations include | ms_marco | Semantic Miss | 0 |
| q_b25a939899fca89e | what is the temperature of denatured alcohol burning in air | ms_marco | Ranking Error | 1 |
| q_e64837804c491097 | can am engine rebuild | ms_marco | Ranking Error | 1 |
| q_71b536d65138b8d0 | Init client | code_search_net | Semantic Miss | 0 |
| q_ec06d612050314d3 | subway dealership cost | ms_marco | Ranking Error | 1 |
| q_fbc8e01fc3693f01 | how much does a director get paid | ms_marco | Semantic Miss | 0 |
| q_9a98fed83cf3d312 | date shakespeare was born and died | ms_marco | Ranking Error | 1 |
| q_66a79b5913be9e61 | causes of hypokalemic periodic paralysis | ms_marco | Ranking Error | 1 |
| q_113464d5d3d8b40d | Which one of Fresno's hotels burned down? | squad | Semantic Miss | 0 |
| q_c7245efd815c0873 | reserved powers definition | ms_marco | Ranking Error | 1 |
| q_a4c17ef3058e9cb9 | what is the longitude and latitude of the great barrier reef | ms_marco | Ranking Error | 1 |
| q_5d7a5a7a9802e2d9 | what are accounting estimates | ms_marco | Ranking Error | 1 |
| q_403a9b873d1279fc | average years for an nfl player | ms_marco | Semantic Miss | 0 |
| q_eb72a3621f000580 | what zone is langley | ms_marco | Ranking Error | 1 |
| q_6a7068599b78340e | how do i make my stitches loose in knitting | ms_marco | Ranking Error | 1 |
| q_20800ad11e46cf0a | what year was rockford university was established | ms_marco | Ranking Error | 1 |
| q_6db3558a17b65f35 | what is scaffolding bruner | ms_marco | Semantic Miss | 0 |
| q_9da5a2ca22b782f7 | does medicare pay hearing aids | ms_marco | Ranking Error | 1 |
| q_abba72c94d4e2b5b | does neutering a dog help with marking | ms_marco | Ranking Error | 1 |
| q_3cee9d846ba7a2ea | how much do forensic crime scene investigators make | ms_marco | Ranking Error | 1 |
| q_ae3bbb5b08322818 | how to calculate annual salary to hourly rate | ms_marco | Ranking Error | 1 |
| q_7ddeebbcb4bede72 | what is aerobic glycolysis | ms_marco | Ranking Error | 1 |
| q_11cc3c1dbcf5a71a | what makes cacao nibs healthy | ms_marco | Ranking Error | 1 |
| q_1d071d8f8ff6733e | what language do hungarians speak | ms_marco | Ranking Error | 1 |
| q_282ce25b998b8d6c | where are white blood cells formed | ms_marco | Ranking Error | 1 |
| q_b32ce4fc5902bd4f | what causes the color of uranus | ms_marco | Ranking Error | 1 |
| q_1dbf69110526ef22 | salata franchise cost | ms_marco | Ranking Error | 1 |
| q_a4ca08fc9d44c1ba | how is carbon monoxide administered | ms_marco | Ranking Error | 1 |
| q_17aec842cfb4c4a2 | what is a distressed reaction | ms_marco | Ranking Error | 1 |
| q_4b1ebe76afe129af | how much does it cost to go paintballing in atlanta | ms_marco | Ranking Error | 1 |
| q_9d00599e823c420c | average cost of a roofing | ms_marco | Ranking Error | 1 |
| q_a304c52ad08175f2 | What kind of resource is soil? | sciq | Semantic Miss | 0 |
| q_6f467f0013f9c118 | do lice bites scar | ms_marco | Ranking Error | 1 |
| q_12206a479652f5c4 | average hours to learn how to drive | ms_marco | Ranking Error | 1 |
| q_465b6d5b6bf815d2 | what are dew claws | ms_marco | Ranking Error | 1 |
| q_634d4d07b0fd0f18 | the cause of bipolar disorder | ms_marco | Ranking Error | 1 |
| q_3cd31f3bb4ad37d6 | Are Palm Trees Poisonous | ms_marco | Ranking Error | 1 |
| q_dcf16fd99551cace | how much cost skip hire | ms_marco | Ranking Error | 1 |
| q_c091bd10e9143de8 | mnsure cost | ms_marco | Ranking Error | 1 |
| q_dd2f1167a00f61b8 | where do roseate spoonbills live | ms_marco | Ranking Error | 1 |
| q_fc25dd9ff8c17319 | what are leafy greens good for | ms_marco | Ranking Error | 1 |
| q_9eb9eae1c77fba64 | how long should the pool circulation run | ms_marco | Ranking Error | 1 |
| q_b39e4ae65dc5ce62 | what is retrogradation | ms_marco | Ranking Error | 1 |
| q_17e0f6264dbf3117 | are lymph nodes always involved in tumor spread | ms_marco | Ranking Error | 1 |
| q_001ba7967b8f175a | synonym for fee | ms_marco | Ranking Error | 1 |
| q_6a3d3d9400ff4e97 | punta cana weather averages | ms_marco | Ranking Error | 1 |
| q_57e2a62366767c03 | what causes toxic megacolon | ms_marco | Ranking Error | 1 |
| q_83f35f1cb3b4209e | average soccer player salary in the world | ms_marco | Ranking Error | 1 |
| q_7821599c07a423b2 | what is a ridge | ms_marco | Ranking Error | 1 |
| q_c7f71e162e5f5fd5 | uses for minerals | ms_marco | Semantic Miss | 0 |
| q_3da1ba2d6c19a395 | what breed of dog is a westie | ms_marco | Ranking Error | 1 |
| q_9f7037d0b6fb9076 | what genus is human | ms_marco | Semantic Miss | 0 |
| q_08f1f6d3db66a333 | what age can you spay a dog | ms_marco | Ranking Error | 1 |
| q_76d0211be839e8bd | what is non-market socialism | ms_marco | Ranking Error | 1 |
| q_22e3203aaa95ba6b | the meaning of the name april | ms_marco | Ranking Error | 1 |
| q_138140fc296c775d | what is pressure necrosis | ms_marco | Ranking Error | 1 |
| q_c0d5dee9fd399ead | what is a direct supervisor | ms_marco | Ranking Error | 1 |
| q_372ffe1a066ee04e | How often should you have the oil in your car changed | ms_marco | Ranking Error | 1 |
| q_165c1c0203d59386 | what age should a foal be weaned | ms_marco | Ranking Error | 1 |
| q_78be2d6d0a786814 | what does grass contain | ms_marco | Ranking Error | 1 |
| q_5e94b3b9770971a4 | prosthodontics cost | ms_marco | Ranking Error | 1 |
| q_9b6d5d9c22928a4b | What religion is the western region mostly? | squad | Semantic Miss | 0 |
| q_b1b9abbe20f5a6b4 | conspicuous meaning | ms_marco | Ranking Error | 1 |
| q_839a58683bedbc4a | uses of rocks in everyday life | ms_marco | Ranking Error | 1 |
| q_69c4aea0a0fe436d | colon cancer that has spread to liver | ms_marco | Ranking Error | 1 |
| q_359a3d188fb36b89 | what is an action potential quizlet | ms_marco | Ranking Error | 1 |
| q_c1fd0b1a5a57e5a7 | what is gene | ms_marco | Ranking Error | 1 |
| q_e2a5ec15fe6a90be | typical salary emler swim school hourly | ms_marco | Ranking Error | 1 |
| q_14c791b88567afd0 | Vertebrates differ from invertebrates because they lack this? | sciq | Semantic Miss | 0 |
| q_b1ae808077c5ada9 | turbotax can i pay my taxes with a credit card | ms_marco | Ranking Error | 1 |
| q_a147b2a2a050104d | what causes the hiv virus? | ms_marco | Ranking Error | 1 |
| q_333546da0154b746 | what does aa grade gemstone mean | ms_marco | Ranking Error | 1 |
| q_e49330b396155d48 | what is spiriva for | ms_marco | Ranking Error | 1 |
| q_59a0c4059afc23f1 | what does zamboni do | ms_marco | Ranking Error | 1 |
| q_59f072092a56f86b | the beginning of medicare | ms_marco | Semantic Miss | 0 |
| q_637c7bbedabb88b6 | how long will a dui show up on my driving record | ms_marco | Ranking Error | 1 |
| q_948593aedbc59849 | jaundice definition hepatitis | ms_marco | Ranking Error | 1 |
| q_26a0df8aa3df2d9a | what do langerhans cells do | ms_marco | Ranking Error | 1 |
| q_ff427d3fef672d53 | mumps contagious | ms_marco | Ranking Error | 1 |
| q_60ff70a6c34aaf96 | salary ranges for nurses | ms_marco | Ranking Error | 1 |
| q_77d0a4d3daa21160 | what is angio | ms_marco | Ranking Error | 1 |
| q_6e89bbc11bdeb5fd | Who ruled Cyprus in 1191? | squad | Semantic Miss | 0 |
| q_20d3e816b4578ffb | What were some of Tesla's experiments? | squad | Semantic Miss | 0 |
| q_b8dce4d4b2018c6b | what is dutch lap vinyl siding | ms_marco | Ranking Error | 1 |
| q_05d08deed1c98277 | what is transference healing | ms_marco | Ranking Error | 1 |
| q_2c505c893d3e696e | what is a deemed contract | ms_marco | Semantic Miss | 0 |
| q_b3e64ea301d2902e | what classifies as plankton | ms_marco | Ranking Error | 1 |
| q_3eafebed2c504a72 | what is a pilsner beer | ms_marco | Semantic Miss | 0 |
| q_3e99dfe39055bbe0 | when was the first diesel train invented | ms_marco | Ranking Error | 1 |
| q_d190b6ee0543c7e1 | What are lipids' function in relation to nerves? | sciq | Semantic Miss | 0 |
| q_2a26025728a328a4 | how to cook pork belly strips in oven | ms_marco | Ranking Error | 1 |
| q_e89a7b77e0d42c0c | what type of pain is fracture pain | ms_marco | Ranking Error | 1 |
| q_18e3654919a54969 | how much should a dog drink | ms_marco | Semantic Miss | 0 |
| q_0da7c8c4423f8c60 | what did newton invent calculus | ms_marco | Ranking Error | 1 |
| q_46ba83c4bb59c826 | what is echocardiogram test | ms_marco | Ranking Error | 1 |
| q_9863d0189d26dd25 | average temperature in summer for the temperate deciduous forest biome | ms_marco | Ranking Error | 1 |
| q_7c0295454af74897 | what is sourdough starter | ms_marco | Ranking Error | 1 |
| q_252341412c7abc03 | what is confucian filial piety | ms_marco | Ranking Error | 1 |
| q_189a10708d31fa35 | how to switch your straight talk phone to another | ms_marco | Ranking Error | 1 |
| q_83bb9282f70fb122 | australian geographic location | ms_marco | Ranking Error | 1 |
| q_f099ea357e8b01a1 | what is average closing costs for a seller of a home | ms_marco | Ranking Error | 1 |
| q_b1fa8423691e343f | how long can dogs go without food when sick | ms_marco | Semantic Miss | 0 |
| q_5df22c267d3c9401 | what is ashwagandha turmeric | ms_marco | Ranking Error | 1 |
| q_75dab5e6099eeae0 | what is cdf disease | ms_marco | Ranking Error | 1 |
| q_5486bf7539a02f2d | are there deer in china | ms_marco | Ranking Error | 1 |
| q_ff8c63f986c826c0 | what gland is cortisol secreted from | ms_marco | Ranking Error | 1 |
| q_7c3a5c9775471b02 | what functional groups are in all monosaccharides | ms_marco | Ranking Error | 1 |
| q_57e9ef12bd04559b | average lifespan of a thoroughbred horse | ms_marco | Ranking Error | 1 |
| q_ba6897fced8dfd8f | where is the anterior cavity of the eye located | ms_marco | Ranking Error | 1 |
| q_24d9756b99ca0f4b | what is floriculture | ms_marco | Ranking Error | 1 |
| q_facaa9f009e88336 | vitamins and minerals good for the skin | ms_marco | Semantic Miss | 0 |
| q_6d842d82c6ffbba2 | what is pultrusion | ms_marco | Ranking Error | 1 |
| q_cf35b46ffcbb6ac3 | where is buenos aires located in argentina | ms_marco | Ranking Error | 1 |
| q_9ff60e54d843af5a | what does unicef need help | ms_marco | Ranking Error | 1 |
| q_166e7aeb0f27d992 | what is malaria caused by | ms_marco | Ranking Error | 1 |
| q_59123f30954be50f | how old should a dog be to start breeding | ms_marco | Semantic Miss | 0 |
| q_3e346a6cb461ac78 | vehicle payload definition | ms_marco | Ranking Error | 1 |
| q_29e4bb7d32a298cc | how long should kittens stay with mother cat | ms_marco | Ranking Error | 1 |
| q_9a3fcd924b3b7516 | when were delaware indians moved to oklahoma | ms_marco | Ranking Error | 1 |
| q_42495107cd8dddfe | what is love susan polis schutz | ms_marco | Ranking Error | 1 |
| q_c22c2da27f84b4c8 | how to cook eat crab | ms_marco | Semantic Miss | 0 |
| q_94e190d812a60074 | how many states have legalized marijuana | ms_marco | Ranking Error | 1 |
| q_be690c02b31f4daa | what the name elvie means | ms_marco | Ranking Error | 1 |
| q_e81a9e9e86574636 | When was the UMC formed? | squad | Semantic Miss | 0 |
| q_dfc6d81da0525f6b | what is omnicef for? | ms_marco | Ranking Error | 1 |
| q_b891a9b69fc8aed9 | negative side effects of lumigan | ms_marco | Ranking Error | 1 |
| q_d33a5a64217b64fc | what is the meaning of gould? | ms_marco | Ranking Error | 1 |
| q_0d7174687504fd97 | are digestive bitters and digestive enzymes the same thing | ms_marco | Ranking Error | 1 |
| q_914c406c44792ad5 | what is in allium root tip | ms_marco | Ranking Error | 1 |
| q_bff1673b96edf166 | is it possible to exchange out of state driver license for nj driver license | ms_marco | Ranking Error | 1 |
| q_7635f88e4e247399 | what is afap abbreviation | ms_marco | Ranking Error | 1 |
| q_a8f0048474b1d65d | A man made lake is known as what? | sciq | Semantic Miss | 0 |
| q_2811d42b1f2b10b9 | is there a website to check comma usage | ms_marco | Ranking Error | 1 |
| q_a8b031382afe9c30 | domestic insurer definition in florida | ms_marco | Ranking Error | 1 |
| q_ead0ac4d5464384e | what is the habitat and range of a golden lion tamarin | ms_marco | Ranking Error | 1 |
| q_566ac9d750a98372 | where is Faro in portugal | ms_marco | Ranking Error | 1 |
| q_f788083334f75b88 | substances are exchanged between the blood and body cells in the | ms_marco | Ranking Error | 1 |
| q_d35eb3719244f47e | what does pyridine dissociate into | ms_marco | Ranking Error | 1 |
| q_e93affa4c1080e26 | metabolic causes of memory loss | ms_marco | Ranking Error | 1 |
| q_490582628ea5bf8c | what is amoebas | ms_marco | Ranking Error | 1 |
| q_ad794986cb5e202d | what is genomic dna | ms_marco | Ranking Error | 1 |
| q_713da0a3c7efd139 | how fast do english walnut trees grow | ms_marco | Ranking Error | 1 |
| q_a3e606d4637d87ac | what are ore concentrates examples | ms_marco | Ranking Error | 1 |
| q_2131af8d9ebc2f8b | what is thd | ms_marco | Ranking Error | 1 |
| q_e8eda2d470472a75 | what does the name talitha mean | ms_marco | Ranking Error | 1 |
| q_90509b0393994331 | cost of bathroom update | ms_marco | Ranking Error | 1 |
| q_6232e7e1057e8822 | when was venezuela colonized by spain | ms_marco | Ranking Error | 1 |
| q_d496b25ab134b61b | how many health careers are there | ms_marco | Semantic Miss | 0 |
| q_871c0f476a14c4db | average cost per watt commercial electricity | ms_marco | Ranking Error | 1 |
| q_cce8fc963ecdb93f | how do i plant my knockout roses | ms_marco | Ranking Error | 1 |
| q_ff7ce1ff5a8b260c | what seeds are poisonous to humans | ms_marco | Ranking Error | 1 |
| q_d24b33f138379bbf | why is thermal energy important | ms_marco | Ranking Error | 1 |
| q_4cf25ef952c0c4fc | In what way do bacteria reproduce? | sciq | Semantic Miss | 0 |
| q_517a6c272ebf9c83 | what is the role of plasmids in antibiotic resistance | ms_marco | Semantic Miss | 0 |
| q_c3e8b9baad2604d2 | what salary can you earn as a counsellor | ms_marco | Ranking Error | 1 |
| q_8b1419c17e4a78fa | where is marylebone london | ms_marco | Ranking Error | 1 |
| q_e315456be59538d3 | import tax from china to usa | ms_marco | Ranking Error | 1 |
| q_97183137b9dbc62a | what is a Positive fecal occult blood test | ms_marco | Ranking Error | 1 |
| q_ab96243a04756027 | how much does it cost to add a floor and renovate home | ms_marco | Ranking Error | 1 |
| q_8e1332a36eac42ff | identity definition webster | ms_marco | Ranking Error | 1 |
| q_d3ecf392b36f6651 | does advantage contain fipronil | ms_marco | Ranking Error | 1 |
| q_ff8a2e0c98c3f892 | what is present progressive | ms_marco | Ranking Error | 1 |
| q_65ee29c2a18122d1 | can i service my own subpoena | ms_marco | Ranking Error | 1 |
| q_2d4352038a4585aa | hourly salary at homegoods | ms_marco | Ranking Error | 1 |
| q_89071dde997ded04 | synthetic oil change how often jeep patriot | ms_marco | Ranking Error | 1 |
| q_f9e75e45d01b66ca | pilot salary in air india | ms_marco | Ranking Error | 1 |
| q_b4a44f63efeea57b | how does the first amendment protect citizens from the government | ms_marco | Ranking Error | 1 |
| q_36f00745cb957f8f | salary of construction workers in lima peru | ms_marco | Ranking Error | 1 |
| q_60332da201129de3 | what happened to pangaea in the triassic period | ms_marco | Ranking Error | 1 |
| q_533b73c21ab5dc9d | what does warez mean | ms_marco | Ranking Error | 1 |
| q_0cb0733956e2fc28 | what molecules make up chromosomes | ms_marco | Ranking Error | 1 |
| q_a0e03c104aebda16 | do breccia contain clasts? | ms_marco | Ranking Error | 1 |
| q_5c7b5fc727f04958 | infrared spectroscopy definition | ms_marco | Ranking Error | 1 |
| q_b1a1705eb292cff7 | way the adaptive immune response is different from the innate immune response | ms_marco | Ranking Error | 1 |
| q_1a448c982d8a33a3 | what chromosome is huntington's disease found on | ms_marco | Ranking Error | 1 |
| q_ef3471856c3d49a6 | how long does it take to get a degree in addiction counseling online | ms_marco | Ranking Error | 1 |
| q_6a05d18659d0f6d5 | name of delphi priestess | ms_marco | Ranking Error | 1 |
| q_9fe44c47f0cf8e8b | price per square foot for laminate flooring installed | ms_marco | Ranking Error | 1 |
| q_b718b48c791152ef | what is a bear's hand called | ms_marco | Semantic Miss | 0 |
| q_995e46641b3facc1 | what is prolactin made of | ms_marco | Ranking Error | 1 |
| q_a9446df81dee94c3 | where is the three gorges dam located | ms_marco | Ranking Error | 1 |
| q_69656df8a4c17480 | average salary for an assistant greenskeeper at a golf course | ms_marco | Semantic Miss | 0 |
| q_1bb117d014d7ec25 | what is astrocyte function | ms_marco | Ranking Error | 1 |
| q_a07bb863b6fbe149 | price to resurface garage floor | ms_marco | Semantic Miss | 0 |
| q_c7907774febad07a | what ingredients are in noxzema | ms_marco | Ranking Error | 1 |
| q_64db240a3921dfcb | Who did Martin Luther say was the lone granter of forgiveness? | squad | Semantic Miss | 0 |
| q_b74230065f1f775d | How do cestids swim? | squad | Semantic Miss | 0 |
| q_32c0ec468876e639 | how old do you have to be to watch a child | ms_marco | Ranking Error | 1 |
| q_c76bbc5a5722ceef | what is apache spark | ms_marco | Ranking Error | 1 |
| q_51d0b989f0812f3f | what is marrow edema | ms_marco | Ranking Error | 1 |
| q_b514dd0963e96226 | names of crystalline igneous rocks | ms_marco | Ranking Error | 1 |
| q_218b97c291a00eb7 | how long does it take to heal from a broken ankle surgery | ms_marco | Ranking Error | 1 |
| q_b9d2aa4d5a53b595 | salary for air force officer | ms_marco | Ranking Error | 1 |
| q_abd7e55b492b2af5 | where is henlow | ms_marco | Ranking Error | 1 |
| q_0d043b118328bf57 | how to manually calculate cumulative gpa | ms_marco | Ranking Error | 1 |
| q_f7066714cc07e3bc | how to become a realtor in memphis tn | ms_marco | Semantic Miss | 0 |
| q_0cc93a5860f2935e | what are the native bird species of Guam? | ms_marco | Ranking Error | 1 |
| q_b5d214c77aa9e047 | how long does it take for the govt to give u a tax refund when you have electronically filed | ms_marco | Semantic Miss | 0 |
| q_a48eb2a0002c4a60 | marble headstone cost | ms_marco | Ranking Error | 1 |
| q_85044e3260dca9a9 | how long does it take to recover from viral meningitis | ms_marco | Ranking Error | 1 |
| q_1da9fcfc9367dce2 | what is a retainer fee | ms_marco | Ranking Error | 1 |
| q_9827c87cee7282bb | does ibogaine contain dmt | ms_marco | Ranking Error | 1 |
| q_173330c6089672b9 | what is xanthine pills | ms_marco | Ranking Error | 1 |
| q_b224fa91d78b2ae1 | where is popocatepetl located | ms_marco | Ranking Error | 1 |
| q_2de8296615da704d | what is the birthday of the actor james bolam | ms_marco | Ranking Error | 1 |
| q_61049b7db23c3df1 | what is the difference between nuclear dna and mitochondrial dna | ms_marco | Ranking Error | 1 |
| q_daf206c7af6260db | can you use a copyright speech | ms_marco | Ranking Error | 1 |
| q_80cb76a8f956f88d | swollen glands under tongue cause | ms_marco | Ranking Error | 1 |
| q_1198cc75bf8a83bb | how to determine confidence interval in excel | ms_marco | Ranking Error | 1 |
| q_c47d3c6292fc6bf2 | what does meristem culture | ms_marco | Ranking Error | 1 |
| q_a1a59e312eee0a23 | what is in LSD | ms_marco | Ranking Error | 1 |
| q_1ef7e9c0e3b335af | what does corporate culture mean | ms_marco | Ranking Error | 1 |
| q_052cdb66404357c7 | how much does a new garage door cost installed | ms_marco | Ranking Error | 1 |
| q_09b4b00191873955 | is there an age requirement to be a flight attendant | ms_marco | Ranking Error | 1 |
| q_01196f3361dcdca9 | what language do they speak in finland | ms_marco | Semantic Miss | 0 |
| q_b28707aae7e2dd4d | What's the term for the gradual progression from simple plants to larger more complex ones in an area? | sciq | Ranking Error | 1 |
| q_103754874867e7b7 | what is brostep | ms_marco | Ranking Error | 1 |
| q_89839eeb9088426d | list of low carb foods for weight loss | ms_marco | Ranking Error | 1 |
| q_cdbd3ba301007238 | when was the liberty bell built | ms_marco | Ranking Error | 1 |
| q_e28e3d67b31f4977 | john travolta first film | ms_marco | Ranking Error | 1 |
| q_755734f5ab8f7a8f | do blue whales have a predator | ms_marco | Ranking Error | 1 |
| q_62958d225db385f8 | Through digestion, polysaccharides are broken down into | ms_marco | Ranking Error | 1 |
| q_c13e854e78585609 | nutritional information of small date square | ms_marco | Ranking Error | 1 |
| q_1f10749b27163028 | human body flexion definition | ms_marco | Ranking Error | 1 |
| q_e4fe64344590f69b | who was catherine helen spence | ms_marco | Ranking Error | 1 |
| q_c3fa83d58b15ffdd | disease caused by bacteria pathogen | ms_marco | Ranking Error | 1 |
| q_1a0869040553df6e | what is the chemical name for limestone | ms_marco | Ranking Error | 1 |
| q_900794cede04e15c | estimated cost siding a house | ms_marco | Semantic Miss | 0 |
| q_c50efa3841a64540 | what are barnacles | ms_marco | Ranking Error | 1 |
| q_e6b9c44ff34379a6 | yeast infections are caused by quizlet | ms_marco | Semantic Miss | 0 |
| q_d4d190782f4a30e8 | how often should you vaccinate your cows | ms_marco | Ranking Error | 1 |
| q_18fea5be868c93ea | what is the purpose of iodoform reaction | ms_marco | Semantic Miss | 0 |
| q_b4941668c6aa9342 | how much to replace ipad screen | ms_marco | Ranking Error | 1 |
| q_628d275a113a6369 | what is magnesium used for | ms_marco | Ranking Error | 1 |
| q_24bf44d3914c30f6 | how long before the irs approves my refund | ms_marco | Ranking Error | 1 |
| q_a6cfceee35af4513 | how much is a house inspection cost | ms_marco | Ranking Error | 1 |
| q_938d3bee798dbec9 | what are villous lymphocytes | ms_marco | Ranking Error | 1 |
| q_81c5d8f5cbc28c76 | how long does it take to charge a nimh rc battery | ms_marco | Ranking Error | 1 |
| q_6f84dc3ccfed32b6 | what temperature does rainbow lake trout like | ms_marco | Ranking Error | 1 |
| q_796226e14a241a1e | what do microbiologists do | ms_marco | Ranking Error | 1 |
| q_2794b076398e82f6 | how to turn xerox printer online | ms_marco | Ranking Error | 1 |
| q_3f4ad76956a643e2 | describe the structure of a capillary network | ms_marco | Semantic Miss | 0 |
| q_99e1e975dac9dc33 | What seldom mutates? | squad | Ranking Error | 1 |
| q_43c45ae56df4c05a | oceanic crust is made of | ms_marco | Ranking Error | 1 |
| q_65d787beace2e5e4 | What did this help accomplish? | squad | Ranking Error | 1 |
| q_9908062a349b589b | atopic definition medical | ms_marco | Ranking Error | 1 |
| q_d601292aa1db750a | Which Florida venue was one of three considered for Super Bowl 50? | squad | Semantic Miss | 0 |
| q_6b8cf3e7e561e223 | In human beings, when a female becomes pregnant, what is fertilized and then embedded in the uterus? | sciq | Semantic Miss | 0 |
| q_28bc1683182014c2 | how long to cook a mini roast lamb | ms_marco | Semantic Miss | 0 |
| q_980beb587bd4c682 | how often are representatives to be elected | ms_marco | Ranking Error | 1 |
| q_9c032eae80f0abf7 | buerger's disease definition | ms_marco | Ranking Error | 1 |
| q_b98774a427b606fe | energy: what is work | ms_marco | Ranking Error | 1 |
| q_0a2e29ad8fbec791 | what is reflexology used for | ms_marco | Ranking Error | 1 |
| q_be7393fc59ea4f63 | What is the name for substances with a ph above 7? | sciq | Semantic Miss | 0 |
| q_1022d390117e53d7 | kelsey name meaning | ms_marco | Ranking Error | 1 |
| q_0c1750b3658b87f6 | is switzerland landlocked | ms_marco | Ranking Error | 1 |
| q_261357c0318c5fb5 | what percentage of agriculture in us is livestock production | ms_marco | Ranking Error | 1 |
| q_25f7c3eb11c4174b | average salary in drc | ms_marco | Ranking Error | 1 |
| q_100242dfc4ebebda | where are cinder cones located | ms_marco | Ranking Error | 1 |
| q_1a89e2861645b30f | what causes scours in dairy cows | ms_marco | Ranking Error | 1 |
| q_544468ef96132b9c | does earthpaste contain lead | ms_marco | Ranking Error | 1 |
| q_f6d17270e964c577 | which gene mutation is constitutive mutation gene regulation lac operon | ms_marco | Ranking Error | 1 |
| q_93458c433d886c2d | In which way do sunspots occur? | sciq | Semantic Miss | 0 |
| q_3fb0b6bd133c16c3 | The cecum is the first part of what structure, where wastes in a liquid state enter from the small intestine? | sciq | Semantic Miss | 0 |
| q_739949c3e31d568e | what is mpg | ms_marco | Ranking Error | 1 |
| q_e3955eed8cd4a681 | how many football players have cte | ms_marco | Ranking Error | 1 |
| q_bde29fed27dda629 | Who was given the esteemed status of MVP for Super Bowl 50? | squad | Ranking Error | 1 |
| q_d78607cd260b3a80 | weekly cost of agisting horses | ms_marco | Ranking Error | 1 |
| q_bf12c9f129bbaf84 | what are the three monounsaturated oils | ms_marco | Ranking Error | 1 |
| q_224b5348e7c0d5db | what is a muscle up | ms_marco | Ranking Error | 1 |
| q_4e7bbac94e177b96 | when was the EEC created | ms_marco | Ranking Error | 1 |
| q_907fb86a2ab2a25b | define manage | ms_marco | Ranking Error | 1 |
| q_96a19c20b51f4add | what is pepperoni made from | ms_marco | Ranking Error | 1 |
| q_ebc2fd18783eb63d | what is the maximum dose of slo niacin | ms_marco | Ranking Error | 1 |
| q_e9da3121316a83a6 | gestation period of whitetail deer | ms_marco | Ranking Error | 1 |
| q_e6bbe649378104b6 | what is a tamarind plant | ms_marco | Ranking Error | 1 |
| q_f0f8c37d09326d1b | what is the relationship between a gene a dna molecule and a protein | ms_marco | Ranking Error | 1 |
| q_7852ffbe9406784b | prophylactic ovary removal what to expect | ms_marco | Ranking Error | 1 |
| q_9d31fbc411aa61ea | what is a feminist theory | ms_marco | Ranking Error | 1 |
| q_59080378c7a14eea | what is qr code | ms_marco | Ranking Error | 1 |
| q_ce3cc1964f8ec1a1 | difference between compressional and transverse waves | ms_marco | Ranking Error | 1 |
| q_e87cac8227e9bfa6 | what is the butterfly a symbol of | ms_marco | Ranking Error | 1 |
| q_583fb8cb489c22dc | Deficiency of what is symptomized by nausea, fatigue and dizziness, and can be triggered by excessive sweating? | sciq | Semantic Miss | 0 |
| q_bea7a986d2ded364 | where can the arctic tundra be found | ms_marco | Ranking Error | 1 |
| q_b6cb88839a6b213f | connecticut name origin | ms_marco | Ranking Error | 1 |
| q_1f649c9462df4e4e | what is acetal plastic | ms_marco | Ranking Error | 1 |
| q_a494c8e0f2346cfb | where do depositions of fact witnesses take place | ms_marco | Ranking Error | 1 |
| q_862d7c792fdcc534 | two step movie meaning | ms_marco | Ranking Error | 1 |
| q_1aba125efc3ed13f | why was corrymeela founded | ms_marco | Ranking Error | 1 |
| q_ec18811f412f9a99 | how are human mitochondria inherited | ms_marco | Ranking Error | 1 |
| q_010cc2677079725e | how many members of congress are there | ms_marco | Ranking Error | 1 |
| q_18c1abf156f55ce5 | average salary for teachers in hawaii | ms_marco | Ranking Error | 1 |
| q_5d5c449ad9ebb4a9 | Electrons in the "outer shell" are also known as what kind of electrons? | sciq | Semantic Miss | 0 |
| q_43510965d1906fac | what is the scientific species of wolverine | ms_marco | Ranking Error | 1 |
| q_6e41d8d8b072d4ff | how did the missouri compromise split the nation | ms_marco | Ranking Error | 1 |
| q_1359882b7c27a42b | what type of car does shu todoroki drive | ms_marco | Ranking Error | 1 |
| q_d75e4d1039bb954d | at what temperature does tap water boil | ms_marco | Semantic Miss | 0 |
| q_6f6a5cdafc278993 | what was the first transistor made of | ms_marco | Ranking Error | 1 |
| q_010794299ad24337 | what biome does an acacia come from | ms_marco | Ranking Error | 1 |
| q_073ac9c77a1c5d90 | how many saturated fats should you consume per day | ms_marco | Ranking Error | 1 |
| q_af49c70ac3bbd98e | when was the death penalty abolished | ms_marco | Ranking Error | 1 |
| q_1199c7df110b26ef | outsourcing when did it start | ms_marco | Ranking Error | 1 |
| q_1abcac5dd26551b5 | what is a tree urn | ms_marco | Ranking Error | 1 |
| q_fdfc0366d60aea89 | is glucose a monosaccharide | ms_marco | Ranking Error | 1 |
| q_af7a19cdbb17a0d6 | medium sized chicken cutlets, how long to fry | ms_marco | Ranking Error | 1 |
| q_200b72ceedafd7a1 | what type of birth control pill is alesse | ms_marco | Ranking Error | 1 |
| q_1a184cf6075c2b1a | epinephrine and norepinephrine regulatory mechanism is | ms_marco | Ranking Error | 1 |
| q_c26c66733faa93ee | what is wind energy used for | ms_marco | Ranking Error | 1 |
| q_eb0b84853eab6dce | regulatory guidance definition | ms_marco | Semantic Miss | 0 |
| q_1c2c9a95e7a8ee83 | what type of tragedy is oedipus | ms_marco | Ranking Error | 1 |
| q_c37a6e91f45341f4 | what causes steel corrosion | ms_marco | Ranking Error | 1 |
| q_36e46f3e009d05fb | average salary of a nurse | ms_marco | Ranking Error | 1 |
| q_a5d52a3699021c38 | what is a marketing authorisation | ms_marco | Semantic Miss | 0 |
| q_decf0d04c8b0b775 | What award was given to Tesla? | squad | Semantic Miss | 0 |
| q_779e1e5d04b65081 | how much postage for a letter to scotland | ms_marco | Ranking Error | 1 |
| q_e03e8d6ab5f0b54e | what is a tokoloshe | ms_marco | Ranking Error | 1 |
| q_bb96881038cded94 | What else was publically questioned? | squad | Semantic Miss | 0 |
| q_edab1c9d78337915 | what kind of climate does ginger grow in | ms_marco | Ranking Error | 1 |
| q_8e4cfe47fbfe6df0 | what is barbacoa in what region does this originate | ms_marco | Semantic Miss | 0 |
| q_52ac751351f69527 | what to do as community service | ms_marco | Ranking Error | 1 |
| q_97ded06d30686ca9 | meaning of the name robbie | ms_marco | Ranking Error | 1 |
| q_7d4f40a7ada0fe9b | what are the ingredients in becel margarine | ms_marco | Ranking Error | 1 |
| q_c591660642e33a2d | what is the normal dosage for digoxin | ms_marco | Ranking Error | 1 |
| q_d4a46034a6d57e06 | what is pid | ms_marco | Ranking Error | 1 |
| q_956ce860bfed56a7 | where is the tibialis posterior muscle located | ms_marco | Ranking Error | 1 |
| q_36f7d00a76ec34ed | levelized cost of energy | ms_marco | Ranking Error | 1 |
| q_ad433761c1c98774 | how much does working at target pay | ms_marco | Ranking Error | 1 |
| q_f91d9fedb3c63fc9 | what muscles are used during alternating ankle touches | ms_marco | Ranking Error | 1 |
| q_01fe0375e2cf110c | what is the airheads mystery flavor what is it | ms_marco | Semantic Miss | 0 |
| q_ee2fef893ef7dbc0 | what is the closest living area to disney world | ms_marco | Ranking Error | 1 |
| q_fcd6526155873a22 | when to plant garden per moon phases | ms_marco | Semantic Miss | 0 |
| q_789fbb5ab5b978f2 | cost for fiberglass inground pool | ms_marco | Ranking Error | 1 |
| q_a9f2848dc8a262ad | which part of a nucleotide contains the genetic code | ms_marco | Semantic Miss | 0 |
| q_2356d2fee8533441 | what is another name for infectious diseases | ms_marco | Ranking Error | 1 |
| q_e46a718c32db020e | how much does it cost for kitchen remodel | ms_marco | Ranking Error | 1 |
| q_c00857a7831b8a7e | what foods to eat for leg cramps | ms_marco | Ranking Error | 1 |
| q_d80c047c8f65e96d | what is contract furniture | ms_marco | Ranking Error | 1 |
| q_02fdf2112e5eb410 | define systematic psychology | ms_marco | Ranking Error | 1 |
| q_0b69e640ab28badb | what is a pbr | ms_marco | Semantic Miss | 0 |
| q_e2fc6290c2d8562f | why did the united states express concern after spain returned louisiana to france | ms_marco | Ranking Error | 1 |
| q_9557d2539ab3bf84 | what does ikat mean | ms_marco | Ranking Error | 1 |
| q_884747bbb805cbf6 | what does a geneticist do | ms_marco | Semantic Miss | 0 |
| q_4351edbb1c48515f | what does purdah mean | ms_marco | Ranking Error | 1 |
| q_1ca2a27a2494be43 | what are chemical bonds in biology | ms_marco | Ranking Error | 1 |
| q_4db6e5d0dcaaadc4 | what diseases do mosquito carry | ms_marco | Ranking Error | 1 |
| q_7103b92a139c6620 | stress fracture in hip that causes pain in a different location | ms_marco | Semantic Miss | 0 |
| q_a0765f140ad88540 | how much does a professional bowler make | ms_marco | Ranking Error | 1 |
| q_21a9393b909393e4 | what type of government does singapore have | ms_marco | Ranking Error | 1 |
| q_aa8de1328bad28d5 | what is a broken clavicle | ms_marco | Ranking Error | 1 |
| q_b065a0ead2c42f02 | Who decides the fate of protesters most of the time? | squad | Ranking Error | 1 |
| q_685c5f4e99fcb72d | when did australia gain independence | ms_marco | Semantic Miss | 0 |
| q_4dc9a1463c259da3 | douwe meaning name | ms_marco | Ranking Error | 1 |
| q_5e1936aa060eca9b | where does the name tory come from | ms_marco | Ranking Error | 1 |
| q_070ff63ca4ae9d0a | how much is it to get a bath and brush at petsmart | ms_marco | Ranking Error | 1 |
| q_05581dea702e2343 | how long does it take to cook a turkey on gas grill | ms_marco | Semantic Miss | 0 |
| q_47b2fc1e32376095 | is kefir protein | ms_marco | Ranking Error | 1 |
| q_a34951c017e1c989 | What attracts the tourists to Kenya? | squad | Semantic Miss | 0 |
| q_ebf2df12e8bfb35f | how do the nhl playoff matchups work | ms_marco | Ranking Error | 1 |
| q_0728859be6a4fddd | should i take magnesium to gain muscles | ms_marco | Ranking Error | 1 |
| q_bd958f38a031597c | what is polychromasia | ms_marco | Semantic Miss | 0 |
| q_4fe936ec38ccd01a | what is the ancestral allele | ms_marco | Ranking Error | 1 |
| q_6c3f377fdd49e156 | what is tocopherols in food | ms_marco | Ranking Error | 1 |
| q_9915b0d279d9f835 | what spices do they use in india | ms_marco | Ranking Error | 1 |
| q_7d93fb73092f0bcd | who was the australian constitution written for | ms_marco | Ranking Error | 1 |
| q_8c8b517f304516dd | what is atopic skin | ms_marco | Ranking Error | 1 |
| q_5c2455719084814d | where was the godfather filmed | ms_marco | Ranking Error | 1 |
| q_dbb5ab416abae1f2 | can i book my origin digital meter now for december | ms_marco | Ranking Error | 1 |
| q_f452425765b75346 | best vitamins for stomach health | ms_marco | Ranking Error | 1 |
| q_260b8cd79784b557 | define noun phrase | ms_marco | Semantic Miss | 0 |
| q_8465befb3918e91e | What was the name of Watt's partner? | squad | Semantic Miss | 0 |
| q_52d6135de0025aaa | is mount baker active | ms_marco | Ranking Error | 1 |
| q_6395ec3ee79723a9 | what is a dwarfs | ms_marco | Ranking Error | 1 |
| q_5e40a7b0939b2c27 | registered nurse salary las vegas | ms_marco | Ranking Error | 1 |
| q_2c8da13c3d05864b | typical sales commission percentage | ms_marco | Semantic Miss | 0 |
| q_1120ced8619d7d64 | What is the general shape of centrioles? | sciq | Semantic Miss | 0 |
| q_5415610840f2abb5 | what is gist cancer | ms_marco | Semantic Miss | 0 |
| q_e6df2508e7e6f498 | does msft pay dividends | ms_marco | Ranking Error | 1 |
| q_b8c63f3be0d5f38a | examples of vaccines are cell mediated immunity | ms_marco | Ranking Error | 1 |
| q_c5e633ddd65553d5 | how to prepare to get an ultrasound | ms_marco | Ranking Error | 1 |
| q_e199aa1d8521705c | what does medium do | ms_marco | Ranking Error | 1 |
| q_5048841a0ac0c7e7 | what is roast beef made of | ms_marco | Ranking Error | 1 |
| q_cee8eda19e2c7e2f | carbs count for a pre diabetes | ms_marco | Ranking Error | 1 |
| q_481f4c801b548ac1 | the major muscles of your arms biceps and triceps | ms_marco | Ranking Error | 1 |
| q_6705ef1b39673e90 | where is sodium mostly found | ms_marco | Ranking Error | 1 |
| q_fe6a9d48144e8be6 | how much faster is the northwest passage | ms_marco | Ranking Error | 1 |
| q_90782aa844c087c7 | how quickly does a tax refund come | ms_marco | Ranking Error | 1 |
| q_23ccd9cafe6a25f3 | what is bigger system or organism | ms_marco | Ranking Error | 1 |
| q_9f907968a02b21e1 | when do robin eggs hatch | ms_marco | Ranking Error | 1 |
| q_63e3151bc89c7319 | is sunshine minting reputable | ms_marco | Ranking Error | 1 |
| q_f4351a862afc18c4 | what are signs of osteoarthritis | ms_marco | Ranking Error | 1 |
| q_d30af42524e721e3 | What is the strength of an earthquake called? | sciq | Semantic Miss | 0 |
| q_506240d10adbc8a5 | what is trident | ms_marco | Ranking Error | 1 |
| q_951f448077796edd | BOD biological oxygen definition | ms_marco | Semantic Miss | 0 |
| q_1ae37a6d7642639d | two basic tissues of which the skin is composed are | ms_marco | Ranking Error | 1 |
| q_b07d1577893b94bc | where in tasmania does a platypus live | ms_marco | Ranking Error | 1 |
| q_9ad69993a50d0452 | who invented the first rocket that went into space | ms_marco | Ranking Error | 1 |
| q_e9e39e320c03979a | what is the hazchem code | ms_marco | Ranking Error | 1 |
| q_d36dd3fd232fdd1b | what is chaat masala | ms_marco | Ranking Error | 1 |
| q_5c6b8c77ef5d6b7a | how does a seafloor volcano create an island | ms_marco | Semantic Miss | 0 |
| q_c8d4a52e19049412 | average temperature dhaka | ms_marco | Ranking Error | 1 |
| q_c2b206b4d96822d1 | dosage of tylenol for geriatric | ms_marco | Ranking Error | 1 |
| q_3604a3dff01393bd | how to catch fish in a survival situation | ms_marco | Ranking Error | 1 |
| q_023c42020ead8636 | What other event made the BBC concerned that viewers had not seen the premier of Doctor Who? | squad | Ranking Error | 1 |
| q_6a787e9dc47d98ca | is there a certain university degree to become an occupational therapist | ms_marco | Ranking Error | 1 |
| q_222ed82eb63b7801 | do motorcycles come with automatic transmission | ms_marco | Ranking Error | 1 |
| q_453fa36f0f151790 | what element is in solder | ms_marco | Ranking Error | 1 |
| q_cb990e4db607f7ce | what are proteins formed by? | ms_marco | Ranking Error | 1 |
| q_12da1a93f1ab3e31 | how much do I pay someone to install my ceramic, backsplash | ms_marco | Ranking Error | 1 |
| q_4f445cf510014c5f | where are your deltoids muscles located | ms_marco | Ranking Error | 1 |
| q_ef2b06e47a24a7c4 | why does shoreline erosion occur | ms_marco | Ranking Error | 1 |
| q_2f05b1fd5094a78d | what is a sound barrier | ms_marco | Ranking Error | 1 |
| q_9e3952313ea07475 | different types of usb ports | ms_marco | Semantic Miss | 0 |
| q_a5aef5e15df39562 | average house price toowoomba | ms_marco | Ranking Error | 1 |
| q_582288106a6c503c | what biome has plants spaced far apart | ms_marco | Semantic Miss | 0 |
| q_2dfa1e2bbba72ff9 | surgery tech salary | ms_marco | Ranking Error | 1 |
| q_a2ba4305d7f290b4 | why is it called a moon cactus | ms_marco | Semantic Miss | 0 |
| q_77415958c1e97810 | how many ounces of water should i drink a day to lose weight | ms_marco | Ranking Error | 1 |
| q_30ae0ba44d83cd73 | what does aerobic exercise mean | ms_marco | Ranking Error | 1 |
| q_782bbb97dcc926e6 | what is bacon preservative | ms_marco | Semantic Miss | 0 |
| q_577a0d902ae6c051 | are animal warts contagious | ms_marco | Ranking Error | 1 |
| q_0a047d9b583ee56b | how to do basketball skills for beginners | ms_marco | Semantic Miss | 0 |
| q_2038118d0ad77745 | what is a rheostat | ms_marco | Ranking Error | 1 |
| q_eb654983f991473c | what is an fbc blood test | ms_marco | Ranking Error | 1 |
| q_23534334768be8a9 | how long does it take to make a million dollars in the stocks market | ms_marco | Ranking Error | 1 |
| q_7e4b9f7b30cf77ce | what type of food does pancreatic juice help to digest | ms_marco | Ranking Error | 1 |
| q_b32233ec9c75e7e4 | age limit for renting a car enterprise | ms_marco | Ranking Error | 1 |
| q_9d34201f09fb42e4 | what currency is used in vietnam? | ms_marco | Ranking Error | 1 |
| q_0e593d6ea3528ef3 | what are animals that hunt eagles | ms_marco | Ranking Error | 1 |
| q_a66368e1c36ff2bd | average starting teaching salary in minnesota | ms_marco | Ranking Error | 1 |
| q_f81076817ec9719b | what is emiesitelist | ms_marco | Ranking Error | 1 |
| q_a809b5edd45a5436 | why sedimentary rocks are porous | ms_marco | Ranking Error | 1 |
| q_df0e9d88c5c945c6 | costs of utilities per month | ms_marco | Ranking Error | 1 |
| q_d87f6fa1eaca4a7e | what is a hyperbolic curve | ms_marco | Ranking Error | 1 |
| q_8d0e9b9148a6e0f6 | how far is heimaey from reykjavik | ms_marco | Ranking Error | 1 |
| q_d2264d44eeeece94 | what hotel is on goat island ri | ms_marco | Ranking Error | 1 |
| q_57f58f7f6255508e | why do fossil fuels cause pollution | ms_marco | Ranking Error | 1 |
| q_bc90372084e74088 | what is the panama canal history | ms_marco | Ranking Error | 1 |
| q_a4b2b9ec18296659 | technology invented during the harlem renaissance | ms_marco | Ranking Error | 1 |
| q_db673069228973f6 | is tuna good for heart patients | ms_marco | Semantic Miss | 0 |
| q_e7773ebacce171b1 | is a subpoena a court order | ms_marco | Ranking Error | 1 |
| q_d92de9eb3290ee4f | Pain felt in the iris is known as | ms_marco | Ranking Error | 1 |
| q_2f61376f41648f7b | what part of the brain is linked with cognitive function | ms_marco | Ranking Error | 1 |
| q_25832db56899e6fe | is there a part of the brain called superior | ms_marco | Ranking Error | 1 |
| q_6cdfe28fcbeb1e5a | what temp should coffee be | ms_marco | Semantic Miss | 0 |
| q_8fd736d84861850b | why should kids get paid for coming to school | ms_marco | Ranking Error | 1 |
| q_4593177494140023 | why does my iphone keep going black | ms_marco | Ranking Error | 1 |
| q_b7e22d2d1bea4095 | is chuck e cheese still popular | ms_marco | Ranking Error | 1 |
| q_0c1563ec0fccaec2 | what does occipital defect mean | ms_marco | Ranking Error | 1 |
| q_d6745ebf660fbbb5 | heaviest birth weight | ms_marco | Ranking Error | 1 |
| q_923676887ec35186 | what is gastropathy | ms_marco | Ranking Error | 1 |
| q_21162198432ada2e | what is cremora | ms_marco | Ranking Error | 1 |
| q_38a17fac80d0ebf0 | what is psychosomatic | ms_marco | Ranking Error | 1 |
| q_b8c1b8dbf9a9553e | is pope francis saying priests should marry? | ms_marco | Ranking Error | 1 |
| q_a87a0ca0937785ef | what is the name of the star called la superba | ms_marco | Ranking Error | 1 |
| q_484934e2f40875d0 | what causes tias | ms_marco | Ranking Error | 1 |
| q_192a311ed0e7c346 | un applying ipsas: the cost and benefits | ms_marco | Ranking Error | 1 |
| q_4f53cec2786e59b9 | What type of bacteria stains red? | sciq | Semantic Miss | 0 |
| q_1532e22c8aafca8b | what kind of vaccine is tetanus | ms_marco | Ranking Error | 1 |
| q_c274314f2fe58fb5 | ethics is the study of what is | ms_marco | Ranking Error | 1 |
| q_22085ddf7f5799cd | what does vitamins do | ms_marco | Ranking Error | 1 |
| q_799bf479bd77c820 | Who discussed Twigg's study in 2002? | squad | Semantic Miss | 0 |
| q_f7aee95e2055e80f | why limits on roth ira | ms_marco | Semantic Miss | 0 |
| q_855d6d6aa524a117 | what will happen with oil prices | ms_marco | Semantic Miss | 0 |
| q_e8d845fd05b74d4c | what is night soil | ms_marco | Ranking Error | 1 |
| q_61a2b1e151a984d2 | what is the dosage for cymbalta | ms_marco | Semantic Miss | 0 |
| q_f155d122ca77564d | what is caucasian mean | ms_marco | Semantic Miss | 0 |
| q_535468fc275fc1be | negative effects of alcohol on society | ms_marco | Ranking Error | 1 |
| q_7d789eba778a2213 | what zone is carpal tunnel in hand | ms_marco | Ranking Error | 1 |
| q_b2b566af275df49e | why do we need to take a bmi test | ms_marco | Ranking Error | 1 |
| q_4dd6f03951c9b990 | highest radiologist salary | ms_marco | Ranking Error | 1 |
| q_f4bd8b6d699d788e | what are flavonoids in marijuana | ms_marco | Ranking Error | 1 |
| q_7a693f850ac00880 | What mechanism can be used to make oxygen? | squad | Semantic Miss | 0 |
| q_e2627ab66faf7983 | where does clownfish live | ms_marco | Ranking Error | 1 |
| q_6a46895828f37612 | when do smear tests start | ms_marco | Ranking Error | 1 |
| q_229da4ed54358f3d | how much can i charge for bankruptcy petition preparer | ms_marco | Semantic Miss | 0 |
| q_d96acb0762084428 | how long does chicken last in fridge | ms_marco | Ranking Error | 1 |
| q_821dc098ec786ff8 | motor nerve cell what do their parts do | ms_marco | Ranking Error | 1 |
| q_91935a9637876e36 | types of cartilaginous joints | ms_marco | Semantic Miss | 0 |
| q_c6a3be1427046082 | how many figures is a billion | ms_marco | Ranking Error | 1 |
| q_ae60d453d065ffc7 | how to tell if crab legs are precooked | ms_marco | Ranking Error | 1 |
| q_b7a3814485e4891e | what is the omentum | ms_marco | Ranking Error | 1 |
| q_68d8c5416b0bc8f3 | what to do on the isle of wight for disabled | ms_marco | Ranking Error | 1 |
| q_d6d09ba3f7d3186a | What are molecules that the immune system recognize as foreign to the body? | sciq | Semantic Miss | 0 |
| q_8934990981fb8a6f | the principle of faunal succession was created by quizlet | ms_marco | Ranking Error | 1 |
| q_8589f7d7fd440d17 | what is an inducer? | ms_marco | Ranking Error | 1 |
| q_d6806301007bd34d | incubation period for mumps for kids | ms_marco | Ranking Error | 1 |
| q_497bbd52ff4feaf6 | bacterial immune system | ms_marco | Semantic Miss | 0 |
| q_e4770fbbc2d5fafa | what does a comprehensive metabolic panel consist of | ms_marco | Ranking Error | 1 |
| q_ea5be787f25933e7 | the name anzac when was it formed | ms_marco | Ranking Error | 1 |
| q_547fce020a8e4bf0 | what is bilingual education and what are the advantages | ms_marco | Ranking Error | 1 |
| q_a91411031e32a13a | what is the difference between a shark and a whale | ms_marco | Ranking Error | 1 |
| q_48c7f61018bf5028 | what is pmi mip funding fee | ms_marco | Ranking Error | 1 |
| q_c006c28d28adedd4 | Why did many slaves travel immediately after gaining freedom | ms_marco | Ranking Error | 1 |
| q_e2c47334905a0e8f | what food produces serotonin | ms_marco | Semantic Miss | 0 |
| q_cd51e3c46cdb65d6 | what is a burrito | ms_marco | Ranking Error | 1 |
| q_9337afc99a85aeaa | rendering --meaning | ms_marco | Ranking Error | 1 |
| q_f1eb876a1e0a4443 | How is the due date for a pregnancy typically calculated? coursehero | ms_marco | Ranking Error | 1 |
| q_5c610870dcbf071c | What is the English translation of tawhid? | squad | Semantic Miss | 0 |
| q_feda5a3fe96f594d | chromosomes are made when dna wraps around | ms_marco | Ranking Error | 1 |
| q_77d1b51929c97be8 | what type of government does jamaica have | ms_marco | Ranking Error | 1 |
| q_6bd9692a05bd2734 | what is cfc in styrofoam | ms_marco | Ranking Error | 1 |
| q_14cb71291b123c9c | what is a falafel | ms_marco | Ranking Error | 1 |
| q_27de2a12562570af | what papers do i need to have dog | ms_marco | Semantic Miss | 0 |
| q_b95b9047a99cd35a | what is internalizing behaviors | ms_marco | Ranking Error | 1 |
| q_dbc87c074d71e1b0 | hypnotic ability psychology definition | ms_marco | Ranking Error | 1 |
| q_896f2445286b8265 | what kind of shoes do flamenco dancers wear | ms_marco | Ranking Error | 1 |
| q_4d276e0d7c28e50a | how much money do verizon retail sales reps make | ms_marco | Ranking Error | 1 |
| q_d965208415e3b555 | where did the khoisan come from | ms_marco | Ranking Error | 1 |
| q_a153389b5c787291 | how long does it take for someone to be charged an interest on discover credit card | ms_marco | Ranking Error | 1 |
| q_c4cbb52554ec1e32 | what foods contain tryptophan | ms_marco | Ranking Error | 1 |
| q_028ef89063ad049d | covalent bonds in dna are made of what | ms_marco | Ranking Error | 1 |
| q_cc658514abfd8c14 | Which of the following is a product that is considered a commodity | ms_marco | Ranking Error | 1 |
| q_2352714a246995c9 | what part of the heart is the pericardium attached to | ms_marco | Ranking Error | 1 |
| q_958c04520be36792 | what is glyceryl caprylate | ms_marco | Ranking Error | 1 |
| q_9266ddb09c26da2d | is stubhub reliable | ms_marco | Semantic Miss | 0 |
| q_e1ac0b1156a39d53 | average price per square foot for rent in USA | ms_marco | Ranking Error | 1 |
| q_d8c52942298507f6 | where is waikeria prison | ms_marco | Ranking Error | 1 |
| q_ae3d70aa54dfcdd3 | cost for poured concrete walls | ms_marco | Ranking Error | 1 |
| q_00e65a01472911a2 | how many hours does the average person volunteer | ms_marco | Ranking Error | 1 |
| q_56c506bc169c5eef | what essential oils are good for stuffy nose and sore throat | ms_marco | Ranking Error | 1 |
| q_3b21a5e584c0084a | magnetic bracelets for arthritis pros and cons | ms_marco | Ranking Error | 1 |
| q_f720642d6cd229c7 | which problem caused the most debated during the constitutional convention | ms_marco | Semantic Miss | 0 |
| q_6b359364902472fd | how long is a person certified to do electrical work | ms_marco | Ranking Error | 1 |
| q_e16e69fbda4bba44 | what is snmp used for | ms_marco | Ranking Error | 1 |
| q_807ce17f4374b76f | what causes your urine to smell | ms_marco | Ranking Error | 1 |
| q_7692d9eaf427fe95 | what age children do pediatricians treat | ms_marco | Ranking Error | 1 |
| q_7d9be6b0b27f56ac | mainstreaming services - definition | ms_marco | Ranking Error | 1 |
| q_98eb246e311cb5bb | what is a wicklow | ms_marco | Semantic Miss | 0 |
| q_da2532e05cb8023a | What organization arranged to founding of school? | squad | Semantic Miss | 0 |
| q_beb4f7d821c07290 | production rate for carpet cleaning | ms_marco | Ranking Error | 1 |
| q_92ce4afa06956ea2 | are garden spiders poisonous | ms_marco | Ranking Error | 1 |
| q_d476cd583a1f798a | what are the differences between chromosome chromatid and chromatin | ms_marco | Ranking Error | 1 |
| q_9a3a1c415a4aa50f | where are ocean trenches located | ms_marco | Semantic Miss | 0 |
| q_eeb251cee9eb9015 | what are radiolaria | ms_marco | Ranking Error | 1 |
| q_391023085f386839 | Where does the development of a fetus take place? | sciq | Semantic Miss | 0 |
| q_96dd7c2ee609627f | What was the cost for a half minute ad? | squad | Semantic Miss | 0 |
| q_dadafe3dc06ab412 | The eardrum is part of what part of the ear? | sciq | Semantic Miss | 0 |
| q_dfe0f540dd444bff | best temperature for sunflower to germinate | ms_marco | Ranking Error | 1 |
| q_1d0c025285a628b9 | what does a crankshaft do | ms_marco | Ranking Error | 1 |
| q_d5716cdcd12bde06 | where is the island of patmos | ms_marco | Ranking Error | 1 |
| q_c14f86e4e38cd9f1 | maximum pay and average pay of orthotists | ms_marco | Ranking Error | 1 |
| q_76c4877298586d9e | is hepatitis classified as autoimmune disease | ms_marco | Ranking Error | 1 |
| q_5eb0644f4b2d6f5a | what is gruyere cheese | ms_marco | Semantic Miss | 0 |
| q_ace7df0916b7df57 | what is south china tiger habitat location | ms_marco | Ranking Error | 1 |
| q_ee76919afd234652 | meaning of agnostic | ms_marco | Ranking Error | 1 |
| q_7c77796203686a35 | when did slavery end in usa | ms_marco | Ranking Error | 1 |
| q_4d62c210466b4ed5 | what is the benefit of having a dark green vegetables | ms_marco | Ranking Error | 1 |
| q_126d6f49e046cd85 | why did the polynesians migrate | ms_marco | Ranking Error | 1 |
| q_192abca33c892f45 | what ethnicity is the last name dean | ms_marco | Semantic Miss | 0 |
| q_26e49ca1c4aa99d9 | what causes a navicular fracture | ms_marco | Ranking Error | 1 |
| q_8f836e27c7faa6b9 | average cost of college in canada | ms_marco | Semantic Miss | 0 |
| q_aebc8cd5464c30a2 | what does otoacoustic emissions measure | ms_marco | Ranking Error | 1 |
| q_663244f06de08ccc | how long does it take a banana peel to decompose | ms_marco | Ranking Error | 1 |
| q_72bd9816efe23f80 | what does the median mean | ms_marco | Ranking Error | 1 |
| q_f25d5f9894bb70ef | In what language were the classes given? | squad | Ranking Error | 1 |
| q_ed98e9e31c66e11a | max income for a roth ira | ms_marco | Ranking Error | 1 |
| q_4aafa2c4341cd8e5 | what is the difference between certified and registered mail | ms_marco | Semantic Miss | 0 |
| q_571ad147c85b77c4 | what is the purpose of the labrador retriever breed | ms_marco | Ranking Error | 1 |
| q_55fba5922159f4e0 | best nutrients for vegetable garden | ms_marco | Ranking Error | 1 |
| q_ec7072a5b48d78e7 | differences between saturated unsaturated monounsaturated and polyunsaturated fatty acids | ms_marco | Ranking Error | 1 |
| q_d060ca59e8d0c732 | unt average annual cost | ms_marco | Ranking Error | 1 |
| q_ec70f0b6ab6ba6e9 | inventor definition uspto | ms_marco | Ranking Error | 1 |
| q_0de2996697225af1 | what is the largest planet in solar system | ms_marco | Ranking Error | 1 |
| q_ca7c10f8b1c1b20c | which is a warm countercurrent that periodically flows | ms_marco | Ranking Error | 1 |
| q_2458b5e8fd807765 | why does cpu fan speed up | ms_marco | Ranking Error | 1 |
| q_4499255f4983952e | When was the charter for this church signed? | squad | Semantic Miss | 0 |
| q_fd44eb23d3eb0cf9 | Why do hummingbirds have long narrow bills? | sciq | Semantic Miss | 0 |
| q_56c2edc68571bdf8 | what are blood diamonds | ms_marco | Ranking Error | 1 |
| q_821faba07b82d44e | what is a tufted rug | ms_marco | Ranking Error | 1 |
| q_a1c9357134af42cd | what is amba sauce | ms_marco | Ranking Error | 1 |
| q_a0837f9f231c4230 | geography crust definition synonym | ms_marco | Ranking Error | 1 |
| q_d1dde2bc03ed2b60 | is a peach tree an angiosperm | ms_marco | Ranking Error | 1 |
| q_0d69ade040280f42 | why is aum the symbol for hinduism | ms_marco | Ranking Error | 1 |
| q_c59c3e46dba60202 | how much does a business coach cost | ms_marco | Ranking Error | 1 |
| q_8104c0b2ca355bca | what is an unconformity rock | ms_marco | Ranking Error | 1 |
| q_ee1308cce641dc37 | how to end period early | ms_marco | Ranking Error | 1 |
| q_b2268dc6077d43c9 | is celtic different from irish or scottish? | ms_marco | Semantic Miss | 0 |
| q_ca4e5ad180faa228 | how long to hatch chicken eggs | ms_marco | Semantic Miss | 0 |
| q_3347ea7bb452db95 | how to become a cna fast | ms_marco | Ranking Error | 1 |
| q_af008bd0b0257c10 | is saccharomyces boulardii heat resistant | ms_marco | Ranking Error | 1 |
| q_897bc52affb78c93 | cataract surgery price | ms_marco | Ranking Error | 1 |
| q_d176063880f655c5 | how to block a vent register | ms_marco | Ranking Error | 1 |
| q_adca652d46d2aa0e | What force pulls bodies with mass together? | sciq | Semantic Miss | 0 |
| q_8905642446a0eb9d | what is honey made of chemically | ms_marco | Ranking Error | 1 |
| q_78afb415e5ce1105 | Continental climates are generally found in what areas of landmasses? | sciq | Semantic Miss | 0 |
| q_4c45fa5899f6b749 | cell types are specifically responsible for humoral immunity | ms_marco | Ranking Error | 1 |
| q_5b9d068a34ef6a3f | what is ra latex turbid mean | ms_marco | Ranking Error | 1 |
| q_849959a0d166dd50 | average cost for seamless gutters installed | ms_marco | Ranking Error | 1 |
| q_ceabbc1ee336bbd9 | does vaping cause gum disease | ms_marco | Ranking Error | 1 |
| q_176f4be26a3e49e8 | what is solder made of | ms_marco | Ranking Error | 1 |
| q_f6db227264c4e99a | does a water softener change ph | ms_marco | Ranking Error | 1 |
| q_fa2bba76add28cec | what education do you need to become a surgeon | ms_marco | Ranking Error | 1 |
| q_7a2e4866305a239a | how to delete user in redhat linux | ms_marco | Ranking Error | 1 |
| q_4b6d5460017d4852 | labor cost to install ceramic tile shower | ms_marco | Ranking Error | 1 |
| q_e166e209bb6ffa00 | how does lactobacillus acidophilus ferment inulin | ms_marco | Ranking Error | 1 |
| q_44bcb9172501fe27 | diseases caused by fungi | ms_marco | Semantic Miss | 0 |
| q_1263b1d30e98bbd5 | ee business number | ms_marco | Ranking Error | 1 |
| q_0b0a9eb7b691db24 | what movie is baymax from | ms_marco | Ranking Error | 1 |
| q_80a307ffce506161 | where is the pancreas located relative to other organs | ms_marco | Ranking Error | 1 |
| q_2e482440cb8a9dc2 | average length of treatment for eating disorder | ms_marco | Ranking Error | 1 |
| q_b378f50c6419cbde | what is translocation in plants | ms_marco | Ranking Error | 1 |
| q_9ff65a418f96112b | What is rusting an example of? | sciq | Semantic Miss | 0 |
| q_cb2e89f834cabf68 | what damage do fully blocked arteries | ms_marco | Ranking Error | 1 |
| q_b9ddd00b31157c63 | what is a poultice | ms_marco | Ranking Error | 1 |
| q_b32ffeafc44b195d | why la tomatina is celebrated | ms_marco | Ranking Error | 1 |
| q_59a7a04fdb70d8b0 | how can problem solving skills be improved | ms_marco | Ranking Error | 1 |
| q_00683af0e1fee621 | how long should lambs nurse till weaned | ms_marco | Ranking Error | 1 |
| q_b5ff090079c3e67f | what is cosmetic bonding | ms_marco | Ranking Error | 1 |
| q_b166e4abd7846a22 | what does waist circumference measure | ms_marco | Ranking Error | 1 |
| q_3a2b46f4d047ecea | where is the viaduct in seattle | ms_marco | Ranking Error | 1 |
| q_a53498bcb6c67395 | what is cost of replacing a capacitor in an air conditioner | ms_marco | Ranking Error | 1 |
| q_19ce24069b04651a | what is the difference between inhuman and inhumane | ms_marco | Semantic Miss | 0 |
| q_0914ccb9e18c1832 | what causes knee swelling and stiffness | ms_marco | Ranking Error | 1 |
| q_6b3957cf5ba334b6 | is hdl good cholesterol | ms_marco | Ranking Error | 1 |
| q_ec70752c179de66b | what function diffuses water molecules | ms_marco | Semantic Miss | 0 |
| q_41b56dbfff4ae000 | when did japan declare war on china | ms_marco | Ranking Error | 1 |
| q_122a688bfc1c2cfc | what causes melena stools | ms_marco | Ranking Error | 1 |
| q_82392e9bc18f8400 | is will smith really dead | ms_marco | Ranking Error | 1 |
| q_973b92b93e679ed8 | parkinson disease spiritual meaning | ms_marco | Ranking Error | 1 |
| q_b33e9733948cea97 | who was ambrose bierce | ms_marco | Ranking Error | 1 |
| q_91d1d590e628bb1f | what are ferns | ms_marco | Ranking Error | 1 |
| q_8838d2f989c96263 | what is Polygonum cuspidatum extract | ms_marco | Ranking Error | 1 |
| q_9d7eab13851ea12e | How do you spell chicken | ms_marco | Ranking Error | 1 |
| q_8a555e0ba25aea91 | What is the name of food that the plants cells make | ms_marco | Ranking Error | 1 |
| q_10ba1ad28c8e6b03 | What elements do mafic minerals typically include? | sciq | Ranking Error | 1 |
| q_8266728444aae059 | what is a gamp | ms_marco | Ranking Error | 1 |
| q_721f45434a10b181 | how to grill and finish pork steaks in the oven | ms_marco | Ranking Error | 1 |
| q_279234171949c326 | pv yield as a function of temperature | ms_marco | Ranking Error | 1 |
| q_0941ac0fbab73f62 | what made princess diana a great leader | ms_marco | Ranking Error | 1 |
| q_3e0486dfec280024 | Kangaroos, koala and opossums are part of what group? | sciq | Semantic Miss | 0 |
| q_f448aae15cc1a8f3 | how much does an animal shelter worker get paid | ms_marco | Semantic Miss | 0 |
| q_58851c2159196eb1 | how to put photos on computer from sd card | ms_marco | Ranking Error | 1 |
| q_52c7d43d7645299b | how to make a blurred background | ms_marco | Ranking Error | 1 |
| q_cf0fc1bc8e6e12a4 | after your dog has given birth how long before she is in season again | ms_marco | Semantic Miss | 0 |
| q_fc57ca6dbb87f201 | A solute generally has what effect on the boiling point of a solvent? | sciq | Semantic Miss | 0 |
| q_c2c4f304d5aa0dcf | what is a korvai | ms_marco | Ranking Error | 1 |
| q_cbc88ae42dc7123d | what state means great river | ms_marco | Ranking Error | 1 |
| q_1a8bdc11f703255b | what do the maasai do | ms_marco | Ranking Error | 1 |
| q_8682ffd5235de540 | how to nail a phone interview | ms_marco | Semantic Miss | 0 |
| q_6e54673658069447 | what is a major cause of arteriosclerosis | ms_marco | Semantic Miss | 0 |
| q_fb105085fc60d460 | what county is walnut il in | ms_marco | Ranking Error | 1 |
| q_b53b7a16d39f0117 | what does mire mean | ms_marco | Ranking Error | 1 |
| q_aa58b314deefd8bc | is cala mayor quiet | ms_marco | Ranking Error | 1 |
| q_9f4b37eca59b2518 | how many carbs should a diabetic have in one meal | ms_marco | Ranking Error | 1 |
| q_ecf88063d2685a26 | does ocelot have a backbone | ms_marco | Ranking Error | 1 |
| q_49983eca93925f26 | how to write a receptionist cover letter | ms_marco | Ranking Error | 1 |
| q_a698ff9bd6147dd4 | what is a nickelback | ms_marco | Ranking Error | 1 |
| q_8aebd5d6087ae02a | what was the reformist patriot movement | ms_marco | Ranking Error | 1 |
| q_5b1d009f964d276f | how long is a day on earth compared to space | ms_marco | Ranking Error | 1 |
| q_f664adbe2956f3ec | cost to change a delta flight | ms_marco | Ranking Error | 1 |
| q_576563c1b75d8059 | how long does it take to cook ribeye roast | ms_marco | Ranking Error | 1 |
| q_464886b00415dd2d | what is the exact location of cliff rocamadour | ms_marco | Ranking Error | 1 |
| q_14f779639afd93b2 | what was the yalta conference for | ms_marco | Ranking Error | 1 |
| q_3298781d9d42dafb | disease is something which causes | ms_marco | Ranking Error | 1 |
| q_3082984df367b466 | can you pass a urine test for alcohol the night before | ms_marco | Ranking Error | 1 |
| q_b3ff54f531313719 | what is magnesium oxide made up of | ms_marco | Ranking Error | 1 |
| q_50332c40500d5182 | what is customer acquisition cost | ms_marco | Ranking Error | 1 |
| q_ac8a094f02bcfead | most male last name | ms_marco | Ranking Error | 1 |
| q_b070de98ebd6d0d5 | how much money do radiology techs make | ms_marco | Ranking Error | 1 |
| q_c8274a86f047df6e | what is an aquamarine gem | ms_marco | Ranking Error | 1 |
| q_67d5685d62942eac | cost per square foot to build a home addition | ms_marco | Ranking Error | 1 |
| q_0a6a429b3ed28274 | what is bromazepam used for | ms_marco | Ranking Error | 1 |
| q_696c49e3399d46a1 | why was the roman army so victorious | ms_marco | Ranking Error | 1 |
| q_c3de469ebaee51a5 | where does vetiver come from | ms_marco | Ranking Error | 1 |
| q_cd4a4c1f1a5cf8e0 | what is the difference between alcohol and denatured alcohol | ms_marco | Ranking Error | 1 |
| q_2f6cda6f706450c9 | is asparagus fern a perennial | ms_marco | Ranking Error | 1 |
| q_86139ad7d431fdb7 | biome geography definition | ms_marco | Ranking Error | 1 |
| q_b5d800995c74fd4e | What are the two types of vascular plants? | sciq | Semantic Miss | 0 |
| q_c3fceb9c76897735 | course page | code_search_net | Semantic Miss | 0 |
| q_ce733da9f5f3751e | what does argentinosaurus mean | ms_marco | Ranking Error | 1 |
| q_812111205ba294ca | What did Tesla do for a job that paid two dollars a day? | squad | Ranking Error | 1 |
| q_9b51afd197d72ae8 | what is cmt | ms_marco | Ranking Error | 1 |
| q_0b90ce2c044d1ded | davita starting pay | ms_marco | Ranking Error | 1 |
| q_42b2c7e9df6e0cd6 | how to get access to a death certificate | ms_marco | Ranking Error | 1 |
| q_815d51aa8298f2f9 | how long does it take to bake a pork loin roast in the oven | ms_marco | Ranking Error | 1 |
| q_209d93c23b4978ff | Lead shielding is used to block what type of rays? | sciq | Semantic Miss | 0 |
| q_98de3973bb6523fd | what trees are in the taiga biome | ms_marco | Ranking Error | 1 |
| q_083633adeee0f4d3 | salary for qa manager | ms_marco | Ranking Error | 1 |
| q_bd5050b46957c537 | overtime for salaried employees law | ms_marco | Semantic Miss | 0 |
| q_abfc4f5cd5a3f082 | copenhagen temperatures october | ms_marco | Ranking Error | 1 |
| q_acd1d46d8642a09f | what parts of capers are used in food | ms_marco | Ranking Error | 1 |
| q_a832ff009e822817 | what are members of the kingdom protista called | ms_marco | Ranking Error | 1 |
| q_5c84c21ffe280b71 | what is the raccoons scientific name | ms_marco | Ranking Error | 1 |
| q_a9495e855fa48fee | what does stimming mean | ms_marco | Ranking Error | 1 |
| q_657443aeb7271cd6 | what is clipping morphology | ms_marco | Ranking Error | 1 |
| q_39803bdac55e25ba | average cost spay cat calgary | ms_marco | Ranking Error | 1 |
| q_a2ebff1838f14176 | how long does defrosting take | ms_marco | Ranking Error | 1 |
| q_b70ccafa1c53025b | what is the chivalry thesis | ms_marco | Ranking Error | 1 |
| q_a8263d15d95c6ff9 | what is structural protein | ms_marco | Ranking Error | 1 |
| q_009407ae820ee28e | what does earthed mean in electricity | ms_marco | Ranking Error | 1 |
| q_2f321de3973cb9d1 | how much does it cost to score a concrete floor | ms_marco | Ranking Error | 1 |
| q_85e3a02f2a106160 | can you heal knuckles arthritis | ms_marco | Ranking Error | 1 |
| q_dc09ecde18ea9854 | different types of herring | ms_marco | Ranking Error | 1 |
| q_8fb24e3dc690226a | ghana electricity cost per kwh | ms_marco | Ranking Error | 1 |
| q_e97554ebc05a135a | how much for tune up | ms_marco | Ranking Error | 1 |
| q_872bf1df3e7978c6 | why are venus fly traps carnivores | ms_marco | Semantic Miss | 0 |
| q_35c7b077c75364dd | what is the primary somatosensory cortex responsible for | ms_marco | Semantic Miss | 0 |
| q_10a40f974e8a7995 | what is latitude | ms_marco | Ranking Error | 1 |
| q_9d8f4fb78b412542 | what is the longest medical word | ms_marco | Ranking Error | 1 |
| q_4503fbdf86130aa8 | which planets are considered twins | ms_marco | Semantic Miss | 0 |
| q_b9d52f2d67e36812 | how much can music teachers make | ms_marco | Ranking Error | 1 |
| q_568a2bf90d4a3949 | when did the access to knowledge movement | ms_marco | Ranking Error | 1 |
| q_89536c4052874346 | How much did it cost to build the stadium where Super Bowl 50 was played? | squad | Ranking Error | 1 |
| q_b26edc6fe00858f5 | why did the battle of normandy happen | ms_marco | Ranking Error | 1 |
| q_5738d560296a4749 | how much can a student transfer to a parent? | ms_marco | Ranking Error | 1 |
| q_73a754fa39d16a8b | Who did the Broncos prevent from going to the Super Bowl? | squad | Ranking Error | 1 |
| q_4e0fc8a378cf9002 | what does occult blood in urine mean | ms_marco | Ranking Error | 1 |
| q_3524da4b9db64585 | what is the bottom lip piercing called | ms_marco | Ranking Error | 1 |
| q_b0baec46b9e61395 | kilaya name meaning | ms_marco | Ranking Error | 1 |
| q_6a7da7f01ad582fe | how long do walruses live | ms_marco | Ranking Error | 1 |
| q_b5529e4392c6d043 | Which measure indicates the number of electrons in a given sublevel? | sciq | Semantic Miss | 0 |
| q_f8d7af85b25bc7dd | what is static ip | ms_marco | Ranking Error | 1 |
| q_5b30c4fc9c617ac8 | what muscles are involved with a pain beside shoulder blade | ms_marco | Ranking Error | 1 |
| q_ba8c8735e187302f | what does apatite do | ms_marco | Ranking Error | 1 |
| q_7842b90b89297125 | is it ok to eat spinach raw | ms_marco | Semantic Miss | 0 |
| q_e9e03c2a221d2933 | what does mri look like | ms_marco | Ranking Error | 1 |
| q_a8e1c899fc4ad74d | can you determine device by mac address on network | ms_marco | Ranking Error | 1 |
| q_879f485dd5582a42 | How do bacteria reproduce? | sciq | Semantic Miss | 0 |
| q_6115e5fa01896a51 | what is worm juice | ms_marco | Ranking Error | 1 |
| q_a21b40faf547425d | how long do period pains last | ms_marco | Ranking Error | 1 |
| q_289a3873af7f317f | what is the longest river in africa | ms_marco | Ranking Error | 1 |
| q_d4495475480eda9d | radon is | ms_marco | Ranking Error | 1 |
| q_86fa6ee8c4e8db7c | cost of drywall ceiling | ms_marco | Ranking Error | 1 |
| q_4cc6245cdc05eb14 | How long do you broil scallops wrapped in bacon | ms_marco | Ranking Error | 1 |
| q_ff403bd2cefefa09 | what is a heightened sense of smell a symptom of | ms_marco | Semantic Miss | 0 |
| q_405e2570037a40b1 | how to fix column width in pivot table | ms_marco | Ranking Error | 1 |
| q_8572a9e73ef2bdb5 | r', | code_search_net | Semantic Miss | 0 |
| q_b75ce9cb739b44df | what is the normal dosage of citalopram for depression | ms_marco | Ranking Error | 1 |
| q_610098f1b2444152 | what is mongolian bbq | ms_marco | Ranking Error | 1 |
| q_7ef73f441c57507a | what is misdemeanor battery | ms_marco | Ranking Error | 1 |
| q_4ff4ce30209bb179 | types of spices and herbs | ms_marco | Ranking Error | 1 |
| q_238133ec7b398dcd | are beans inflammatory | ms_marco | Ranking Error | 1 |
| q_60dfd94ef80a0223 | how long does an female eagle leave the egg to hunt for food | ms_marco | Ranking Error | 1 |
| q_3a3cbcc04d9323ce | do.muslims not believe the holocaust happened | ms_marco | Ranking Error | 1 |
| q_77279bd35a6e8430 | what is the age limit for life insurance | ms_marco | Ranking Error | 1 |
| q_2b42d0879467c995 | average salary of a ups driver | ms_marco | Ranking Error | 1 |
| q_21ebfc2bfbe84257 | what is the difference between polar satellite and geostationary | ms_marco | Ranking Error | 1 |
| q_636749d736fdf9c9 | what europeans did to native american | ms_marco | Ranking Error | 1 |
| q_ea727e599738fbc2 | why are alloys classified as mixtures | ms_marco | Ranking Error | 1 |
| q_5e9f37d7c9ab48e1 | best way to find raikou in crystal | ms_marco | Semantic Miss | 0 |
| q_01b5a1319244e0eb | what does jitter mean | ms_marco | Ranking Error | 1 |
| q_9c6e59ad1b75756e | when does it become a fetus | ms_marco | Ranking Error | 1 |
| q_bfffbe2222febb6f | where is the headquarters of google | ms_marco | Ranking Error | 1 |
| q_071e849ce9ff8264 | average weight of human excrement | ms_marco | Ranking Error | 1 |
| q_a5e143e492f941f3 | what causes arterial plaque | ms_marco | Ranking Error | 1 |
| q_eeed9050c576e9b3 | how many calories in a slice of watermelon | ms_marco | Ranking Error | 1 |
| q_b62681dff6955711 | average cost of tiling a shower | ms_marco | Ranking Error | 1 |
| q_f062f2b8ecb67202 | The amount of energy needed to raise the temperature of one gram of liquid water by 1°c is also known as? | sciq | Semantic Miss | 0 |
| q_1a19cf99927d7f00 | what is lacquer | ms_marco | Ranking Error | 1 |
| q_de99b3aff297db70 | when did seat belt laws go into effect | ms_marco | Ranking Error | 1 |
| q_37aa43630f30e317 | types of joins in relational algebra with examples | ms_marco | Ranking Error | 1 |
| q_11575b5d77a9c9f4 | what do organ systems that work together form | ms_marco | Ranking Error | 1 |
| q_7133532ab530e5cf | ttl meaning electronics | ms_marco | Ranking Error | 1 |
| q_40efc745b06f5273 | what to get someone whose pet has died | ms_marco | Ranking Error | 1 |
| q_8591024ea4ea87e7 | what is tnf alpha | ms_marco | Semantic Miss | 0 |
| q_b8fdc33c42b30ebc | how long should you leave a thermometer under your tongue | ms_marco | Ranking Error | 1 |
| q_955cefc811110424 | what is a captor | ms_marco | Ranking Error | 1 |
| q_a772a5689a1d8f00 | where to get corso riggs | ms_marco | Ranking Error | 1 |
| q_8af3fb3f32d71811 | non deductible ira to roth ira | ms_marco | Ranking Error | 1 |
| q_ecdedb989b6bc296 | what type of horse does ferrari use | ms_marco | Ranking Error | 1 |
| q_d0d9adb96dd4991a | What causes eutrophication to occur? | sciq | Ranking Error | 1 |
| q_5cd03ee2a4571655 | when is a good time to start tomato seeds indoors | ms_marco | Semantic Miss | 0 |
| q_b9102b86d9aa2e37 | what is speed of an object | ms_marco | Ranking Error | 1 |
| q_76ad20e7dccd1962 | how to cook the perfect tuna steak | ms_marco | Ranking Error | 1 |
| q_d8fd5d145ab2fc87 | does cat litter reduce humidity in home | ms_marco | Ranking Error | 1 |
| q_9468fe7b787a89b2 | what is an operations management degree | ms_marco | Ranking Error | 1 |
| q_aeec020531bbfa3a | what is jra | ms_marco | Ranking Error | 1 |
| q_5713855218a503c4 | how long does it take to complete a hs CRP | ms_marco | Ranking Error | 1 |
| q_62181cff51bb0903 | what purpose does public policy serve | ms_marco | Ranking Error | 1 |
| q_ba13672f6f767512 | what age does baskin robbins hire | ms_marco | Ranking Error | 1 |
| q_8c0ffa9a7393a566 | Which authority figure is designated to schedule and set the work of the EU? | squad | Semantic Miss | 0 |
| q_171acba144f5aa50 | typical medigap insurance costs | ms_marco | Ranking Error | 1 |
| q_768084d9561ac386 | salary limit for income tax | ms_marco | Ranking Error | 1 |
| q_0515e8d4bb30644e | what is smallest particle size a human eye can see | ms_marco | Ranking Error | 1 |
| q_e201397343ce93ac | describe how mitosis maintains a constant chromosome number | ms_marco | Ranking Error | 1 |
| q_058b6761e3f8b204 | what is the native american word for coyote | ms_marco | Semantic Miss | 0 |
| q_82136aca87589e66 | When something is described as "hydrophilic", you can determine something about how it interacts with what? | sciq | Semantic Miss | 0 |
| q_3981be3b8ee5fc79 | pesto slang meaning | ms_marco | Ranking Error | 1 |
| q_a24abe2303010572 | how long is cooked turkey good in the fridge | ms_marco | Ranking Error | 1 |
| q_d41e66ab9d722da8 | what molecules are plastic bags made up of | ms_marco | Ranking Error | 1 |
| q_3a37e3acda794258 | how much does behavior analyst make | ms_marco | Ranking Error | 1 |
| q_02c11e43b6b552b1 | what are gray wolves predators | ms_marco | Ranking Error | 1 |
| q_cf6db9bff6f5ac1f | What was the boat called? | squad | Semantic Miss | 0 |
| q_e3976b60e05bb1dd | what is the salary range for a cardiac rehab director | ms_marco | Ranking Error | 1 |
| q_621809397b09d40e | how much is a guinea worth now | ms_marco | Ranking Error | 1 |
| q_63248ecad06ad51f | can you use vicks vaporub when pregnant | ms_marco | Ranking Error | 1 |
| q_41ce410ce41c7cb0 | what is nmr and mri | ms_marco | Ranking Error | 1 |
| q_9a99b61003fb042f | do I have to have pci dss | ms_marco | Ranking Error | 1 |
| q_de5575a1356fe4d5 | what is a retail buyer | ms_marco | Ranking Error | 1 |
| q_6023be198c2f04e9 | what is a pull groin | ms_marco | Ranking Error | 1 |
| q_2a202499905cf487 | where is the baobab trees in madagascar | ms_marco | Ranking Error | 1 |
| q_dcf282a2173baa85 | hormones are chemicals that are secreted and go directly into | ms_marco | Ranking Error | 1 |
| q_b460388a5f382d74 | what is chytridiomycosis caused by | ms_marco | Ranking Error | 1 |
| q_4c62271c53221b5d | normal dosage of diazepam | ms_marco | Ranking Error | 1 |
| q_8d36a02137d01aa8 | what are the units of gauss | ms_marco | Ranking Error | 1 |
| q_977074e6f2c349e9 | how much does a good pair of hearing aids cost | ms_marco | Ranking Error | 1 |
| q_918f7696fe22572b | What do you call the zone in a body of water where there is too little sunlight for photosynthesis? | sciq | Semantic Miss | 0 |
| q_d983ae2f29542436 | how to cook a duck in the oven | ms_marco | Ranking Error | 1 |
| q_14959a23737833a1 | how old must a child be to have a simple ira account | ms_marco | Ranking Error | 1 |
| q_cbf591511237f00e | how long to cook a smithfield marinated pork tenderloin | ms_marco | Ranking Error | 1 |
| q_aa9a38b1df1a6ba6 | how much is an lady americana mattress worth | ms_marco | Ranking Error | 1 |
| q_09d60a815dd088e3 | what kind of flour do gluten free | ms_marco | Ranking Error | 1 |
| q_5d2c8293db3aa3b8 | what the average cost of getting a cement foundation | ms_marco | Semantic Miss | 0 |
| q_4d24db22a52236bc | Humor is a part of the classroom for what type of teacher? | squad | Semantic Miss | 0 |
| q_dad30bda5eb9ceca | what does circumduction mean | ms_marco | Semantic Miss | 0 |
| q_fb6245ea065118e2 | what are watersheds | ms_marco | Ranking Error | 1 |
| q_7f67af39ff421dcd | what makes a thunderstorm | ms_marco | Ranking Error | 1 |
| q_d2aaf3b4e9e744fd | how much does it cost to repair a washer machine | ms_marco | Semantic Miss | 0 |
| q_b291591998301950 | function of acth | ms_marco | Ranking Error | 1 |
| q_350f90d9959a64a5 | annual salary of a forensic scientist in texas | ms_marco | Ranking Error | 1 |
| q_56dd2d231f7a911c | What is prosopagnosia? | sciq | Semantic Miss | 0 |
| q_c1e14706b16cea23 | What did giving money to the church absolve the giver from? | squad | Semantic Miss | 0 |
| q_daad0fbd05a84c9f | what is normal urine frequency per day | ms_marco | Ranking Error | 1 |
| q_c8b678d0bccd07d0 | what were early dry cell batteries made of | ms_marco | Ranking Error | 1 |
| q_9eb7e1b235cc68af | how much do you get paid fostering a child | ms_marco | Ranking Error | 1 |
| q_f3c6f5582ea7e7f5 | where can a cheetah be found | ms_marco | Semantic Miss | 0 |
| q_c5f0807d1c5550d4 | what is paw paw | ms_marco | Ranking Error | 1 |
| q_e721d7a4e2e11c0d | where is your appendix located on a male | ms_marco | Ranking Error | 1 |
| q_87c4ee3cdeae7666 | cost for relining dentures | ms_marco | Ranking Error | 1 |
| q_a80b1cc16e057e3e | What is the first part of the large intestine called? | sciq | Ranking Error | 1 |
| q_4e47e3bf784a936f | what was the purpose of abraham lincoln's gettysburg address | ms_marco | Ranking Error | 1 |
| q_cf73ba7bb6d8a127 | where is grand cayman island located | ms_marco | Ranking Error | 1 |
| q_686cabebe2ce1a33 | how much do bodybuilders make | ms_marco | Ranking Error | 1 |
| q_a1ad259b5936af0f | what is solder paste used for | ms_marco | Ranking Error | 1 |
| q_15b906059f2085af | Who conducted this survey? | squad | Semantic Miss | 0 |
| q_24992c68eec9e512 | diseases caused by viruses list | ms_marco | Semantic Miss | 0 |
| q_87e485d17151c74d | where do orangutans live | ms_marco | Ranking Error | 1 |
| q_b52072974abfc4e0 | what is alcantara leather | ms_marco | Ranking Error | 1 |
| q_d6d098ae8394d046 | how does dragonfly moves | ms_marco | Ranking Error | 1 |
| q_cec41fde21b87c06 | which civilization is considered the world's oldest | ms_marco | Ranking Error | 1 |
| q_578e304516c51b9a | what are ice plants | ms_marco | Ranking Error | 1 |
| q_e9f673e1349292e5 | how long does it take for pterygium to heal after surgery | ms_marco | Semantic Miss | 0 |
| q_9ebecb1bcb6e73cf | what kind of gravel is bad for a fish tank | ms_marco | Semantic Miss | 0 |
| q_1c16cf6c28b5a46d | what does the name bronson mean | ms_marco | Ranking Error | 1 |
| q_4d7ff5bd19481cf4 | What exactly happens during rna translation? | sciq | Semantic Miss | 0 |
| q_06df2a908b22b3e8 | what is a bore diameter | ms_marco | Ranking Error | 1 |
| q_aaf3b176530bdc6a | what diseases do chickens carry that harm humans | ms_marco | Ranking Error | 1 |
| q_6e0972e5c1d26c38 | how fast does first response detect pregnancy | ms_marco | Ranking Error | 1 |
| q_27ab3943e14c6afe | What is the meaning of polymeric? | ms_marco | Semantic Miss | 0 |
| q_c1c190fbfe736f78 | What was the black death originally blamed on? | squad | Ranking Error | 1 |
| q_4c0c2f1386c8b8b6 | supervolcano definition | ms_marco | Ranking Error | 1 |
| q_aab10907205ee8b0 | what temp should a dog be while in labor | ms_marco | Ranking Error | 1 |
| q_879c8dd5b417ee10 | frequency of data definition | ms_marco | Ranking Error | 1 |
| q_c95681438ac8f501 | what decade did manufacturing start singapore | ms_marco | Ranking Error | 1 |
| q_0889b27b9ff2e177 | define dropsy disease | ms_marco | Ranking Error | 1 |
| q_59c2b6e1928cd1c9 | what diseases can skin rashes | ms_marco | Semantic Miss | 0 |
| q_0752311856bb4cf1 | what does ounce mean | ms_marco | Ranking Error | 1 |
| q_006f273bb699ed98 | what is a snowy owl's climate | ms_marco | Ranking Error | 1 |
| q_cde06938d3914e06 | where does water reabsorption occur | ms_marco | Ranking Error | 1 |
| q_91c96b3bd6501a42 | is a mri a test or imaging | ms_marco | Ranking Error | 1 |
| q_0a758885bbe34dc8 | why volcanoes occur | ms_marco | Ranking Error | 1 |
| q_2c8de61534152846 | what is the largest muscle in the body | ms_marco | Semantic Miss | 0 |
| q_304193d6e4a1622f | what sort of mouth does barbus barbus have | ms_marco | Ranking Error | 1 |
| q_55b524b96b494020 | geothermal cost to install | ms_marco | Ranking Error | 1 |
| q_db3cfb4956a50b92 | why is a pineapple called a pineapple | ms_marco | Semantic Miss | 0 |
| q_27ffce3310c7f7cd | why are gas prices going up in oregon | ms_marco | Ranking Error | 1 |
| q_f89fef3758d0ef1e | is cholesterol only found in animal products | ms_marco | Ranking Error | 1 |
| q_495b41017ddbb282 | what is brand archetype or essence | ms_marco | Ranking Error | 1 |
| q_b2b6210b91a6551f | how much does southwest charge to change a reservation to another person | ms_marco | Ranking Error | 1 |
| q_9eee7939bb6771f5 | where is rottnest island located | ms_marco | Ranking Error | 1 |
| q_94adb893cd300d76 | what are examples of GMOs | ms_marco | Semantic Miss | 0 |
| q_1f3fd5777a50c2e7 | What is the wavelength of light expressed in? | sciq | Ranking Error | 1 |
| q_36c535c1cd3e776d | a group of many islands is called what | ms_marco | Ranking Error | 1 |
| q_37ec0aa81c0864c4 | plasmids definition biology | ms_marco | Ranking Error | 1 |
| q_2d718773e8dd9276 | where is it cheaper to fly in october | ms_marco | Ranking Error | 1 |
| q_e0307276c7916d75 | how much does a circuit judge make | ms_marco | Ranking Error | 1 |
| q_7a3ac415f68996c9 | Who if the commissioner of the NFL? | squad | Semantic Miss | 0 |
| q_f70453675e62e1ac | what is a windage tray | ms_marco | Ranking Error | 1 |
| q_5668bad4a953e3e4 | bandwidth utilization definition | ms_marco | Ranking Error | 1 |
| q_545215642b65c503 | what level of oxygen is dangerous | ms_marco | Ranking Error | 1 |
| q_49347b008ac048c0 | food good in potassium | ms_marco | Ranking Error | 1 |
| q_7e964312fe935364 | what is venus | ms_marco | Ranking Error | 1 |
| q_12b8bc65aa38f13c | how much does ipl facial cost | ms_marco | Ranking Error | 1 |
| q_0a778ef11874cd2c | what is acetoin | ms_marco | Ranking Error | 1 |
| q_d20cb145289a4bc2 | Creates the email | code_search_net | Semantic Miss | 0 |
| q_10ba9fdea270299b | what is a gini coefficient | ms_marco | Ranking Error | 1 |
| q_92866ca2c2faf2bf | maine average temperature | ms_marco | Ranking Error | 1 |
| q_da13b3302b39f67f | how much do radiologists techs make an hour | ms_marco | Ranking Error | 1 |
| q_91aa976fca7b662b | what cells contain hemoglobin genes | ms_marco | Ranking Error | 1 |
| q_df533d66c20554f6 | man utd goalkeeper | ms_marco | Ranking Error | 1 |
| q_6e77434104472262 | cost to replace heat pump and furnace | ms_marco | Ranking Error | 1 |
| q_d0a8157233019b4b | where are fjords found | ms_marco | Ranking Error | 1 |
| q_7598c103119b2116 | how much is a chef paid well | ms_marco | Ranking Error | 1 |
| q_e83745745ea1b10f | what is opportunity qualification process | ms_marco | Ranking Error | 1 |
| q_9aecd1a60b8f83a3 | what is culture within a business | ms_marco | Ranking Error | 1 |
| q_6fba5986e4acf19d | what type of response by the afferent arterioles | ms_marco | Ranking Error | 1 |
| q_4347625c07fd24a4 | where was laura ingalls wilder born | ms_marco | Ranking Error | 1 |
| q_92f5232d60365065 | where is the blarney castle in ireland | ms_marco | Ranking Error | 1 |
| q_5e5f173e9fde27e2 | is it normal to get period week after your period | ms_marco | Ranking Error | 1 |
| q_8212edb14a810e1e | how long is a teaching degree | ms_marco | Ranking Error | 1 |
| q_74059a6b81ede9cb | how do i get a dining plan with an annual pass at disney world | ms_marco | Ranking Error | 1 |
| q_66d2e417936a867e | what dominant traits are advantageous | ms_marco | Ranking Error | 1 |
| q_803ef0ee7033da63 | What two other rulers had their graves hidden under a river? | squad | Semantic Miss | 0 |
| q_71989c23308dc2fb | what region is ireland in | ms_marco | Ranking Error | 1 |
| q_588e9a7f48d422a9 | cost of renewing a passport | ms_marco | Ranking Error | 1 |
| q_7aa4ec6bb55b20a6 | how thick should a driveway cap be | ms_marco | Ranking Error | 1 |
| q_447e2c84644370d8 | cayenne peppers the average price | ms_marco | Ranking Error | 1 |
| q_2e823a7c4cd0faf8 | how to change your pc login password | ms_marco | Ranking Error | 1 |
| q_31860aa88bbcfc39 | is penicillin a bacteriostatic | ms_marco | Ranking Error | 1 |
| q_8d0790c57a293ca8 | what are characteristics of a republic government | ms_marco | Ranking Error | 1 |
| q_72350f085b880b94 | examples of opportunistic fungi | ms_marco | Ranking Error | 1 |
| q_c018e33b5a2fc760 | geography what research methods do they use | ms_marco | Ranking Error | 1 |
| q_7652a0223394def1 | what is dust from mites | ms_marco | Ranking Error | 1 |
| q_fc633284044ae60b | Which church's saint is nicknamed The Martyr? | squad | Semantic Miss | 0 |
| q_6a9b6e86f24ea0f8 | what causes takayasu arteritis | ms_marco | Ranking Error | 1 |
| q_cf5e4ca3ee22a1c3 | what structures are associated with cell movement | ms_marco | Ranking Error | 1 |
| q_552dd9244e7a1a6b | What type of civil disobedience is accompanied by aggression? | squad | Ranking Error | 1 |
| q_c1d17b8dff93300f | Mushrooms are an example of what type of organism, which includes beneficial and toxic specimens? | sciq | Semantic Miss | 0 |
| q_aac58584282d658d | ufc membership cost | ms_marco | Ranking Error | 1 |
| q_08670322099bbd3d | what does the rpc server is unavailable mean | ms_marco | Ranking Error | 1 |
| q_56cd18d3f395ca0f | what are good fat food | ms_marco | Ranking Error | 1 |
| q_9271a3d54c931f18 | how to share wireless with virtual pc | ms_marco | Semantic Miss | 0 |
| q_482bbcc781937c1c | What important organelle (that would otherwise be centrally located and crucial to the cell's survival) do prokaryotic cells lack? | sciq | Ranking Error | 1 |
| q_43b2974c5c420e2e | what is a wetland restoration | ms_marco | Ranking Error | 1 |
| q_7a1692c5c5afa953 | when should my insurance renewal be received | ms_marco | Ranking Error | 1 |
| q_441990412590ff6a | mars average surface temperature in celsius | ms_marco | Semantic Miss | 0 |
| q_5ee3ace443b29025 | does alcohol aggravate osteoarthritis | ms_marco | Ranking Error | 1 |
| q_685dd5d5f21e281f | what is recao | ms_marco | Ranking Error | 1 |
| q_e017c117c6f399c2 | what is fg in catheter | ms_marco | Ranking Error | 1 |
| q_d6ae6e769482d831 | flagstone cost per square foot installed | ms_marco | Ranking Error | 1 |
| q_14f1e96c5c224186 | average cost of coolsculpting procedure | ms_marco | Ranking Error | 1 |
| q_eb6e4acb6ca53d80 | what are the four types of fossils | ms_marco | Ranking Error | 1 |
| q_ea77370af2f315bf | what disease do cockroaches cause | ms_marco | Semantic Miss | 0 |
| q_1f126938229f1bd9 | how to boil a perfect egg | ms_marco | Ranking Error | 1 |
| q_caf3a291ee189fb9 | are yeezys ever going to be widely available | ms_marco | Ranking Error | 1 |
| q_ed27716d56a9d6c6 | what is the meaning of wright | ms_marco | Ranking Error | 1 |
| q_45ef88fb1b2205a5 | when did alcohol become illegal | ms_marco | Ranking Error | 1 |
| q_2f1958ca3bceca7f | what is pnp mean | ms_marco | Ranking Error | 1 |
| q_dfd941f40fdda185 | does probiotics work for cat diarrhea | ms_marco | Ranking Error | 1 |
| q_0a24d3942184894e | what is difference between planned amounts and budgeted amounts | ms_marco | Ranking Error | 1 |
| q_aad8a10a912e4795 | how often should you receive a tetanus shot | ms_marco | Ranking Error | 1 |
| q_24b8c7f89d151ce5 | is dimethicone organic | ms_marco | Ranking Error | 1 |
| q_00b61608a640ea42 | what is in a bratwurst | ms_marco | Ranking Error | 1 |
| q_dcffd7c12984ec39 | what is the prostate gland and what does it do | ms_marco | Semantic Miss | 0 |
| q_546a9f3ae3c7ad9f | what do hopi ear candles do | ms_marco | Ranking Error | 1 |
| q_e7d18fbd405bf77e | what is the climate polar environment | ms_marco | Ranking Error | 1 |
| q_1c1cafb0e9f30ccc | what is the total fee for a petition | ms_marco | Ranking Error | 1 |
| q_84d295dd9dc14b8d | is phagocytosis autotrophic or heterotrophic | ms_marco | Ranking Error | 1 |
| q_e78ffbaac5a20423 | cost to install hardwood floor | ms_marco | Ranking Error | 1 |
| q_e540e7a1e55015a5 | what is a beta particle made up of | ms_marco | Ranking Error | 1 |
| q_f4851900fe16b33e | average cost to tile a shower | ms_marco | Semantic Miss | 0 |
| q_7e576043020ec747 | what function does the thyroid perform | ms_marco | Ranking Error | 1 |
| q_cf21556b72b97d25 | what if jury summons excuses confirmation notice | ms_marco | Ranking Error | 1 |
| q_190ea760af8bbb06 | how long does it take for hair to grow back | ms_marco | Ranking Error | 1 |
| q_577d4c56ff750523 | what is spontaneous radioactive decay | ms_marco | Ranking Error | 1 |
| q_be42cbc61845c6c0 | what is a diocese | ms_marco | Ranking Error | 1 |
| q_3c11dabfdbf3aaea | what happens if you over contribute to tfsa | ms_marco | Ranking Error | 1 |
| q_d14182acc0d3199c | how to get dog hair off of clothes | ms_marco | Semantic Miss | 0 |
| q_80d1d980b4069ede | anaya name meaning | ms_marco | Ranking Error | 1 |
| q_2b8f92bb0a22806d | meaning of ilona | ms_marco | Ranking Error | 1 |
| q_8c1fb0d7e0aaccc6 | what are the three major groups of amphibians alive today | ms_marco | Semantic Miss | 0 |
| q_a0786d47a4128514 | what team does adrian peterson play for | ms_marco | Ranking Error | 1 |
| q_32c2f31565581a54 | what is the equation for amplitude of a wave | ms_marco | Ranking Error | 1 |
| q_a04ff1848d24da5c | where was spike lee born | ms_marco | Semantic Miss | 0 |
| q_5c85e59eaebd128f | how much salary in USA for GM of a restaurant? | ms_marco | Ranking Error | 1 |
| q_f86808ed5a8d4abe | how much are the court fees for a divorce | ms_marco | Ranking Error | 1 |
| q_6e4a42a38d1d465a | what does disclosure mean under hipaa | ms_marco | Ranking Error | 1 |
| q_038332311309e770 | who invented the very first washing machine ever | ms_marco | Semantic Miss | 0 |
| q_f7095b0c0200b6d5 | is there such thing as a work spouse? | ms_marco | Ranking Error | 1 |
| q_6506b40e6036b60e | financial service designations | ms_marco | Ranking Error | 1 |
| q_081cc3b9710eb5a2 | what is buccal midazolam | ms_marco | Ranking Error | 1 |
| q_c6f28b2250cb74ed | does msm and biotin change hair texture | ms_marco | Ranking Error | 1 |
| q_1de66b5140cd46bc | average condo association fees chicago | ms_marco | Semantic Miss | 0 |
| q_c8b3639a7c6fcafd | how much does a rent roll cost | ms_marco | Ranking Error | 1 |
| q_2776e3c6374b69f1 | what is the link between alveoli and capillaries | ms_marco | Ranking Error | 1 |
| q_9cfef7be2ddaea70 | what is dogma | ms_marco | Ranking Error | 1 |
| q_d7ef6bbf01c955f0 | what is the name of the mountain range in caracas | ms_marco | Ranking Error | 1 |
| q_47046eeb7ead7af5 | how does pressure affect phase change | ms_marco | Ranking Error | 1 |
| q_a5164197f5418260 | Which country is not badly hit by the embargo? | squad | Semantic Miss | 0 |
| q_79b1be9044128cff | when was daenerys born | ms_marco | Ranking Error | 1 |
| q_fe2a8560b024626e | what process do plants use to break down the sugars they produce | ms_marco | Ranking Error | 1 |
| q_135ba8f59c52277b | what causes a collapsed lung in a teenager | ms_marco | Ranking Error | 1 |
| q_6e88fcdcbf3603c4 | what language do they speak in saudi arabia | ms_marco | Semantic Miss | 0 |
| q_3db66def356ad198 | how much does it cost to get retainers replace at western dental | ms_marco | Ranking Error | 1 |
| q_3db3937f796ae80d | Start the timer. | code_search_net | Semantic Miss | 0 |
| q_57d6e845e1f1e45a | starting dose of neurontin | ms_marco | Ranking Error | 1 |
| q_d09c4323a77cab54 | best natural sources of calcium | ms_marco | Ranking Error | 1 |
| q_4af5e8e147615dfc | what is produced from limestone | ms_marco | Ranking Error | 1 |
| q_71ef59db9a56e524 | what are amalgam filling made of | ms_marco | Ranking Error | 1 |
| q_0bca7a1efe7c7707 | What is the tectonic zone called where two plates come together? | sciq | Semantic Miss | 0 |
| q_742e78c297061191 | failure to configure windows update reverting | ms_marco | Ranking Error | 1 |
| q_ecdaf886dad20e73 | which blood test is for folate | ms_marco | Ranking Error | 1 |
| q_b5ce223764eae8d5 | what is the hindi name for calotropis? | ms_marco | Ranking Error | 1 |
| q_910bab2a63b4345b | how much does a pregnancy cost without insurance | ms_marco | Ranking Error | 1 |
| q_d67306c4159b73aa | nylon or cotton socks for cold weather | ms_marco | Ranking Error | 1 |
| q_e03b64dc5c5ac7cc | define altruism | ms_marco | Ranking Error | 1 |
| q_76134d921450507d | cost to repair brake pads | ms_marco | Ranking Error | 1 |
| q_c881a50b8692059f | what is hardboard used for | ms_marco | Ranking Error | 1 |
| q_231e51416da77b78 | define contract employee | ms_marco | Ranking Error | 1 |
| q_7221c137f60bae97 | how to take apart pallets | ms_marco | Ranking Error | 1 |
| q_4f259a2b59dd8874 | types of dimorphic fungi | ms_marco | Ranking Error | 1 |
| q_d838626f9bc4088d | average lifespan for collie | ms_marco | Ranking Error | 1 |
| q_45c496ae01a5fb0c | name meaning companion | ms_marco | Ranking Error | 1 |
| q_5d0ccc7b992bcbdd | what does hss stand for | ms_marco | Ranking Error | 1 |
| q_0abe1f508a543f52 | What causes strain in structures? | squad | Semantic Miss | 0 |
| q_dca7e976a0a1ec68 | do intralipids cause infections | ms_marco | Semantic Miss | 0 |
| q_d7861b8a810c99f5 | where is endometrial ablation performed | ms_marco | Semantic Miss | 0 |
| q_675438c9b3296f7b | how long to cook sweet potatoes in the oven | ms_marco | Semantic Miss | 0 |
| q_7eae2df5b216d366 | what does wallahi azeem mean | ms_marco | Ranking Error | 1 |
| q_c31f947daa205dab | irs publication origination fees | ms_marco | Ranking Error | 1 |
| q_103dcced4a564716 | pool renovation cost | ms_marco | Ranking Error | 1 |
| q_887ae5a526ee80e5 | what is FBG service corporation | ms_marco | Ranking Error | 1 |
| q_9bc51ba5e006b375 | how much does a carpenter charge per hour | ms_marco | Ranking Error | 1 |
| q_35bc36093847f847 | how did they build the pyramids of egypt | ms_marco | Ranking Error | 1 |
| q_e77a13b1c59e151c | what is the symbol of pheasants | ms_marco | Ranking Error | 1 |
| q_b4daba06b535d724 | What protects reptiles from injury and loss of water? | sciq | Semantic Miss | 0 |
| q_f131be641e5abc37 | What is the NASUWT? | squad | Semantic Miss | 0 |
| q_90269e42078fb00c | what is bax | ms_marco | Ranking Error | 1 |
| q_743b3a63548a7421 | what is the currency for cyprus | ms_marco | Ranking Error | 1 |
| q_bf0223230c00806b | what is the cerrados plain | ms_marco | Ranking Error | 1 |
| q_867c1fccba8c054d | talbots hourly wage | ms_marco | Ranking Error | 1 |
| q_9271d6e103cc7f5a | what is the average cost to stretch carpet | ms_marco | Ranking Error | 1 |
| q_ace8dabc1cd03716 | why are dragonflies called mosquito hawks | ms_marco | Ranking Error | 1 |
| q_625f36c02fe4d453 | what age should children get the pneumococcal vaccine? | ms_marco | Ranking Error | 1 |
| q_8b92e43f6bdc96ca | what kind of a volcano is osorno | ms_marco | Ranking Error | 1 |
| q_1bcdd6774d5ad542 | where is the dinosaur coast | ms_marco | Ranking Error | 1 |
| q_90cee56588231b07 | what part of the body does the coronary artery supply | ms_marco | Semantic Miss | 0 |
| q_e2228391a29a88e0 | what is a fuse | ms_marco | Ranking Error | 1 |
| q_e5f2c7726745ca12 | normal range heart rate | ms_marco | Ranking Error | 1 |
| q_a8f5e10c15bc44f5 | are american corns bad | ms_marco | Ranking Error | 1 |
| q_8b885c43edf569de | average salary increase for bachelor's degree | ms_marco | Semantic Miss | 0 |
| q_7c63b37a7206f04c | what continent is saudi arabia | ms_marco | Ranking Error | 1 |
| q_4277d3046c052772 | what does thyroid stimulating hormone do | ms_marco | Ranking Error | 1 |
| q_0e6d3fe3083810c7 | what is paraffin | ms_marco | Ranking Error | 1 |
| q_dbdf9d3555b78538 | how much does home a/c unit | ms_marco | Ranking Error | 1 |
| q_ff06b4039ffac138 | why are elephants considered mammals | ms_marco | Ranking Error | 1 |
| q_ef4abe42fd7e84c5 | what is nasal reflux | ms_marco | Ranking Error | 1 |
| q_773b95455700d945 | how tall is a redwood tree | ms_marco | Ranking Error | 1 |
| q_0d95a7116061a0f1 | what causes osteoarthritis flare up | ms_marco | Ranking Error | 1 |
| q_c8cede7f7d1b9a8b | where is hitlers crows nest located | ms_marco | Ranking Error | 1 |
| q_5877c263b39b3d5d | What was the definition of professionals, for this study? | squad | Semantic Miss | 0 |
| q_083263722c7afefe | how to take care aloe vera plant at home | ms_marco | Ranking Error | 1 |
| q_1efdbec32f4a78e6 | what is egmont cheese | ms_marco | Ranking Error | 1 |
| q_a015d79760c7b5f2 | What was the name of the legislation passed in 1850? | squad | Semantic Miss | 0 |
| q_8e0a918d7fb89827 | cost to send a postcard | ms_marco | Ranking Error | 1 |
| q_b23606b38b656865 | what is a gorge | ms_marco | Ranking Error | 1 |
| q_d0350e41dc500692 | Who would have been the lowest-ranked class? | squad | Semantic Miss | 0 |
| q_81b69c662de3a746 | what is altitude training | ms_marco | Ranking Error | 1 |
| q_6ffd61cd3b0285dd | when did first wave feminism begin | ms_marco | Semantic Miss | 0 |
| q_c50d280a8be50692 | is dyslexia hereditary | ms_marco | Ranking Error | 1 |
| q_00ce85b5c23d675d | Who is the designer of the "50?" | squad | Semantic Miss | 0 |
| q_48fc53a7f39565c3 | how much does a computer engineer earn | ms_marco | Ranking Error | 1 |
| q_c85ac556da48437b | what structure is responsible for moving the chromosomes during mitosis | ms_marco | Ranking Error | 1 |
| q_d125c276189f8112 | how to get stronger at home without weights | ms_marco | Ranking Error | 1 |
| q_96c1aa5029db21da | which hemisphere are the largest land masses found | ms_marco | Ranking Error | 1 |
| q_40ab09af9d0c068a | air handler replacement cost | ms_marco | Ranking Error | 1 |
| q_ed50acaeaaf6c550 | What is another term for nearsightedness? | sciq | Semantic Miss | 0 |
| q_13de8def3414fdcb | does playing tennis burn calories | ms_marco | Ranking Error | 1 |
| q_73d63639dff68723 | average cost of one physical therapy visit | ms_marco | Ranking Error | 1 |
| q_42dc7411a117204e | what is amqp mqtt | ms_marco | Ranking Error | 1 |
| q_40ae548239df470b | what is biphasic action potential | ms_marco | Ranking Error | 1 |
| q_1cfbf87093f87743 | who sings the song goodnight irene | ms_marco | Ranking Error | 1 |
| q_cc2cb241833f361c | average salary rugby player | ms_marco | Ranking Error | 1 |
| q_c04b87212ce033b4 | reasons why fossil fuels are bad | ms_marco | Ranking Error | 1 |
| q_87cc4d7e5310fc36 | what are the parathyroid hormones | ms_marco | Ranking Error | 1 |
| q_97857b24933794b8 | what age do babies get teeth | ms_marco | Ranking Error | 1 |
| q_bf482b620e037e52 | how much money does the accuplacer companies make | ms_marco | Ranking Error | 1 |
| q_9cda08b0670f678a | what is an amide | ms_marco | Semantic Miss | 0 |
| q_29499089844960d6 | what is chicken wire | ms_marco | Ranking Error | 1 |
| q_6a397480f934f4ba | what is considered a seizure of person under the fourth amendment | ms_marco | Ranking Error | 1 |
| q_9a6d1aa58c50ccf7 | salary costs to employer | ms_marco | Ranking Error | 1 |
| q_e0c80e8e6c8dfe67 | which choice is an example of ethnicity | ms_marco | Ranking Error | 1 |
| q_c3dd1d76bb8f283b | what is a chard in drugs | ms_marco | Ranking Error | 1 |
| q_036ae064e2d6c3f6 | what causes abscess | ms_marco | Ranking Error | 1 |
| q_acc61d4696d1a095 | are drew and jonathan scott twins | ms_marco | Ranking Error | 1 |
| q_1acc7dcf7ec150f5 | is net interest expense the same as interest payments | ms_marco | Ranking Error | 1 |
| q_e9bdbed6827dbaa7 | who is the actress that plays beckett on castle | ms_marco | Ranking Error | 1 |
| q_adb26b07c67e42e9 | how to cook swordfish in a pan | ms_marco | Ranking Error | 1 |
| q_26a28bf68267a0b4 | What happens to old oceanic crust at convergent boundaries? | sciq | Semantic Miss | 0 |
| q_4c50c2f3f2018cf8 | how much does it cost to run an electric pool heater | ms_marco | Ranking Error | 1 |
| q_ffbcfc6dee3d6b23 | do angiosperms have spores | ms_marco | Ranking Error | 1 |
| q_20a4e39476a50fb2 | how long until the nfl draft | ms_marco | Ranking Error | 1 |
| q_21dbc7319753b567 | what are the chances of rheumatoid arthritis if anti CCP is positive | ms_marco | Ranking Error | 1 |
| q_749ba61b89a297cf | what is acceptance contract law | ms_marco | Ranking Error | 1 |
| q_388c5cacd0c8d899 | What entity owns V/Line? | squad | Semantic Miss | 0 |
| q_f6193b9093a4bf0f | average np salary in texas | ms_marco | Semantic Miss | 0 |
| q_f4eca4af46b8f2b8 | describe the plants and animals found in the desert biome | ms_marco | Semantic Miss | 0 |
| q_4fadc6d727100f36 | biggest island in bahamas | ms_marco | Ranking Error | 1 |
| q_cef033f731ed2257 | define human geography | ms_marco | Ranking Error | 1 |
| q_601b146185d2d5e5 | is edta safe for everyone | ms_marco | Ranking Error | 1 |
| q_cb5ccc8f176ae1b9 | what region is ecuador in | ms_marco | Ranking Error | 1 |
| q_6e871ad1be921ffa | in a standard normal distribution the mean is | ms_marco | Ranking Error | 1 |
| q_abc268a12ee901ff | what is similar to cholera | ms_marco | Ranking Error | 1 |
| q_b01cf791cda219ea | what is oleoresin | ms_marco | Ranking Error | 1 |
| q_91b33ed743a3f6f5 | Up to what age do students in the United Kingdom attend preparatory schools? | squad | Semantic Miss | 0 |
| q_ed801bb9f31df15c | what color are split peas | ms_marco | Semantic Miss | 0 |
| q_1dbfc174ca6ffd93 | lsat score range | ms_marco | Ranking Error | 1 |
| q_51a76b1e966927ba | where is energy located in the atp molecule | ms_marco | Ranking Error | 1 |
| q_60c1b429022b0f48 | what is a gastritis | ms_marco | Ranking Error | 1 |
| q_b9d6a97ee4bccd71 | what is in garcinia cambogia | ms_marco | Ranking Error | 1 |
| q_90861fb62be23a98 | what is the average distance a baseball can be thrown | ms_marco | Ranking Error | 1 |
| q_d6a017bcd8fef936 | how much would it cost to move a manufactured home | ms_marco | Ranking Error | 1 |
| q_f38ed4cae0594ccc | what is a cheesecloth used for | ms_marco | Ranking Error | 1 |
| q_25f170e7285147b4 | average cost to replace shocks and struts | ms_marco | Ranking Error | 1 |
| q_fec97ab5974f58cf | name that means unique | ms_marco | Ranking Error | 1 |
| q_72bfcb69b6342047 | what is used motherboard | ms_marco | Semantic Miss | 0 |
| q_d3d1dd5673a778cd | what is sedan car means | ms_marco | Ranking Error | 1 |
| q_255ef9d012000c07 | what happens when add turps to oil paint | ms_marco | Ranking Error | 1 |
| q_bcce1bfcf98fb1e2 | how do you cook sweet potatoes in the microwave | ms_marco | Ranking Error | 1 |
| q_aefeaf47f68f1473 | Sedimentary rocks that are formed partially by animals and plants are called what? | ms_marco | Semantic Miss | 0 |
| q_fcb65bd8160cfde1 | how long to robins nest | ms_marco | Ranking Error | 1 |
| q_c708aa1cbe2e3429 | which branch of a spinal nerve is the widest in diameter | ms_marco | Ranking Error | 1 |
| q_32bbb237986becc4 | how long do bald eagles live | ms_marco | Ranking Error | 1 |
| q_22688140e12d995b | A kilocalorie of heat is required to raise the temperature of | ms_marco | Semantic Miss | 0 |
| q_650a7ada9fcf762b | what does leyla mean in turkish | ms_marco | Ranking Error | 1 |
| q_9ccaba1a1e6ef5b2 | what are the differences between a male and female pelvis | ms_marco | Ranking Error | 1 |
| q_0cc65de5cac86515 | what is anthrax | ms_marco | Ranking Error | 1 |
| q_9efdc3e559e1f274 | how much transmission fluid | ms_marco | Semantic Miss | 0 |
| q_bff96ea7e919907d | what is the sodium limit per day | ms_marco | Semantic Miss | 0 |
| q_ad36a1a8ebf64aec | what is wasting disease | ms_marco | Ranking Error | 1 |
| q_b35f89f071ca49c9 | how much money do NFL games bring in? | ms_marco | Ranking Error | 1 |
| q_fcce9e1aa9533449 | what is responsible for peristaltic waves | ms_marco | Ranking Error | 1 |
| q_a9fc61bd69cb04a5 | what is used for a coagulase test | ms_marco | Semantic Miss | 0 |
| q_465928cdbcb77626 | what is physiology mean | ms_marco | Ranking Error | 1 |
| q_eaa6d3051130a07a | what year did jamestown settle | ms_marco | Ranking Error | 1 |
| q_d2aa3dd43aa2a55d | what is the average cost for a martial arts studio lease | ms_marco | Ranking Error | 1 |
| q_d5546bbba994826b | what does mobo stand for computer | ms_marco | Ranking Error | 1 |
| q_be935c856c262e92 | ocwen mortgage phone number customer service | ms_marco | Semantic Miss | 0 |
| q_be55cae8fb3fae45 | el chapo net worth | ms_marco | Ranking Error | 1 |
| q_33ce761b15268686 | how did the missouri compromise affect massachusetts | ms_marco | Ranking Error | 1 |
| q_687c5bcbd8740a93 | As ph increases what happens to a solution? | sciq | Ranking Error | 1 |
| q_75834323b49369e4 | is bp stock a good investment | ms_marco | Ranking Error | 1 |
| q_ecaebd41df21957e | health benefits of liquid aminos | ms_marco | Ranking Error | 1 |
| q_79b956cffafcada7 | when and why was the berlin wall built | ms_marco | Ranking Error | 1 |
| q_a6dee4b2c85d6037 | what is pragmatism in philosophy | ms_marco | Ranking Error | 1 |
| q_8910188ee0942b20 | meaning name inayat | ms_marco | Ranking Error | 1 |
| q_6a65fa55266363bc | maximum earnings to contribute to roth ira | ms_marco | Semantic Miss | 0 |
| q_ae89c4fd62a5c7ab | what is midazolam versed | ms_marco | Ranking Error | 1 |
| q_d02c6f1628ecc4b6 | are satsuma mandarins seedless | ms_marco | Ranking Error | 1 |
| q_5e16dac0c72cb1ad | how much does cristiano ronaldo earn | ms_marco | Ranking Error | 1 |
| q_6e872ef0d8736068 | what causes an upper respiratory infection | ms_marco | Ranking Error | 1 |
| q_834bce3667cc7551 | best form of choline | ms_marco | Ranking Error | 1 |
| q_68c6bdc64aea6276 | The muscles of the anterior neck assist in deglutition also known as what? | sciq | Ranking Error | 1 |
| q_06ea80f07d3c84e1 | Update synopsis. | code_search_net | Semantic Miss | 0 |
| q_7fda723e3126a3a6 | what is a normal temperature | ms_marco | Ranking Error | 1 |
| q_05b96a48ac940aa1 | What type of electrons are attracted to the positive nucleus? | sciq | Semantic Miss | 0 |
| q_4dfeb38f3401b85a | cost of vinyl floor installation | ms_marco | Ranking Error | 1 |
| q_618c8343996901f2 | does tumbling work harden stainless steel | ms_marco | Ranking Error | 1 |
| q_be21403414555dc1 | how much does price chopper pay | ms_marco | Ranking Error | 1 |
| q_bf59ed32b32ce7a9 | average temperature in dhaka | ms_marco | Ranking Error | 1 |
| q_b5dcaa956309273d | what parts of the male reproductive system are affected by transmitted by gonorrhea | ms_marco | Ranking Error | 1 |
| q_b631eccb8d327746 | what's the average salary for a sous chef | ms_marco | Ranking Error | 1 |
| q_c87c3c7927d20598 | what is aldebaran made of | ms_marco | Ranking Error | 1 |
| q_4c8b37ba19e88a36 | is peat moss considered a mineral | ms_marco | Ranking Error | 1 |
| q_53614a6f8c7cd770 | where is sang nila utama from | ms_marco | Ranking Error | 1 |
| q_8b1ab05eada574dc | where is blood coming from when it goes into the aorta | ms_marco | Ranking Error | 1 |
| q_1af79d24dffd2083 | what are kidney stone made of | ms_marco | Semantic Miss | 0 |
| q_97ac003deef8371b | what is a quatrain poem | ms_marco | Ranking Error | 1 |
| q_2b4fc02bc863167a | what is corporate communication in business | ms_marco | Ranking Error | 1 |
| q_67a0ad854d3b8437 | what is the meaning of kaleem name | ms_marco | Ranking Error | 1 |
| q_f45be6938abec19f | what is meant by a company corporate culture | ms_marco | Ranking Error | 1 |
| q_9dc4f030c6492735 | how grams in an ounce | ms_marco | Ranking Error | 1 |
| q_2f5acae1149e2509 | what is twig | ms_marco | Ranking Error | 1 |
| q_2f30054c82c2bbfc | average length of nursing home stay | ms_marco | Semantic Miss | 0 |
| q_3ae36c19c949be91 | robert hooke invented the light microscope | ms_marco | Ranking Error | 1 |
| q_8866c50099df51ee | characteristics of blood vessels | ms_marco | Ranking Error | 1 |
| q_faaf55915261add3 | why am I getting popup are you a human | ms_marco | Ranking Error | 1 |
| q_81dc025e6fd8d9cc | what is glycolysis energy system | ms_marco | Ranking Error | 1 |
| q_27ffe0d0a832b9be | which branch of government is responsible for interpreting laws | ms_marco | Ranking Error | 1 |
| q_f172aed1b536e3fe | what is hijama or cupping | ms_marco | Ranking Error | 1 |
| q_10f04a2be3a85605 | What is the smallest geographical region discussed? | squad | Semantic Miss | 0 |
| q_49729814029fffc1 | how much does traffic cost the average person | ms_marco | Ranking Error | 1 |
| q_68c5890300e4fa83 | What are 3 types of light? | sciq | Semantic Miss | 0 |
| q_0b908c60ed10d5c0 | average umbrella company fee | ms_marco | Ranking Error | 1 |
| q_8fcad0df3be2cc0f | average cost wedding flowers | ms_marco | Ranking Error | 1 |
| q_5d898b1f778b51bb | how long does it take to hatch a chicken egg in an incubator | ms_marco | Ranking Error | 1 |
| q_1b02100739326a49 | are mb bigger than kb | ms_marco | Ranking Error | 1 |
| q_f1e365e3f610fde4 | how much does it cost to service a sump pump | ms_marco | Ranking Error | 1 |
| q_04a63d8bbec630a1 | what makes a halal chicken | ms_marco | Ranking Error | 1 |
| q_0ec8066be85c0f05 | what is papillary thyroid cancer | ms_marco | Ranking Error | 1 |
| q_decf76925f672e0e | what is a pothole | ms_marco | Semantic Miss | 0 |
| q_34b827119f100038 | The long tentacles on the pleurbrachia are protected by what? | squad | Semantic Miss | 0 |
| q_1c8e6f1bf28410c0 | bhavana name meaning | ms_marco | Ranking Error | 1 |
| q_bc7e989f067639f3 | what type of music did beethoven perform | ms_marco | Ranking Error | 1 |
| q_33febdb595095fad | how long to chill a fridge | ms_marco | Ranking Error | 1 |
| q_835aea820178202e | what is the code to type registered symbol | ms_marco | Ranking Error | 1 |
| q_9e6cddcc26616539 | cost for bricklayer | ms_marco | Ranking Error | 1 |
| q_90ab79422eeb08d0 | biological species consists of groups of | ms_marco | Ranking Error | 1 |
| q_ec3df8dd6755e6ae | what is another name for femur | ms_marco | Ranking Error | 1 |
| q_9eefb43a53eb56e9 | what is a cumulonimbus cloud? | ms_marco | Ranking Error | 1 |
| q_586dd8613d0219d2 | what did the emancipation proclamation do for the civil war | ms_marco | Ranking Error | 1 |
| q_d5cf4045047d671c | where is zadar in croatia | ms_marco | Ranking Error | 1 |
| q_70894c7ba8b1ce9f | what is disease when pancreas produces excessive insulin | ms_marco | Ranking Error | 1 |
| q_212a651f2a2e9096 | when you boiling water does it make it more acidic | ms_marco | Ranking Error | 1 |
| q_56e84af5ad62942e | what diseases is flagyl used for | ms_marco | Semantic Miss | 0 |
| q_349d2b5a13ffba74 | what is igneous rock definition | ms_marco | Ranking Error | 1 |
| q_1cc2a63b20e70865 | What happened to the SM upon reentry to the atmosphere? | squad | Semantic Miss | 0 |
| q_40df8abe1e3c3121 | how to calculate how many litres in my pool | ms_marco | Ranking Error | 1 |
| q_4cb8869e2d16ec8a | george strait i got a car | ms_marco | Ranking Error | 1 |
| q_d268f410d778d2ad | cause of erdheim-chester disease | ms_marco | Ranking Error | 1 |
| q_efb031fe30e78070 | who wrote the music for aladdin on broadway | ms_marco | Ranking Error | 1 |
| q_dcc3c2cc45f6f8b3 | What is the average cost of chiwawa puppies | ms_marco | Semantic Miss | 0 |
| q_21d48812629c3bf5 | What was the result of the 1967 referendum? | squad | Semantic Miss | 0 |
| q_f6ea8d2b6d4fbb08 | how long does type b influenza last | ms_marco | Ranking Error | 1 |
| q_f3aeb53585f59ed4 | where are the submandibular lymph nodes located | ms_marco | Ranking Error | 1 |
| q_f583299e834cc769 | can baby bunnies have strawberries | ms_marco | Ranking Error | 1 |
| q_9f0240f3dfa925f6 | what does the american pika do | ms_marco | Semantic Miss | 0 |
| q_ddd7cb00985083e2 | move windows file to linux share | ms_marco | Ranking Error | 1 |
| q_5c9d295726b6fc3f | what kind of food is good for depression | ms_marco | Ranking Error | 1 |
| q_66ec08f04bf6fc39 | different types of orchids and their names | ms_marco | Ranking Error | 1 |
| q_1a7bc4b8533b1e8f | replace cambelt cost | ms_marco | Ranking Error | 1 |
| q_4c4a59c8fbbbc2d5 | what are the different types of pancreatic enzymes | ms_marco | Ranking Error | 1 |
| q_b159caf7dc159c74 | What is the primary gas produced from burning of wood? | sciq | Semantic Miss | 0 |
| q_13a4ee9e5c2fcbd7 | where is maldon victoria | ms_marco | Ranking Error | 1 |
| q_671f22250807c188 | which type weather briefing should a pilot request | ms_marco | Ranking Error | 1 |
| q_9bf84e99d974fe4e | rheumatoid arthritis is it hereditary | ms_marco | Ranking Error | 1 |
| q_5e7ce0f5add6e0ad | what is boli used for | ms_marco | Ranking Error | 1 |
| q_44adfba961c07af3 | how tall is a wall | ms_marco | Ranking Error | 1 |
| q_b12f8f61eab648f2 | is pain normal a month after kyphoplasty | ms_marco | Ranking Error | 1 |
| q_2f2e9a806a66e641 | what is polyurethane used for | ms_marco | Ranking Error | 1 |
| q_088b884db3d7167c | how long can i be out of ontario and keep ohip | ms_marco | Ranking Error | 1 |
| q_f1e6b7f3ec7b3a4b | should you take your regular medications before a thyroid check | ms_marco | Ranking Error | 1 |
| q_1e0f927ec1e40733 | literary definition of petrarchan sonnet | ms_marco | Ranking Error | 1 |
| q_2838788e6b3e79da | cost for concrete | ms_marco | Ranking Error | 1 |
| q_1e283fab803e100f | what is rhino poaching definition | ms_marco | Ranking Error | 1 |
| q_040cf185a54cc105 | What does ctenophore mean in Greek? | squad | Semantic Miss | 0 |
| q_a9814e13eb13ee8f | hygienist cost | ms_marco | Ranking Error | 1 |
| q_1408140f800366c6 | is a combi suitable for a large four bed house | ms_marco | Ranking Error | 1 |
| q_b933ea918aad387d | what are the names of the varying kinds of maple trees | ms_marco | Ranking Error | 1 |
| q_6e24eb06ddd699a2 | will walking burn fat | ms_marco | Ranking Error | 1 |
| q_cc3c962a92ee6abb | safe internal temperature for prime rib | ms_marco | Ranking Error | 1 |
| q_d59baf5e453d17da | why is knee numb from shingles | ms_marco | Ranking Error | 1 |
| q_ae4a84acd2103a52 | cost to advertise a company | ms_marco | Ranking Error | 1 |
| q_d84364b99571f159 | what is a brain lesion | ms_marco | Ranking Error | 1 |
| q_8dd34b7a856ef07f | what is the cost for ivf treatment | ms_marco | Ranking Error | 1 |
| q_7b7d86c375397ba6 | what does geometric mean minimize | ms_marco | Ranking Error | 1 |
| q_88b453360e63dc93 | full tuition cost uh | ms_marco | Ranking Error | 1 |
| q_df09840307eb7918 | Ectotherms undergo a variety of changes at the cellular level to acclimatize to shifts in what? | sciq | Semantic Miss | 0 |
| q_0c7d43733ba08560 | how long does it take to grill chicken | ms_marco | Ranking Error | 1 |
| q_8b550b9ff1bfe846 | what is the purpose of PCR | ms_marco | Ranking Error | 1 |
| q_6408c87582b7d838 | In the article's title, what did the machine hope to end? | squad | Semantic Miss | 0 |
| q_ee92a39afd6b852c | who sings downtown with macklemore | ms_marco | Ranking Error | 1 |
| q_f17638a719bae6b2 | who is david dukes kkk | ms_marco | Ranking Error | 1 |
| q_7642d3ac69795c2c | what does hashem mean in arabic | ms_marco | Ranking Error | 1 |
| q_237a3314f01e8d27 | do female bison reject a newborn bison calf | ms_marco | Ranking Error | 1 |
| q_edf647f93ccf9630 | do tenancy agreements need to be stamped | ms_marco | Semantic Miss | 0 |
| q_55994e8d1837c63c | What is the limiting factor for bacteria in a dish? | sciq | Semantic Miss | 0 |
| q_8cba1b2a55f24a9f | garage door spring replacement cost | ms_marco | Ranking Error | 1 |
| q_94eeb56979e45ec2 | is serrapeptase enzyme a salicylate | ms_marco | Ranking Error | 1 |
| q_e6d72b06079af895 | what education do you need to become a genetic counselor | ms_marco | Ranking Error | 1 |
| q_bf069d69e0d9519d | does smell based memory affect the thalamus? | ms_marco | Ranking Error | 1 |
| q_2bb6de98a70620c8 | what kind of bank is usaa | ms_marco | Ranking Error | 1 |
| q_1153253113567743 | how long does it take for a scab mark to disappear | ms_marco | Semantic Miss | 0 |
| q_58cc8056089ab238 | how much does an rn make in florida | ms_marco | Ranking Error | 1 |
| q_513d53f1af83882e | cerebral oedema definition | ms_marco | Ranking Error | 1 |
| q_b9ceab3a4be09930 | primary secondary and tertiary sectors definition | ms_marco | Ranking Error | 1 |
| q_3c36f7ec45512505 | What are the molecular inputs for photosynthesis? | squad | Semantic Miss | 0 |
| q_9a7acce973ded962 | what was the major issue of newly formed republican party | ms_marco | Ranking Error | 1 |
| q_b78099d5fcb932c6 | how big should should my ceiling fan be | ms_marco | Ranking Error | 1 |
| q_6a23a710cd66ec4a | does heartwood contain extractives | ms_marco | Ranking Error | 1 |
| q_a835829d2e7d7b6c | what is a virginia dmv control number | ms_marco | Ranking Error | 1 |
| q_6d4ad1b7bcec6c84 | when were terracotta warriors found | ms_marco | Ranking Error | 1 |
| q_fe0b3b3f311eb262 | why does a protein have a great potential for variation of structure | ms_marco | Ranking Error | 1 |
| q_b5b241c14bac2838 | best temperature for fridge | ms_marco | Ranking Error | 1 |
| q_9dc1f794dcda9320 | what is the rural urban fringe | ms_marco | Ranking Error | 1 |
| q_2b5a97332dfc68ce | how to oven roast brussel sprouts | ms_marco | Ranking Error | 1 |
| q_1b6adec2632f59bd | what is meant by clogging | ms_marco | Ranking Error | 1 |
| q_32dd2d6e49d9e3a0 | ms is actually lyme disease | ms_marco | Semantic Miss | 0 |
| q_174d448975b4aa81 | taste and simplicity of nutrients and ingredients used in italian cuisine | ms_marco | Semantic Miss | 0 |
| q_53a9d29cc3af8e5d | Evaporation of water from plant leaves is called ________. | ms_marco | Semantic Miss | 0 |
| q_d6db19bcd0bcc39f | collection of hyphae is known as | ms_marco | Semantic Miss | 0 |
| q_ad69a115ab008220 | english pronunciation of irish name eamonn | ms_marco | Ranking Error | 1 |
| q_6f0b7854ffa8392f | does dna repair itself | ms_marco | Ranking Error | 1 |
| q_ac503f792382e7d1 | annuit coeptis why eye does it mean | ms_marco | Ranking Error | 1 |
| q_1053fc756f6b97be | what is meant by business logic in java | ms_marco | Ranking Error | 1 |
| q_b557c8d6c6ac161f | what are medium chain plant fats | ms_marco | Ranking Error | 1 |
| q_1609adb24b7b4a73 | how much do coffered ceilings cost | ms_marco | Ranking Error | 1 |
| q_cb98e931715b2b66 | is calcitonin bad | ms_marco | Ranking Error | 1 |
| q_b12cb4eb7acba639 | is ethanol an element or compound | ms_marco | Ranking Error | 1 |
| q_8a5753772825ab8f | what animal is uniqua from backyardigans | ms_marco | Semantic Miss | 0 |
| q_7a5736341420091c | how big of a reservoir do i need water cooling | ms_marco | Ranking Error | 1 |
| q_7b81d437899ab7ae | where is the leaning tower of pisa located in italy | ms_marco | Ranking Error | 1 |
| q_4bcb3e743fca7cfa | what is accounting cost in economics | ms_marco | Ranking Error | 1 |
| q_f8af973692951043 | how much does a credit hour cost at tcc | ms_marco | Ranking Error | 1 |
| q_fab366a2193ef9f7 | internal cooking temperature for medium prime rib roast | ms_marco | Ranking Error | 1 |
| q_bdac89d39f1fa479 | how to predict lottery numbers mathematically | ms_marco | Semantic Miss | 0 |
| q_cc146828a7ae508b | what is scarlatina | ms_marco | Ranking Error | 1 |
| q_4a8708ad1e721a68 | what size is the human eye | ms_marco | Ranking Error | 1 |
| q_ccd746cf4f61a421 | what does the muscular system do | ms_marco | Ranking Error | 1 |
| q_7f140ab2d9125c33 | who is the director of ncis | ms_marco | Ranking Error | 1 |
| q_20772e2c7c9ff453 | can ipads be used as a laptop | ms_marco | Ranking Error | 1 |
| q_3e920d8807110dc3 | where is mittagong rsl | ms_marco | Ranking Error | 1 |
| q_9381cff8b3ccd2c9 | can i contribute both roth ira and traditional ira | ms_marco | Ranking Error | 1 |
| q_90a74107b19bf060 | what is jittery | ms_marco | Ranking Error | 1 |
| q_34d43179d1928ff8 | cost of disability related obesity on nhs | ms_marco | Ranking Error | 1 |
| q_ed1ffcd8475c801e | what does geomorphic | ms_marco | Ranking Error | 1 |
| q_a1ff3e7e134e2d4a | how neurons communicate for dummies | ms_marco | Semantic Miss | 0 |
| q_9ec33da639ae905a | what is arduino written in | ms_marco | Ranking Error | 1 |
| q_bc5b7618befec9aa | autosomal recessive polycystic kidney disease | ms_marco | Ranking Error | 1 |
| q_a8107ed2cb7d41e9 | who created the first ever motion picture | ms_marco | Ranking Error | 1 |
| q_190bf59a793ef9f5 | what does annealing mean | ms_marco | Semantic Miss | 0 |
| q_9199add4bf9ca5bf | average private school tuition | ms_marco | Ranking Error | 1 |
| q_26029086a75276ab | who was louis xvi | ms_marco | Ranking Error | 1 |
| q_9fc7e6a70aa7bf0a | temp rating for pvc | ms_marco | Ranking Error | 1 |
| q_8bbc8027264b75c5 | what type of mackerel does supermarkets sell | ms_marco | Ranking Error | 1 |
| q_b13f28d9c3927329 | what is descriptive paragraph | ms_marco | Ranking Error | 1 |
| q_cd05353565e0c051 | what is evaporative cooling | ms_marco | Ranking Error | 1 |
| q_0b1445c4cc57c520 | inflamed muscles symptoms | ms_marco | Ranking Error | 1 |
| q_b3c438bd4963627a | how long to defrost meat in a refrigerator | ms_marco | Semantic Miss | 0 |
| q_406bea50de6fd92d | what kind of name is kilik | ms_marco | Ranking Error | 1 |
| q_6c927ced6134e286 | when was roberto clemente born and died | ms_marco | Semantic Miss | 0 |
| q_c50e88fe14217a12 | what is the chemical formula for emerald and what is it used for | ms_marco | Ranking Error | 1 |
| q_6943d3b35915b611 | what is chupacabra | ms_marco | Ranking Error | 1 |
| q_4fd341392d204dfd | difference between rheumatoid arthritis and lupus | ms_marco | Ranking Error | 1 |
| q_724fe80aa4f3234b | what are the physical properties of minerals | ms_marco | Ranking Error | 1 |
| q_1846c3deed2e3f89 | what is the function of cranial nerve x | ms_marco | Semantic Miss | 0 |
| q_0ac432ff10b44af6 | is lima dangerous | ms_marco | Ranking Error | 1 |
| q_6b303683ca1c19e7 | part time best buy salary | ms_marco | Ranking Error | 1 |
| q_7cf226cf4e6b344c | what helps maintain homeostasis | ms_marco | Ranking Error | 1 |
| q_5cf515ea87130034 | does pepsin digest protein | ms_marco | Ranking Error | 1 |
| q_ef57564ad7a95530 | what is a gold level ncrc | ms_marco | Ranking Error | 1 |
| q_656d40e98edf8faf | where are hormones produced | ms_marco | Ranking Error | 1 |
| q_3766b0aa33af4243 | meaning of name myah | ms_marco | Ranking Error | 1 |
| q_4cd443e052044d4d | what is an example of discretionary fixed cost | ms_marco | Ranking Error | 1 |
| q_9f5b6f02a564151f | What kind of state was the Khwarezmia? | squad | Ranking Error | 1 |
| q_b84f4e6bfc480091 | osteoporosis what does it mean | ms_marco | Ranking Error | 1 |
| q_68e3febb7437c95e | how long to cook chuck roast in the oven | ms_marco | Ranking Error | 1 |
| q_cfce568444f846af | What was extent of Celeron's expedition? | squad | Semantic Miss | 0 |
| q_cfe51a62e0dc2827 | what is ethernet over ip | ms_marco | Ranking Error | 1 |
| q_59e29a96aae33b86 | how fast do elephants run | ms_marco | Ranking Error | 1 |
| q_03698d8b11a2175e | calcium contain food list | ms_marco | Ranking Error | 1 |
| q_94866f1a9fd35e18 | what is meant by the word - notwithstanding | ms_marco | Ranking Error | 1 |
| q_a33d1da9e3be9bb7 | roman name definition | ms_marco | Ranking Error | 1 |
| q_837dfb4e6017c3dc | antigone was the third play written by | ms_marco | Ranking Error | 1 |
| q_a86c9f9b8126a4e9 | nose surgery average cost canada | ms_marco | Ranking Error | 1 |
| q_f9709315dc3df2f5 | food groups and what they do for your body | ms_marco | Ranking Error | 1 |
| q_7d9eeeed315a53d9 | when you unfollow someone on facebook do they see your posts | ms_marco | Ranking Error | 1 |
| q_716c43650b9fba01 | pharmacist salary in oregon | ms_marco | Ranking Error | 1 |
| q_48dec5f40de5633b | what is a single bond | ms_marco | Ranking Error | 1 |
| q_f90a13d4fe45cb65 | What is the full name of the ASER? | squad | Semantic Miss | 0 |
| q_c002d05ae103079a | what types of food are digested in the stomach first | ms_marco | Ranking Error | 1 |
| q_602ba3d79d397c34 | average starting salary for preschool teacher | ms_marco | Ranking Error | 1 |
| q_a4dc8c20cb8a0ce6 | what is the meaning of lily | ms_marco | Ranking Error | 1 |
| q_098dbc9722f08dec | what region is the creuse in | ms_marco | Ranking Error | 1 |
| q_82a77533aea6ff48 | how long do you cook noodles | ms_marco | Ranking Error | 1 |
| q_d590f529afbd71a5 | ideal body temperature for humans | ms_marco | Ranking Error | 1 |
| q_4a2a22a91650604c | symptoms of diseases from ticks | ms_marco | Ranking Error | 1 |
| q_ef2879655d1911ed | how to fix a leaky bathtub faucet | ms_marco | Ranking Error | 1 |
| q_4e391448f47bdf21 | what does minimum salary requirement mean | ms_marco | Ranking Error | 1 |
| q_3d53ff1139d3d703 | which was a republican response to the sedition act | ms_marco | Semantic Miss | 0 |
| q_6205f2a63675d3af | what is a clinical study | ms_marco | Ranking Error | 1 |
| q_528f0209457f0d50 | antagonist muscle definition | ms_marco | Ranking Error | 1 |
| q_11d9a40b771ff98a | what is phonetic symbolism | ms_marco | Ranking Error | 1 |
| q_b623a721478389cb | color of urine and meaning | ms_marco | Ranking Error | 1 |
| q_540b778a21d4384e | Colonial rule in African nations did all of the following, except | ms_marco | Ranking Error | 1 |
| q_84c4c30e96b8f88b | habitat fragmentation meaning | ms_marco | Ranking Error | 1 |
| q_bcbe64c45eec9668 | what anemone do clownfish host | ms_marco | Ranking Error | 1 |
| q_21df70e143db906a | What does  mnemiopsis eat? | squad | Semantic Miss | 0 |
| q_4671bf771a9cc70f | celebrities who have or had cancer | ms_marco | Ranking Error | 1 |
| q_bc6bd0755dd9b876 | how much deposit do you pay on exchange | ms_marco | Ranking Error | 1 |
| q_cb1c969e85be8de5 | who benefited from the mercantilist system | ms_marco | Semantic Miss | 0 |
| q_7597adee8da58664 | how much do puppy shots cost at the vet | ms_marco | Ranking Error | 1 |
| q_bb8c0a1be414fa1a | what is the meaning of claymore | ms_marco | Ranking Error | 1 |
| q_a4e631a70c2c734e | what is trait | ms_marco | Ranking Error | 1 |
| q_094cc64eacf78239 | average radon levels in homes | ms_marco | Ranking Error | 1 |
| q_7d8533c140401b11 | what are healing stones used for | ms_marco | Ranking Error | 1 |
| q_23dbe14595b0228f | who was joseph smith | ms_marco | Ranking Error | 1 |
| q_8685dcdbea682301 | What is an underbid? | squad | Semantic Miss | 0 |
| q_0483c786af96c17d | what is greta van susteren salary | ms_marco | Ranking Error | 1 |
| q_984dbdf4342153a5 | how old do bears live to be? | ms_marco | Ranking Error | 1 |
| q_16eb4b8b6001baf6 | what does the planets aligning mean | ms_marco | Ranking Error | 1 |
| q_ea6c3970b3c080f4 | what are the triceps brachii | ms_marco | Ranking Error | 1 |
| q_251a9ca0e7e7df97 | nalbuphine dosage | ms_marco | Ranking Error | 1 |
| q_eef3893c845d62f8 | pancreas is an organ that regulate blood glucose levels | ms_marco | Ranking Error | 1 |
| q_25f277655ad9a579 | what enzymes and proteins are needed for transcription | ms_marco | Ranking Error | 1 |
| q_d1f37835c722292a | how long does a sunburn take to heal | ms_marco | Ranking Error | 1 |
| q_012cc26fa28c3499 | how much of fare to uber drivers get | ms_marco | Ranking Error | 1 |
| q_09f3156952f0fd8e | on average how often is someone online a day | ms_marco | Ranking Error | 1 |
| q_e8fc14abaad0a2e2 | cost of ntuc membership renewal | ms_marco | Ranking Error | 1 |
| q_5eaeca56baa1a07d | What radio network carried the Super Bowl? | squad | Semantic Miss | 0 |
| q_b7985c99968d703d | what is the function of mitochondria | ms_marco | Ranking Error | 1 |
| q_a561923b93916852 | what flooring to use on uneven floor | ms_marco | Semantic Miss | 0 |
| q_7b61caf19a827715 | what is patent leather made from | ms_marco | Semantic Miss | 0 |
| q_9d663a66dfa1af9e | where is matadi | ms_marco | Ranking Error | 1 |
| q_5505565c2ab6c26c | What do angiosperms produce? | sciq | Semantic Miss | 0 |
| q_c85cf9589a85b39d | what is FSH blood test | ms_marco | Ranking Error | 1 |
| q_041b9f66c95d37f3 | what is symptoms of pneumonia | ms_marco | Ranking Error | 1 |
| q_eee02f2da85a55e0 | what type of lake is lake victoria | ms_marco | Ranking Error | 1 |
| q_bb73757da4612831 | calories in a jumbo egg | ms_marco | Ranking Error | 1 |
| q_d9fb97145e3896ea | how long do you bake chicken legs and thighs in the oven | ms_marco | Ranking Error | 1 |
| q_da0f07a4e8bcbb36 | what was the third reich | ms_marco | Ranking Error | 1 |
| q_641bfd99be9c4bca | What is an Aft Cabin | ms_marco | Ranking Error | 1 |
| q_98c0057d787ec06b | What is another word for cryptophytes? | squad | Semantic Miss | 0 |
| q_72cc3bee4e385eae | how long can chicken be kept in refrigerator | ms_marco | Ranking Error | 1 |
| q_a0bc67bdf87fc3a3 | what are the symptoms of a broken hip | ms_marco | Ranking Error | 1 |
| q_5a97d5d96b0ff778 | what is iridium | ms_marco | Ranking Error | 1 |
| q_dcbabfa363e79f19 | how often should a treadmill be lubricated | ms_marco | Ranking Error | 1 |
| q_1bd578f3128a845e | how do shower pumps work | ms_marco | Ranking Error | 1 |
| q_513edc0b9fa9a95f | average cost of a doctor's visit | ms_marco | Ranking Error | 1 |
| q_2e761c464857384b | eiza name meaning | ms_marco | Semantic Miss | 0 |
| q_612c3c651a8dc00e | what does algaecide do | ms_marco | Ranking Error | 1 |
| q_45fc2f20a3918b14 | Subscribe to device status messages

        # Parameters
        typeId (string): typeId for the subscription, optional.  Defaults to all device types (MQTT `+` wildcard)
        deviceId (string): deviceId for the subscription, optional.  Defaults to all devices (MQTT `+` wildcard)

        # Returns
        int: If the subscription was successful then the return Message ID (mid) for the subscribe request
            will be returned. The mid value can be used to track the subscribe request by checking against
            the mid argument if you register a subscriptionCallback method.
            If the subscription fails then the return value will be `0` | code_search_net | Ranking Error | 1 |
| q_38ed5c84321615e4 | how much of personality is genetic | ms_marco | Ranking Error | 1 |
| q_449f32e04ef945f6 | stages of a sea turtle's life | ms_marco | Ranking Error | 1 |
| q_bb6f83a1b9b3c3e4 | what is basal cell and squamous cell carcinomas treatment | ms_marco | Ranking Error | 1 |
| q_1d17c4f207860f85 | how much does an associates degree in dental hygiene cost | ms_marco | Ranking Error | 1 |
| q_ef5eb08052b6a41a | how to become a cna in alabama | ms_marco | Ranking Error | 1 |
| q_9e9adab0e31aede6 | where does the diaphragm attach to the medial lumber segment | ms_marco | Ranking Error | 1 |
| q_90081b113952cc8c | how much is chiropractic care | ms_marco | Ranking Error | 1 |
| q_7f3269900701df43 | what do the capillaries around the air sacs do | ms_marco | Ranking Error | 1 |
| q_00e742abb2bb9053 | what does fpo membrane | ms_marco | Ranking Error | 1 |
| q_36f1987e95195110 | What is another name for the Tabula Rogeriana? | squad | Semantic Miss | 0 |
| q_dce0155bb5907900 | estimate concrete patio cost | ms_marco | Ranking Error | 1 |
| q_408501c4995b2f86 | what is pleiotropy conditions | ms_marco | Ranking Error | 1 |
| q_17521f27831f69e8 | geographical definition of isthmus | ms_marco | Semantic Miss | 0 |
| q_91bb9d4bddc0cc3f | what did congress do to organize the northwest territory | ms_marco | Ranking Error | 1 |
| q_843260c1607f197d | how long to cook a mini apple pie | ms_marco | Ranking Error | 1 |
| q_d01c0d196084f9b5 | are peace lilies poisonous if eaten | ms_marco | Ranking Error | 1 |
| q_fa3a2b52b6f2776e | proclamation definition legal | ms_marco | Ranking Error | 1 |
| q_3409b3cbb8102a17 | how thick does a concrete footing need to be | ms_marco | Ranking Error | 1 |
| q_9ae15ab3970d8d98 | roth eligibility requirements | ms_marco | Ranking Error | 1 |
| q_1127048150399d79 | what is the difference between lantus and levemir | ms_marco | Ranking Error | 1 |
| q_f45b8bef949b7c35 | neural layer of retina definition | ms_marco | Ranking Error | 1 |
| q_252045757e910250 | what should freezer temperature be set at | ms_marco | Ranking Error | 1 |
| q_741fe12f659ef141 | how much does it cost to get your passport expedited | ms_marco | Ranking Error | 1 |
| q_8cd4c54c7e154437 | what lab shows active hepatitis a | ms_marco | Ranking Error | 1 |
| q_2e9e7a08b4fb7a33 | what are the types of symbiosis | ms_marco | Ranking Error | 1 |
| q_31c0bc25ef977f35 | average cost for textbooks in college | ms_marco | Ranking Error | 1 |
| q_a5efb06d0d7e6ffe | why should drinking age be lowered | ms_marco | Semantic Miss | 0 |
| q_42dc132eba3a0a8b | is two thirds equivalent to four sixths | ms_marco | Ranking Error | 1 |
| q_66c207e034878d87 | what are the two main functions of the skeletal system | ms_marco | Ranking Error | 1 |
| q_c3c3357566339971 | what do the carvings on a totem pole mean | ms_marco | Ranking Error | 1 |
| q_d493ea6646a600f5 | biogas cost per kwh | ms_marco | Ranking Error | 1 |
| q_a03f912f3ac18f00 | chicago il population | ms_marco | Ranking Error | 1 |
| q_67b44f372808c210 | where do wolves come from | ms_marco | Semantic Miss | 0 |
| q_c6fddf843c15b2f2 | when was the new model army formed | ms_marco | Ranking Error | 1 |
| q_37d2d81d3014e95a | when did falun gong start | ms_marco | Ranking Error | 1 |
| q_f7a380a85d9ccfb6 | average cost per hospital day | ms_marco | Ranking Error | 1 |
| q_dc134daf66d81b23 | ordinal level of measurement definition statistics | ms_marco | Ranking Error | 1 |
| q_4230bebbf292341a | what is ashwagandha herb good for | ms_marco | Ranking Error | 1 |
| q_4cf2826d23a597e6 | TODO | code_search_net | Semantic Miss | 0 |
| q_40510f441761eef4 | how long to hard boil small eggs | ms_marco | Ranking Error | 1 |
| q_cce4a89dd0eb6758 | What were the "great Forces" mentioned in the article's title? | squad | Semantic Miss | 0 |
| q_79b254e72b00bc51 | angelo definition name | ms_marco | Ranking Error | 1 |
| q_79506dc75fa58d15 | How much is platinum? | ms_marco | Ranking Error | 1 |
| q_d4e0ede0459266b2 | rhetorical term definition | ms_marco | Ranking Error | 1 |
| q_28cdb35cc22f7d9e | how much to charge for dog sitting overnight | ms_marco | Semantic Miss | 0 |
| q_99f093229c6e23fe | how much is a sunpass | ms_marco | Ranking Error | 1 |
| q_1c4b8094b23ad28a | how much tax deducted from salary | ms_marco | Ranking Error | 1 |
| q_75a1f35f3bb99893 | how to search database in asp.net | ms_marco | Ranking Error | 1 |
| q_d9fda487fc87e128 | grilling thick pork chops temperature | ms_marco | Ranking Error | 1 |
| q_3045a8f241d7336d | muscle disorders are often evaluated by | ms_marco | Semantic Miss | 0 |
| q_ba20487d44b452a3 | what is scrying | ms_marco | Ranking Error | 1 |
| q_1ffb5f605938049d | What is the method of reproduction for echinoderms? | sciq | Semantic Miss | 0 |
| q_d2e4a1abc1446266 | how far apart should a woman period be | ms_marco | Ranking Error | 1 |
| q_c33e8c5369af1b45 | meaning of name takaki | ms_marco | Ranking Error | 1 |
| q_6acae85182280e87 | how long can you keep lentils in the fridge for | ms_marco | Ranking Error | 1 |
| q_b36db8e92ac2b90b | when was houston founded | ms_marco | Ranking Error | 1 |
| q_35162f14e2741f03 | What type of fertilization do most reptiles use to reproduce? | sciq | Semantic Miss | 0 |
| q_121315a57342d4b8 | telephone prefix for columbus kansas | ms_marco | Ranking Error | 1 |
| q_bef88b0d8dfdc903 | do snakes get ticks? | ms_marco | Ranking Error | 1 |
| q_101f8e5b61989f1c | How large are Cytoplasmic ribosomes? | squad | Semantic Miss | 0 |
| q_ba4a2d38404ca451 | what is the structure of a multipolar neuron | ms_marco | Ranking Error | 1 |
| q_bce3486f022535d0 | HR officer average salary | ms_marco | Semantic Miss | 0 |
| q_f25c8a90c1968927 | average anesthesiologist salary | ms_marco | Ranking Error | 1 |
| q_93bbf48711e4a504 | A forced trade agreement between two countries would be an example of what? | squad | Ranking Error | 1 |
| q_1dc80c3f3599c69d | how often should i get a mammogram | ms_marco | Ranking Error | 1 |
| q_b5e478c46794378b | how long can a baby snapping turtle stay underwater | ms_marco | Ranking Error | 1 |
| q_4cf2be8651416992 | what is chora dal | ms_marco | Ranking Error | 1 |
| q_bd122e9423712606 | modularity definition psychology | ms_marco | Ranking Error | 1 |
| q_76ab57401beb3a65 | is advair a corticosteroid | ms_marco | Ranking Error | 1 |
| q_b9cd6dfa1c4ebdcf | is safflower oil safe | ms_marco | Ranking Error | 1 |
| q_f978a31d46f854a1 | three types of blood in human body | ms_marco | Ranking Error | 1 |
| q_2d0c04a4e76e6324 | what does vato mean | ms_marco | Ranking Error | 1 |
| q_2054eb6aca813b67 | most carbon monoxide is produced by | ms_marco | Ranking Error | 1 |
| q_797bd31049ea082a | where is carmignano | ms_marco | Ranking Error | 1 |
| q_e6cbb08c56f91251 | how far is 4 miles in km | ms_marco | Ranking Error | 1 |
| q_aad53404c2325638 | what is seid | ms_marco | Ranking Error | 1 |
| q_13df3aea4503e888 | convert dollar pay into salary to twice a month | ms_marco | Ranking Error | 1 |
| q_150a17a14e2e86f1 | what does tadasana mean | ms_marco | Ranking Error | 1 |
| q_8ddedabc2a1f98ff | titular meaning | ms_marco | Semantic Miss | 0 |
| q_700920136b43c28c | what class of lever is a baseball bat | ms_marco | Ranking Error | 1 |
| q_686811266cace2dd | what is dexilant prescribed for | ms_marco | Ranking Error | 1 |
| q_fc2b81cd2011582f | what is a levo drip | ms_marco | Semantic Miss | 0 |
| q_a2fae8af032bca26 | Australia is home to many endemic species. the (a) wallaby (wallabia bicolor), a medium-sized member of the kangaroo family, is a pouched mammal, or this? | sciq | Semantic Miss | 0 |
| q_2ce9d7b38f1e37f6 | what is dmt | ms_marco | Ranking Error | 1 |
| q_8ac241449f02c3ea | what is the land area of beijing china | ms_marco | Ranking Error | 1 |
| q_485e06e881a12390 | what is the difference in a regular minor and a harmonic minor in music | ms_marco | Semantic Miss | 0 |
| q_82ee3da83b25ca91 | what is room temperature in celsius | ms_marco | Ranking Error | 1 |
| q_298da442d0157214 | rampersaud surname origin | ms_marco | Ranking Error | 1 |
| q_4a28e35925b84cd4 | what carbon used for | ms_marco | Ranking Error | 1 |
| q_eda19a04c153b424 | is foam microwavable | ms_marco | Ranking Error | 1 |
| q_97e127a3d4cd1382 | how long is a parvo vaccine good for | ms_marco | Ranking Error | 1 |
| q_48744469dad92fc1 | what is the meaning of grapevine | ms_marco | Ranking Error | 1 |
| q_31fb2ca3f1f9ab91 | what causes the gyres in each ocean basin to be circular | ms_marco | Ranking Error | 1 |
| q_4cfd0f2369d9b8a4 | what did the yellow river do for china | ms_marco | Ranking Error | 1 |
| q_f02dda1356a0ef3b | what distinguish an algorithm from a method | ms_marco | Ranking Error | 1 |
| q_226cbc59d5507e0e | . | code_search_net | Semantic Miss | 0 |
| q_1802463299fe3498 | what is good in chestnuts | ms_marco | Ranking Error | 1 |
| q_268c2afc32bedfc0 | who is the drummer in metallica | ms_marco | Semantic Miss | 0 |
| q_4572e845cc0ad134 | average cost of child braces | ms_marco | Semantic Miss | 0 |
| q_78bd6d28992d6d6e | what temperature is medium rare prime rib | ms_marco | Ranking Error | 1 |
| q_d5f3e2c48e25f025 | What was the final score for Super Bowl XXXIII? | squad | Ranking Error | 1 |
| q_55410632eb16c278 | average calories per day female | ms_marco | Semantic Miss | 0 |
| q_c31078314da315c9 | what is hopsack material | ms_marco | Ranking Error | 1 |
| q_aaa823af5d589b43 | how long do you have to be working at a job to get maternity leave | ms_marco | Ranking Error | 1 |
| q_bc861f7993de7f60 | does the luteal phase ever change | ms_marco | Ranking Error | 1 |
| q_fefa2b31ff6526a0 | what does sateen weave mean | ms_marco | Ranking Error | 1 |
| q_ae2738345e337782 | how to keep hard boiled eggs from cracking during boiling | ms_marco | Ranking Error | 1 |
| q_12815c919479e42e | buddhist stupa symbolism | ms_marco | Ranking Error | 1 |
| q_30c0f57a66e4f99e | average cost to install carpet | ms_marco | Semantic Miss | 0 |
| q_a9d34cf1f8c724ff | average price for a swimming pool | ms_marco | Ranking Error | 1 |
| q_0a3eb668478189a7 | average salary for clerk of works | ms_marco | Ranking Error | 1 |
| q_ecefe08c8f0632ff | how fast does a jetliner go | ms_marco | Ranking Error | 1 |
| q_6bc5e12f2234f520 | how to stop facial hair from growing back so fast | ms_marco | Ranking Error | 1 |
| q_b1e75d4f5bdf98c5 | what are the statistics of being a registered nurse | ms_marco | Semantic Miss | 0 |
| q_8e503e5ed783f10b | how many min per lbs to cook eye round roast in oven | ms_marco | Semantic Miss | 0 |
| q_9a3ae176cb4bfb47 | what does vagifem cure | ms_marco | Ranking Error | 1 |
| q_e77511a9c9fd24fc | how long to cook ham per pound | ms_marco | Ranking Error | 1 |
| q_c4567898aaf8c749 | is phenomena contagious | ms_marco | Semantic Miss | 0 |
| q_35301587c3989a03 | what is theramine | ms_marco | Ranking Error | 1 |
| q_c99f13227e6c9d37 | what is professional culture definition | ms_marco | Ranking Error | 1 |
| q_128583755aa852bb | what did the jay treaty do for the americans | ms_marco | Ranking Error | 1 |
| q_7eb87934f5d18827 | average cost for yard maintenance | ms_marco | Semantic Miss | 0 |
| q_42d98f4d196368e5 | what is becker's muscular dystrophy | ms_marco | Ranking Error | 1 |
| q_f6fb337af0f6fae5 | how long does alcohol affect your sleep | ms_marco | Ranking Error | 1 |
| q_c1c6f243f30c25e8 | meaning of name kartikeya | ms_marco | Ranking Error | 1 |
| q_834d039c5603a6c8 | average cost to build a bathroom | ms_marco | Ranking Error | 1 |
| q_b64530fea1902e3a | good sources of complex carbohydrates | ms_marco | Semantic Miss | 0 |
| q_382b66ff18c5bb43 | most common medical conditions for use of marijuana | ms_marco | Ranking Error | 1 |
| q_77f07bef6f66fb11 | what regulates calcium levels | ms_marco | Ranking Error | 1 |
| q_9a8d7992d83e56a9 | salary for insurance agent | ms_marco | Semantic Miss | 0 |
| q_2c7c675f5be10c5b | where are equilibrium receptors located | ms_marco | Ranking Error | 1 |
| q_ff83a81309be5489 | Epsom Salt to Water Ratio | ms_marco | Ranking Error | 1 |
| q_e9bdd94abf25601b | What is the supply of water to land or crops to help growth called? | sciq | Semantic Miss | 0 |
| q_774f366c68ac14ca | tia meaning | ms_marco | Ranking Error | 1 |
| q_48f4142f04dc749c | What are two ways cnidarians are able to reproduce? | sciq | Semantic Miss | 0 |
| q_06e08eb7578a8123 | what is sazon seasoning made of | ms_marco | Ranking Error | 1 |
| q_174f71a835278b4f | what is a premium? | ms_marco | Semantic Miss | 0 |
| q_4ff81a3c6e208b3c | define what an aim is | ms_marco | Ranking Error | 1 |
| q_e79c7c78c7d3c640 | what is the oldest age a person has ever lived | ms_marco | Ranking Error | 1 |
| q_cbbd4be860bca428 | name of the sheep clone | ms_marco | Ranking Error | 1 |
| q_f6e2127c81cd13af | what does the project manager do | ms_marco | Ranking Error | 1 |
| q_dd89db99cb99cdfb | is infectious pneumonia contagious | ms_marco | Ranking Error | 1 |
| q_0ccb272daf03d35a | where is grand bahama island located | ms_marco | Ranking Error | 1 |
| q_437462d16cd8f5e5 | what does nursing aides need to know | ms_marco | Ranking Error | 1 |
| q_0e3bd00a8f2e7a37 | where are habitats found | ms_marco | Ranking Error | 1 |
| q_d75f98089cf33482 | average cost of dental implants | ms_marco | Ranking Error | 1 |
| q_92caa84fd916bf3b | name meanings felicity | ms_marco | Ranking Error | 1 |
| q_7ddb6ede259c33d5 | large platelets causes | ms_marco | Semantic Miss | 0 |
| q_5b7f711c92766f10 | allegory definition literature | ms_marco | Ranking Error | 1 |
| q_b7c7b89b8c99748d | describe how a nerve cell is specialized | ms_marco | Ranking Error | 1 |
| q_19fb4e7d71529d32 | what digestive processes occur in the small intestine | ms_marco | Ranking Error | 1 |
| q_ee7b73cf5775dd02 | what is jacketing | ms_marco | Semantic Miss | 0 |
| q_5ed95cf9d7615c7b | what does sepsis mean yahoo | ms_marco | Ranking Error | 1 |
| q_06a23867d5d6b84d | what is biomedical ethics | ms_marco | Ranking Error | 1 |
| q_4769b7fdeee206e1 | what is chinese medicine | ms_marco | Ranking Error | 1 |
| q_fdfff4de8152544c | Highest Football Attendances | ms_marco | Ranking Error | 1 |
| q_03d89c580b6c5dd4 | clinical laboratory scientist salary per hour | ms_marco | Ranking Error | 1 |
| q_5b5008212b04250d | why does respiration take place in organelle | ms_marco | Ranking Error | 1 |
| q_8291a2cff2ee96d1 | how long do hamsters live | ms_marco | Ranking Error | 1 |
| q_4d9bc21cf880f6a4 | what is a sponges family | ms_marco | Ranking Error | 1 |
| q_692fea457a62e10a | how many points to suspend license in bc | ms_marco | Ranking Error | 1 |
| q_85396293eeeb56ae | what vitamins are good for dandruff | ms_marco | Ranking Error | 1 |
| q_5ad064a6a9ae4a23 | can you connect to bluetooth through laptop | ms_marco | Ranking Error | 1 |
| q_a36e6b9eacf14fd1 | What are two of its subsystems? | squad | Semantic Miss | 0 |
| q_4e6663e8dc37fb5e | what is a minerals | ms_marco | Ranking Error | 1 |
| q_a6d20323d1031349 | The heart and the arteries and veins are associated with what system of the body? | sciq | Ranking Error | 1 |
| q_e545f11b05dcbfc1 | what is another name for buccal cavity | ms_marco | Ranking Error | 1 |
| q_97ffc8603b674032 | how much do crutches cost | ms_marco | Ranking Error | 1 |
| q_dee02d6fd3d5c146 | is lyme disease the cause of lupus | ms_marco | Ranking Error | 1 |
| q_75d65d21a53c6aa3 | what can urinalysis detect | ms_marco | Ranking Error | 1 |
| q_d45e59f3f0c37d50 | What should it cost to have an HVAC contractor come to my home a replace my thermostat | ms_marco | Ranking Error | 1 |
| q_1e99cbe0bd24b583 | list of viscous fibre food | ms_marco | Ranking Error | 1 |
| q_f0c6a1446bf5e502 | average price to seal coat a driveway | ms_marco | Ranking Error | 1 |
| q_70497201e458dbec | What are the dark areas of the moon called? | sciq | Semantic Miss | 0 |
| q_b17da6d441588663 | how can you avoid hepatitis | ms_marco | Semantic Miss | 0 |
| q_0fc9028519b76114 | what does acquisition cost include | ms_marco | Ranking Error | 1 |
| q_979bc4ce845a092c | what does shaniqua mean | ms_marco | Ranking Error | 1 |
| q_0878861f1e2a1588 | how much cost to lay laminate flooring | ms_marco | Ranking Error | 1 |
| q_6bf00818b1cbaefb | footballers salary per week | ms_marco | Ranking Error | 1 |
| q_42ab49738cc8a28b | where can i put out my business yard signs | ms_marco | Ranking Error | 1 |
| q_ffa9b7f826dc67de | what are faverolle chickens | ms_marco | Semantic Miss | 0 |
| q_f3f8175d01c2ee89 | example of a dictatorship | ms_marco | Ranking Error | 1 |
| q_bb8c2899f26e08a1 | dental hygienist salary comparison by city | ms_marco | Ranking Error | 1 |
| q_7a0db7c8e7d7e4f4 | how long can nicotine be detected in blood | ms_marco | Semantic Miss | 0 |
| q_a7497b4e7b4865da | what is the highest ACT score | ms_marco | Ranking Error | 1 |
| q_6a99430d2468f049 | where is it brisbane | ms_marco | Ranking Error | 1 |
| q_b16e90c9cc569f63 | List The Roles of Calcium | ms_marco | Semantic Miss | 0 |
| q_a88fd08bb689aaaf | what is earth perihelion and aphelion | ms_marco | Semantic Miss | 0 |
| q_ad1d545ddc90dd66 | foods that cause rheumatoid arthritis flare ups | ms_marco | Semantic Miss | 0 |
| q_5fbbd6af62cce4ac | average amount spent on textbooks per semester | ms_marco | Ranking Error | 1 |
| q_eb026825ecb53b7c | who were the first members of the eu | ms_marco | Ranking Error | 1 |
| q_da524099b11ee325 | can an inherited ira be converted to a roth ira | ms_marco | Ranking Error | 1 |
| q_7bf658e4fc121f2c | shrivelling definition | ms_marco | Ranking Error | 1 |
| q_35170df135adec71 | how much do bartenders make | ms_marco | Semantic Miss | 0 |
| q_ac611b96a140c882 | temperature for yeast fermentation | ms_marco | Ranking Error | 1 |
| q_a4a50cfcefaf7d80 | wrapper | code_search_net | Semantic Miss | 0 |
| q_869611f5ca6dda22 | what meals does kfc do | ms_marco | Ranking Error | 1 |
| q_18c3cce147bdb728 | where are your ribs in your back located | ms_marco | Ranking Error | 1 |
| q_0e928210e545fe2a | average cost of pavers per square foot | ms_marco | Ranking Error | 1 |
| q_a63a94510f782340 | how much does a hospice nurse make? | ms_marco | Ranking Error | 1 |
| q_f1bd977264805ee5 | average home construction cost | ms_marco | Ranking Error | 1 |
| q_8c5c1dd2652e2e9c | where is nunavut | ms_marco | Ranking Error | 1 |
| q_f5f006708f05ae3f | What is the name of the high-energy compound that cells use directly to fuel other chemical reactions? | ms_marco | Semantic Miss | 0 |
| q_3afbe7aea2446dfd | In naming ternary compounds, which type of particle is stated first? | sciq | Semantic Miss | 0 |
| q_ac2737cfc36ac640 | what is fibroid | ms_marco | Ranking Error | 1 |
| q_bf162e73104c066e | are there different types of vertigo | ms_marco | Ranking Error | 1 |
| q_67356f258f7e8f98 | Genetic markers show the presence of a predisposition to a disease or condition by | ms_marco | Ranking Error | 1 |
| q_2cc62b163ba01114 | tv character who sang the opening theme song | ms_marco | Ranking Error | 1 |
| q_51c8fe916ed59a32 | how many stomach does a cow have | ms_marco | Ranking Error | 1 |
| q_549035d9565b999c | how much does a professional tattoo artist make | ms_marco | Ranking Error | 1 |
| q_f7158e60678f8733 | what are mycoplasmas | ms_marco | Ranking Error | 1 |
| q_dc7754a440cb80e4 | who was willie beir | ms_marco | Ranking Error | 1 |
| q_07e64535085e83c1 | find out which computer a user is locking an account | ms_marco | Ranking Error | 1 |
| q_e41351cf3a2b1d80 | saxmundham meaning of name | ms_marco | Ranking Error | 1 |
| q_af8bbf775e7eb167 | Neutrophils and lymphocytes are examples of what type of cell? | sciq | Semantic Miss | 0 |
| q_4b7e1451603dc9ef | medicare ppo what does it cover | ms_marco | Semantic Miss | 0 |
| q_f86878906b3b329d | how long does it take to cook a pork tenderloin | ms_marco | Ranking Error | 1 |
| q_ac90e7552bc36745 | what can i do with my psychology degree | ms_marco | Ranking Error | 1 |
| q_fa57194c4b9cc8fe | how to call mexico from canada | ms_marco | Ranking Error | 1 |
| q_983267be49f8b24f | what is notation in math | ms_marco | Ranking Error | 1 |
| q_ded8ef3c0d2a1780 | how to tell age of tire | ms_marco | Semantic Miss | 0 |
| q_e2c131b4136514e0 | what is the meaning of atharva veda | ms_marco | Ranking Error | 1 |
| q_bf24580d2f0cf051 | what is a shelter care order | ms_marco | Semantic Miss | 0 |
| q_1d1c256ae684e64c | does wipe data factory reset delete pictures | ms_marco | Ranking Error | 1 |
| q_add0a2064c7a9f29 | cost of mailing letter to canada | ms_marco | Ranking Error | 1 |
| q_8e7103e93d2555d4 | hyaline cartilage definition | ms_marco | Semantic Miss | 0 |
| q_0cd83550055ecbd4 | names of cells that cause disease | ms_marco | Ranking Error | 1 |
| q_ace501b90fa8284f | why is it called a kissing bug | ms_marco | Ranking Error | 1 |
| q_e533e6df87c41717 | what does unremarkable mean on a liver mri | ms_marco | Ranking Error | 1 |
| q_3b0f55c74116413e | What one point was not agreed on that was dear to Luther? | squad | Semantic Miss | 0 |
| q_96d16da31805ead3 | oculomotor nerve definition | ms_marco | Ranking Error | 1 |
| q_93953bb9828841d1 | what age to start toilet training puppies | ms_marco | Ranking Error | 1 |
| q_4a57f9dfeecbb7cb | what does the earth's magnetic field do | ms_marco | Ranking Error | 1 |
| q_87f0ca85aa3c07ce | george orwell orthodoxy is unconsciousness | ms_marco | Ranking Error | 1 |
| q_631444effcdd9ff5 | cost of lucentis injection | ms_marco | Ranking Error | 1 |
| q_7148712d05580379 | the ___were victory at the first battle of bull run | ms_marco | Ranking Error | 1 |
| q_d4b45b38342e1f64 | what did the royal fusiliers do | ms_marco | Semantic Miss | 0 |
| q_4cc63742e8e9ff44 | how long to hatch dove eggs | ms_marco | Ranking Error | 1 |
| q_da513e6e3ba22b67 | normal range of haemoglobin in australian medicine | ms_marco | Ranking Error | 1 |
| q_fbc4cdf0767268b9 | is charles manson dead | ms_marco | Semantic Miss | 0 |
| q_11c8e02a2791353e | comprehensive immigration reform definition | ms_marco | Ranking Error | 1 |
| q_60e4874312eb081f | how long to cook beef rolled rib roast | ms_marco | Ranking Error | 1 |
| q_1c9ab571575ada28 | what is the meaning of inflorescence | ms_marco | Ranking Error | 1 |
| q_d3d8894acc24da03 | what instruments do the kruger brothers play | ms_marco | Ranking Error | 1 |
| q_5992ff472641f86f | side effects of cogentin | ms_marco | Ranking Error | 1 |
| q_0480cb303774d61b | charter colony definition | ms_marco | Ranking Error | 1 |
| q_a33dac418ffb1b4e | what vision abnormality occurs | ms_marco | Ranking Error | 1 |
| q_875b795cfcf15c97 | meaning of the name amica | ms_marco | Ranking Error | 1 |
| q_215dfb5b208de426 | is kodak still making cameras | ms_marco | Ranking Error | 1 |
| q_0faf27b71785a309 | how much does it cost for an electrician to install dimmers | ms_marco | Ranking Error | 1 |
| q_304f22f903323b03 | incubation time for cold | ms_marco | Ranking Error | 1 |
| q_a5462795c829f406 | at what gestational age can you feel a fetus move | ms_marco | Ranking Error | 1 |
| q_eeb9a58985ca1ab9 | best way to use chromecast | ms_marco | Ranking Error | 1 |
| q_c342b215d4ece629 | are millipedes nocturnal | ms_marco | Ranking Error | 1 |
| q_6c4dfa68cd2340f3 | average weight of a female cow | ms_marco | Ranking Error | 1 |
| q_e76288faeaebd6eb | what is inside a corn | ms_marco | Semantic Miss | 0 |
| q_3e0e47d4a44fa66d | what nationality is alex wagner | ms_marco | Ranking Error | 1 |
| q_c9e3875ebf217f65 | What were the win/loss game stats for the Denver Bronco's regular season in 2015? | squad | Ranking Error | 1 |
| q_10d3e2fe3de830fd | what does a power conditioner do | ms_marco | Ranking Error | 1 |
| q_76e7d4d5f8e9f3fd | difference between xml xsl jsp html css | ms_marco | Ranking Error | 1 |
| q_8b18aa8ac08db8be | what electrical plug ins are used in portugal | ms_marco | Ranking Error | 1 |
| q_2d37616d014c3cdf | why hibiscus flower is important | ms_marco | Ranking Error | 1 |
| q_dae398ea07d3bcf5 | what food can you have at a luau party | ms_marco | Ranking Error | 1 |
| q_4539678ed97f2388 | what b vitamins for vegetarians | ms_marco | Semantic Miss | 0 |
| q_f2cf067d1c3bc349 | How did Natives in Logstown take Celeron's information? | squad | Semantic Miss | 0 |
| q_e78fb67bb5d091c7 | does medical insurance cover freezing eggs | ms_marco | Ranking Error | 1 |
| q_a413e87476a92041 | where orangutans live | ms_marco | Ranking Error | 1 |
| q_a8f4e25467fbe828 | what are malware signatures | ms_marco | Semantic Miss | 0 |
| q_d2def05376d60454 | tablet android how to close application | ms_marco | Semantic Miss | 0 |
| q_ce402c2d822d2ad3 | how to cut down a sim card | ms_marco | Ranking Error | 1 |
| q_8e7e68c0780a9456 | what canadian province is located between saskatchewan and ontario | ms_marco | Ranking Error | 1 |
| q_c647027ebe287c2d | how much money do nurses make | ms_marco | Ranking Error | 1 |
| q_87de70cf578e7039 | economic entity principle definition | ms_marco | Ranking Error | 1 |
| q_d527576eb59ac130 | what does a fbc blood test check for | ms_marco | Ranking Error | 1 |
| q_efea423c5b84ba91 | What band names were the Beatles known as | ms_marco | Ranking Error | 1 |
| q_6e77e45c4a4d6bf5 | what does the psoas muscle do | ms_marco | Ranking Error | 1 |
| q_65da1347ceee8270 | where does the river itchen start | ms_marco | Ranking Error | 1 |
| q_21c8565c0ad7c74e | What was a non-religious reason for the massacre? | squad | Semantic Miss | 0 |
| q_b59102985835844e | when do you have to start withdrawing from your ira | ms_marco | Ranking Error | 1 |
| q_89c89d7e0802217e | what is the role of the sodium chloride detergent solution in the dna extraction process | ms_marco | Ranking Error | 1 |
| q_ce0f68480dda8cca | how much does it cost to make an application for iphone | ms_marco | Semantic Miss | 0 |
| q_9a412336cd05c5c8 | how long to keep tax returns | ms_marco | Ranking Error | 1 |
| q_e514e9cb5dfca480 | what temperature does a house fire reach | ms_marco | Ranking Error | 1 |
| q_17ab655332d0a072 | how to do a background check on a potential tenant | ms_marco | Semantic Miss | 0 |
| q_38d88d2ab8883c37 | where is abbotsbury | ms_marco | Ranking Error | 1 |
| q_4a939b4d5e93a3a1 | is cellulose considered a energy source | ms_marco | Ranking Error | 1 |
| q_0ed1c3df088f0e93 | what receptor does MIBG target | ms_marco | Ranking Error | 1 |
| q_1e580dffad9e9906 | what is a basketcase? | ms_marco | Ranking Error | 1 |
| q_c96f3b51429e9d09 | where does anthrax live | ms_marco | Ranking Error | 1 |
| q_8a191c2c4f79e9d3 | what temperature can aloe survive | ms_marco | Ranking Error | 1 |
| q_dc3bf9c8385c2af4 | example of population in an ecosystem | ms_marco | Ranking Error | 1 |
| q_5ae5e210da17a4b9 | what is the order of the subunits in a strand of dna is called | ms_marco | Ranking Error | 1 |
| q_6a2b5a12cafdb408 | who is the founder of microsoft | ms_marco | Ranking Error | 1 |
| q_19146377188e10e5 | what is cryo treatment | ms_marco | Ranking Error | 1 |
| q_bbd8679f577424ee | how do you get rid of eczema on your buttocks | ms_marco | Ranking Error | 1 |
| q_6691c118cf778886 | What is the problem with cysteine? | squad | Semantic Miss | 0 |
| q_63fa2fe4cefd6e2e | how long do i cook brown rice in the microwave | ms_marco | Ranking Error | 1 |
| q_31f66903f9427fa2 | what type of flooring can be installed on concrete | ms_marco | Ranking Error | 1 |
| q_d81954e06862123e | what impulsive means | ms_marco | Semantic Miss | 0 |
| q_ca24ed9f63e13d8b | what does fusee movement mean in clocks | ms_marco | Ranking Error | 1 |
| q_2c80daf2215b6d46 | mineral rocks definition | ms_marco | Ranking Error | 1 |
| q_a950104f3f799327 | How near to his death was the work published? | squad | Semantic Miss | 0 |
| q_b09ae3b020322fc5 | how long is pork good for in the fridge | ms_marco | Ranking Error | 1 |
| q_2cb071afca6237e9 | extra insurance cost for an inground pool | ms_marco | Semantic Miss | 0 |
| q_58ee8fbb53bae061 | why do road crews use road salt in the winter months to treat icy roads | ms_marco | Semantic Miss | 0 |
| q_f87f00c3b5b0f7bf | what type of bedding for chickens | ms_marco | Ranking Error | 1 |
| q_5b65103b9fb4b1e7 | what is the common name for nh4cl | ms_marco | Ranking Error | 1 |
| q_da5251c9678647a4 | do sponges drain water in minecraft | ms_marco | Ranking Error | 1 |
| q_394b7e373bc06e7d | why was fort jefferson built | ms_marco | Ranking Error | 1 |
| q_5ca35bf14ec9c087 | The structural explanation of how a muscle fiber contracts is called the | ms_marco | Ranking Error | 1 |
| q_1f83535d20433a33 | what is the class that includes sedimentary rocks which are deposited from a solution made from organic process | ms_marco | Ranking Error | 1 |
| q_b6f4f8d953bb8f15 | when were historical documents written | ms_marco | Ranking Error | 1 |
| q_53bdbed0ea7377f0 | disease caused by protozoa in animals | ms_marco | Ranking Error | 1 |
| q_eafcec6311a0e433 | fever definition celsius | ms_marco | Ranking Error | 1 |
| q_b59a00cb4b646aa7 | how long does it take to install a pool | ms_marco | Ranking Error | 1 |
| q_d4340ac021458165 | bacterial endocarditis definition | ms_marco | Ranking Error | 1 |
| q_30028584bfe7bb8b | what is albumin | ms_marco | Ranking Error | 1 |
| q_8afe9505087ccddc | cost of blue light treatment with dermatologist | ms_marco | Ranking Error | 1 |
| q_a9c5761cb57e3c77 | meaning of dna | ms_marco | Ranking Error | 1 |
| q_1e652f708e95a3a0 | what chemical reactions do hydrazine block | ms_marco | Ranking Error | 1 |
| q_a95b35382bb4bfe6 | where are limpets found | ms_marco | Ranking Error | 1 |
| q_1ba26ba0aa256631 | what is beryl tourmaline | ms_marco | Ranking Error | 1 |
| q_a1ff57635384fa4d | what is a policy document | ms_marco | Ranking Error | 1 |
| q_0ced0441019b02f1 | what is propylene carbonate | ms_marco | Semantic Miss | 0 |
| q_66fc575999666f4d | accounting annual reporting period definition | ms_marco | Ranking Error | 1 |
| q_1dae9f538f8c6709 | what makes male seman brown | ms_marco | Ranking Error | 1 |
| q_4e4e28a0b4416db8 | what is hypospadia | ms_marco | Semantic Miss | 0 |
| q_7b0313841f89d4ca | the lateral malleolus is formed by the what | ms_marco | Ranking Error | 1 |
| q_4577780ae2b1f518 | solarcity price per watt | ms_marco | Ranking Error | 1 |
| q_bc752bfbf7fc7822 | average length of stay in nursing home | ms_marco | Ranking Error | 1 |
| q_5168718ed19379b7 | what tone is poetry | ms_marco | Ranking Error | 1 |
| q_fa77b45e344379a8 | food that will raise blood pressure count | ms_marco | Ranking Error | 1 |
| q_d287e4a124ba295d | cost of hydrogen steam reforming | ms_marco | Ranking Error | 1 |
| q_66d701d095c2d9e5 | what is a pink eye disease | ms_marco | Ranking Error | 1 |
| q_3f20026bf8e20f55 | what kind of stars are the cepheids | ms_marco | Semantic Miss | 0 |
| q_c7a86d19e6fbbaa5 | what are process of service desk | ms_marco | Ranking Error | 1 |
| q_f3d968f4e9de11e1 | how long should I keep credit card bills? | ms_marco | Ranking Error | 1 |
| q_971be89dbef71f95 | what does a western blot detect | ms_marco | Ranking Error | 1 |
| q_c1b6bf5e49389a43 | what part of the body does hepatitis a affect | ms_marco | Ranking Error | 1 |
| q_f0198ef30cc052fa | what kind of industry helps mexico | ms_marco | Ranking Error | 1 |
| q_c7333727760e914c | what enzyme does a positive TSI test detect | ms_marco | Ranking Error | 1 |
| q_2d02d09036a69b77 | what is decyl glucoside | ms_marco | Ranking Error | 1 |
| q_088efd78908d543c | how to cook ribeye steak on the grill | ms_marco | Ranking Error | 1 |
| q_c4bbfd21b9154c86 | what type of minibeast is scorpion | ms_marco | Semantic Miss | 0 |
| q_84dddbee21a5d5c5 | where is the originals tv show filmed | ms_marco | Semantic Miss | 0 |
| q_82ceb646bd43572b | what are the valves called | ms_marco | Semantic Miss | 0 |
| q_6f9880c09cb85fd9 | jaw points of movement snakes definition | ms_marco | Semantic Miss | 0 |
| q_238641d8f9770865 | weather in moscow in may | ms_marco | Ranking Error | 1 |
| q_3a2d53db1edd86a7 | how much does it cost to replace a water pump in car | ms_marco | Ranking Error | 1 |
| q_bfd827a3d0d60623 | why is glutathione called gsh | ms_marco | Ranking Error | 1 |
| q_88d9e93f34de01b9 | what makes a disease monogenic | ms_marco | Semantic Miss | 0 |
| q_1df5d1ffaf63ec76 | where are stress hormones produced | ms_marco | Ranking Error | 1 |
| q_281d479c18893365 | who is invertebrate paleontologist | ms_marco | Ranking Error | 1 |
| q_9ebe9661072e7982 | why is finn in star wars | ms_marco | Ranking Error | 1 |
| q_0b9876dee4780417 | how long n temperature to grill chicken thighs | ms_marco | Ranking Error | 1 |
| q_b496f8c3f3acbc08 | What direction are sediments deposited? | sciq | Semantic Miss | 0 |
| q_c316ec3c12ab6e40 | vw cambelt replacement cost | ms_marco | Ranking Error | 1 |
| q_d9723626e6003b99 | what is in dmae | ms_marco | Ranking Error | 1 |
| q_a2ade0256c7624d1 | what is a disease that affects the legs | ms_marco | Ranking Error | 1 |
| q_ece4ad186c7700d4 | what are the precipitating factors for addison's disease in dogs | ms_marco | Semantic Miss | 0 |
| q_5262fbfd4fbc05f9 | cost of denture | ms_marco | Ranking Error | 1 |
| q_26610f24baec7ebc | how long for okra to grow | ms_marco | Ranking Error | 1 |
| q_00ff02b57d019d1d | average price dallas cowboys ticket home game | ms_marco | Ranking Error | 1 |
| q_25d60221a1e5ee9b | what is bacterial infection in urine | ms_marco | Ranking Error | 1 |
| q_bbaa69920dddaa54 | where do the richest people in the world live | ms_marco | Ranking Error | 1 |
| q_813db8255741278e | what is the average cost of a polygraph test | ms_marco | Ranking Error | 1 |
| q_718e15522e1d197e | is it mandatory to pay overtime on holidays | ms_marco | Ranking Error | 1 |
| q_a4585bd248cd77c6 | can you use a deactivated sim card again | ms_marco | Ranking Error | 1 |
| q_846dfdebca9c3bfa | how can rocks be formed in the earth's lithosphere | ms_marco | Ranking Error | 1 |
| q_2085388b5b5b750f | how much does it cost for your provisional licence | ms_marco | Ranking Error | 1 |
| q_2d969b764513a033 | what types of food in africa | ms_marco | Ranking Error | 1 |
| q_bcaafdadbef8a2aa | what are the blood sugar blood tests | ms_marco | Ranking Error | 1 |
| q_fab3775863a6f2f8 | what do you do to monitor copd | ms_marco | Ranking Error | 1 |
| q_070f9ae44ec51951 | who do you make check payable for nj state tax | ms_marco | Ranking Error | 1 |
| q_cbe8da7fe7d3c02c | cost of seawall per foot | ms_marco | Ranking Error | 1 |
| q_b2a60de44c9c0d06 | What do tadpoles clear out of waterways? | sciq | Semantic Miss | 0 |
| q_19a64400576a61fe | what type of chemical bond has the most potential energy stored in it | ms_marco | Ranking Error | 1 |
| q_021ac30047ff7bd8 | how to figure out percentage by weight weight | ms_marco | Ranking Error | 1 |
| q_c395856e92490f64 | what is chlorophyll used for | ms_marco | Ranking Error | 1 |
| q_85c5f9ba0d3af9a7 | putting baking soda in water to boil eggs | ms_marco | Ranking Error | 1 |
| q_bbdedc48ba9ed898 | what environment does a coconut live in | ms_marco | Ranking Error | 1 |
| q_0c5fdb08fd9d0418 | What can be calculated by solving the average speed formula? | sciq | Semantic Miss | 0 |
| q_7bbfdebae81a0e82 | what is an incision into the vertebral column | ms_marco | Ranking Error | 1 |
| q_64b84f8e0639ba33 | what foods contain sorbitol | ms_marco | Ranking Error | 1 |
| q_f8187635a39ad193 | where are the baroreceptors located | ms_marco | Ranking Error | 1 |
| q_d1ffd6a7fbb908de | incubation period for quail eggs | ms_marco | Ranking Error | 1 |
| q_bc3ccacd04cbe1ab | Who was Kennedy's vice president? | squad | Semantic Miss | 0 |
| q_e02aa3f7a91d5475 | how to cook yellowfin tuna steaks | ms_marco | Ranking Error | 1 |
| q_9e19d0efec781fd5 | texas When does the legislature meet? | ms_marco | Ranking Error | 1 |
| q_1e61345235027f66 | what does nightly version mean | ms_marco | Ranking Error | 1 |
| q_8f4d9c1866bba42b | is vitamin c good for acne | ms_marco | Ranking Error | 1 |
| q_daeebeb74f08e38a | what is a gyroscope | ms_marco | Semantic Miss | 0 |
| q_2b6800a5ca1cd251 | standard temperature and pressure for water | ms_marco | Ranking Error | 1 |
| q_dd4f3cdf3e88f575 | minimum wage law def | ms_marco | Ranking Error | 1 |
| q_51ab79e2ed4c8fd4 | meaning of the word silhouetted | ms_marco | Ranking Error | 1 |
| q_70c48e5751cc0b56 | what is the bad thing about green cleaning | ms_marco | Ranking Error | 1 |
| q_7effa2c370cb390b | should you fertilize before rain | ms_marco | Ranking Error | 1 |
| q_85fb2354267c5bff | in what year did diamondback bikes start cadel evans career off | ms_marco | Ranking Error | 1 |
| q_c11ac13e82c7b216 | who sang the original venus song | ms_marco | Ranking Error | 1 |
| q_e9a7ef2440c063cb | when was the smallpox vaccine discovered | ms_marco | Ranking Error | 1 |
| q_bac96f59ba71e62e | normal range for blood pressure | ms_marco | Ranking Error | 1 |
| q_c089813ca8040f2a | what is a play genre for | ms_marco | Ranking Error | 1 |
| q_7b837aaed749f623 | volleyball court measurement in meters | ms_marco | Ranking Error | 1 |
| q_46924a924b2e65ec | when was the television invented | ms_marco | Ranking Error | 1 |
| q_bf13e8f6ae8c9dc0 | what does the endoplasmic reticulum do in an animal cell | ms_marco | Ranking Error | 1 |
| q_598f471e921a4e04 | what is an Oculoplastics | ms_marco | Ranking Error | 1 |
| q_cb0f7e1eb3c64222 | where is Llanberis located | ms_marco | Ranking Error | 1 |
| q_f4781600d5ab89bb | does dandelion grow in the summer | ms_marco | Ranking Error | 1 |
| q_27001e312f73dcd8 | freud civilization and its discontents summary | ms_marco | Ranking Error | 1 |
| q_13f29403123032a1 | how much money does donald trump make | ms_marco | Ranking Error | 1 |
| q_1a2a42a3d3733130 | definition iambic pentameter | ms_marco | Semantic Miss | 0 |
| q_6b33c43ed9a93d3a | define rheumatology | ms_marco | Ranking Error | 1 |
| q_b9e29ded36b362c0 | what is an snar reaction | ms_marco | Ranking Error | 1 |
| q_b1cc1541b0b800ea | two most abundant gases from eruptions | ms_marco | Ranking Error | 1 |
| q_7d4eb6d245d4feeb | is there a age requirement to become ny corrections | ms_marco | Semantic Miss | 0 |
| q_499fde7ce793962f | how to stop hair from being affected by humidity | ms_marco | Ranking Error | 1 |
| q_9733147ee43c51cc | what keeps the moon orbiting the earth | ms_marco | Ranking Error | 1 |
| q_ba898d7f93acf0ab | does the stomach digest food | ms_marco | Ranking Error | 1 |
| q_342f50bedafa4e73 | how much does a phlebotomy technician make | ms_marco | Ranking Error | 1 |
| q_d1d9a9ee2ab884cc | what temperature should an apple pie bake | ms_marco | Ranking Error | 1 |
| q_10e280975c02bc2f | what kind of membrane surrounds the nucleus | ms_marco | Ranking Error | 1 |
| q_30d2d01a3bbfba87 | What kind of motion characterizes waves? | sciq | Semantic Miss | 0 |
| q_ae7ac77cd86c3da4 | explain the biochemical process of photosynthesis | ms_marco | Semantic Miss | 0 |
| q_358e04fc27fb1416 | what chamber of the heart do the anterior and posterior vena cava open | ms_marco | Ranking Error | 1 |
| q_596a90c0dd0d340c | what is switzerland's food style | ms_marco | Semantic Miss | 0 |
| q_2271a9833042c74f | how long to cook shoulder of pork | ms_marco | Ranking Error | 1 |
| q_638832f2196782a8 | which president made the most executive orders | ms_marco | Ranking Error | 1 |
| q_38b8964b668c83ab | how long does it take for employer to get back to you after you apply | ms_marco | Ranking Error | 1 |
| q_88253d75c84efd51 | electricity cost / kwh seattle | ms_marco | Ranking Error | 1 |
| q_b529a50429dda790 | Which direction did Romans use to drift through the Rhine? | squad | Semantic Miss | 0 |
| q_2cfcbe5019f46402 | what infrastructure does tpg use | ms_marco | Ranking Error | 1 |
| q_fbf3ecde9aa04af6 | how to determine hoa fees | ms_marco | Ranking Error | 1 |
| q_002c3c79149e02ff | is a peacock a bird | ms_marco | Ranking Error | 1 |
| q_ca92b48b5d6b42c0 | what is peripheral vestibular disorder | ms_marco | Ranking Error | 1 |
| q_433f3886f0b8c840 | What organ system is different in men and women? | sciq | Semantic Miss | 0 |
| q_9fa7d9ce376c8f38 | estimated cost of radial keratotomy | ms_marco | Ranking Error | 1 |
| q_03418bb3fb6ed0d1 | effective way to remove tonsil stones | ms_marco | Ranking Error | 1 |
| q_a6af74ab626ffd9b | An experiment generates what to support a hypothesis? | sciq | Semantic Miss | 0 |
| q_14d86bd117463721 | how successful is back surgery | ms_marco | Ranking Error | 1 |
| q_a5df9225a82d1970 | what is the meaning of chesed | ms_marco | Ranking Error | 1 |
| q_cab156cbce3d08f1 | in which organ-- gizzard or crop-- would you expect to find the contents more ground up | ms_marco | Ranking Error | 1 |
| q_b6f2421d7edd638e | what is haggis made of | ms_marco | Ranking Error | 1 |
| q_ebbd5dc8dabf1f39 | what causes radioactive pollution | ms_marco | Ranking Error | 1 |
| q_18657a98fe7480e1 | spinal fluid which causes the low pressure around the brain | ms_marco | Ranking Error | 1 |
| q_850a1c14f8cb0095 | nike create your own | ms_marco | Ranking Error | 1 |
| q_4fcc87a9dfbdcbf0 | what is the modern name for the city of syene | ms_marco | Ranking Error | 1 |
| q_f5a51caf9d6000bb | what are the significance of Streptococcus pyogenes | ms_marco | Semantic Miss | 0 |
| q_57522667a0b95b9e | what is a LLc | ms_marco | Ranking Error | 1 |
| q_7ca60e20beed6d89 | what is migraine pain | ms_marco | Ranking Error | 1 |
| q_bd3fdc68dbd0a9ab | what is zinc primer | ms_marco | Ranking Error | 1 |
| q_5c20329b45cb40ed | what does franchise fee mean | ms_marco | Ranking Error | 1 |
| q_332f51d01877601a | definition of saute in cooking | ms_marco | Ranking Error | 1 |
| q_6f710cbe7f67447b | what happens to dopamine when taking antipsychotics drugs | ms_marco | Ranking Error | 1 |
| q_452c47508940a7ae | what is the definition of a substance in chemistry | ms_marco | Ranking Error | 1 |
| q_64bfcb0b9b0e52a1 | how much does a theoretical physicist get paid | ms_marco | Ranking Error | 1 |
| q_6b365035517ea75b | how time is the chicken pox incubation period for chickenpox | ms_marco | Semantic Miss | 0 |
| q_535ba4f072c3f005 | name that means intelligent | ms_marco | Ranking Error | 1 |
| q_cfd66c394336b2f8 | what is dbp in nail polish | ms_marco | Ranking Error | 1 |
| q_9d34e73717c0d8b3 | how much does a microchip cost for a dog | ms_marco | Ranking Error | 1 |
| q_b82d93a0c2a72f93 | what do gibbons eat | ms_marco | Ranking Error | 1 |
| q_ec6154a2cff0a8bb | the average income of a college student | ms_marco | Ranking Error | 1 |
| q_9f63357eedf5bd0c | new york mammal is called | ms_marco | Ranking Error | 1 |
| q_05b9767f345a11a0 | how many weeks pregnant can you determine gender | ms_marco | Ranking Error | 1 |
| q_8ec55d4df4877761 | what are the dosage forms tizanidine | ms_marco | Ranking Error | 1 |
| q_e134f3f519fbe7ff | what does the german word wechsel mean | ms_marco | Ranking Error | 1 |
| q_f08b5fefcd403cf9 | average lines per hour entry level medical transcriptionist | ms_marco | Ranking Error | 1 |
| q_a9d8bb060ba442b2 | where is the cerebral cortex located | ms_marco | Ranking Error | 1 |
| q_e5e06afba37d50cd | annual salary definition | ms_marco | Ranking Error | 1 |
| q_03cf1d4583bc516f | hpv vaccine india brand names | ms_marco | Ranking Error | 1 |
| q_2485dad8fa995f67 | dental cap cost | ms_marco | Ranking Error | 1 |
| q_e4b4542262d92eba | what is a common product of anaerobic metabolism | ms_marco | Ranking Error | 1 |
| q_412904581fc22b5e | is the book sleepers based on a true story | ms_marco | Ranking Error | 1 |
| q_ea3f09dc660ff48d | what owls are protected | ms_marco | Ranking Error | 1 |
| q_225a8e87e9afebca | how much does a land survey cost | ms_marco | Ranking Error | 1 |
| q_ae5f3d43f490c8df | site into which releasing hormones or inhibiting hormones | ms_marco | Ranking Error | 1 |
| q_1781219f1df64aa6 | what function does your adrenal gland control | ms_marco | Ranking Error | 1 |
| q_c3a4664b4af3b2d2 | what do they use bear bile for | ms_marco | Ranking Error | 1 |
| q_51e2c4210a3e95df | where is ajaccio | ms_marco | Ranking Error | 1 |
| q_b82ed5a6192d6c47 | what is bioarchaeology | ms_marco | Ranking Error | 1 |
| q_13291bd2f54eb443 | how long to oven cook whole chicken | ms_marco | Ranking Error | 1 |
| q_d95f00d412ea86e8 | how to do closing statement in a debate | ms_marco | Ranking Error | 1 |
| q_22cf5e6945ef6555 | why do they stain pistachios red? | ms_marco | Ranking Error | 1 |
| q_0a016bca9ca04642 | what is a hysterosonogram | ms_marco | Ranking Error | 1 |
| q_2d4b06b26aa60705 | temperature and time roast chicken | ms_marco | Ranking Error | 1 |
| q_3079e31c01b8244d | what is variable expenses | ms_marco | Ranking Error | 1 |
| q_45c229af549bb563 | what causes chemical meningitis | ms_marco | Ranking Error | 1 |
| q_7b8b59a3330d6f7f | what is Primary focal hyperhidrosis | ms_marco | Ranking Error | 1 |
| q_ae362f132eaf78fe | can you major in medical imaging | ms_marco | Semantic Miss | 0 |
| q_b4bd20deeaaba873 | what are food grade chemicals | ms_marco | Ranking Error | 1 |
| q_139f8e1ce5568af8 | how much to cancel sprint cell phone contract | ms_marco | Ranking Error | 1 |
| q_6070c14a1d606ae0 | what is a brigadeiro | ms_marco | Ranking Error | 1 |
| q_cc63ab5961b8e4a2 | do arteries and veins actually connect | ms_marco | Ranking Error | 1 |
| q_35c850eb571fc125 | how much does donor egg ivf cost | ms_marco | Ranking Error | 1 |
| q_2037490ea16e53b8 | aida name has what nationality | ms_marco | Ranking Error | 1 |
| q_635418bb16b40d1d | how to measure resting heart rate on ekg | ms_marco | Ranking Error | 1 |
| q_2adb5f6ebc6f28f8 | cost per square foot to install carpet | ms_marco | Ranking Error | 1 |
| q_b435dd56ea8e1b38 | set forth definition | ms_marco | Semantic Miss | 0 |
| q_f077c357e79c0586 | what satellite does freeview use | ms_marco | Semantic Miss | 0 |
| q_63aea9e18a26d746 | how to use art for depression | ms_marco | Ranking Error | 1 |
| q_20f0b3eec5525fca | what is the submandibular gland function | ms_marco | Ranking Error | 1 |
| q_bda6738703a18226 | what is a chemical reaction definition | ms_marco | Semantic Miss | 0 |
| q_0b7baefa90c827f0 | aleve side effects | ms_marco | Semantic Miss | 0 |
| q_841053a1f051a7c2 | regulation volleyball net professional height | ms_marco | Ranking Error | 1 |
| q_9bb1ab8a1d5b5dc5 | what is a bronsted lowry base example | ms_marco | Ranking Error | 1 |
| q_9f6b6e8ff3704bcb | how do you get a copy of a divorce decree from hawaii | ms_marco | Ranking Error | 1 |
| q_eaf9657e54769480 | cost of maize silage per tonne | ms_marco | Ranking Error | 1 |
| q_464d3cec94a056b6 | how do cats help us | ms_marco | Ranking Error | 1 |
| q_2ab96a3a7cc813dc | what are the proteins that carry out dna replication | ms_marco | Ranking Error | 1 |
| q_7e8733f67adb42ea | what is a dhcp reservation | ms_marco | Ranking Error | 1 |
| q_19ab63675e05fc1c | how much carbohydrates should an athlete consume | ms_marco | Ranking Error | 1 |
| q_01afd6299c4cb6cf | average writing speed by age | ms_marco | Ranking Error | 1 |
| q_272c7c030032c065 | what is a tawa | ms_marco | Ranking Error | 1 |
| q_9d938fa64b2e3bcd | what is lithotomy position | ms_marco | Ranking Error | 1 |
| q_0ba58a39ac3f3902 | what is a mango lassi | ms_marco | Ranking Error | 1 |
| q_62acb0dbd5ed460b | how much does a cat ultrasound cost | ms_marco | Ranking Error | 1 |
| q_93dd03d1fe5660e4 | what is infective endocarditis symptoms | ms_marco | Ranking Error | 1 |
| q_c020d095023c7aab | types of tea plants | ms_marco | Ranking Error | 1 |
| q_b90720e1c30bddb1 | average salary of a lorry driver ireland | ms_marco | Ranking Error | 1 |
| q_1c9f0e412a84e947 | What are the symptoms and causes of conjunctivitis | ms_marco | Ranking Error | 1 |
| q_3a47e5f762fc2df7 | What was notable about the butterflies? | squad | Semantic Miss | 0 |
| q_4de0b7d88eac6678 | What was the cost of the other Super Bowl events in the San Francisco area? | squad | Semantic Miss | 0 |
| q_23ad0684e2d691ad | how does recharging a battery work | ms_marco | Ranking Error | 1 |
| q_9e337378b245b64b | what is the genus and species of ant | ms_marco | Ranking Error | 1 |
| q_ff4e13e91ac82201 | how many ml is in a litre? | ms_marco | Ranking Error | 1 |
| q_c8b1d70c85c7a581 | when was slavery first started | ms_marco | Ranking Error | 1 |
| q_92bad05c40ff7eab | what temperature is the danger zone for food | ms_marco | Ranking Error | 1 |
| q_d297b70080a518e2 | what is an NSULC | ms_marco | Ranking Error | 1 |
| q_b9e1a0d6a71f969e | What is another word for seed plants? | sciq | Semantic Miss | 0 |
| q_035d4b3ba158c8ee | what is the metabolism in plants | ms_marco | Ranking Error | 1 |
| q_6293affbf1b1eedb | correlational study definition | ms_marco | Ranking Error | 1 |
| q_ac389588aa5418b5 | what is the difference between a lizard and a salamander | ms_marco | Ranking Error | 1 |
| q_68c6c38833c89118 | at what age does the average person start walking | ms_marco | Ranking Error | 1 |
| q_4603699c5fe9653e | how to get rid of staff infection | ms_marco | Semantic Miss | 0 |
| q_51747d420e828253 | what kind of flowers do pyrethrins come from | ms_marco | Ranking Error | 1 |
| q_c4168e62c937b9a3 | sales revenues for sound system | ms_marco | Ranking Error | 1 |
| q_d53c153cf993b912 | what is bordetella in dogs | ms_marco | Ranking Error | 1 |
| q_78faa1ab785c300f | who created the first plane | ms_marco | Ranking Error | 1 |
| q_3025c4f2535fae4f | does crestor affect cholesterol | ms_marco | Ranking Error | 1 |
| q_fe4e8e6265c2bc14 | Caffeine is an example of what type of drug? | sciq | Semantic Miss | 0 |
| q_59f9de12fd13a9ac | how to get vitamin d in diet | ms_marco | Ranking Error | 1 |
| q_50f03e707f9373b1 | what causes scratches | ms_marco | Ranking Error | 1 |
| q_5b1abbc04c2c5ee9 | definition of citizenism | ms_marco | Ranking Error | 1 |
| q_6eee970ce54cbfc1 | carbohydrates are stored in the liver and muscles in the form of | ms_marco | Ranking Error | 1 |
| q_81e52d43b070645b | how much does uber pay | ms_marco | Semantic Miss | 0 |
| q_7fb60bbbd636fcd6 | how much do footballers get paid | ms_marco | Ranking Error | 1 |
| q_82c5031de8f4fd81 | fairfax county average salary | ms_marco | Ranking Error | 1 |
| q_b563ea5d653c7b51 | disease that causes inflammation | ms_marco | Ranking Error | 1 |
| q_3fcdb3f85d6529d5 | neuron extending fiber that conducts impulses away from the cell body | ms_marco | Ranking Error | 1 |
| q_10ea6e72910447d8 | are the immune and lymphatic system the same | ms_marco | Ranking Error | 1 |
| q_df0fb7e9f151ed54 | what are kneading movements | ms_marco | Ranking Error | 1 |
| q_a2d6e2adb1bf8844 | what is a CR contract | ms_marco | Ranking Error | 1 |
| q_90a8e0c3cc50427a | what is a slapstick | ms_marco | Ranking Error | 1 |
| q_c09aac9acbe10c2d | what is lean | ms_marco | Ranking Error | 1 |
| q_8ffcff4236902387 | what is a rife machine used for | ms_marco | Ranking Error | 1 |
| q_ba8fbcf5c96efc38 | what is a nupe kappa | ms_marco | Ranking Error | 1 |
| q_60d151be13eef0f1 | what does hacker mean | ms_marco | Ranking Error | 1 |
| q_9879b1c5a8deb697 | where is arizona located | ms_marco | Ranking Error | 1 |
| q_ef75e1fa247a5c9b | justify renting costs | ms_marco | Ranking Error | 1 |
| q_3395718667687cbf | A diploid cell contains two sets of what? | sciq | Semantic Miss | 0 |
| q_50d6a250df1077a1 | what language do they speak in iran | ms_marco | Ranking Error | 1 |
| q_d1cdf32a4aaf0fd4 | will ibuprofen hurt my liver | ms_marco | Ranking Error | 1 |
| q_68d490ae941d5588 | how long can you make payments to the irs | ms_marco | Ranking Error | 1 |
| q_0f094f00f5d9a88c | when did germany declare war on belgium | ms_marco | Ranking Error | 1 |
| q_2f5147c98ccd213d | can you use a teepee trellis for tomatoes | ms_marco | Semantic Miss | 0 |
| q_faf92df4c392f790 | what is absinthe | ms_marco | Ranking Error | 1 |
| q_a045cc4835bc275a | the proximal surface that is located farthest away from the midline is the | ms_marco | Ranking Error | 1 |
| q_76206549534db32f | what does altimeter mean | ms_marco | Ranking Error | 1 |
| q_cd2696fe64ee2a2d | salary of clinical psychologist | ms_marco | Semantic Miss | 0 |
| q_6eea6f2a70a76d51 | what is lactose used for | ms_marco | Ranking Error | 1 |
| q_dd5f058a1b00deec | is the mitochondria a bacteria | ms_marco | Ranking Error | 1 |
| q_70d6dadc387c4cb2 | what is sneezing | ms_marco | Ranking Error | 1 |
| q_db5b1ee18fd30a76 | what region is brampton in | ms_marco | Ranking Error | 1 |
| q_8c99005d3c6bc480 | Mitochondria definition | ms_marco | Ranking Error | 1 |
| q_f03c5544297ed66e | what disabilities are intellectual disabilities | ms_marco | Ranking Error | 1 |
| q_2ca0a0ada817d3c3 | what is ferrous gluconate | ms_marco | Ranking Error | 1 |
| q_d1a9702d114b2aff | how much do nursing assistants in a nursing home make | ms_marco | Semantic Miss | 0 |
| q_ae2cb7eb77ff6794 | where is the jejunum located | ms_marco | Ranking Error | 1 |
| q_d3020725a482f0c7 | Which ctenophora have been studies the most? | squad | Semantic Miss | 0 |
| q_af59db9a219397cb | what helps bruises heal quicker | ms_marco | Ranking Error | 1 |
| q_720d3c46e33b1b6a | what is kop liverpool | ms_marco | Ranking Error | 1 |
| q_1b26b65f14633e95 | italian where is | ms_marco | Ranking Error | 1 |
| q_a5daea55323a701a | air con installation cost | ms_marco | Ranking Error | 1 |
| q_f02cef4fe622fac3 | brand definition business | ms_marco | Ranking Error | 1 |
| q_11d8bfd22e270f3a | what county is catonsville md in | ms_marco | Ranking Error | 1 |
| q_1bdd167a8401a8d3 | where do you see the state of arkansas headed to in the near future | ms_marco | Semantic Miss | 0 |
| q_146084b1617105f4 | where does secretion mostly occur in the nephron | ms_marco | Semantic Miss | 0 |
| q_d582f129d01ffe9b | how long do people on dialysis tend to live | ms_marco | Ranking Error | 1 |
| q_5dc8f87ada8b3a34 | originally iq was defined as | ms_marco | Ranking Error | 1 |
| q_dfe2562ca3258b5e | benefits of curd in diabetes | ms_marco | Semantic Miss | 0 |
| q_4440cebd4c365aaf | what temperature for pork ribs | ms_marco | Ranking Error | 1 |
| q_b8e2c4c281875509 | iatrogenic coagulopathy definition | ms_marco | Ranking Error | 1 |
| q_b4a869c54237b582 | what is a ventilation system | ms_marco | Ranking Error | 1 |
| q_53562264cce6ecf2 | where does king salmon live | ms_marco | Ranking Error | 1 |
| q_91cc5bf5cc9269ba | what enables the thyroid gland to perform its function | ms_marco | Ranking Error | 1 |
| q_655fa1a1268496dd | what does pennyweight mean | ms_marco | Ranking Error | 1 |
| q_f8d0b2925123f7fb | what book made jrr tolkien famous | ms_marco | Ranking Error | 1 |
| q_444d371b80b27fc2 | how wide is the colosseum | ms_marco | Ranking Error | 1 |
| q_f03e0a77694cba1a | food nutrients and their importance | ms_marco | Ranking Error | 1 |
| q_cd013371a904c831 | will burning incense set off the fire alarm | ms_marco | Ranking Error | 1 |
| q_940de824e26e7555 | what are a probation officers duties | ms_marco | Semantic Miss | 0 |
| q_abe60d90de10bd17 | how is sandstone formed? | ms_marco | Ranking Error | 1 |
| q_51a4092c5ed8dfed | what is a NUc | ms_marco | Ranking Error | 1 |
| q_dbcb8e5ea9c6864c | what is a literary agent salary | ms_marco | Ranking Error | 1 |
| q_01a8f3c03cc3a29d | genetically modified organisms for food | ms_marco | Ranking Error | 1 |
| q_7b1d45ad33bdb623 | deforestation affecting animals | ms_marco | Ranking Error | 1 |
| q_0049f3888088cc28 | can i do a group calls on skype international | ms_marco | Semantic Miss | 0 |
| q_60fb9e0bb223f9fb | how much is a root canal with delta dental insurance | ms_marco | Ranking Error | 1 |
| q_cf824aae7e6cb6a4 | what is an ionic lattice | ms_marco | Ranking Error | 1 |
| q_bdb2b10c5c92d202 | recommended dosage of magnesium for anxiety | ms_marco | Ranking Error | 1 |
| q_50f56669f7b26099 | how to insert a footnote in excel | ms_marco | Ranking Error | 1 |
| q_7aadb337a27a08ad | average starting salary for college grads | ms_marco | Ranking Error | 1 |
| q_925f92717717d7f9 | what is the incubation period for chlamydia | ms_marco | Ranking Error | 1 |
| q_cb148d6c4afdacc3 | what is flaxseed oil | ms_marco | Ranking Error | 1 |
| q_9969b7e6403be671 | does alcohol affect the eyes | ms_marco | Ranking Error | 1 |
| q_e5c2460b3c63f842 | signs of hens laying | ms_marco | Semantic Miss | 0 |
| q_02f6c20203b44d0d | how to clean fingerprints off your laptop case | ms_marco | Ranking Error | 1 |
| q_a23d42705235f2ee | how much does a pharmacist tech make an hour | ms_marco | Ranking Error | 1 |
| q_f2b1c25f877294fb | what are bile salts used for | ms_marco | Semantic Miss | 0 |
| q_963f6349ca44cb65 | ________ are the blood vessels that carry blood away from the heart | ms_marco | Ranking Error | 1 |
| q_3f62e9c5a606501d | on which continent is athens greece located | ms_marco | Ranking Error | 1 |
| q_57ec9de4da651803 | what is classical ballet | ms_marco | Ranking Error | 1 |
| q_efae5784a06a3f82 | cost of solar | ms_marco | Ranking Error | 1 |
| q_e5125a270b096cec | what is an allele | ms_marco | Ranking Error | 1 |
| q_12616fef3d133179 | What did lane and vail finance? | squad | Semantic Miss | 0 |
| q_a55191e0ff23b27c | normal puppy temperature in celsius | ms_marco | Ranking Error | 1 |
| q_b2c9fce9a9438dca | what is speakonia | ms_marco | Ranking Error | 1 |
| q_9a85eaa6204580e9 | what is subclinical hyperthyroidism | ms_marco | Ranking Error | 1 |
| q_0b005ce15b8769f4 | how much does a middle class person make | ms_marco | Ranking Error | 1 |
| q_ef34a5ec6eacf117 | define broaden | ms_marco | Ranking Error | 1 |
| q_b52fba39033e759e | how long was the titanic's voyage supposed to be | ms_marco | Ranking Error | 1 |
| q_66f26264ca6b0821 | oona name meaning | ms_marco | Ranking Error | 1 |
| q_bdebf5078b790563 | what is matzo made of | ms_marco | Ranking Error | 1 |
| q_805c52a73376d994 | What is another term for nearsightedness? | sciq | Semantic Miss | 0 |
| q_39a7b692f323fd1e | what does mouse stand for computer | ms_marco | Ranking Error | 1 |
| q_2394adfc575327d0 | what is leucine | ms_marco | Ranking Error | 1 |
| q_583513ebd73892d3 | age limit for station master in railways | ms_marco | Ranking Error | 1 |
| q_6826989e5a704fef | new oil furnace should cost | ms_marco | Ranking Error | 1 |
| q_93eff570af9261e6 | average price for new construction per square foot | ms_marco | Ranking Error | 1 |
| q_dda8b3401c9b7696 | what does a cumulonimbus look like | ms_marco | Ranking Error | 1 |
| q_c30e39fd866ccf1a | what is a brachiopod | ms_marco | Ranking Error | 1 |
| q_e3f70d3897189598 | what are two characteristics of fluids | ms_marco | Ranking Error | 1 |
| q_8629698944dc1a3c | what is a agglutination mean | ms_marco | Ranking Error | 1 |
| q_f2a27f7d17a6eba2 | What modern city is located on the original Huguenot colony? | squad | Ranking Error | 1 |
| q_090ddbeb7742feb5 | why is homeostasis important for cells as well as for an entire organism | ms_marco | Ranking Error | 1 |
| q_99ed2e3e4c8c14b4 | how to change a computer name | ms_marco | Semantic Miss | 0 |
| q_0b588086cc035c66 | definition of burpee | ms_marco | Ranking Error | 1 |
| q_2774139278521f1f | inside sales representative vs outside sales representative | ms_marco | Ranking Error | 1 |
| q_50e785af12e6f189 | what causes pimples | ms_marco | Semantic Miss | 0 |
| q_268b163172b913dc | what is salmeterol | ms_marco | Ranking Error | 1 |
| q_0076056c3f3ce3ed | how long to cook picnic ham in slow cooker | ms_marco | Ranking Error | 1 |
| q_ccbd19823c14a305 | what makes it a persian rug | ms_marco | Ranking Error | 1 |
| q_857e41649f026102 | what is a blue heeler | ms_marco | Ranking Error | 1 |
| q_e04cc8dd50a5119e | globalization of markets definition | ms_marco | Ranking Error | 1 |
| q_cd9efabbab795af5 | what language do icelanders speak | ms_marco | Ranking Error | 1 |
| q_d40ad8f2eb2fbe90 | why are some minerals more rare than others | ms_marco | Semantic Miss | 0 |

---

## main_comparison_all_diagnostic.csv

| System | Recall@1 | Recall@3 | Recall@5 | MRR@5 | NDCG@5 |
| --- | --- | --- | --- | --- | --- |
| CogniSync_RRF | 0.830948957183783 | 0.9305370698592114 | 0.9696368257365482 | 0.8901280807945691 | 0.9089037565312228 |
| Dense | 0.7909657893856804 | 0.9069028748509068 | 0.9619330279013254 | 0.8603300672173361 | 0.8844205888986144 |
| Hybrid_Naive | 0.7679229508744942 | 0.8856491544884013 | 0.9455634328774148 | 0.8393973848777715 | 0.8643081396008889 |
| Lexical | 0.7209755988808257 | 0.8310866245304261 | 0.9027288231949973 | 0.790289714521397 | 0.8167286003799067 |

---

## security_comparison_raw.csv

*Skipped raw/master dump to preserve markdown readability. View CSV directly.*

---

