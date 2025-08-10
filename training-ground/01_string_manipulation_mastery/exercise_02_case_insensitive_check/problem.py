"""
EXERCISE 2: Case-Insensitive Membership Testing
===============================================

LEARNING OBJECTIVE:
Master checking if a word exists in text, regardless of case.
This is CRITICAL for email filtering - you need to find "PSEUDO" even if someone wrote "pseudo".

REAL-WORLD APPLICATION:
This is the heart of search engines, email filters, and content matching.
Your main challenge requires checking if keywords exist in email subjects.

DIFFICULTY: ⭐⭐☆☆☆ (Easy)

PREREQUISITE: 
You MUST complete Exercise 1 first. This builds on lowercase conversion.

INSTRUCTIONS:
1. Complete the function below
2. Run the test file to check your solution  
3. Use the reset file if you need to start over

THE CHALLENGE:
Check if a target word exists in a sentence, ignoring case differences.

EXAMPLE:
Sentence: "I LOVE PYTHON PROGRAMMING"
Target: "python" 
Result: True (because "PYTHON" contains "python" when case is ignored)

TECHNIQUES TO LEARN:
1. Case normalization (from Exercise 1)
2. Membership testing with 'in' operator
3. Combining both techniques

THINK ABOUT:
- How do you make both strings comparable?
- What Python operator checks if one string is inside another?
"""

#How I used to solve this problem in C++
#boolean contains_word_ignore_case(string sentence, string target_word){  
# return sentence.lower().contains(target_word.lower());  
#}
def contains_word_ignore_case(sentence: str, target_word: str) -> bool:
    """
    Check if target_word exists in sentence (case-insensitive).
    
    Args:
        sentence (str): The text to search in
        target_word (str): The word to search for
        
    Returns:
        bool: True if target_word is found in sentence (ignoring case), False otherwise
        
    Examples:
        >>> contains_word_ignore_case("I LOVE PYTHON", "python")
        True
        >>> contains_word_ignore_case("Hello World", "WORLD")  
        True
        >>> contains_word_ignore_case("JavaScript", "java")
        True
        >>> contains_word_ignore_case("Python Programming", "ruby")
        False
    """
    # TODO: Implement case-insensitive word checking
    # HINT: Use what you learned in Exercise 1, then use the 'in' operator
    # Replace the line below with your solution
    result = target_word.lower() in sentence.lower()
    
    return result


def email_subject_contains_keyword(subject: str, keyword: str) -> bool:
    """
    BONUS FUNCTION: Email-specific implementation
    Check if an email subject contains a keyword (case-insensitive).
    
    This is EXACTLY what you'll need for the main challenge!
    
    Args:
        subject (str): The email subject line
        keyword (str): The keyword to search for
        
    Returns:
        bool: True if keyword is found in subject
        
    Example:
        >>> email_subject_contains_keyword("PSEUDO INTERNSHIP APPLICATION", "pseudo")
        True
    """
    # TODO: Implement using the function above
    # This should be a one-line solution calling contains_word_ignore_case
    return keyword in subject.lower()


# Test your function here (optional - main tests are in test_exercise_02.py)
if __name__ == "__main__":
    # Quick self-test
    test_cases = [
        ("I LOVE PYTHON", "python", True),
        ("Hello World", "WORLD", True), 
        ("JavaScript Programming", "script", True),
        ("Python Programming", "ruby", False),
    ]
    
    print("🧪 Quick Self-Test:")
    for sentence, word, expected in test_cases:
        result = contains_word_ignore_case(sentence, word)
        status = "✅" if result == expected else "❌"
        print(f"{status} Sentence: '{sentence}' | Word: '{word}' → {result} (Expected: {expected})")
