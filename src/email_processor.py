import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        filtered_emails = []

        for email in emails:
            subject_lower = email.subject.lower()
            # checking if all three required-keywords are present in the mail subject
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered_emails.append(email)

        return filtered_emails

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
        last_match = None
        last_position = -1

        for pattern in patterns:
            # finding all matches for this pattern
            matches = re.finditer(pattern, email_body)
            for match in matches:
                if match.end() > last_position:
                    last_match = match
                    last_position = match.end()

        if last_match:
            name = last_match.group(1).strip()
            if name:
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

    def _send_single_email(self, email: Email) -> bool:
        """Helper method to send a single email"""
        try:
            # Extract name
            name = self.extract_name_from_email(email.body)
            response_body = self.generate_response(name)
            response_subject = f"Re: {email.subject}"
            success = self.gmail_client.send_email(
                to=email.sender, subject=response_subject, body=response_body
            )
            return success
        except Exception as e:
            # Log any errors that occur during email sending
            print(f"Error sending email to {email.sender}: {e}")
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

        # Calculate optimal number of workers dynamically
        # Performance target: 5 seconds
        # Each email takes 200ms
        # Required workers = (filtered_emails * 200ms) / 5000ms
        # Add some buffer for safety and overhead
        if filtered_emails:
            time_per_email_ms = 200
            target_time_ms = 5000  # 5 seconds
            required_workers = (
                len(filtered_emails) * time_per_email_ms
            ) / target_time_ms
            # Add 20% buffer for safety and overhead
            optimal_workers = int(required_workers * 1.2)
            max_workers = max(1, min(100, optimal_workers))
        else:
            max_workers = 1

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all email sending tasks
            future_to_email = {
                executor.submit(self._send_single_email, email): email
                for email in filtered_emails
            }

            responses_sent = 0
            for future in as_completed(future_to_email):
                email = future_to_email[future]
                try:
                    if future.result():
                        responses_sent += 1
                except Exception as e:
                    print(
                        f"Exception occurred while processing email to {email.sender}: {e}"
                    )

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
