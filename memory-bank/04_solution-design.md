Solution design

Core behavior
- Required keywords: ["pseudo", "internship", "interest"].
- Filter rule: subject must contain all three keywords, case-insensitive, preserve input order.
- Name extraction: detect signatures in body endings:
  - Closers: "Best regards,", "Sincerely,", "Thanks,", "Regards,", "Best,"
  - Name is on the next line; capture letters and spaces only.
  - Return `None` if not found.
- Response body: use provided `generate_response(name)` method.
- Process flow:
  1) `emails = gmail_client.fetch_emails()` once
  2) `filtered = filter_emails(emails)`
  3) For each filtered email:
     - `name = extract_name_from_email(email.body)`
     - `resp_body = generate_response(name)`
     - `subject = f"Re: {email.subject}"`
     - `gmail_client.send_email(email.sender, subject, resp_body)`
  4) Return counts: total, filtered, responses_sent

Performance considerations
- Mock client sleeps ~200ms per `fetch_emails` and per `send_email`.
- Single fetch cost: ~200ms; acceptable.
- Sending must be parallelized to meet <5s for 1000 emails.
  - Use `ThreadPoolExecutor(max_workers=32..64)` to saturate IO wait.
  - Submit all send tasks; count successful futures.
  - Keep extraction and response generation inline (CPU-light).
  - Ensure stable ordering not required by tests; only counts and content are checked.

Type/signature notes
- Keep `EmailProcessor` signatures intact.
- Avoid importing heavy Google libs; tests use `MockGmailClient`.

Lint/style
- Remove unused imports and stray whitespace.
- Keep code black/ruff compliant.


