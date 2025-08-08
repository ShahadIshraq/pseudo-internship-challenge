from math import ceil
import re
import threading
from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        
        filtered_emails = []

        # Check if the email subject contains all required keywords
        for email in emails:
            subject = email.subject.lower()
            if "pseudo" in subject and "internship" in subject and "interest" in subject:
                filtered_emails.append(email)

        return filtered_emails

    def extract_name_from_email(self, email_body: str) -> str | None:
        patterns = [
            r"Best regards,\s*([A-Za-z\s]+)",
            r"Sincerely,\s*([A-Za-z\s]+)",
            r"Thanks,\s*([A-Za-z\s]+)",
            r"Regards,\s*([A-Za-z\s]+)",
            r"Best,\s*([A-Za-z\s]+)",
        ]

        # adding more two patterns in the list as these are also treated as valid endings
        patterns.append(r"Thank you,\s*([A-Za-z\s]+)")
        patterns.append(r"Kind regards,\s*([A-Za-z\s]+)")

        # implement name extraction logic
        name = None
        
        for pattern in patterns:
            match = re.search(pattern, email_body, re.IGNORECASE)
            if match:
                return match.group(1).strip().splitlines()[0].strip(",. ")

        return name

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

        # Helper function to process a batch of emails
        def process_batch(email_batch):
            for email in email_batch:
                name = self.extract_name_from_email(email.body)
                response = self.generate_response(name)
                email.subject = f"Re: {email.subject}"
                self.gmail_client.send_email(email.sender, email.subject, response)

        # Process emails in batches to improve performance
        batch_size = 15
        threads = []
        total_batches = ceil(len(filtered_emails) / batch_size)

        # used muti-threading to process emails in batches as the processing was being time-consuming, over 5 seconds
        for i in range(total_batches):
            batch = filtered_emails[i * batch_size : (i + 1) * batch_size]
            thread = threading.Thread(target=process_batch, args=(batch,))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        responses_sent = len(filtered_emails)
        
        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
