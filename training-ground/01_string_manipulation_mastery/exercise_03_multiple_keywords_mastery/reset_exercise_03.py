"""
RESET EXERCISE 3: Multiple Keywords Mastery - MAIN CHALLENGE SIMULATOR
======================================================================

This script resets the problem.py file to its original state.
Use this when you want to start over or if you accidentally broke your code.

THIS IS THE MOST IMPORTANT EXERCISE - your family's future depends on mastering this!

Run this file: python reset_exercise_03.py
"""

import os


def reset_problem_file():
    """Reset the problem.py file to its original template"""
    
    original_content = '''"""
EXERCISE 3: Multiple Keywords Mastery - THE MAIN CHALLENGE SIMULATOR
===================================================================

LEARNING OBJECTIVE:
Master checking if ALL required keywords exist in text.
THIS IS THE EXACT LOGIC YOU NEED FOR THE MAIN EMAIL FILTERING CHALLENGE!

REAL-WORLD APPLICATION:
This is your main challenge! Email filters need ALL keywords: "pseudo" AND "internship" AND "interest"
Missing even ONE keyword means the email shouldn't be processed.

DIFFICULTY: ⭐⭐⭐☆☆ (Intermediate)

PREREQUISITE: 
You MUST complete Exercises 1 & 2 first. This combines both skills.

CRITICAL SUCCESS FACTOR:
Your family's future depends on mastering this concept. This is THE core logic 
of your main challenge. Master this, and you'll succeed in the real challenge.

INSTRUCTIONS:
1. Complete the functions below
2. Run the test file to check your solution  
3. Use the reset file if you need to start over

THE CHALLENGE:
Check if ALL keywords exist in a text (case-insensitive).

EXAMPLE:
Text: "PSEUDO INTERNSHIP INTEREST APPLICATION"
Keywords: ["pseudo", "internship", "interest"]
Result: True (because ALL three keywords are found)

Text: "PSEUDO INTERNSHIP PROGRAM"  
Keywords: ["pseudo", "internship", "interest"]
Result: False (because "interest" is missing)

TECHNIQUES TO MASTER:
1. Loop through multiple keywords
2. Check each keyword exists (Exercise 2 skill)
3. Logical AND operation (ALL must be true)
4. Early termination for efficiency

THINK ABOUT:
- How do you check if ALL items in a list meet a condition?
- What happens when you find the first missing keyword?
- How can you make this efficient?
"""

def contains_all_keywords(text: str, keywords: list[str]) -> bool:
    """
    Check if ALL keywords exist in text (case-insensitive).
    
    This is THE MOST IMPORTANT FUNCTION for your main challenge!
    
    Args:
        text (str): The text to search in (like an email subject)
        keywords (list[str]): List of keywords that ALL must be present
        
    Returns:
        bool: True if ALL keywords are found, False if ANY keyword is missing
        
    Examples:
        >>> contains_all_keywords("PSEUDO INTERNSHIP INTEREST", ["pseudo", "internship", "interest"])
        True
        >>> contains_all_keywords("PSEUDO INTERNSHIP PROGRAM", ["pseudo", "internship", "interest"])  
        False
        >>> contains_all_keywords("Interest in PSEUDO internship", ["pseudo", "internship", "interest"])
        True
    """
    # TODO: Implement ALL keywords checking
    # HINT 1: You need to check EVERY keyword in the list
    # HINT 2: Use the skills from Exercise 2 for each keyword
    # HINT 3: Think about what happens if ANY keyword is missing
    
    # METHOD 1: Using a loop (recommended for learning)
    # Replace the line below with your solution
    result = None
    
    return result


def contains_all_keywords_advanced(text: str, keywords: list[str]) -> bool:
    """
    ADVANCED VERSION: Using Python's built-in functions
    
    Same functionality as above, but using more Pythonic approaches.
    Try this AFTER you master the basic version above.
    
    HINT: Look up the all() function and list comprehensions
    """
    # TODO: Implement using all() and list comprehension
    # This should be a one-liner!
    return None


def filter_emails_by_keywords(email_subjects: list[str], required_keywords: list[str]) -> list[str]:
    """
    MAIN CHALLENGE SIMULATOR!
    Filter email subjects that contain ALL required keywords.
    
    This is EXACTLY what your main challenge filter_emails() method needs to do!
    
    Args:
        email_subjects (list[str]): List of email subject lines
        required_keywords (list[str]): Keywords that ALL must be present
        
    Returns:
        list[str]: Only email subjects that contain ALL keywords
        
    Example:
        >>> subjects = ["PSEUDO INTERNSHIP INTEREST", "Software Developer", "Pseudo internship interest program"]
        >>> keywords = ["pseudo", "internship", "interest"]  
        >>> filter_emails_by_keywords(subjects, keywords)
        ["PSEUDO INTERNSHIP INTEREST", "Pseudo internship interest program"]
    """
    # TODO: Filter the email subjects using contains_all_keywords function
    # HINT: You need to check each email subject and only keep the ones that pass
    filtered_subjects = []
    
    return filtered_subjects


# Test your function here (optional - main tests are in test_exercise_03.py)
if __name__ == "__main__":
    # Quick self-test - MAIN CHALLENGE SIMULATION
    print("🎯 MAIN CHALLENGE SIMULATION")
    print("=" * 40)
    
    # Test individual keyword checking
    test_cases = [
        ("PSEUDO INTERNSHIP INTEREST APPLICATION", ["pseudo", "internship", "interest"], True),
        ("PSEUDO INTERNSHIP PROGRAM", ["pseudo", "internship", "interest"], False),
        ("Interest in PSEUDO internship opportunities", ["pseudo", "internship", "interest"], True),
        ("Software Developer Position", ["pseudo", "internship", "interest"], False),
    ]
    
    print("Individual text testing:")
    for text, keywords, expected in test_cases:
        result = contains_all_keywords(text, keywords)
        status = "✅" if result == expected else "❌"
        print(f"{status} Text: '{text[:30]}...' → {result} (Expected: {expected})")
    
    # Test email filtering (main challenge simulation)
    print("\\n📧 Email Filtering Simulation:")
    email_subjects = [
        "PSEUDO INTERNSHIP INTEREST APPLICATION",
        "Software Engineer Position", 
        "pseudo internship interest program",
        "PSEUDO coding challenge",
        "internship opportunity",
        "Interest in PSEUDO INTERNSHIP program"
    ]
    
    required_keywords = ["pseudo", "internship", "interest"]
    filtered = filter_emails_by_keywords(email_subjects, required_keywords)
    
    print(f"📥 Input: {len(email_subjects)} emails")
    print(f"📤 Filtered: {len(filtered)} emails")
    print("Passing emails:")
    for email in filtered:
        print(f"  ✅ {email}")
        
    expected_count = 3  # Should find 3 emails that match
    if len(filtered) == expected_count:
        print(f"\\n🎉 SUCCESS! Found {expected_count} matching emails as expected!")
    else:
        print(f"\\n❌ Expected {expected_count} emails, but got {len(filtered)}")'''
    
    # Write the original content back to problem.py
    with open('problem.py', 'w') as f:
        f.write(original_content)
    
    print("🔄 RESET COMPLETE!")
    print("✨ problem.py has been restored to its original state")
    print("📝 You can now start fresh with the MOST IMPORTANT exercise")
    print("🔥 YOUR FAMILY'S FUTURE depends on mastering this!")
    print("🚀 Edit problem.py to implement your solution")


if __name__ == "__main__":
    reset_problem_file()
