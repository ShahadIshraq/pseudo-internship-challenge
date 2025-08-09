from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        # Filter emails that contain all required keywords in subject or body (case-insensitive)
        filtered = []

        for email in emails:
            if all(keyword in email.subject.lower() for keyword in self.required_keywords):
                filtered.append(email)

        return filtered

    def extract_name_from_email(self, email_body: str) -> str | None:
        import re
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
            match = re.search(pattern, email_body, re.IGNORECASE)
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
        emails = self.gmail_client.fetch_emails()
        filtered_emails = self.filter_emails(emails)

        import threading
        responses_sent_lock = threading.Lock()
        threads = []

        def process_batch(batch):
            nonlocal responses_sent
            for email in batch:
                name = self.extract_name_from_email(email.body)
                response = self.generate_response(name)
                sent = self.gmail_client.send_email(email.sender, "Re: " + email.subject, response)
                if sent:
                    with responses_sent_lock:
                        responses_sent += 1

        batch_size = 20
        for i in range(0, len(filtered_emails), batch_size):
            batch = filtered_emails[i:i+batch_size]
            t = threading.Thread(target=process_batch, args=(batch,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        
        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
