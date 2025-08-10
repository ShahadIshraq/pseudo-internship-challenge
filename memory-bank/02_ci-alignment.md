CI alignment

- Workflow file: `.github/workflows/code-quality.yml`
  - Python: 3.11
  - Steps:
    - Install with `pip install -r requirements.txt` then `pip install ruff mypy black pytest`
    - Ruff checks: `ruff check src/ tests/`
    - Mypy: `mypy src/`
    - Black check: `black --check --diff src/ tests/`
    - Ruff format check: `ruff format --check src/ tests/`
    - Unused imports: `ruff check --select F401 src/ tests/`
    - Import sorting: `ruff check --select I src/ tests/`
    - Tests: `python -m pytest tests/ -v`

- Local reproduction:
  - Use Python 3.11 for the virtualenv (required for `X | Y` typing syntax already present in `src/gmail_client.py`).
  - Run the same lint and test commands as CI.


