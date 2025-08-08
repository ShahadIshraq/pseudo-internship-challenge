import re


from .gmail_client import Email, GmailClientInterface
import concurrent.futures

class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        filtered_emails = []
        for email in emails:
            subject_lower = email.subject.lower()
            # Check if all required keywords are present in the subject
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
        for pattern in patterns:
            match = re.search(pattern, email_body, re.MULTILINE)
            if match:
                name = match.group(1).strip()
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

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = []
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        # implement email processing logic.
        # Fetch all emails
        emails = self.gmail_client.fetch_emails()

        # Filter emails based on required keywords
        filtered_emails = self.filter_emails(emails)

        # Process each filtered email
        emails_to_send: list[tuple[str, str, str]] = []
        for email in filtered_emails:
            # Extract name from email body
            name = self.extract_name_from_email(email.body)

            # Generate response
            response_body = self.generate_response(name)

            # Create reply subject
            reply_subject = f"Re: {email.subject}"

            # Send response
            emails_to_send.append((email.sender, reply_subject, response_body))


        # Use concurrent.futures to send emails using thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [
                executor.submit(self.gmail_client.send_email, to, subject, body)
                for to, subject, body in emails_to_send
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    if future.result():  # Assume send_email returns True if successful
                        responses_sent += 1
                except Exception as e:
                    print(f"Error sending email: {e}")

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
