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
        # frozenset for faster keyword lookups
        self.required_keywords = frozenset(["pseudo", "internship", "interest"])

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        filtered = []
        for email in emails:
            subject_lower = email.subject.lower()
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
        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)
        responses_sent = 0
        # end of non-modifiable block

        def send_email(email: Email) -> bool:
            try:
                name = self.extract_name_from_email(email.body)
                response_subject = f"Re: {email.subject}"
                response_body = self.generate_response(name)
                return self.gmail_client.send_email(
                    email.sender, response_subject, response_body
                )
            except Exception:
                return False

        # Safe thread limit (matches first code’s safety cap)
        max_workers = min(50, len(filtered_emails) or 1)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(send_email, filtered_emails, chunksize=4)
            responses_sent = sum(results)

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
