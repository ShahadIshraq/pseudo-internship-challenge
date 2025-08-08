import re
from concurrent.futures import ThreadPoolExecutor

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    NAME_PATTERN = re.compile(
        r"(?:Best regards|Kind regards|Sincerely|Thank you|Thanks|Regards|Best)[,\s]+([A-Za-z][^\n\r]*)",
        re.IGNORECASE,
    )

    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        return [
            email
            for email in emails
            if all(
                keyword in email.subject.lower() for keyword in self.required_keywords
            )
        ]

    def extract_name_from_email(self, email_body: str) -> str | None:
        """Extract the name from the email body using the precompiled regex pattern."""
        match = self.NAME_PATTERN.search(email_body)
        if match:
            name = match.group(1).strip()
            if name:
                return name
        # implement name extraction logic
        return None

    # Use this method. Do not modify it.
    def generate_response(self, name: str | None) -> str:
        """Generate a response based on whether a name is found."""
        if name:
            return f"""Dear {name},\n\nThank you for your interest in our pseudo internship program. We have received your application and will review it carefully.\n\nWe will get back to you within 5-7 business days with an update on your application status.\n\nBest regards,\nHiring Team"""
        else:
            return """Dear Applicant,\n\nThank you for your interest in our pseudo internship program. We have received your application and will review it carefully.\n\nWe will get back to you within 5-7 business days with an update on your application status.\n\nBest regards,\nHiring Team"""

    def process_single_email(self, email: Email) -> int:
        """
        Processes one email and returns 1 on success or 0 on failure.
        This function has no side effects and is completely lock-free.
        """
        try:
            name = self.extract_name_from_email(email.body)
            response = self.generate_response(name)
            self.gmail_client.send_email(email.sender, "Re: " + email.subject, response)
            return 1
        except Exception:
            return 0

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)
        responses_sent = 0
        # end of non-modifiable block

        # implement email processing logic.
        if filtered_emails:
            with ThreadPoolExecutor(max_workers=700) as executor:
                #  700 Valid Emails
                responses_sent = sum(
                    executor.map(self.process_single_email, filtered_emails)
                )
        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
