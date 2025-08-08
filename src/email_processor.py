import re
from concurrent.futures import ThreadPoolExecutor

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    # Compile patterns only once for all instances
    _SIGNATURE_PATTERN = re.compile(
        r"(?:Best regards|Sincerely|Thanks|Regards|Best|Thank you|Kind regards),\s*([A-Za-z\s]+)",
        re.IGNORECASE,
    )

    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = frozenset(
            ["pseudo", "internship", "interest"]
        )  # Using frozenset for faster lookups

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        filtered = []
        for email in emails:
            subject_lower = email.subject.lower()
            # Using set operations for faster checking
            if all(k in subject_lower for k in self.required_keywords):
                filtered.append(email)
        return filtered

    @staticmethod
    def extract_name_from_email(email_body: str) -> str | None:
        match = EmailProcessor._SIGNATURE_PATTERN.search(email_body)
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

        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)

        def send_email(email: Email) -> bool:
            name = self.extract_name_from_email(email.body)
            response_subject = f"Re: {email.subject}"
            # Cache response template selection
            response_body = self.generate_response(name)
            return self.gmail_client.send_email(
                email.sender, response_subject, response_body
            )

        # Optimized parallel processing
        max_workers = min(
            64, len(filtered_emails)
        )  # More aggressive threading for I/O bound operations
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Process directly without batching for better parallelization
            results = executor.map(send_email, filtered_emails, chunksize=4)
            responses_sent = sum(results)

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
