import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        # declare a empty array
        filtered = []
        # traversing through all emails
        for email in emails:
            # subject can be in uppercase or lowercase so avoiding the uppercase issues make it lower case first
            subject_lower = email.subject.lower()
            # checking the keywords are matching with the require keywords or not if matched then adding the email in filtered array
            if all(k in subject_lower for k in self.required_keywords):
                filtered.append(email)
        return filtered

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

        # implement name extraction logic
        for pattern in patterns:
            name = re.search(pattern, email_body)
            if name:
                return name.group(1).strip()
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
        # fetch + filter
        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)

        # precompute payloads
        to_send: list[tuple[str, str, str]] = []
        for e in filtered_emails:
            name = self.extract_name_from_email(e.body)
            response = self.generate_response(name)
            subject = f"Re: {e.subject}"
            to_send.append((e.sender, subject, response))

        # concurrent send (Overlap mock's 0,2sec sleep time)
        if to_send:
            max_workers = min(64, len(to_send))
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                futures = [
                    pool.submit(self.gmail_client.send_email, to, subj, body)
                    for (to, subj, body) in to_send
                ]
                for fut in as_completed(futures):
                    if fut.result():
                        responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
