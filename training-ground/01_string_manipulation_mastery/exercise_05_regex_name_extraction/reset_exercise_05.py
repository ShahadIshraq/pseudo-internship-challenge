"""
RESET SCRIPT: Exercise 5 - Regex Name Extraction Basics
======================================================

This script resets your problem.py file to its original state.
Use this if you want to start the exercise over from scratch.

Command to run: python reset_exercise_05.py
"""

import os

def reset_exercise():
    """Reset the problem.py file to its original state"""
    
    original_content = '''"""
EXERCISE 5: Regex Name Extraction Basics - BRIDGE TO MAIN CHALLENGE
=====================================================================

LEARNING OBJECTIVE:
Master basic regular expressions to extract names from email signatures.
This is THE EXACT SKILL needed for extract_name_from_email() in the main challenge!

REAL-WORLD APPLICATION:
The main challenge requires extracting sender names from email bodies to personalize responses.
This is your introduction to regex - the most powerful text processing tool.

DIFFICULTY: ⭐⭐⭐⭐☆ (Advanced)

PREREQUISITE: 
You MUST complete Exercises 1-4 first. This introduces completely new concepts.

CRITICAL BRIDGE TO MAIN CHALLENGE:
This exercise teaches the EXACT regex patterns used in src/email_processor.py
Master this and you're 80% ready for the extract_name_from_email() method!

INSTRUCTIONS:
1. Complete the functions below
2. Run the test file to check your solution  
3. Use the reset file if you need to start over

THE CHALLENGE:
Extract names from various email signature formats using regular expressions.

EXAMPLE:
Email body: "Dear Sir,\\n\\nI am interested in the position.\\n\\nBest regards,\\nJohn Smith"
Result: "John Smith"

EMAIL SIGNATURE FORMATS TO HANDLE:
- "Best regards,\\nJohn Smith"
- "Sincerely,\\nEmily Johnson"  
- "Thanks,\\nMichael Brown"
- "Regards,\\nSarah Davis"
- "Best,\\nDavid Wilson"

TECHNIQUES TO MASTER:
1. Import and use the 're' module
2. Basic pattern matching with re.search()
3. Capture groups with parentheses ()
4. Character classes [A-Za-z\\s]
5. Quantifiers + for one or more
6. Handling multiple patterns
"""

import re


def extract_name_basic(email_body: str) -> str | None:
    """
    Extract name from "Best regards," signature format.
    
    This is your introduction to regex! Start simple with just one pattern.
    
    Args:
        email_body (str): Full email body text
        
    Returns:
        str | None: Extracted name or None if no match
        
    Example:
        >>> extract_name_basic("Email content\\n\\nBest regards,\\nJohn Smith")
        "John Smith"
        >>> extract_name_basic("Email content\\n\\nSincerely,\\nJane Doe")
        None  # This function only handles "Best regards,"
    """
    # TODO: Implement basic regex name extraction
    # HINT 1: Use re.search() to find the pattern
    # HINT 2: Pattern should be: "Best regards,\\s*([A-Za-z\\s]+)"
    # HINT 3: Use capture group () to extract just the name part
    # HINT 4: Return match.group(1) if found, None otherwise
    
    return None


def extract_name_multiple_patterns(email_body: str) -> str | None:
    """
    Extract name from multiple signature formats.
    
    This is closer to the main challenge - handle multiple patterns!
    
    Args:
        email_body (str): Full email body text
        
    Returns:
        str | None: Extracted name or None if no match
        
    Example:
        >>> extract_name_multiple_patterns("Email\\n\\nSincerely,\\nJane Doe")
        "Jane Doe"
        >>> extract_name_multiple_patterns("Email\\n\\nThanks,\\nBob Wilson")
        "Bob Wilson"
    """
    # TODO: Handle multiple signature patterns
    # HINT 1: Create a list of patterns to try
    # HINT 2: Loop through patterns until you find a match
    # HINT 3: Patterns: "Best regards,", "Sincerely,", "Thanks,", "Regards,", "Best,"
    
    return None


def extract_name_advanced(email_body: str) -> str | None:
    """
    MAIN CHALLENGE SIMULATOR!
    Extract name with the EXACT logic needed for the main challenge.
    
    This is identical to what you'll implement in src/email_processor.py!
    
    Args:
        email_body (str): Full email body text
        
    Returns:
        str | None: Extracted name or None if no match
    """
    # TODO: Implement the exact logic from the main challenge
    # HINT: Look at the patterns in src/email_processor.py lines 16-22
    # This should be identical to extract_name_multiple_patterns but cleaner
    
    return None


def validate_extracted_name(name: str) -> bool:
    """
    BONUS FUNCTION: Validate that an extracted name looks reasonable.
    
    This helps catch extraction errors and improve reliability.
    
    Args:
        name (str): Extracted name to validate
        
    Returns:
        bool: True if name looks valid, False otherwise
    """
    # TODO: Implement name validation logic
    # HINT 1: Check if name is not empty after stripping
    # HINT 2: Check if name contains at least 2 words (first + last)
    # HINT 3: Check if name only contains letters and spaces
    # HINT 4: Maybe check minimum/maximum length
    
    return False


# Test your function here (optional - main tests are in test_exercise_05.py)
if __name__ == "__main__":
    # Quick self-test - MAIN CHALLENGE SIMULATION
    print("🎯 REGEX NAME EXTRACTION SIMULATION")
    print("=" * 50)
    
    # Test cases from the main challenge
    test_emails = [
        "Email body\\nBest regards,\\nJohn Smith",
        "Email body\\nSincerely,\\nEmily Johnson", 
        "Email body\\nThanks,\\nMichael Brown",
        "Email body\\nRegards,\\nSarah Davis",
        "Email body\\nBest,\\nDavid Wilson",
        "Email body with no signature",
    ]
    
    expected_names = ["John Smith", "Emily Johnson", "Michael Brown", "Sarah Davis", "David Wilson", None]
    
    print("Testing basic extraction:")
    for email, expected in zip(test_emails, expected_names):
        result = extract_name_basic(email)
        status = "✅" if (result == expected and expected == "John Smith") or (result is None and expected != "John Smith") else "❌"
        print(f"{status} Email: '...{email[-20:]}' → '{result}' (Expected: '{expected if expected else 'None'}')")
    
    print("\\nTesting multiple patterns:")
    for email, expected in zip(test_emails, expected_names):
        result = extract_name_multiple_patterns(email)
        status = "✅" if result == expected else "❌"
        print(f"{status} Email: '...{email[-20:]}' → '{result}' (Expected: '{expected if expected else 'None'}')")
    
    print("\\nTesting advanced extraction (main challenge ready):")
    for email, expected in zip(test_emails, expected_names):
        result = extract_name_advanced(email)
        status = "✅" if result == expected else "❌"
        print(f"{status} Email: '...{email[-20:]}' → '{result}' (Expected: '{expected if expected else 'None'}')")
        
    # Test name validation
    print("\\nTesting name validation:")
    test_names = ["John Smith", "Emily", "", "John123", "A B", "VeryLongNameThatShouldFailValidation"]
    expected_valid = [True, False, False, False, True, False]
    
    for name, expected in zip(test_names, expected_valid):
        result = validate_extracted_name(name)
        status = "✅" if result == expected else "❌"
        print(f"{status} Name: '{name}' → {result} (Expected: {expected})")
    
    print("\\n🎉 If all tests pass, you're ready for the main challenge name extraction!")
'''

    try:
        with open('problem.py', 'w') as f:
            f.write(original_content)
        print("✅ Exercise 5 has been reset successfully!")
        print("📝 You can now start fresh with problem.py")
        print("🧪 Run 'python test_exercise_05.py' to test your solution")
    except Exception as e:
        print(f"❌ Error resetting exercise: {e}")

if __name__ == "__main__":
    print("🔄 Resetting Exercise 5: Regex Name Extraction Basics...")
    reset_exercise()