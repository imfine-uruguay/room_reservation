# My Python Project (`roombooking_agent`)

This project uses **[uv](https://github.com/astral-sh/uv)** as a package and virtual environment manager. `uv` is an extremely fast Python project manager written in Rust, designed to replace tools like `pip`, `pip-tools`, `poetry`, `pipenv`, and `virtualenv`.

---

## Why `uv`? Key Advantages

- **Extremely fast performance:** 10x to 100x faster than `pip` or `poetry`.
- **Integrated management:** Handles Python versions, virtual environments, and dependencies from `pyproject.toml`.
- **Deterministic locking (`uv.lock`):** Generates fast and universal lock files to ensure exact reproducibility.
- **Space efficiency:** Uses a global deduplicated cache to avoid duplicating packages on disk.

---

## Project Initialization

### 1. Install `uv`

If you don't have it installed yet:

```bash
# macOS/Linux:
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# Windows (PowerShell):
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

## 2. Initialize the project

```bash
#Wherever operating system you are on, run the following command to initialize the project
uv sync

## To set up the project, a .env file must be created:

```python
# ── LLM ──
LLM_MODEL_IN_GROP=llama-3.3-70b-versatile
LLM_MODEL_URL=https://api.groq.com/openai/v1
LLM_MODEL_TEMPERATURE=0.0
LLM_MODEL_PROVIDER=GROQ
LLM_MODEL_API_KEY=your_api_key_here

DB_ENGINE=sqlite
SQLITE_DB_PATH=utils/database/call_agent_ai_sqlite.db

BACKEND_CORS_ORIGINS="*"

PROJECT_NAME=Call_Agent_AI
API_STR=/api

ROOT_PATH=/call_agent_ai

SSL_ENABLED=false


PYTHONPATH=.


APP_NAME=call_agent_ai
APP_ENV=production
LOG_ENABLED=true
LOG_STDOUT=false
LOG_DIR=./logs
LOG_PRIMARY_DIR=/var/log/call_agent_ai