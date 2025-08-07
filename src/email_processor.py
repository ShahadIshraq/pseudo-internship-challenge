import re
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

from .gmail_client import Email, GmailClient 


class EmailProcessor:
    def __init__(self, gmail_client: GmailClient):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
    
    #filtering emails based on the required keywords
    def filter_emails(self, emails: List[Email]) -> List[Email]:
        filtered_emails: List[Email] = []
        for email in emails:
            subject = email.subject.lower()
            if all(keyword in subject for keyword in self.required_keywords):
                filtered_emails.append(email)
        return filtered_emails

    def extract_name_from_email(self, email_body: str) -> Optional[str]:
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
            match = re.search(pattern, email_body, flags=re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if name:
                    return name

        return None

    # Use this method. Do not modify it.
    def generate_response(self, name: Optional[str]) -> str:
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

        def send_email_task(email: Email) -> bool:
            name = self.extract_name_from_email(email.body)
            response = self.generate_response(name)
            return self.gmail_client.send_email(
                to=email.sender, subject=f"Re: {email.subject}", body=response
            )

        with ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(send_email_task, filtered_emails)
            responses_sent = sum(1 for result in results if result)

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block