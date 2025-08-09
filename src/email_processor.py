import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    MAX_WORKERS = 50
    NAME_PATTERNS = [
        r"Best regards,\s*([A-Za-z\s]+)",
        r"Sincerely,\s*([A-Za-z\s]+)",
        r"Thanks,\s*([A-Za-z\s]+)",
        r"Regards,\s*([A-Za-z\s]+)",
        r"Best,\s*([A-Za-z\s]+)",
        r"Thank you,\s*([A-Za-z\s]+)",
        r"Kind regards,\s*([A-Za-z\s]+)",
    ]
        
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        filtered_emails = []
        for email in emails:
            subject_lower = email.subject.lower()
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered_emails.append(email)
        return filtered_emails

    def extract_name_from_email(self, email_body: str) -> str | None:
        # implement name extraction logic
        for pattern in self.NAME_PATTERNS:
            match = re.search(pattern, email_body, flags=re.IGNORECASE)
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

        if not filtered_emails:
            return {
                "total_emails": len(emails),
                "filtered_emails": 0,
                "responses_sent": 0,
            }

        # use ThreadPoolExecutor to send responses concurrently
        futures = []
        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            for email in filtered_emails:
                name = self.extract_name_from_email(email.body)
                response_body = self.generate_response(name)

                future = executor.submit(
                    self.gmail_client.send_email,
                    to=email.sender,
                    subject="Re: " + email.subject,
                    body=response_body,
                )
                futures.append(future)

            # process results as they complete
            for future in as_completed(futures):
                try:
                    if future.result():
                        responses_sent += 1
                except Exception as e:
                    print(f"[Error] Failed to send email: {e}")

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
