import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        # Pre-compile regex patterns for efficiency and add multiline support
        self.name_patterns = [
            re.compile(p, re.IGNORECASE | re.MULTILINE) for p in [
                r"^\s*Best regards,\s*([A-Za-z\s]+)",
                r"^\s*Sincerely,\s*([A-Za-z\s]+)",
                r"^\s*Thanks,\s*([A-Za-z\s]+)",
                r"^\s*Regards,\s*([A-Za-z\s]+)",
                r"^\s*Best,\s*([A-Za-z\s]+)",
                r"^\s*Thank you,\s*([A-Za-z\s]+)",
                r"^\s*Kind regards,\s*([A-Za-z\s]+)",
            ]
        ]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        """
        Filters emails to only include those that contain all the required keywords in the subject.
        """
        filtered_emails = []
        for email in emails:
            subject_lower = email.subject.lower()
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered_emails.append(email)
        return filtered_emails

    def extract_name_from_email(self, email_body: str) -> str | None:
        """
        Extracts the sender's name from the email body using pre-compiled regex patterns.
        """
        for pattern in self.name_patterns:
            match = pattern.search(email_body)
            if match:
                # Extract the name, which is the first capturing group
                name = match.group(1).strip()
                # A simple check to avoid matching large chunks of the email body
                if '\n' not in name:
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
        """
        Processes emails by fetching, filtering, and sending responses concurrently.
        """
        # Do not modify this block
        emails = []
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)

        # Use a ThreadPoolExecutor to send emails concurrently to meet performance requirements
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_email = {}
            for email in filtered_emails:
                name = self.extract_name_from_email(email.body)
                response_body = self.generate_response(name)
                response_subject = f"Re: {email.subject}"

                # Submit the send_email task to the executor
                future = executor.submit(self.gmail_client.send_email, email.sender, response_subject, response_body)
                future_to_email[future] = email

            # Process results as they are completed
            for future in as_completed(future_to_email):
                try:
                    success = future.result()
                    if success:
                        responses_sent += 1
                except Exception:
                    pass

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block