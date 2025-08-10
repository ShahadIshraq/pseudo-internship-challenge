Commands to reproduce CI locally (Python 3.11)

Setup (macOS with pyenv-installed 3.11.7):

```bash
cd /Users/tomchamp/Documents/temp_repo/pseudo-internship-challenge
rm -rf .venv
/Users/tomchamp/.pyenv/versions/3.11.7/bin/python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Quality checks:

```bash
ruff check src/ tests/
mypy src/
black --check --diff src/ tests/
ruff format --check src/ tests/
ruff check --select F401 src/ tests/
ruff check --select I src/ tests/
```

Run tests:

```bash
python -m pytest tests/ -v
```


