import time
import re
import threading

from .gmail_client import Email, GmailClientInterface
from concurrent.futures import ThreadPoolExecutor


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        filtered = []
        for email in emails:
            subject_lower = email.subject.lower()
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered.append(email)
        return filtered

    def extract_name_from_email(self, email_body: str) -> str | None:
        patterns = [
            r"Best regards,\s*([A-Za-z\s]+)",
            r"Sincerely,\s*([A-Za-z\s]+)",
            r"Thanks,\s*([A-Za-z\s]+)",
            r"Regards,\s*([A-Za-z\s]+)",
            r"Best,\s*([A-Za-z\s]+)",
            r"Thank you,\s*([A-Za-z\s]+)",
            r"Kind regards,\s*([A-Za-z\s]+)",
            r"Yours sincerely,\s*([A-Za-z\s]+)",
            r"Yours truly,\s*([A-Za-z\s]+)",
            r"Cheers,\s*([A-Za-z\s]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, email_body, re.IGNORECASE)
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

        # Fetch emails from Gmail
        emails = self.gmail_client.fetch_emails()

        # Filter based on keywords
        filtered_emails = self.filter_emails(emails)

        # Process emails in parallel using multiple threads
        max_workers = min(31, len(filtered_emails))
        if max_workers > 0:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Create all the tasks first
                tasks = {}
                for email in filtered_emails:
                    def process_one_email(e=email):
                        name = self.extract_name_from_email(e.body)
                        response_body = self.generate_response(name)
                        response_subject = f"Re: {e.subject}"
                        return self.gmail_client.send_email(
                            to=e.sender,
                            subject=response_subject,
                            body=response_body
                        )

                    # Submit the task
                    task = executor.submit(process_one_email)
                    tasks[task] = email

                # Wait for all tasks and collect results
                for task in tasks:
                    if task.result():
                        responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
