import re
import time
from concurrent.futures import ThreadPoolExecutor
from .gmail_client import GmailClientInterface, Email


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        self.max_workers = 20  # limit concurrency for API safety

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        """Return only emails containing all required keywords (case-insensitive)."""
        filtered = []
        for email in emails:
            content = (email.subject + " " + email.body).lower()
            if all(kw.lower() in content for kw in self.required_keywords):
                filtered.append(email)
        return filtered

    def extract_name_from_email(self, email_body: str) -> str | None:
        """Extracts a name from the email body based on common sign-off patterns."""
        patterns = [
            r"(?i)Best regards,?\s*\n(.+)",
            r"(?i)Sincerely,?\s*\n(.+)",
            r"(?i)Thanks,?\s*\n(.+)",
            r"(?i)Regards,?\s*\n(.+)",
            r"(?i)Best,?\s*\n(.+)",
            r"(?i)Thank you,?\s*\n(.+)",
            r"(?i)Kind regards,?\s*\n(.+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, email_body)
            if match:
                name_line = match.group(1)
                name = name_line.strip()
                if name and any(c.isalpha() for c in name):
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

    def _send_email_with_delay(self, email: Email, response: str):
        """Helper to simulate sending delay."""
        time.sleep(0.01)
        self.gmail_client.send_email(email.sender, response)

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = []
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        # Implementation
        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for email in filtered_emails:
                name = self.extract_name_from_email(email.body)
                response = self.generate_response(name)
                futures.append(executor.submit(self._send_email_with_delay, email, response))

            for f in futures:
                f.result()
                responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block

