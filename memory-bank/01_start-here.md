Start here

- Purpose: quick guide to run tests like CI and the minimal plan to get all tests green (no code changes in this step).

- CI Python version: 3.11 (from `.github/workflows/code-quality.yml`). Use a 3.11 venv locally.

What we ran locally (Python 3.11):
- Lint: ruff reported a few issues in `src/email_processor.py` and a trailing-whitespace warning in `tests/test_email_processor.py`.
- Tests: 10 collected; 3 passed, 7 failed. Failures are due to unimplemented logic in `EmailProcessor`.

Key fixes needed (to be implemented later):
1) `EmailProcessor.filter_emails`: select emails whose subject contains all of the required keywords: "pseudo", "internship", "interest" (case-insensitive), while preserving input order.
2) `EmailProcessor.extract_name_from_email`: extract sender name from signatures like:
   - "Best regards,\n{name}"
   - "Sincerely,\n{name}"
   - "Thanks,\n{name}"
   - "Regards,\n{name}"
   - "Best,\n{name}"
   Return `None` if not present.
3) `EmailProcessor.process_emails`:
   - Fetch emails once from the `gmail_client`.
   - Filter them using `filter_emails`.
   - For each filtered email, extract name and generate a response via `generate_response(name)`.
   - Send responses with subject prefixed by `"Re: "` using the client.
   - Performance: parallelize sending with a thread pool so 1000 emails complete under 5s (Mock client sleeps 200ms per send, so concurrency is required).

Read next:
- 02_ci-alignment.md
- 03_test-failures.md
- 04_solution-design.md
- 05_step-by-step-implementation.md
- 06_commands.md
- 07_performance-notes.md
- 08_success-criteria.md


