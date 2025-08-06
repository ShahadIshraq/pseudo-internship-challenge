import re
import threading

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.keywords = ["pseudo", "internship", "interest"]

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

    # Do not modify
    def generate_response(self, name: str | None) -> str:
        if name:
            return (
                f"Dear {name},"
                "Thank you for your interest in our pseudo internship program. "
                "We have received your application and will review it carefully."
                "We will get back to you within 5-7 business days with an update on your application status."
                "Best regards,"
                "Hiring Team"
            )
        else:
            return (
                "Dear Applicant,"
                "Thank you for your interest in our pseudo internship program. "
                "We have received your application and will review it carefully."
                "We will get back to you within 5-7 business days with an update on your application status."
                "Best regards,"
                "Hiring Team"
            )

    def _handle_sending(self, mail: Email, sent_counter: list[int]) -> None:
        """Handles email response logic in a thread-safe way"""
        try:
            recipient_name = self.extract_name_from_email(mail.body)
            reply = self.generate_response(recipient_name)
            sent = self.gmail_client.send_email(
                to=mail.sender,
                subject=f"Re: {mail.subject}",
                body=reply,
            )
            if sent:
                sent_counter[0] += 1
        except Exception as err:
            print(f"Failed to send email to {mail.sender}: {err}")

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = self.gmail_client.fetch_emails()
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        filtered_emails = self.filter_emails(emails)
        count = [0]
        job_threads = []

        for mail in filtered_emails:
            t = threading.Thread(target=self._handle_sending, args=(mail, count))
            t.daemon = True
            job_threads.append(t)
            t.start()

        for t in job_threads:
            t.join()

        responses_sent = count[0]

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
