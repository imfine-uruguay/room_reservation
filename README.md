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