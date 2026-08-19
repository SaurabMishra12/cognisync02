---
title: "Deque"
type: concept
tags: [concept, data-structures]
created: 2026-04-12
updated: 2026-04-12
sources: ["2026-04-12 Queue"]
related: ["[[Queue]]"]
---

# Deque (Double-Ended Queue)

> **Domain:** Computer Science / Data Structures
> **First mentioned:** [[sources/2026-04-12 Queue]] (2026-04-12)

---

## Definition

A Deque is a linear data structure that generalizes both Stacks and Queues by allowing both insertions and deletions at *both* the front and the rear.

## Two Main Sub-Types:
1. **Input-Restricted:** Insertion only at one end, deletion at both.
2. **Output-Restricted:** Deletion only at one end, insertion at both.

---

## Systems Context

- **Task Scheduling / Load Balancing:** Used in modern multitasking OS environments and multi-agent schedulers where threads can "steal" work from the back of another thread's deque to maintain load balance (Work Stealing algorithm).
- **LLM Prompt Context Windows:** When maintaining a sliding window of recent conversation history in a memory-constrained agent, operations can be framed as a deque (pop old context from the left, append new from the right). Python's `collections.deque` is highly optimized for this.

---

## Sources

| Source | Contribution to this page |
|--------|--------------------------|
| [[sources/2026-04-12 Queue]] | Basic operations (InsertFront, InsertRear, DeleteFront, DeleteRear) |
