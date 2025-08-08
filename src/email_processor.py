import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        filtered_emails = []
        for email in emails:
            subject_lower = email.subject.lower()
            # Require ALL keywords to be present for stricter filtering
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered_emails.append(email)
        return filtered_emails

    def filtered_emails_generator(self, emails):
        for email in emails:
            subject_lower = email.subject.lower()
            if all(keyword in subject_lower for keyword in self.required_keywords):
                yield email

    def extract_name_from_email(self, email_body: str) -> str | None:
        patterns = [
            r"Best regards,\s*([A-Za-z\s]+)",
            r"Sincerely,\s*([A-Za-z\s]+)",
            r"Thanks,\s*([A-Za-z\s]+)",
            r"Regards,\s*([A-Za-z\s]+)",
            r"Best,\s*([A-Za-z\s]+)",
            r"Kind regards,\s*([A-Za-z\s]+)",
            r"Thank you,\s*([A-Za-z\s]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, email_body)
            if match:
                return match.group(1).strip()
        return None

    def _process_single_email(self, email: Email) -> bool:
        """Process a single email and return True if successful."""
        try:
            name = self.extract_name_from_email(email.body)
            response = self.generate_response(name)
            reply_subject = f"Re: {email.subject}"
            self.gmail_client.send_email(
                to=email.sender, subject=reply_subject, body=response
            )
            return True
        except Exception:
            return False

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

        # Ensure emails is a list so len() works in return block
        if not hasattr(emails, "__len__"):
            emails = list(emails)

        filtered_emails_iter = self.filtered_emails_generator(emails)
        filtered_emails = list(filtered_emails_iter)
        filtered_emails_count = len(filtered_emails)

        max_workers = min(50, max(5, filtered_emails_count))

        responses_sent = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self._process_single_email, email)
                for email in filtered_emails
            ]

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
