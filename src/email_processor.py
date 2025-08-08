import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
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
        ]

        # implement name extraction logic
        for pattern in patterns:
            match = re.search(pattern, email_body, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if name and " " in name:
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
        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)
        responses_sent = 0
        # end of non-modifiable block

        def send_single_response(email: Email) -> bool:
            try:
                name = self.extract_name_from_email(email.body)
                response_body = self.generate_response(name)
                subject_reply = f"Re: {email.subject}"
                return self.gmail_client.send_email(
                    to=email.sender,
                    subject=subject_reply,
                    body=response_body,
                )
            except Exception:
                # Optionally log exception here
                return False

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(send_single_response, email) for email in filtered_emails]

            for future in as_completed(futures):
                if future.result():
                    responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
