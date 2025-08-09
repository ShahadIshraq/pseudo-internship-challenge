import re
from concurrent.futures import ThreadPoolExecutor

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        filtered = []

        for email in emails:
            subject = email.subject.lower()
            found_all = True
            for keyword in self.required_keywords:
                if keyword not in subject:
                    found_all = False
                    break

            if found_all:
                filtered.append(email)

        return filtered

    def extract_name_from_email(self, email_body: str) -> str | None:
        patterns = [
            r"Best regards,\s*([A-Za-z\s]+)",
            r"Sincerely,\s*([A-Za-z\s]+)",
            r"Thanks,\s*([A-Za-z\s]+)",
            r"Regards,\s*([A-Za-z\s]+)",
            r"Best,\s*([A-Za-z\s]+)",
        ]

        # implement name extraction logic
        normalized_body = re.sub(r"(?i)Thank you,", "Thanks,", email_body)
        normalized_body = re.sub(r"(?i)Kind regards,", "Regards,", normalized_body)

        for pattern in patterns:
            match = re.search(pattern, normalized_body, re.IGNORECASE)
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
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [
                executor.submit(
                    self.gmail_client.send_email,
                    to=email.recipient,
                    subject=f"Re: {email.subject}",
                    body=self.generate_response(
                        self.extract_name_from_email(email.body)
                    ),
                )
                for email in filtered_emails
            ]
            for f in futures:
                if f.result():
                    responses_sent += 1
        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
