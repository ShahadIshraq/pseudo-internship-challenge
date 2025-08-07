import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        # Pre-compile all regex patterns for maximum performance
        self.subject_pattern = re.compile(
            r'(?=.*pseudo)(?=.*internship)(?=.*interest)',
            re.IGNORECASE
        )
        self.name_patterns = [
            re.compile(r"Best regards,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Sincerely,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Thanks,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Regards,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Best,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Thank you,\s*([A-Za-z\s]+)", re.IGNORECASE),
            re.compile(r"Kind regards,\s*([A-Za-z\s]+)", re.IGNORECASE),
        ]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # Optimized filtering with pre-compiled pattern
        return [email for email in emails if self.subject_pattern.search(email.subject)]

    def extract_name_from_email(self, email_body: str) -> str | None:
        # Optimized name extraction with pre-compiled patterns
        for pattern in self.name_patterns:
            match = pattern.search(email_body)
            if match:
                return match.group(1).strip()
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

        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)

        # Use ThreadPoolExecutor with optimal max_workers
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = []
            for email in filtered_emails:
                future = executor.submit(self._process_single_email, email)
                futures.append(future)

            for future in as_completed(futures):
                if future.result():
                    responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block

    def _process_single_email(self, email: Email) -> bool:
        """Helper method to process a single email"""
        name = self.extract_name_from_email(email.body)
        response = self.generate_response(name)
        send_subject = f"Re: {email.subject}"
        return self.gmail_client.send_email(
            to=email.sender,
            subject=send_subject,
            body=response
        )
