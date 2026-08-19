# The Data Lake

This is the raw, unpolished storage zone for your diverse data sources. **Antigravity does NOT read directly from here.** 

Everything dropped here requires a **Parsing Script** to translate it into a `.md` file inside `02 - Wiki/` so it can be indexed by the Vector Brain.

## Folders
- `emails/` -> Drop your `.mbox` files here.
- `search_history/` -> Drop `history.json` or CSV exports here.
- `images/` -> Raw image dumps (use OCR scripts to translate).
- `course_data/` -> Drop Google Classroom exports, lecture PDFs, and notes here.
- `internships/` -> Job descriptions, offers, tasks.
- `research_papers/` -> ArXiv PDFs, drafts.
- `personal_docs/` -> Anything else.

*To activate an integration (e.g., Google Classroom Sync), ask Antigravity to "Build the Classroom Parser".*
