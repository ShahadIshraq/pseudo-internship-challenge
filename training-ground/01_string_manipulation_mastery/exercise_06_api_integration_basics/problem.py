"""
EXERCISE 6: API Integration Basics - CLIENT METHOD MASTERY
==========================================================

LEARNING OBJECTIVE:
Master calling client methods and chaining operations for email processing.
This teaches the EXACT pattern needed for the process_emails() method in the main challenge!

REAL-WORLD APPLICATION:
The main challenge requires fetching emails, processing them, and sending responses.
This exercise teaches you to work with the GmailClient interface safely.

DIFFICULTY: ⭐⭐⭐☆☆ (Intermediate)

PREREQUISITE: 
You MUST complete Exercises 1-5 first. This builds on all previous skills.

CRITICAL BRIDGE TO MAIN CHALLENGE:
This exercise simulates the EXACT workflow in src/email_processor.py process_emails() method!
Master this and you're 85% ready for the main challenge!

INSTRUCTIONS:
1. Complete the functions below
2. Run the test file to check your solution  
3. Use the reset file if you need to start over

THE CHALLENGE:
Work with mock Gmail client to fetch, process, and send emails.

EXAMPLE WORKFLOW:
1. client.fetch_emails() → get list of emails
2. filter emails → keep only relevant ones
3. process each email → extract names, generate responses  
4. client.send_email() → send personalized responses

API METHODS TO MASTER:
- gmail_client.fetch_emails() → list[Email]
- gmail_client.send_email(to, subject, body) → bool
- Error handling and data flow management
"""

from dataclasses import dataclass


@dataclass
class Email:
    id: str
    subject: str
    body: str
    sender: str
    recipient: str


class MockGmailClient:
    """Simplified mock client for learning - mimics the real GmailClient interface"""
    
    def __init__(self, mock_emails: list[Email] | None = None):
        self.mock_emails = mock_emails or []
        self.sent_emails: list[dict[str, str]] = []
    
    def fetch_emails(self) -> list[Email]:
        """Fetch all available emails"""
        return self.mock_emails
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email - returns True if successful"""
        self.sent_emails.append({"to": to, "subject": subject, "body": body})
        return True


def basic_email_fetching(client: MockGmailClient) -> int:
    """
    Fetch emails from client and return count.
    
    This is your introduction to API interaction!
    
    Args:
        client (MockGmailClient): The Gmail client to use
        
    Returns:
        int: Number of emails fetched
        
    Example:
        >>> client = MockGmailClient([Email(...), Email(...)])
        >>> basic_email_fetching(client)
        2
    """
    # TODO: Implement basic email fetching
    # HINT 1: Call client.fetch_emails() to get the emails
    # HINT 2: Return the length of the fetched emails list
    
    emails = client.fetch_emails()
    return len(emails)


def filter_and_count_relevant_emails(client: MockGmailClient, keywords: list[str]) -> dict:
    """
    Fetch emails, filter by keywords, and return statistics.
    
    This combines API interaction with your filtering skills from previous exercises!
    
    Args:
        client (MockGmailClient): The Gmail client to use
        keywords (list[str]): Keywords that ALL must be present in subject
        
    Returns:
        dict: {"total": int, "filtered": int, "keywords": list[str]}
        
    Example:
        >>> emails = [Email("1", "pseudo internship interest", ...)]
        >>> client = MockGmailClient(emails)
        >>> filter_and_count_relevant_emails(client, ["pseudo", "internship"])
        {"total": 1, "filtered": 1, "keywords": ["pseudo", "internship"]}
    """
    # TODO: Implement email fetching and filtering
    # HINT 1: Fetch emails using client.fetch_emails()
    # HINT 2: Filter emails using skills from Exercise 3 (ALL keywords must be present)
    # HINT 3: Return a dictionary with the required statistics
    
    emails = client.fetch_emails()
    
    # Filter emails that contain ALL keywords (case-insensitive)
    filtered_emails = [
        email for email in emails 
        if all(keyword.lower() in email.subject.lower() for keyword in keywords)
    ]
    
    return {
        "total": len(emails),
        "filtered": len(filtered_emails),
        "keywords": keywords
    }


def send_simple_responses(client: MockGmailClient, emails: list[Email]) -> int:
    """
    Send simple responses to a list of emails.
    
    This teaches you the send_email API pattern!
    
    Args:
        client (MockGmailClient): The Gmail client to use
        emails (list[Email]): Emails to respond to
        
    Returns:
        int: Number of responses sent successfully
        
    Example:
        >>> emails = [Email("1", "subject", "body", "sender@test.com", "rec@test.com")]
        >>> client = MockGmailClient()
        >>> send_simple_responses(client, emails)
        1
    """
    # TODO: Send responses to each email
    # HINT 1: Loop through each email
    # HINT 2: For each email, call client.send_email(to, subject, body)
    # HINT 3: Use email.sender as 'to', "Re: " + email.subject as subject
    # HINT 4: Use a simple thank you message as body
    # HINT 5: Count successful sends
    
    responses_sent = 0
    
    for email in emails:
        to = email.sender
        subject = f"Re: {email.subject}"
        body = """Dear Applicant,

Thank you for your interest in our program. We have received your application and will review it carefully.

We will get back to you within 5-7 business days with an update on your application status.

