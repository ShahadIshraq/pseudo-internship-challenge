import re
import time
import concurrent.futures
from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        
        # Compile regex patterns once and store them.
        
        self.name_extraction_patterns = [
            re.compile(p, re.IGNORECASE | re.MULTILINE) for p in [
                r"Best regards,\s*([A-Za-z\s]+)",
                r"Sincerely,\s*([A-Za-z\s]+)",
                r"Thanks,\s*([A-Za-z\s]+)",
                r"Regards,\s*([A-Za-z\s]+)",
                r"Best,\s*([A-Za-z\s]+)",
                r"Thank you,\s*([A-Za-z\s]+)",
                r"Kind regards,\s*([A-Za-z\s]+)",
            ]
        ]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        """
        Filters emails based on required keywords in the subject.
        """
        filtered = []
        for email in emails:
            subject_lower = email.subject.lower()
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered.append(email)
        return filtered

    def extract_name_from_email(self, email_body: str) -> str | None:
        """
        Extracts a name from the email body using pre-compiled regex patterns.
        """
        for pattern in self.name_extraction_patterns:
            match = pattern.search(email_body)
            if match:
                name = match.group(1).strip()
                if name:
                    return name
        return None

    
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

        def process_and_send(email: Email) -> bool:
            name = self.extract_name_from_email(email.body)
            response_body = self.generate_response(name)
            response_subject = f"Re: {email.subject}"
            return self.gmail_client.send_email(
                to=email.sender, subject=response_subject, body=response_body
            )

        num_emails_to_send = len(filtered_emails)
        if num_emails_to_send > 0:
            # This ensures all I/O operations (send_email) run in parallel.
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_emails_to_send) as executor:
                results = executor.map(process_and_send, filtered_emails)
                responses_sent = sum(1 for result in results if result)

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block