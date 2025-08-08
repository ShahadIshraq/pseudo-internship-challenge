import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface, max_workers: int = 50):
        self.gmail_client = gmail_client
        self.keywords = ["pseudo", "internship", "interest"]
        self.max_workers = max_workers
        self.count_lock = threading.Lock()

    def filter_emails(self, all_emails: list[Email]) -> list[Email]:
        matched = []
        for mail in all_emails:
            content = mail.subject.lower()
            if all(kw in content for kw in self.keywords):
                matched.append(mail)
        return matched

    def extract_name_from_email(self, body: str) -> str | None:
        regex_patterns = [
            r"Best regards,\s*([A-Za-z\s]+)",
            r"Sincerely,\s*([A-Za-z\s]+)",
            r"Thanks,\s*([A-Za-z\s]+)",
            r"Regards,\s*([A-Za-z\s]+)",
            r"Best,\s*([A-Za-z\s]+)",
            r"Thank you,\s*([A-Za-z\s]+)",
            r"Kind regards,\s*([A-Za-z\s]+)",
        ]
        best_match = None
        furthest_index = -1
        for pattern in regex_patterns:
            for match in re.finditer(pattern, body, re.IGNORECASE):
                if match.end() > furthest_index:
                    best_match = match
                    furthest_index = match.end()
        if best_match:
            extracted_name = best_match.group(1).strip()
            return extracted_name if extracted_name else None
        return None

    def generate_response(self, name: str | None) -> str:
        if name:
            return (
                f"Dear {name}, "
                "Thank you for your interest in our pseudo internship program. "
                "We have received your application and will review it carefully. "
                "We will get back to you within 5-7 business days with an update on your application status. "
                "Best regards, "
                "Hiring Team"
            )
        else:
            return (
                "Dear Applicant, "
                "Thank you for your interest in our pseudo internship program. "
                "We have received your application and will review it carefully. "
                "We will get back to you within 5-7 business days with an update on your application status. "
                "Best regards, "
                "Hiring Team"
            )

    def _handle_sending(self, mail: Email) -> bool:
        """Send email and return True if sent successfully."""
        try:
            recipient_name = self.extract_name_from_email(mail.body)
            reply = self.generate_response(recipient_name)
            sent = self.gmail_client.send_email(
                to=mail.sender,
                subject=f"Re: {mail.subject}",
                body=reply,
            )
            return sent
        except Exception as err:
            print(f"Failed to send email to {mail.sender}: {err}")
            return False

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = self.gmail_client.fetch_emails()
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        filtered_emails = self.filter_emails(emails)

        responses_sent = 0

        # Use ThreadPoolExecutor to limit concurrency
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._handle_sending, mail): mail
                for mail in filtered_emails
            }

            for future in as_completed(futures):
                try:
                    sent = future.result()
                    if sent:
                        with self.count_lock:
                            responses_sent += 1
                except Exception as e:
                    mail = futures[future]
                    print(f"Exception for email from {mail.sender}: {e}")

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