Best regards,
Hiring Team"""
        
        success = client.send_email(to, subject, body)
        if success:
            responses_sent += 1
    
    return responses_sent


def complete_email_processing_workflow(client: MockGmailClient, required_keywords: list[str]) -> dict:
    """
    MAIN CHALLENGE SIMULATOR!
    Complete email processing workflow - fetch, filter, and respond.
    
    This is EXACTLY the pattern needed for process_emails() in the main challenge!
    
    Args:
        client (MockGmailClient): The Gmail client to use
        required_keywords (list[str]): Keywords for filtering
        
    Returns:
        dict: {"total_emails": int, "filtered_emails": int, "responses_sent": int}
        
    This is the EXACT return format expected by the main challenge!
    """
    # TODO: Implement complete workflow
    # HINT 1: Fetch emails using client.fetch_emails()
    # HINT 2: Filter emails by keywords (ALL must be present in subject)
    # HINT 3: For each filtered email, send a response
    # HINT 4: Return statistics in the exact format shown above
    
    # Step 1: Fetch all emails
    emails = client.fetch_emails()
    
    # Step 2: Filter emails based on required keywords
    filtered_emails = [
        email for email in emails 
        if all(keyword.lower() in email.subject.lower() for keyword in required_keywords)
    ]
    
    # Step 3: Send responses to filtered emails
    responses_sent = send_simple_responses(client, filtered_emails)
    
    # Step 4: Return statistics
    return {
        "total_emails": len(emails),
        "filtered_emails": len(filtered_emails),
        "responses_sent": responses_sent
    }


def advanced_workflow_with_error_handling(client: MockGmailClient, required_keywords: list[str]) -> dict:
    """
    BONUS FUNCTION: Complete workflow with error handling.
    
    This teaches production-ready patterns for the main challenge!
    
    Args:
        client (MockGmailClient): The Gmail client to use
        required_keywords (list[str]): Keywords for filtering
        
    Returns:
        dict: {"total_emails": int, "filtered_emails": int, "responses_sent": int, "errors": list[str]}
    """
    # TODO: Implement workflow with error handling
    # HINT 1: Use try/except blocks around API calls
    # HINT 2: Collect any errors in a list
    # HINT 3: Continue processing even if individual emails fail
    # HINT 4: Return error information along with statistics
    
    errors = []
    emails = []
    filtered_emails = []
    responses_sent = 0
    
    try:
        # Step 1: Fetch emails with error handling
        emails = client.fetch_emails()
    except Exception as e:
        errors.append(f"Failed to fetch emails: {str(e)}")
        return {"total_emails": 0, "filtered_emails": 0, "responses_sent": 0, "errors": errors}
    
    try:
        # Step 2: Filter emails
        filtered_emails = [
            email for email in emails 
            if all(keyword.lower() in email.subject.lower() for keyword in required_keywords)
        ]
    except Exception as e:
        errors.append(f"Failed to filter emails: {str(e)}")
    
    # Step 3: Send responses with individual error handling
    for email in filtered_emails:
        try:
            to = email.sender
            subject = f"Re: {email.subject}"
            body = "Thank you for your interest. We will review your application."
            
            success = client.send_email(to, subject, body)
            if success:
                responses_sent += 1
        except Exception as e:
            errors.append(f"Failed to send response to {email.sender}: {str(e)}")
    
    return {
        "total_emails": len(emails),
        "filtered_emails": len(filtered_emails),
        "responses_sent": responses_sent,
        "errors": errors
    }


# Test your function here (optional - main tests are in test_exercise_06.py)
if __name__ == "__main__":
    # Quick self-test - MAIN CHALLENGE SIMULATION
    print("🎯 API INTEGRATION SIMULATION")
    print("=" * 50)
    
    # Create test emails
    test_emails = [
        Email("1", "pseudo internship interest application", "body1", "john@test.com", "hr@company.com"),
        Email("2", "Software Engineer Position", "body2", "jane@test.com", "hr@company.com"),
        Email("3", "PSEUDO INTERNSHIP INTEREST", "body3", "bob@test.com", "hr@company.com"),
    ]
    
    client = MockGmailClient(test_emails)
    required_keywords = ["pseudo", "internship", "interest"]
    
    print(f"📥 Test emails: {len(test_emails)}")
    print(f"🔍 Required keywords: {required_keywords}")
    
    # Test basic fetching
    print("\n📝 Testing basic email fetching:")
    count = basic_email_fetching(client)
    print(f"  ✅ Fetched {count} emails")
    
    # Test filtering
    print("\n📝 Testing filtering:")
    stats = filter_and_count_relevant_emails(client, required_keywords)
    print(f"  ✅ Total: {stats['total']}, Filtered: {stats['filtered']}")
    
    # Test complete workflow
    print("\n📝 Testing complete workflow (main challenge simulation):")
    result = complete_email_processing_workflow(client, required_keywords)
    print(f"  ✅ Total: {result['total_emails']}")
    print(f"  ✅ Filtered: {result['filtered_emails']}")
    print(f"  ✅ Responses sent: {result['responses_sent']}")
    print(f"  ✅ Sent emails in client: {len(client.sent_emails)}")
    
    # Verify responses were actually sent
    print("\n📧 Sent email details:")
    for sent in client.sent_emails:
        print(f"  → To: {sent['to']}")
        print(f"    Subject: {sent['subject']}")
        print(f"    Body: {sent['body'][:50]}...")
    
    expected_filtered = 2  # Should match emails 1 and 3
    if result['filtered_emails'] == expected_filtered and result['responses_sent'] == expected_filtered:
        print(f"\n🎉 SUCCESS! Workflow completed correctly!")
        print("🚀 You're ready for process_emails() method in the main challenge!")
    else:
        print(f"\n❌ Expected {expected_filtered} filtered/sent, got {result['filtered_emails']}/{result['responses_sent']}")