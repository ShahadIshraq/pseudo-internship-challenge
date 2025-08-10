"""
RESET EXERCISE 4: Email Object Filtering - FINAL MASTERY CHALLENGE
==================================================================

This script resets the problem.py file to its original state.
Use this when you want to start over or if you accidentally broke your code.

This is your FINAL exercise before the main challenge - master this and you're ready!

Run this file: python reset_exercise_04.py
"""

import os


def reset_problem_file():
    """Reset the problem.py file to its original template"""
    
    original_content = '''"""
EXERCISE 4: Email Object Filtering - FINAL MASTERY CHALLENGE
===========================================================

LEARNING OBJECTIVE:
Apply string manipulation skills to actual Email objects.
Bridge the gap between string filtering and the real Email object filtering in your main challenge.

REAL-WORLD APPLICATION:
This is the FINAL step before the main challenge! You'll work with actual Email objects,
exactly like in email_processor.py's filter_emails() method.

DIFFICULTY: ⭐⭐⭐⭐☆ (Advanced)

PREREQUISITE: 
You MUST complete Exercises 1, 2, and 3 first. This combines ALL previous skills.

CRITICAL BRIDGE:
Exercise 3 taught you to filter strings. This teaches you to filter Email objects.
Your main challenge needs to filter list[Email] → list[Email], not strings!

INSTRUCTIONS:
1. Complete the functions below
2. Run the test file to check your solution  
3. Use the reset file if you need to start over

THE CHALLENGE:
Filter a list of Email objects based on keywords in their subjects.
This is EXACTLY what filter_emails() does in the main challenge!

EXAMPLE:
Input: [Email(subject="PSEUDO INTERNSHIP INTEREST"), Email(subject="Software Dev")]
Keywords: ["pseudo", "internship", "interest"]
Output: [Email(subject="PSEUDO INTERNSHIP INTEREST")]  # Only the matching one

KEY INSIGHT:
Email objects have a .subject attribute. You need to apply your Exercise 3 logic
to email.subject instead of just strings.
"""

from dataclasses import dataclass


@dataclass
class Email:
    """
    Email class - IDENTICAL to the one in your main challenge!
    This prepares you for the real email_processor.py
    """
    id: str
    subject: str
    body: str
    sender: str
    recipient: str


def filter_emails_by_keywords(emails: list[Email], required_keywords: list[str]) -> list[Email]:
    """
    Filter Email objects that have ALL required keywords in their subject.
    
    THIS IS THE EXACT SIGNATURE OF YOUR MAIN CHALLENGE filter_emails() METHOD!
    
    Args:
        emails (list[Email]): List of Email objects to filter
        required_keywords (list[str]): Keywords that ALL must be present in subject
        
    Returns:
        list[Email]: Only Email objects whose subjects contain ALL keywords
        
    Example:
        >>> emails = [
        ...     Email("1", "PSEUDO INTERNSHIP INTEREST", "body", "sender@test.com", "rec@test.com"),
        ...     Email("2", "Software Developer", "body", "sender2@test.com", "rec@test.com")
        ... ]
        >>> keywords = ["pseudo", "internship", "interest"]
        >>> result = filter_emails_by_keywords(emails, keywords)
        >>> len(result)  # Should be 1
        1
        >>> result[0].subject
        'PSEUDO INTERNSHIP INTEREST'
    """
    # TODO: Filter emails based on their subject containing ALL keywords
    # HINT 1: This is like Exercise 3, but you need to check email.subject
    # HINT 2: You can reuse the logic from Exercise 3's contains_all_keywords function
    # HINT 3: You need to return Email objects, not just subjects
    
    filtered_emails = []
    
    return filtered_emails


def contains_all_keywords_in_subject(email: Email, keywords: list[str]) -> bool:
    """
    HELPER FUNCTION: Check if an Email's subject contains all keywords.
    
    This breaks down the problem - you can use this in filter_emails_by_keywords.
    
    Args:
        email (Email): The Email object to check
        keywords (list[str]): Keywords that ALL must be present
        
    Returns:
        bool: True if ALL keywords are found in email.subject
    """
    # TODO: Check if ALL keywords exist in email.subject (case-insensitive)
    # HINT: Use the exact same logic as Exercise 3's contains_all_keywords function
    # but apply it to email.subject instead of a regular string
    
    return None


def get_matching_email_ids(emails: list[Email], required_keywords: list[str]) -> list[str]:
    """
    BONUS FUNCTION: Get IDs of emails that match the criteria.
    
    Sometimes you need just the IDs, not the full Email objects.
    This is useful for tracking and logging.
    
    Args:
        emails (list[Email]): List of Email objects to check
        required_keywords (list[str]): Keywords that ALL must be present
        
    Returns:
        list[str]: List of email IDs that match the criteria
    """
    # TODO: Return list of email.id for emails that match the keywords
    # HINT: This is similar to filter_emails_by_keywords but returns IDs instead
    
    matching_ids = []
    
    return matching_ids


def count_matching_emails(emails: list[Email], required_keywords: list[str]) -> int:
    """
    BONUS FUNCTION: Count how many emails match the criteria.
    
    Useful for statistics and reporting.
    
    Args:
        emails (list[Email]): List of Email objects to check  
        required_keywords (list[str]): Keywords that ALL must be present
        
    Returns:
        int: Number of emails that match the criteria
    """
    # TODO: Count emails that match (don't return the emails, just the count)
    # HINT: You can use len() with filter_emails_by_keywords, or count directly
    
    return 0


# Test your function here (optional - main tests are in test_exercise_04.py)
if __name__ == "__main__":
    # Quick self-test - MAIN CHALLENGE FINAL SIMULATION
    print("🎯 MAIN CHALLENGE FINAL SIMULATION")
    print("=" * 50)
    
    # Create test emails (just like in main challenge)
    test_emails = [
        Email("1", "pseudo internship interest application", "body1", "john@test.com", "hr@company.com"),
        Email("2", "Software Engineer Position", "body2", "jane@test.com", "hr@company.com"),
        Email("3", "PSEUDO INTERNSHIP INTEREST OPPORTUNITY", "body3", "bob@test.com", "hr@company.com"),
        Email("4", "internship program details", "body4", "alice@test.com", "hr@company.com"),
        Email("5", "Interest in PSEUDO internship program", "body5", "charlie@test.com", "hr@company.com"),
    ]
    
    required_keywords = ["pseudo", "internship", "interest"]
    
    print(f"📥 Input: {len(test_emails)} emails")
    print("Email subjects:")
    for email in test_emails:
        print(f"  {email.id}: '{email.subject}'")
    
    # Test filtering
    filtered = filter_emails_by_keywords(test_emails, required_keywords)
    
    print(f"\\n📤 Filtered: {len(filtered)} emails")
    print("Matching emails:")
    for email in filtered:
        print(f"  ✅ {email.id}: '{email.subject}'")
    
    # Expected: emails 1, 3, and 5 should match (3 total)
    expected_count = 3
    if len(filtered) == expected_count:
        print(f"\\n🎉 SUCCESS! Found {expected_count} matching emails as expected!")
        print("🚀 You're ready for the main challenge!")
    else:
        print(f"\\n❌ Expected {expected_count} emails, but got {len(filtered)}")
        print("💡 Check your logic - compare with Exercise 3")
        
    # Test helper function
    print("\\n🧪 Testing helper function:")
    email_1 = test_emails[0]  # Should match
    email_2 = test_emails[1]  # Should not match
    
    result_1 = contains_all_keywords_in_subject(email_1, required_keywords)
    result_2 = contains_all_keywords_in_subject(email_2, required_keywords)
    
    print(f"Email 1 ('{email_1.subject}'): {result_1} (should be True)")
    print(f"Email 2 ('{email_2.subject}'): {result_2} (should be False)")'''
    
    # Write the original content back to problem.py
    with open('problem.py', 'w') as f:
        f.write(original_content)
    
    print("🔄 RESET COMPLETE!")
    print("✨ problem.py has been restored to its original state")
    print("📝 You can now start fresh with the FINAL exercise")
    print("🔥 Master this and you're ready for the main challenge!")
    print("🚀 Edit problem.py to implement your solution")


if __name__ == "__main__":
    reset_problem_file()
