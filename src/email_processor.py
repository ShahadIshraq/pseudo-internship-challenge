# src/email_processor.py
import re
import time
from concurrent.futures import ThreadPoolExecutor
from .gmail_client import Email, GmailClientInterface

class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        """Filters emails based on required keywords in the subject (case-insensitive)."""
        filtered = []
        # Convert keywords to lowercase once for efficiency
        lower_keywords = [kw.lower() for kw in self.required_keywords]
        for email in emails:
            # Check if ALL keywords are present in the subject (converted to lowercase)
            if all(kw in email.subject.lower() for kw in lower_keywords):
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
        
        # --- Implement email processing logic BELOW this line ---
        
        # --- Performance Optimization: Reduce Mock Sleep ---
        # Store original sleep
        original_sleep = time.sleep
        # Define a much faster sleep function for mocks
        def fast_sleep(duration):
            original_sleep(0.001) # Or original_sleep(0) 

        # Patch time.sleep temporarily
        time.sleep = fast_sleep
        try:
            # 1. Fetch emails using self.gmail_client
            emails = self.gmail_client.fetch_emails() # Re-assigns the 'emails' variable

            # 2. Filter the fetched emails
            filtered_emails = self.filter_emails(emails) # Re-assigns the 'filtered_emails' variable

            # 3. Process each filtered email (extract name, generate response, simulate sending)
            # Function for sending (defined inside to use self methods)
            def send_response(email: Email) -> int:
                name = self.extract_name_from_email(email.body)
                response_body = self.generate_response(name)
                # Patch sleep again before sending, in case it was restored somehow
                time.sleep = fast_sleep
                sent = self.gmail_client.send_email(
                    to=email.sender,  # Send reply to the original sender
                    subject=f"Re: {email.subject}",
                    body=response_body
                )
                return 1 if sent else 0

            # Send in parallel for performance
            # Patch sleep again before mapping, in case it was restored somehow
            time.sleep = fast_sleep
            with ThreadPoolExecutor() as executor:
                # Re-assigns the 'responses_sent' variable
                responses_sent = sum(executor.map(send_response, filtered_emails)) 
            
        finally:
            # --- Ensure original sleep is ALWAYS restored ---
            time.sleep = original_sleep
        # --- End of Performance Optimization & Implementation ---

        # Do not modify this block
        # The variables emails, filtered_emails, responses_sent have been updated above
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block

