#!/usr/bin/env python3
"""
STRING MANIPULATION MASTERY - Training Ground
===============================================

Master the art of string manipulation and case sensitivity!
Each challenge builds upon the previous one.

Complete each function and run the file to see if you pass all tests.
"""

def challenge_1_basic_lowercase():
    """
    CHALLENGE 1: Basic Lowercase Conversion
    
    Convert the string "HELLO WORLD" to lowercase.
    This is the foundation - all email filtering depends on case-insensitive matching.
    """
    text = "HELLO WORLD"
    
    # TODO: Convert 'text' to lowercase and return it
    result = None  # Replace this line
    
    return result


def challenge_2_case_insensitive_check():
    """
    CHALLENGE 2: Case-Insensitive Membership
    
    Check if the word "python" exists in "I LOVE PYTHON PROGRAMMING" (case-insensitive).
    Return True if found, False otherwise.
    """
    sentence = "I LOVE PYTHON PROGRAMMING"
    target_word = "python"
    
    # TODO: Check if target_word exists in sentence (ignore case)
    result = None  # Replace this line
    
    return result


def challenge_3_multiple_keywords():
    """
    CHALLENGE 3: Multiple Keywords Check
    
    Check if ALL of these words exist in the text (case-insensitive):
    Words to find: ["job", "application", "resume"]
    Text: "Please review my JOB APPLICATION and attached RESUME"
    
    Return True only if ALL words are found.
    """
    text = "Please review my JOB APPLICATION and attached RESUME"
    keywords = ["job", "application", "resume"]
    
    # TODO: Check if ALL keywords exist in text (case-insensitive)
    result = None  # Replace this line
    
    return result


def challenge_4_email_subject_filter():
    """
    CHALLENGE 4: Email Subject Filter (Basic)
    
    Filter email subjects that contain the word "internship" (case-insensitive).
    Return a list of subjects that match.
    """
    subjects = [
        "Software Engineer Position",
        "INTERNSHIP OPPORTUNITY at TechCorp",
        "internship application",
        "Full-time Developer Role",
        "Summer Internship Program"
    ]
    
    # TODO: Return list of subjects containing "internship" (case-insensitive)
    result = []  # Replace this line
    
    return result


def challenge_5_exact_keyword_matching():
    """
    CHALLENGE 5: Exact Keyword Matching
    
    Check if "intern" exists in "international conference" - should return False!
    This teaches you about partial matches vs exact word boundaries.
    
    Hint: "intern" is INSIDE "international" but it's not the word "intern"
    """
    text = "international conference"
    keyword = "intern"
    
    # TODO: Check if the EXACT word "intern" exists (not as part of another word)
    # Hint: You might need to think about word boundaries or splitting
    result = None  # Replace this line
    
    return result


def challenge_6_advanced_filtering():
    """
    CHALLENGE 6: Advanced Multi-Keyword Filter
    
    Filter emails that contain ALL three keywords: ["pseudo", "internship", "interest"]
    This is exactly like the main challenge!
    
    Return list of email subjects that contain all keywords (case-insensitive).
    """
    email_subjects = [
        "pseudo internship interest application",
        "Software Developer Position",
        "PSEUDO INTERNSHIP OPPORTUNITY - HIGH INTEREST",
        "internship program",
        "pseudo coding challenge",
        "Interest in PSEUDO internship program"
    ]
    
    required_keywords = ["pseudo", "internship", "interest"]
    
    # TODO: Return subjects that contain ALL required keywords
    result = []  # Replace this line
    
    return result


def challenge_7_string_cleaning():
    """
    CHALLENGE 7: String Cleaning & Normalization
    
    Clean and normalize this messy text:
    "  PSEUDO    INTERNSHIP   INTEREST!!!  "
    
    Remove extra spaces, convert to lowercase, remove punctuation,
    and return a clean string: "pseudo internship interest"
    """
    messy_text = "  PSEUDO    INTERNSHIP   INTEREST!!!  "
    
    # TODO: Clean the text - remove extra spaces, punctuation, make lowercase
    result = None  # Replace this line
    
    return result


def challenge_8_smart_keyword_detection():
    """
    CHALLENGE 8: Smart Keyword Detection
    
    Create a function that can find keywords even with different separators:
    - "pseudo-internship-interest"
    - "pseudo_internship_interest"  
    - "pseudo/internship/interest"
    - "pseudo.internship.interest"
    
    All should return True for keywords ["pseudo", "internship", "interest"]
    """
    test_strings = [
        "pseudo-internship-interest",
        "pseudo_internship_interest", 
        "pseudo/internship/interest",
        "pseudo.internship.interest"
    ]
    keywords = ["pseudo", "internship", "interest"]
    
    # TODO: Return True if ANY of the test_strings contains ALL keywords
    # (keywords might be separated by special characters, not just spaces)
    result = None  # Replace this line
    
    return result


def challenge_9_fuzzy_matching():
    """
    CHALLENGE 9: Fuzzy Matching
    
    Handle common typos and variations:
    - "intership" (missing 'n') should match "internship"
    - "intrship" (missing 'en') should match "internship"  
    - "pseudo" with numbers "p5eudo" should match "pseudo"
    
    Return True if the text contains keyword variations.
    """
    text = "I want an intership at your company with p5eudo projects"
    target_keywords = ["internship", "pseudo"]
    
    # TODO: Return True if text contains variations of the target keywords
    # Hint: You might want to check for partial matches or common patterns
    result = None  # Replace this line
    
    return result


