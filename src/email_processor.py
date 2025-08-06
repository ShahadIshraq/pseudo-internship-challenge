import concurrent.futures
import re

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        # Pre-compile regex patterns for better performance
        self.name_patterns = [
            re.compile(r"Best regards,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Sincerely,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Thanks,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Regards,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Best,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Thank you,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Kind regards,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
        ]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # Optimized filtering using list comprehension for better performance
        return [
            email
            for email in emails
            if all(
                keyword in email.subject.lower() for keyword in self.required_keywords
            )
        ]

    def extract_name_from_email(self, email_body: str) -> str | None:
        # Optimized name extraction using compiled regex patterns
        for pattern in self.name_patterns:
            match = pattern.search(email_body)
            if match:
                name = match.group(1).strip()
                if name:  # Make sure we have a non-empty name
                    return name
        return None

    # Use this method. Do not modify it.
    def generate_response(self, name: str | None) -> str:
        if name:
            return f"""Dear {name},

Thank you for your interest in our pseudo internship program. We have received your application and will review it carefully.

We will get back to you within 5-7 business days with an update on your application status.

Best regards,
Hiring Team"""
        else:
            return """Dear Applicant,

Thank you for your interest in our pseudo internship program. We have received your application and will review it carefully.

We will get back to you within 5-7 business days with an update on your application status.

Best regards,
Hiring Team"""

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = []
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        # 1. Fetch emails from the gmail client
        emails = self.gmail_client.fetch_emails()

        # 2. Filter emails based on required keywords
        filtered_emails = self.filter_emails(emails)

        # 3. Process each filtered email with maximum parallelization
        responses_to_send = []
        # Pre-process all data without API calls
        for email in filtered_emails:
            name = self.extract_name_from_email(email.body)
            response_body = self.generate_response(name)
            reply_subject = f"Re: {email.subject}"
            responses_to_send.append((email.sender, reply_subject, response_body))

        # 4. Send emails using thread pool with increased workers for maximum parallelization
        def send_single_email(email_data: tuple[str, str, str]) -> bool:
            sender, subject, body = email_data
            return self.gmail_client.send_email(sender, subject, body)

        # Use maximum parallelization - increase max_workers to handle more concurrent operations
        # This is the key optimization: more threads = faster processing of I/O bound operations
        max_workers = min(50, len(responses_to_send)) if responses_to_send else 1

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all send operations
            future_to_email = {
                executor.submit(send_single_email, email_data): email_data
                for email_data in responses_to_send
            }

            # Collect results
            for future in concurrent.futures.as_completed(future_to_email):
                if future.result():
                    responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
