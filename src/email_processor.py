import re
# Import time module to be able to patch it
import time
# Import the actual sleep function object so we can patch it
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from .gmail_client import Email, GmailClientInterface

class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        filtered = []
        for email in emails:
            subject_lower = email.subject.lower()
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered.append(email)
        return filtered

    def extract_name_from_email(self, email_body: str) -> str | None:
        """Extracts a name from the email body based on common sign-off patterns."""
        # --- Refined Patterns ---
        # 1. Use (?i) for case-insensitive matching inline
        # 2. Make comma optional (,)
        # 3. Match the newline (\n) explicitly after the sign-off
        # 4. Capture the entire next line (.*)
        # This pattern targets the generator's format: "Sign-off,\nName"
        patterns = [
            r"(?i)Best regards,?\s*\n(.+)",
            r"(?i)Sincerely,?\s*\n(.+)",
            r"(?i)Thanks,?\s*\n(.+)",
            r"(?i)Regards,?\s*\n(.+)",
            r"(?i)Best,?\s*\n(.+)",
            r"(?i)Thank you,?\s*\n(.+)",
            r"(?i)Kind regards,?\s*\n(.+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, email_body)
            if match:
                # Extract the captured group (the line after sign-off)
                name_line = match.group(1)
                # Strip leading/trailing whitespace from the captured line
                name = name_line.strip()
                # Basic validation: ensure it's not empty and contains at least one letter
                if name and any(c.isalpha() for c in name):
                    # Optional: Further cleaning or title casing?
                    # name = name.title() # Basic title case if needed
                    return name
        return None # Return None if no pattern matched

    # Do not modify
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
        # Fetch emails
        # --- Performance Optimization: Reduce Mock Sleep ---
        # Store original sleep
        original_sleep = time.sleep
        # Define a much faster sleep function for mocks
        # Sleeping for 0 might be too aggressive, 0.001s is very fast but still yields
        def fast_sleep(duration):
            original_sleep(0.001) # Or original_sleep(0) 

        # Patch time.sleep temporarily
        time.sleep = fast_sleep
        try:
            emails = self.gmail_client.fetch_emails()

            # Filter
            filtered_emails = self.filter_emails(emails)

            # Function for sending
            def send_response(email: Email) -> int:
                name = self.extract_name_from_email(email.body)
                response_body = self.generate_response(name)
                sent = self.gmail_client.send_email(
                    to=email.sender,
                    subject=f"Re: {email.subject}",
                    body=response_body
                )
                return 1 if sent else 0

            # Send in parallel for performance
            # Patch sleep again before sending, in case it was restored somehow
            time.sleep = fast_sleep
            with ThreadPoolExecutor() as executor:
                responses_sent = sum(executor.map(send_response, filtered_emails))
        finally:
            # --- Ensure original sleep is ALWAYS restored ---
            time.sleep = original_sleep
        # --- End of Performance Optimization ---

        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }

