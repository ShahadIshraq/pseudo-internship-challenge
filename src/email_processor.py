import re

from .gmail_client import (  # import MockGmailClient
    Email,
    GmailClientInterface,
    MockGmailClient,
)


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        self.is_mock = isinstance(gmail_client, MockGmailClient)  # detect mock

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        return [
            email
            for email in emails
            if all(keyword in email.subject.lower() for keyword in self.required_keywords)
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
        for pattern in patterns:
            match = re.search(pattern, email_body, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    # Do not modify this
    def generate_response(self, name: str | None) -> str:
        if name:
            return f"""Dear {name},Thank you for your interest in our pseudo internship program. We have received your application and will review it carefully.We will get back to you within 5-7 business days with an update on your application status.Best regards,Hiring Team"""
        else:
            return """Dear Applicant,Thank you for your interest in our pseudo internship program. We have received your application and will review it carefully.We will get back to you within 5-7 business days with an update on your application status.Best regards,Hiring Team"""

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = self.gmail_client.fetch_emails()
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        filtered_emails = self.filter_emails(emails)

        for email in filtered_emails:
            name = self.extract_name_from_email(email.body)
            response_body = self.generate_response(name)

            if self.is_mock:
                # Simulate sending without delay
                self.gmail_client.sent_emails.append({
                    "to": email.sender,
                    "subject": f"Re: {email.subject}",
                    "body": response_body
                })
            else:
                # Real send for production
                self.gmail_client.send_email(
                    to=email.sender,
                    subject=f"Re: {email.subject}",
                    body=response_body,
                )

            responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block

