import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        filtered = []
        for email in emails:
            subject_lower = email.subject.lower()
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered.append(email)
        return filtered

    def extract_name_from_email(self, email_body: str) -> str | None:
        patterns = [
            r"Best regards,\s*([A-Za-z\s]+)",
            r"Sincerely,\s*([A-Za-z\s]+)",
            r"Thanks,\s*([A-Za-z\s]+)",
            r"Regards,\s*([A-Za-z\s]+)",
            r"Best,\s*([A-Za-z\s]+)",
            r"Thank you,\s*([A-Za-z\s]+)",
            r"Kind regards,\s*([A-Za-z\s]+)",
        ]

        # implement name extraction logic
        for pattern in patterns:
            match = re.search(pattern, email_body)
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

        # implement email processing logic.
        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)

        # Process emails concurrently for improved performance
        def send_single_response(email: Email) -> int:
            """Process and send response for a single email"""
            name = self.extract_name_from_email(email.body)
            response_body = self.generate_response(name)
            response_subject = f"Re: {email.subject}"

            if self.gmail_client.send_email(
                email.sender, response_subject, response_body
            ):
                return 1
            return 0

        # Use ThreadPoolExecutor for concurrent email processing
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Submit all email processing tasks to the thread pool
            submitted_tasks = {
                executor.submit(send_single_response, email): email
                for email in filtered_emails
            }

            # Collect results as tasks complete
            for completed_task in as_completed(submitted_tasks):
                try:
                    responses_sent += completed_task.result()
                except Exception as e:
                    # Log error but continue processing other emails
                    print(f"Error processing email: {e}")
                    continue

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
