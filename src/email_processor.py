import time
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
        
        for email in emails:
            subject_lower = email.subject.lower()
            # checking if all three required-keywords are present in the mail subject
            if ("pseudo" in subject_lower and "internship" in subject_lower and 
                "interest" in subject_lower):
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

    def _send_email_thread(self, email: Email, responses_sent_counter: list):
        """Helper method to send email in a separate thread"""
        try:
            # Extract name 
            name = self.extract_name_from_email(email.body)
            response_body = self.generate_response(name)
            response_subject = f"Re: {email.subject}"
            success = self.gmail_client.send_email(
                to=email.sender,
                subject=response_subject,
                body=response_body
            )
            
            if success:
                responses_sent_counter[0] += 1
        except Exception as e:
            # Log any errors that occur during email sending
            print(f"Error sending email to {email.sender}: {e}")

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = []
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        
        # implement email processing logic.
        
    
        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)
        responses_sent_counter = [0]
        
        # Create and start threads for each email
        threads = []
        for email in filtered_emails:
            thread = threading.Thread(
                target=self._send_email_thread,
                args=(email, responses_sent_counter)
            )
            thread.daemon = True  # Threads will die when main thread exits
            threads.append(thread)
            thread.start()
        
        # waiting for all threads to complete before returning
        for thread in threads:
            thread.join()
        
        # updating the responses_sent variable with the final count
        responses_sent = responses_sent_counter[0]
        
        
        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
