import time
import re
from concurrent.futures import ThreadPoolExecutor
import threading

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:

    # Inclusive pattern for common signatures
    # Precompiled regex pattern to match various signature formats
    # This pattern matches common phrases followed by a name, allowing for variations in spacing and punctuation.
    # It captures names that may include spaces, periods, apostrophes, and hyphens.
    # The pattern is case-insensitive to match different capitalizations. Allows faster processing
    
    NAME_PATTERN = re.compile(
        r"(?:Best regards|Kind regards|Regards|Sincerely|Thanks|Best|Thank you)[,\s]*([\w\s\.\'\-]+)",
        re.IGNORECASE
    )

    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        #threding
    
        # Initialize a lock to manage access to shared resource
        self.responses_sent = 0

        #this will be used to count the number of responses sent
        # Use a lock to ensure thread-safe access to the responses_sent counter
        self.lock = threading.Lock()

    def filter_emails(self, emails: list[Email]) -> list[Email]:

        #Filter emails based on required keywords in the subject
        #Turned into lower case to ensure case-insensitive matching

        return [
            email for email in emails
            if all(keyword in email.subject.lower() for keyword in self.required_keywords)
        ]

    def extract_name_from_email(self, email_body: str) -> str | None:
        match = self.NAME_PATTERN.search(email_body)

        # If a match is found, extract the name and return it
        # If no match is found, return None
        # This method uses a regex pattern to find names in the email body.
        # It captures names that may include spaces, periods, apostrophes, and hyphens.
        # The pattern is case-insensitive to match different capitalizations.

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

        # Fetch emails from the Gmail client
        emails = self.gmail_client.fetch_emails()

        # Filter emails based on required keywords
        filtered_emails = self.filter_emails(emails)

        # Process each email in parallel using a thread pool
        # This allows for concurrent processing of emails, improving efficiency.
        # Each email is processed to extract the sender's name and generate a response.
        # The responses are sent back to the respective senders.
        # The number of responses sent is tracked using a shared counter.

        with ThreadPoolExecutor(max_workers=32) as executor:
            future_to_email = {
                executor.submit(self.process_single_email, email): email
                for email in filtered_emails
            }
            for future in future_to_email:
                future.result()
        responses_sent = self.responses_sent

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block

    def process_single_email(self, email: Email):

        # Extract the name from the email body
        # Generate a response based on the extracted name
        # Send the response back to the sender
        # Increment the responses_sent counter in a thread-safe manner
        # This method processes a single email by extracting the sender's name,
        # generating a response, and sending the response back to the sender.
        # It uses a lock to ensure thread-safe access to the responses_sent counter.

        name = self.extract_name_from_email(email.body)
        response = self.generate_response(name)
        self.gmail_client.send_email(email.sender, "Re: " + email.subject, response)
        with self.lock:
            self.responses_sent += 1
