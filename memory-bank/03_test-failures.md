Test failures (Python 3.11)

- Total tests: 10
- Passed: 3
- Failed: 7

Failing tests and causes:
- test_filter_emails_with_all_keywords: `filter_emails` returns empty list; must filter by all required keywords in subject (case-insensitive).
- test_extract_name_from_email_various_formats: `extract_name_from_email` returns None; needs regex to capture signatures on the next line after specific closings.
- test_process_emails_basic_functionality: `process_emails` returns zeros; needs full fetch-filter-respond pipeline.
- test_email_filtering_accuracy: expects 100 valid filtered of 200 mixed; `filter_emails` unimplemented.
- test_name_extraction_accuracy: expects ≥45/50 names extracted; `extract_name_from_email` unimplemented.
- test_end_to_end_processing_with_mixed_data: totals and counts zero; `process_emails` unimplemented and must send responses only to filtered set.
- test_performance_with_1000_emails: needs to finish under 5 seconds; must parallelize sends (and possibly extractions) due to mock 200ms latency.


