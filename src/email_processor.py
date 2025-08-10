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
            txt = f"{email.subject}".lower()
            if all(keyword.lower() in txt for keyword in self.required_keywords):
                filtered.append(email)

        return filtered

    def extract_name_from_email(self, email_body: str) -> str | None:
        patterns = [
            r"Best regards,\s*([A-Za-z\s]+)",
            r"Sincerely,\s*([A-Za-z\s]+)",
            r"Thanks,\s*([A-Za-z\s]+)",
            r"Regards,\s*([A-Za-z\s]+)",
            r"Best,\s*([A-Za-z\s]+)",
            r"Kind regards,\s*([A-Za-z\s]+)",
            r"Thank you,\s*([A-Za-z\s]+)",
            r"Yours truly,\s*([A-Za-z\s]+)",
        ]

        # implement name extraction logic

        for pattern in patterns:
            match = re.search(pattern, email_body, re.IGNORECASE)
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

    def send_single_email(self, email: Email) -> bool:
        found_names = self.extract_name_from_email(email_body=email.body)
        response_body = self.generate_response(found_names)
        return self.gmail_client.send_email(
            to=email.sender,
            subject="Re: Application Received for the Pseudo Internship Program",
            body=response_body,
        )

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = []
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        # implement email processing logic.

        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails=emails)

        with ThreadPoolExecutor(max_workers=50) as executor:
            res = list(executor.map(self.send_single_email, filtered_emails))
            responses_sent = sum(res)

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
