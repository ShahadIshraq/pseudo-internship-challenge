import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        self.name_patterns = [
            re.compile(r"Best regards,\s*([A-Za-z\s]+)"),
            re.compile(r"Sincerely,\s*([A-Za-z\s]+)"),
            re.compile(r"Thanks,\s*([A-Za-z\s]+)"),
            re.compile(r"Regards,\s*([A-Za-z\s]+)"),
            re.compile(r"Best,\s*([A-Za-z\s]+)"),
            re.compile(r"Thank you,\s*([A-Za-z\s]+)"),
            re.compile(r"Kind regards,\s*([A-Za-z\s]+)"),
        ]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        filtered = []
        for email in emails:
            subject_lower = email.subject.lower()
            if all(
                keyword.lower() in subject_lower for keyword in self.required_keywords
            ):
                filtered.append(email)
        return filtered

    def extract_name_from_email(self, email_body: str) -> str | None:
        for pattern in self.name_patterns:
            match = pattern.search(email_body)
            if match:
                name = match.group(1).strip()
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

    def _send_email_response(self, email: Email) -> bool:
        # Extract name from email body
        name = self.extract_name_from_email(email.body)

        # Generate response using provided method
        response_body = self.generate_response(name)

        # Send response with proper subject format
        subject = f"Re: {email.subject}"
        return self.gmail_client.send_email(email.sender, subject, response_body)

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = []
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        # Fetch emails from Gmail client
        emails = self.gmail_client.fetch_emails()

        # Filter emails based on required keywords
        filtered_emails = self.filter_emails(emails)

        # Send responses to all filtered emails using parallel processing
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Submit all email sending tasks
            future_to_email = {
                executor.submit(self._send_email_response, email): email
                for email in filtered_emails
            }

            # Collect results as they complete
            for future in as_completed(future_to_email):
                if future.result():
                    responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
