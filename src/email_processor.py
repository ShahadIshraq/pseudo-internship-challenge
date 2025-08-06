import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        self.name_match_pattern = re.compile(
            r"(?:Best regards|Sincerely|Thanks|Regards|Best|Thank you|Kind regards),\s*([A-Za-z\s]+)",
            re.IGNORECASE,
        )
        self.responses_sent_lock = Lock()

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        filtered_email = []
        for email in emails:
            subject = email.subject.lower()

            if all(kw in subject for kw in self.required_keywords):
                filtered_email.append(email)

        return filtered_email

    def extract_name_from_email(self, email_body: str) -> str | None:
        # patterns = [
        #     r"Best regards,\s*([A-Za-z\s]+)",
        #     r"Sincerely,\s*([A-Za-z\s]+)",
        #     r"Thanks,\s*([A-Za-z\s]+)",
        #     r"Regards,\s*([A-Za-z\s]+)",
        #     r"Best,\s*([A-Za-z\s]+)",
        #     r"Thank you,\s*([A-Za-z\s]+)",
        #     r"Kind regards,\s*([A-Za-z\s]+)",
        # ]

        # implement name extraction logic
        # pattern = r"(?:Best regards|Sincerely|Thanks|Regards|Best|Thank you|Kind regards),\s*([A-Za-z\s]+)"
        
        matches = list(re.finditer(self.name_match_pattern, email_body))
        return matches[-1].group(1).strip() if matches else None

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

    def _process_single_email(self, email: Email) -> bool:
        try:
            name = self.extract_name_from_email(email_body=email.body)
            email_body = self.generate_response(name=name)
            email_reply_subject = f"Re: {email.subject}"
            self.gmail_client.send_email(
                to=email.sender, subject=email_reply_subject, body=email_body
            )
            return True

        except Exception:
            return False

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = []
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        # implement email processing logic.

        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)

        max_workers = 60  # need to be adjusted based on delay
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_email = {
                executor.submit(self._process_single_email, email): email
                for email in filtered_emails
            }
            for future in as_completed(future_to_email):
                if future.result():
                    responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