def challenge_10_performance_optimization():
    """
    CHALLENGE 10: Performance Optimization
    
    You have 10,000 email subjects to filter for keywords ["pseudo", "internship", "interest"].
    Optimize your solution for speed - avoid unnecessary string operations.
    
    Return count of matching subjects (should be around 3000 based on the pattern).
    """
    # Simulate 10,000 email subjects
    subjects = []
    for i in range(10000):
        if i % 3 == 0:
            subjects.append(f"pseudo internship interest application {i}")
        elif i % 5 == 0:
            subjects.append(f"PSEUDO software internship high interest {i}")
        elif i % 7 == 0:
            subjects.append(f"interest in pseudo internship program {i}")
        else:
            subjects.append(f"random email subject {i}")
    
    keywords = ["pseudo", "internship", "interest"]
    
    # TODO: Count subjects containing ALL keywords - optimize for performance!
    count = 0  # Replace this line with your optimized solution
    
    return count


def challenge_11_unicode_and_accents():
    """
    CHALLENGE 11: Unicode & International Characters
    
    Handle international characters and accents:
    - "café" should match "cafe"
    - "résumé" should match "resume"
    - "naïve" should match "naive"
    
    Check if the text contains the target word (ignoring accents).
    """
    text = "Send your résumé for the café internship position"
    target_word = "resume"
    
    # TODO: Return True if target_word exists (ignoring accents/diacritics)
    # Hint: Look up unicodedata.normalize or string encoding methods
    result = None  # Replace this line
    
    return result


def challenge_12_master_level_email_processor():
    """
    CHALLENGE 12: Master Level - Real Email Processor
    
    Create a production-ready email filter that handles:
    - Case insensitivity
    - Multiple keyword requirements
    - Performance optimization
    - Edge cases (empty strings, None values)
    - Unicode support
    - Fuzzy matching for common typos
    
    This is your final test!
    """
    emails = [
        {"subject": "PSEUDO internship interest application", "sender": "john@test.com"},
        {"subject": "pseudo-INTERNSHIP high interest program", "sender": "mary@test.com"},
        {"subject": "Software Developer", "sender": "dev@test.com"},
        {"subject": "intership pseudo project interest", "sender": "bob@test.com"},  # typo
        {"subject": "", "sender": "empty@test.com"},  # edge case
        {"subject": None, "sender": "null@test.com"},  # edge case
        {"subject": "café pseudo internship with high interest", "sender": "international@test.com"},
    ]
    
    required_keywords = ["pseudo", "internship", "interest"]
    
    # TODO: Return list of email addresses whose subjects match the criteria
    # Handle all edge cases and advanced matching techniques you've learned
    result = []  # Replace this line with your master solution
    
    return result


# ===============================================
# TEST SUITE - DO NOT MODIFY BELOW THIS LINE
# ===============================================

def run_tests():
    """Run all tests and show results"""
    tests = [
        (challenge_1_basic_lowercase, "hello world", "Challenge 1: Basic Lowercase"),
        (challenge_2_case_insensitive_check, True, "Challenge 2: Case-Insensitive Check"),
        (challenge_3_multiple_keywords, True, "Challenge 3: Multiple Keywords"),
        (challenge_4_email_subject_filter, ["INTERNSHIP OPPORTUNITY at TechCorp", "internship application", "Summer Internship Program"], "Challenge 4: Email Subject Filter"),
        (challenge_5_exact_keyword_matching, False, "Challenge 5: Exact Keyword Matching"),
        (challenge_6_advanced_filtering, ["pseudo internship interest application", "PSEUDO INTERNSHIP OPPORTUNITY - HIGH INTEREST", "Interest in PSEUDO internship program"], "Challenge 6: Advanced Multi-Keyword Filter"),
        (challenge_7_string_cleaning, "pseudo internship interest", "Challenge 7: String Cleaning"),
        (challenge_8_smart_keyword_detection, True, "Challenge 8: Smart Keyword Detection"),
        (challenge_9_fuzzy_matching, True, "Challenge 9: Fuzzy Matching"),
        (challenge_10_performance_optimization, lambda x: 2800 <= x <= 3200, "Challenge 10: Performance (should be ~3000)"),
        (challenge_11_unicode_and_accents, True, "Challenge 11: Unicode & Accents"),
        (challenge_12_master_level_email_processor, ["john@test.com", "mary@test.com", "bob@test.com", "international@test.com"], "Challenge 12: Master Level"),
    ]
    
    passed = 0
    total = len(tests)
    
    print("🎯 STRING MANIPULATION MASTERY - Test Results")
    print("=" * 50)
    
    for i, (func, expected, description) in enumerate(tests, 1):
        try:
            result = func()
            
            # Special handling for challenge 10 (performance test with range)
            if callable(expected):
                success = expected(result)
                expected_str = "within expected range"
            else:
                success = result == expected
                expected_str = str(expected)
            
            if success:
                print(f"✅ {description}")
                passed += 1
            else:
                print(f"❌ {description}")
                print(f"   Expected: {expected_str}")
                print(f"   Got: {result}")
                
        except Exception as e:
            print(f"💥 {description} - ERROR: {str(e)}")
    
    print("=" * 50)
    print(f"🏆 Score: {passed}/{total} challenges completed!")
    
    if passed == total:
        print("🎉 CONGRATULATIONS! You've mastered string manipulation!")
        print("🚀 You're ready for the main email processor challenge!")
    elif passed >= total * 0.8:
        print("🌟 Great progress! Just a few more challenges to master!")
    elif passed >= total * 0.5:
        print("💪 You're getting there! Keep practicing!")
    else:
        print("📚 Keep studying the concepts and try again!")


if __name__ == "__main__":
    run_tests()
