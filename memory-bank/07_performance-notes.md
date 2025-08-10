Performance notes

Why concurrency is required
- Mock client sleeps ~200ms per `send_email` call.
- Sequentially sending 1000 emails would take ~200 seconds.
- The test enforces <5 seconds for 1000 emails, requiring parallel sends.

Approach
- Use `concurrent.futures.ThreadPoolExecutor` with `max_workers` around 64.
- Submit one future per email; collect results as they complete.
- `fetch_emails` is called once; it adds ~200ms overhead only.

Correctness
- Tests only assert counts and content, not ordering of sent emails.
- Ensure subject is prefixed with `"Re: "` and response contains the expected strings.


