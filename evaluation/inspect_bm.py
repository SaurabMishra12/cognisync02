import json

bm = json.load(open('results/data/cognisync_benchmark.json', encoding='utf-8'))
qs = bm['eval_queries']
sess = bm['sessions']

print("=== BENCHMARK v2.0 STATS ===")
print(f"Sessions : {len(sess)}")
print(f"Queries  : {len(qs)}")
diff_counts = {}
for q in qs:
    diff_counts[q['difficulty']] = diff_counts.get(q['difficulty'], 0) + 1
print(f"Difficulty: {diff_counts}")
print()

# Sample one of each difficulty
for diff in ('easy', 'medium', 'hard'):
    q = next(x for x in qs if x['difficulty'] == diff)
    print(f"--- {diff.upper()} ---")
    print(f"  query : {q['query']}")
    print(f"  gt    : {q['ground_truth_chunk_ids']}")
    print(f"  type  : {q['task_type']}")
    print()

# Sample sessions by turn
print("=== SESSION EXAMPLES ===")
for turn in (1, 2, 3, 4, 5):
    s = next(x for x in sess if x['turn'] == turn)
    print(f"Turn {turn}: {s['content'][:120]}")
