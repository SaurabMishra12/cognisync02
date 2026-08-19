---
title: "Circular Queue"
type: concept
tags: [concept, data-structures]
created: 2026-04-12
updated: 2026-04-12
sources: ["2026-04-12 Queue"]
related: ["[[Queue]]"]
---

# Circular Queue

> **Domain:** Computer Science / Data Structures
> **First mentioned:** [[sources/2026-04-12 Queue]] (2026-04-12)

---

## Core Idea

A Circular Queue is an advanced form of a queue where the last position is logically connected back to the first position. When the `rear` reaches the end of the array, it wraps around to the beginning (index 0), provided the space is empty.

**Condition for moving pointers:** `rear = (rear + 1) mod size`

---

## Contextual Importance (Agentic RL)

For your research in alignment and training (e.g., AURA, RL algorithms):
- **Experience Replay Buffers:** Deep Reinforcement Learning agents (like DQN) store past transitions `(state, action, reward, next_state)` in a replay memory. This memory is typically implemented conceptually as a massive Circular Queue. Once the buffer is full, the oldest experiences are naturally overwritten by the newest, ensuring the agent learns from recent data without indefinite memory growth.

---

## See Also

- [[concepts/Queue]] — The parent data structure.

## Sources

| Source | Contribution to this page |
|--------|--------------------------|
| [[sources/2026-04-12 Queue]] | Overflow logic, modulo arithmetic, pointer wrapping |
