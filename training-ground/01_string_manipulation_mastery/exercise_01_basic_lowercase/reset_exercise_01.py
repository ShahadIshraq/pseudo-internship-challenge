"""
RESET EXERCISE 1: Basic Lowercase Conversion
============================================

This script resets the problem.py file to its original state.
Use this when you want to start over or if you accidentally broke your code.

Run this file: python reset_exercise_01.py
"""

import os


def reset_problem_file():
    """Reset the problem.py file to its original template"""
    
    original_content = '''"""
EXERCISE 1: Basic Lowercase Conversion
=====================================

LEARNING OBJECTIVE:
Master the fundamental .lower() method - the foundation of all case-insensitive text processing.

REAL-WORLD APPLICATION:
Every email filter, search engine, and text processor relies on this basic concept.
In your main challenge, you'll need this to match "PSEUDO" with "pseudo".

DIFFICULTY: ⭐☆☆☆☆ (Beginner)

INSTRUCTIONS:
1. Complete the function below
2. Run the test file to check your solution
3. Use the reset file if you need to start over

THE CHALLENGE:
Convert any given string to lowercase and return it.

EXAMPLE:
Input: "HELLO WORLD"
Output: "hello world"

HINT:
Python strings have a built-in method for this. Think about what method 
makes text "lower" case.
"""

def convert_to_lowercase(text: str) -> str:
    """
    Convert the input text to lowercase.
    
    Args:
        text (str): The input string to convert
        
    Returns:
        str: The lowercase version of the input string
        
    Example:
        >>> convert_to_lowercase("HELLO WORLD")
        "hello world"
        >>> convert_to_lowercase("PyThOn")
        "python"
    """
    # TODO: Implement lowercase conversion
    # Replace the line below with your solution
    result = None
    
    return result


# Test your function here (optional - main tests are in test_exercise_01.py)
if __name__ == "__main__":
    # Quick self-test
    test_cases = [
        ("HELLO", "hello"),
        ("World", "world"),
        ("PYTHON PROGRAMMING", "python programming"),
    ]
    
    print("🧪 Quick Self-Test:")
    for input_text, expected in test_cases:
        result = convert_to_lowercase(input_text)
        status = "✅" if result == expected else "❌"
        print(f"{status} Input: '{input_text}' → Output: '{result}' (Expected: '{expected}')")'''
    
    # Write the original content back to problem.py
    with open('problem.py', 'w') as f:
        f.write(original_content)
    
    print("🔄 RESET COMPLETE!")
    print("✨ problem.py has been restored to its original state")
    print("📝 You can now start fresh with the exercise")
    print("🚀 Edit problem.py to implement your solution")


if __name__ == "__main__":
    reset_problem_file()
