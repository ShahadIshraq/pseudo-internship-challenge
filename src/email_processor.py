import concurrent.futures
import re

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        filtered_emails = list(
            filter(
                lambda email: all(
                    re.search(rf"{keyword}\w*", email.subject, re.IGNORECASE)
                    for keyword in self.required_keywords
                ),
                emails,
            )
        )

        return filtered_emails

    def extract_name_from_email(self, email_body: str) -> str | None:
        patterns = [
            r"Best regards,\s*\n?\s*([A-Za-z\s]+)",
            r"Sincerely,\s*\n?\s*([A-Za-z\s]+)",
            r"Thanks,\s*\n?\s*([A-Za-z\s]+)",
            r"Regards,\s*\n?\s*([A-Za-z\s]+)",
            r"Best,\s*\n?\s*([A-Za-z\s]+)",
            r"Thank you,\s*\n?\s*([A-Za-z\s]+)",
        ]

        # implement name extraction logic
        for pattern in patterns:
            match = re.search(pattern, email_body, re.IGNORECASE | re.MULTILINE)
            if match:
                extracted_name = match.group(1).strip()
                return extracted_name

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

        def send_single_email(email: Email) -> bool:
            name = self.extract_name_from_email(email.body)
            response_body = self.generate_response(name)
            return self.gmail_client.send_email(
                email.sender,
                "Re: Pseudo-Internship Application" + email.subject,
                response_body,
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_email = {
                executor.submit(send_single_email, email): email
                for email in filtered_emails
            }

            for future in concurrent.futures.as_completed(future_to_email):
                if future.result():
                    responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
