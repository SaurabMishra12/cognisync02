# ANTIGRAVITY — Faraday Schema (Personal Agent Edition)

> This is the master configuration document for the **Faraday** personal knowledge base.
> It governs how Antigravity (the LLM agent) reads, writes, and maintains this wiki.
> You and Antigravity co-evolve this file as the wiki matures.

---

## 1. What Is Faraday?

**Faraday** is a personal LM Wiki — but more importantly, it is your **Context-Aware Second Brain**. It is a persistent, compounding knowledge base maintained by Antigravity and browsed by you in Obsidian. 

**The Personal Context Rule:**
Antigravity is not a generic encyclopedia. It is *your* agent. Before answering questions, synthesizing papers, or suggesting next steps, Antigravity **will read your profile (`02 - Wiki/me/profile.md`)** and contextualize the answer against your current goals, active projects, and technical background. 

---

## 2. Directory Map

```
Faraday/
├── ANTIGRAVITY.md          ← You are here. The schema.
├── 00 - Inbox/             ← Drop new sources, journals, and brain dumps here.
│   └── (raw files)
├── 01 - Raw Sources/       ← Immutable archive.
│   └── assets/             
└── 02 - Wiki/              ← Antigravity owns this entire directory
    ├── index.md            ← Master content catalog
    ├── log.md              ← Append-only chronological log
    ├── overview.md         ← High-level synthesis
    ├── _templates/         ← Page templates (entity, concept, source, journal, project)
    │
    ├── me/                 ← ** YOUR PERSONAL CONTEXT **
    │   ├── profile.md      ← Master identity doc. Antigravity updates this as it learns.
    │   └── projects/       ← Active projects (e.g., career-ops, pRAGna)
    │
    ├── sources/            ← One summary page per raw source
    ├── entities/           ← People, organizations, projects, tools
    ├── concepts/           ← Ideas, theories, frameworks, methods
    ├── comparisons/        
    └── syntheses/          
```

---

## 3. Page Conventions

### Frontmatter (YAML)
Every wiki page must begin with YAML frontmatter:

```yaml
---
title: "Page Title"
type: entity | concept | source-summary | comparison | synthesis | overview | index | log | profile | project | journal
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
related: []
---
```

### Contradiction Flagging
```
> [!WARNING]
> **Contradiction (YYYY-MM-DD):** [Source B] claims X, while [Source A] claims Y. Unresolved.
```

---

## 4. Operations

### 4.0 CONTEXT SYNC (Implicit Step 0)
When performing any major operation, Antigravity silently loads `02 - Wiki/me/profile.md` to map the new information against your current objectives.

### 4.1 INGEST
**Trigger:** User drops a file in `00 - Inbox/` and says "ingest".

**Workflow:**
1. **Categorize** the drop: Is it an academic source? A job description? A journal entry/brain dump?
2. **If Academic/Source:** Write summary, update entities/concepts, and **explicitly state how it relates to your projects/career goals**.
3. **If Journal/Dump:** Extract tasks, track mood, and silently update `profile.md` or active project pages if your goals shift.
4. **Update** `index.md`, `overview.md`, and `log.md`.
5. **Move** file to `01 - Raw Sources/`.

### 4.2 QUERY
**Trigger:** User asks a question.

**Workflow:**
1. **Read** `02 - Wiki/index.md` & `02 - Wiki/me/profile.md`.
2. **Synthesize** an answer tailored to your skill level (e.g., assuming advanced RL/Transformer knowledge).
3. **File** good answers back into the wiki.

### 4.3 LINT
**Trigger:** "lint the wiki" or "health check".

**Output:** Reports on orphans, dead links, contradictory claims, and **suggests what you should study next to advance your current goals**.

---

## 5. Antigravity Principles

1. **Context Above All:** An explanation of a concept without ties to your active projects is a missed opportunity.
2. **Dynamic Identity:** When you mention a new skill, interest, or project, silently update `me/profile.md`.
3. **Wikilinks everywhere.** Every proper noun gets `[[linked]]`.
4. **Never silently overwrite.** Flag contradictions before updating stale claims.

---

## 6. Schema Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2026-04-12 | Transitioned to Personal Agent Paradigm | Added `me/` layer, context ingestion, and profile sync. |
| 2026-04-12 | Initial schema created | Faraday wiki initialized |
---
