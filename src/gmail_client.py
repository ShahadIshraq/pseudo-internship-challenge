import time
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Email:
    id: str
    subject: str
    body: str
    sender: str
    recipient: str


# Do not modify the GmailClientInterface or MockGmailClient
class GmailClientInterface(ABC):
    @abstractmethod
    def fetch_emails(self) -> list[Email]:
        pass

    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> bool:
        pass


class GmailClient(GmailClientInterface):
    def __init__(self, credentials_path: str | None = None) -> None:
        self.credentials_path = credentials_path

    def fetch_emails(self) -> list[Email]:
        raise NotImplementedError("Gmail client not implemented yet")

    def send_email(self, to: str, subject: str, body: str) -> bool:
        raise NotImplementedError("Gmail client not implemented yet")


class MockGmailClient(GmailClientInterface):
    def __init__(self, mock_emails: list[Email] | None = None) -> None:
        self.mock_emails = mock_emails or []
        self.sent_emails: list[dict[str, str]] = []

    def fetch_emails(self) -> list[Email]:
        time.sleep(0.2)  # 200ms delay
        return self.mock_emails

    def send_email(self, to: str, subject: str, body: str) -> bool:
        time.sleep(0.2)  # 200ms delay
        self.sent_emails.append({"to": to, "subject": subject, "body": body})
        return True
