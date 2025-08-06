import re
from concurrent.futures import ThreadPoolExecutor

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        return [
            email
            for email in emails
            if (
                (subj_lower := email.subject.lower())
                and all(keyword in subj_lower for keyword in self.required_keywords)
            )
        ]

    def extract_name_from_email(self, email_body: str) -> str | None:
        patterns = [
            r"Best regards,\s*([A-Za-z\s]+)",
            r"Sincerely,\s*([A-Za-z\s]+)",
            r"Thanks,\s*([A-Za-z\s]+)",
            r"Regards,\s*([A-Za-z\s]+)",
            r"Best,\s*([A-Za-z\s]+)",
            r"Thank you,\s*([A-Za-z\s]+)",
            r"Kind regards,\s*([A-Za-z\s]+)",
        ]

        # implement name extraction logic
        if not hasattr(self, "_compiled_patterns"):
            self._compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]

        for pattern in self._compiled_patterns:
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

        # implement email processing logic.
        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)

        counter: list = []
        num_workers = len(filtered_emails) // 10 + 1

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            for email in filtered_emails:
                executor.submit(self._send_single_email, email, counter)

        responses_sent = len(counter)

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block

    def _send_single_email(self, email: Email, counter: list) -> None:
        name = self.extract_name_from_email(email.body)
        response = self.generate_response(name)
        response_subject = f"Re: {email.subject}"

        if self.gmail_client.send_email(email.recipient, response_subject, response):
            counter.append(1)
