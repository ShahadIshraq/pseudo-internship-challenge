Success criteria

- Linting:
  - `ruff check src/ tests/` reports no errors.
  - `black --check --diff src/ tests/` passes.
  - `ruff format --check src/ tests/` passes.
  - `mypy src/` passes.

- Tests:
  - `pytest -v` passes all tests.
  - Specifically:
    - Filtering returns exactly the valid set.
    - Name extraction accuracy thresholds are met (≥45/50; ≥20/25 none).
    - End-to-end: totals, filtered count, and responses sent match; subject starts with `"Re: "`.
    - Performance: 1000 emails processed under 5 seconds on the provided mock.


