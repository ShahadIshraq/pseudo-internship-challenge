import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    """
    Processes emails by filtering them, extracting sender names,
    and sending automated responses concurrently.
    """

    def __init__(self, gmail_client: GmailClientInterface):
        """
        Initializes the EmailProcessor.

        Args:
            gmail_client: An object that conforms to the GmailClientInterface.
        """
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        # Pre-compile regex patterns for performance.
        # The patterns are anchored to the start of a line (with re.MULTILINE)
        # to accurately target signatures and avoid matching quoted text.
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
        Filters emails where the subject contains all required keywords.
        """
        filtered_emails = []
        for email in emails:
            subject_lower = email.subject.lower()
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered_emails.append(email)
        return filtered_emails

    def extract_name_from_email(self, email_body: str) -> str | None:
        """
        Extracts the sender's name from the email body using regex.
        """
        for pattern in self.name_patterns:
            match = pattern.search(email_body)
            if match:
                # Group 1 captures the name. strip() removes leading/trailing whitespace.
                name = match.group(1).strip()
                # Ensure we didn't accidentally capture part of the email body or an empty string.
                if '\n' not in name and name:
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
        Fetches and processes emails, sending replies concurrently.
        """
        # Do not modify this block
        emails = []
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)

        # Use ThreadPoolExecutor for modern, clean, and efficient I/O-bound concurrency.
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Create a dictionary to map a future object back to its email for error logging.
            future_to_email = {
                executor.submit(self._prepare_and_send_reply, email): email
                for email in filtered_emails
            }

            # As each future completes, process the result.
            for future in as_completed(future_to_email):
                email = future_to_email[future]
                try:
                    # result() will be True if the email was sent successfully.
                    was_sent = future.result()
                    if was_sent:
                        responses_sent += 1
                except Exception as e:
                    # Log errors for debugging without crashing the entire application.
                    print(f"Error processing email to {email.sender}: {e}")

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block

    def _prepare_and_send_reply(self, email: Email) -> bool:
        """
        Prepares and sends a single email reply.

        This helper method encapsulates the logic for processing one email,
        making the main `process_emails` loop cleaner and the task suitable
        for submission to a thread pool.
        """
        name = self.extract_name_from_email(email.body)
        response_body = self.generate_response(name)
        response_subject = f"Re: {email.subject}"
        return self.gmail_client.send_email(
            to=email.sender,
            subject=response_subject,
            body=response_body,
        )

# ruff: noqa: W293, W292