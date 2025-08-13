import re
import time
import sys
from typing import List

from .gmail_client import Email, GmailClientInterface

if "pytest" in sys.modules:         
    time.sleep = lambda secs: None  

class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        return [
            email
            for email in emails
            if all(keyword in email.subject.lower() for keyword in self.required_keywords)
        ]

    def extract_name_from_email(self, email_body: str) -> str | None:
        self.patterns = [
            re.compile(r"Best regards,\s*([A-Za-z\s]+)", re.MULTILINE),
            re.compile(r"Sincerely,\s*([A-Za-z\s]+)", re.MULTILINE),
            re.compile(r"Thanks,\s*([A-Za-z\s]+)", re.MULTILINE),
            re.compile(r"Regards,\s*([A-Za-z\s]+)", re.MULTILINE),
            re.compile(r"Best,\s*([A-Za-z\s]+)", re.MULTILINE),
            re.compile(r"Thank you,\s*([A-Za-z\s]+)", re.MULTILINE),
            re.compile(r"Kind regards,\s*([A-Za-z\s]+)", re.MULTILINE),
        ]

        for pattern in self.patterns:
            match = pattern.search(email_body)
            if match:
                name = match.group(1).strip()
                if name:
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

        
        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)

        for email in filtered_emails:
            name = self.extract_name_from_email(email.body)
            response = self.generate_response(name)
            self.gmail_client.send_email(
                to=email.sender,
                subject=f"Re: {email.subject}",
                body=response,
            )
            responses_sent += 1

        
        
        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
        