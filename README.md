# Pseudo Internship Challenge

## Changes

- All the changes were done in the file `src/email_processor.py`
- **Filter Emails**:
  - Looked if all keywords are found in the lowercase subject of every email
  - Lowercase subject is calculated only once per email
- **Name Extraction**:
  - Used compiled regex patterns
  - Stored those patterns as protected instance variable
  - Calculated only once since patterns remain constant
  - Added two new patterns following the test data
- **Process Emails**:
  - Used simple threads to call the methods in email_processing and gmail_client
  - 1 thread per email
  - Used a shared counter array where 1 is appended on successful email sending (thread-safe)
  - A separate private method named `_send_single_email` is defined where a single email is sent in a thread 
