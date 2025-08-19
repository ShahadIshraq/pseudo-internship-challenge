import time

from src.email_processor import EmailProcessor
from src.gmail_client import Email, MockGmailClient
from tests.test_data_generator import TestDataGenerator


# Do not modify this file
class TestEmailProcessor:
    def setup_method(self):
        self.data_generator = TestDataGenerator()
        self.performance_threshold = 5.0  # 5 seconds max

    def test_filter_emails_with_all_keywords(self):
        mock_client = MockGmailClient()
        processor = EmailProcessor(mock_client)

        emails = [
            Email(
                "1",
                "pseudo internship interest",
                "body",
                "sender@test.com",
                "recipient@test.com",
            ),
            Email(
                "2", "job application", "body", "sender@test.com", "recipient@test.com"
            ),
            Email(
                "3",
                "PSEUDO INTERNSHIP INTEREST APPLICATION",
                "body",
                "sender@test.com",
                "recipient@test.com",
            ),
        ]

        filtered = processor.filter_emails(emails)
        assert len(filtered) == 2
        assert filtered[0].id == "1"
        assert filtered[1].id == "3"

    def test_extract_name_from_email_various_formats(self):
        mock_client = MockGmailClient()
        processor = EmailProcessor(mock_client)

        test_cases = [
            ("Email body\nBest regards,\nJohn Smith", "John Smith"),
            ("Email body\nSincerely,\nEmily Johnson", "Emily Johnson"),
            ("Email body\nThanks,\nMichael Brown", "Michael Brown"),
            ("Email body\nRegards,\nSarah Davis", "Sarah Davis"),
            ("Email body\nBest,\nDavid Wilson", "David Wilson"),
            ("Email body with no signature", None),
        ]

        for email_body, expected_name in test_cases:
            result = processor.extract_name_from_email(email_body)
            assert result == expected_name

    def test_generate_response_with_name(self):
        mock_client = MockGmailClient()
        processor = EmailProcessor(mock_client)

        response = processor.generate_response("John Smith")
        assert "Dear John Smith," in response
        assert "Thank you for your interest" in response
        assert "Hiring Team" in response

    def test_generate_response_without_name(self):
        mock_client = MockGmailClient()
        processor = EmailProcessor(mock_client)

        response = processor.generate_response(None)
        assert "Dear Applicant," in response
        assert "Thank you for your interest" in response
        assert "Hiring Team" in response

    def test_process_emails_basic_functionality(self):
        test_emails = self.data_generator.generate_test_emails(10)
        mock_client = MockGmailClient(test_emails)
        processor = EmailProcessor(mock_client)

        result = processor.process_emails()

        assert "total_emails" in result
        assert "filtered_emails" in result
        assert "responses_sent" in result
        assert result["total_emails"] == 10
        

    def test_email_filtering_accuracy(self):
        valid_emails = []
        invalid_emails = []

        for _ in range(100):
            valid_emails.append(self.data_generator.generate_valid_email())
            invalid_emails.append(self.data_generator.generate_invalid_email())

        all_emails = valid_emails + invalid_emails
        mock_client = MockGmailClient(all_emails)
        processor = EmailProcessor(mock_client)

        filtered_emails = processor.filter_emails(all_emails)

        assert (
            len(filtered_emails) == 100
        ), f"Expected 100 valid emails, got {len(filtered_emails)}"

        for email in filtered_emails:
            subject_lower = email.subject.lower()
            assert "pseudo" in subject_lower
            assert "internship" in subject_lower
            assert "interest" in subject_lower

    def test_name_extraction_accuracy(self):
        mock_client = MockGmailClient()
        processor = EmailProcessor(mock_client)

        emails_with_names = []
        for _ in range(50):
            emails_with_names.append(self.data_generator.generate_valid_email())

        emails_without_names = []
        for _ in range(25):
            emails_without_names.append(
                self.data_generator.generate_email_without_name()
            )

        names_extracted = 0
        for email in emails_with_names:
            name = processor.extract_name_from_email(email.body)
            if name:
                names_extracted += 1

        no_names_extracted = 0
        for email in emails_without_names:
            name = processor.extract_name_from_email(email.body)
            if name is None:
                no_names_extracted += 1

        assert (
            names_extracted >= 45
        ), f"Expected at least 45 names extracted from 50 emails, got {names_extracted}"
        assert (
            no_names_extracted >= 20
        ), f"Expected at least 20 emails without names, got {no_names_extracted}"

    def test_response_generation_with_extracted_names(self):
        test_emails = []
        for _ in range(20):
            test_emails.append(self.data_generator.generate_valid_email())

        mock_client = MockGmailClient(test_emails)
        processor = EmailProcessor(mock_client)

        result = processor.process_emails()

        assert len(mock_client.sent_emails) == result["responses_sent"]

        for sent_email in mock_client.sent_emails:
            assert "Thank you for your interest" in sent_email["body"]
            assert "Hiring Team" in sent_email["body"]
            assert sent_email["subject"].startswith("Re: ")

    def test_end_to_end_processing_with_mixed_data(self):
        test_emails = self.data_generator.generate_test_emails(500)
        mock_client = MockGmailClient(test_emails)
        processor = EmailProcessor(mock_client)

        start_time = time.time()
        result = processor.process_emails()
        end_time = time.time()

        assert result["total_emails"] == 500
        assert result["filtered_emails"] <= result["total_emails"]
        assert result["responses_sent"] == result["filtered_emails"]
        assert (end_time - start_time) < self.performance_threshold
        assert len(mock_client.sent_emails) == result["responses_sent"]


    def test_performance_with_1000_emails(self):
        test_emails = self.data_generator.generate_test_emails(1000)
        mock_client = MockGmailClient(test_emails)
        processor = EmailProcessor(mock_client)

        start_time = time.time()
        result = processor.process_emails()
        end_time = time.time()

        processing_time = end_time - start_time

        assert result["total_emails"] == 1000
        assert (
            processing_time < self.performance_threshold
        ), f"Processing took {processing_time:.2f}s, exceeded threshold of {self.performance_threshold}s"
