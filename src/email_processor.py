# Here I import `re`, which is Python's regular expression module.
# I use it below to search text for signature patterns and capture the sender's name.
import re
from concurrent.futures import ThreadPoolExecutor

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        """Return only the emails whose subject contains all required keywords.

        Here I used a straightforward, readable approach:
        - First, I convert each subject to lowercase so we can match regardless of case.
        - Then, I check that every keyword in `self.required_keywords` exists in that lowercase subject.
        - If all keywords are present, I keep the email; otherwise, I skip it.
        - I iterate in order and append matching emails to preserve the original ordering.
        """

        filtered_emails: list[Email] = []

        # Here I process emails one by one to preserve their original order
        for email in emails:
            # Here I normalize the subject once for case-insensitive checks
            subject_lower: str = email.subject.lower()

            # Here I check the presence of every required keyword in the subject
            has_all_keywords: bool = True
            for keyword in self.required_keywords:
                if keyword not in subject_lower:
                    has_all_keywords = False
                    break

            # Here I keep only the emails that include all keywords
            if has_all_keywords:
                filtered_emails.append(email)

        return filtered_emails

    def extract_name_from_email(self, email_body: str) -> str | None:
        # Here I keep a patterns list and try them one by one.
        # Each pattern matches a common signature closer, followed by optional whitespace
        # (including a newline), and then captures the sender's name made of letters and spaces.
        patterns = [
            r"Best regards,\s*([A-Za-z\s]+)",
            r"Sincerely,\s*([A-Za-z\s]+)",
            r"Thanks,\s*([A-Za-z\s]+)",
            r"Regards,\s*([A-Za-z\s]+)",
            r"Best,\s*([A-Za-z\s]+)",
            # These are added by me.
            r"Thank you,\s*([A-Za-z\s]+)",
            r"Kind regards,\s*([A-Za-z\s]+)",
        ]

        # I am trying each pattern until one matches.
        for pattern_text in patterns:
            match = re.search(pattern_text, email_body, flags=re.IGNORECASE)
            if match:
                raw_name: str = match.group(1).strip()

                # Normalized multiple spaces inside the captured name
                split_parts = raw_name.split(" ")
                name_parts: list[str] = []
                for part in split_parts:
                    if part:
                        name_parts.append(part)
                    else:
                        pass

                if len(name_parts) > 0:
                    cleaned_name: str = " ".join(name_parts)
                else:
                    cleaned_name = ""

                if cleaned_name:
                    return cleaned_name

        # If no pattern matched, here I return None explicitly
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

        # Here I fetch all emails once from the Gmail client
        fetched_emails = self.gmail_client.fetch_emails()
        emails = fetched_emails

        # Here I filter the emails using the keywords rule to keep only the relevant ones
        only_relevant_emails = self.filter_emails(emails)
        filtered_emails = only_relevant_emails

        # Here I prepare to send replies. Sending one-by-one would be slow because the
        # mock client sleeps briefly for each send. So I use a thread pool to send in parallel.
        # I picked 64 workers because it gives us enough parallelism for 1000 emails while
        # keeping the code simple and reliable.
        futures = []
        with ThreadPoolExecutor(max_workers=64) as executor:
            for email in filtered_emails:
                # Here I extract the sender's name from the body (if present)
                extracted_name = self.extract_name_from_email(email.body)

                # Here I generate the response body using the provided helper
                response_body = self.generate_response(extracted_name)

                # Here I build the reply subject so it starts with "Re: " as expected
                reply_subject = "Re: " + email.subject

                # Here I decide who to send to (the sender of the original email)
                to_address = email.sender

                # Here I submit the send task to the thread pool
                future = executor.submit(
                    self.gmail_client.send_email,
                    to_address,
                    reply_subject,
                    response_body,
                )
                futures.append(future)

            # Here I collect results from all the futures and count the successful sends
            for future in futures:
                sent_ok = future.result()
                if sent_ok:
                    responses_sent = responses_sent + 1
                else:
                    pass

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
