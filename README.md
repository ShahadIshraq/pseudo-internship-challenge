# Email Processor Optimization

## Key Changes

### 1. `extract_name_from_email` function
- Pre-compiled regular expression pattern in constructor for improved performance
- Added support for additional signature patterns (Kind regards, Thank you)

### 2. `filter_emails` function
- Implemented keyword filtering to check all required keywords are present in email subject

### 3. `process_emails` function
- Implemented parallel email processing using `ThreadPoolExecutor`
- Addresses the 200ms delay per email by processing multiple emails concurrently
- Added error handling for individual email processing failures