AI_reporter/
├─ run_digest.py ← Entry point/orchestrator for one full run
├─ requirements.txt ← Python dependencies (installed into .venv)
├─ .env ← Template of environment variables (no secrets)
├─ .gitignore ← Files/folders to ignore in git (e.g., .venv, .env)
├─ README.md ← Project intro, setup, and usage
├─ dev.sh / dev.ps1 ← Optional developer helper scripts (setup/run/test)
│
├─ config/ ← Configuration parsing & constants
│ └─ settings.py ← Reads env vars (e.g., FEED_URLS, MAX_ITEMS)
│
├─ sources/ ← Data source adapters
│ └─ rss.py ← Fetch & parse RSS/Atom feeds → Article objects
│
├─ core/ ← Domain logic (pure, testable)
│ ├─ models.py ← Dataclasses/types: Article, DigestItem
│ ├─ selection.py ← Tech filter + random‑3 selector (+ deterministic seed)
│ ├─ summarize.py ← Extractive summary (short, 1–2 sentences)
│ └─ formatters.py ← Output builders (console/Markdown/HTML)
│
├─ delivery/ ← Output channels (pluggable)
│ ├─ telegram.py ← Telegram Bot API sender
│ 
├─ state/ ← Runtime state & run metadata (git-ignored by default)
│ └─ state.json ← De‑dup cache (IDs already sent)
│
├─ tests/ ← Unit/integration tests
│ ├─ test_selection.py ← Validates tech filter & sampler behavior
│ └─ conftest.py ← Pytest config/fixtures 
│
└─ .github/
└─ workflows/
└─ daily-digest.yml ← GitHub Actions scheduler (daily cron; later)