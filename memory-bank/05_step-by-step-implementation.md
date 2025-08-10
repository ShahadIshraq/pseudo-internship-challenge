Step-by-step implementation (to be done when approved)

1) `filter_emails`
   - Build `required = {"pseudo", "internship", "interest"}`.
   - For each email, lowercase subject and check `all(k in subject for k in required)`.
   - Append matching emails to result, preserving order.

2) `extract_name_from_email`
   - Use regex: look for one of the closers followed by a newline and capture `([A-Za-z][A-Za-z ]*[A-Za-z])`.
   - Try multiple closers; return the first match group stripped; else `None`.

3) `process_emails`
   - Fetch emails: `emails = self.gmail_client.fetch_emails()`.
   - Filter: `filtered_emails = self.filter_emails(emails)`.
   - Prepare tasks for each filtered email: compute name and response body, then send.
   - Concurrency: `ThreadPoolExecutor(max_workers=64)` to call `self.gmail_client.send_email(...)`.
   - Count `responses_sent` by summing `future.result()` truthiness.
   - Return dict with counts.

4) Clean up lint
   - Remove unused import `time` in `email_processor.py`.
   - Strip trailing whitespace lines.

5) Verify
   - Run ruff, mypy, black check, pytest.
   - Ensure tests pass within performance threshold.


