"""
TEST SUITE FOR EXERCISE 2: Case-Insensitive Membership Testing
==============================================================

This file contains comprehensive tests for your case-insensitive checking function.
Run this file to check if your solution is correct.

Command to run: python test_exercise_02.py
"""

import sys
from problem import contains_word_ignore_case, email_subject_contains_keyword


def test_basic_case_insensitive():
    """Test basic case-insensitive checking"""
    assert contains_word_ignore_case("HELLO WORLD", "hello") == True
    assert contains_word_ignore_case("hello world", "HELLO") == True
    assert contains_word_ignore_case("Python Programming", "python") == True
    print("✅ Basic case-insensitive tests passed!")


def test_exact_matches():
    """Test when cases already match"""
    assert contains_word_ignore_case("python", "python") == True
    assert contains_word_ignore_case("PYTHON", "PYTHON") == True
    print("✅ Exact match tests passed!")


def test_partial_matches():
    """Test partial word matches"""
    assert contains_word_ignore_case("JavaScript", "script") == True
    assert contains_word_ignore_case("UNDERSTAND", "stand") == True
    assert contains_word_ignore_case("programming", "gram") == True
    print("✅ Partial match tests passed!")


def test_no_matches():
    """Test when words don't exist"""
    assert contains_word_ignore_case("Python Programming", "java") == False
    assert contains_word_ignore_case("HELLO WORLD", "goodbye") == False
    assert contains_word_ignore_case("internship", "job") == False
    print("✅ No match tests passed!")


def test_empty_and_edge_cases():
    """Test edge cases"""
    assert contains_word_ignore_case("", "test") == False
    assert contains_word_ignore_case("test", "") == True  # Empty string is always found
    assert contains_word_ignore_case("a", "A") == True
    print("✅ Edge case tests passed!")


def test_email_subject_scenarios():
    """Test real email subject scenarios - THIS IS YOUR MAIN CHALLENGE PREP!"""
    # These are real email subjects you'll encounter in the main challenge
    test_cases = [
        ("PSEUDO INTERNSHIP INTEREST APPLICATION", "pseudo", True),
        ("pseudo internship interest", "PSEUDO", True),
        ("Pseudo-Internship-Interest", "internship", True),
        ("Software Developer Position", "pseudo", False),
        ("URGENT: PSEUDO OPPORTUNITY", "pseudo", True),
        ("internship program details", "ship", True),  # partial match
    ]
    
    for subject, keyword, expected in test_cases:
        result = contains_word_ignore_case(subject, keyword)
        assert result == expected, f"Failed: '{subject}' should {'contain' if expected else 'not contain'} '{keyword}'"
    
    print("✅ Email subject scenario tests passed!")


def test_bonus_email_function():
    """Test the bonus email-specific function"""
    try:
        assert email_subject_contains_keyword("PSEUDO INTERNSHIP APPLICATION", "pseudo") == True
        assert email_subject_contains_keyword("Software Developer", "internship") == False
        print("✅ Bonus email function tests passed!")
    except (TypeError, AttributeError):
        print("⚠️  Bonus email function not implemented (that's okay for now)")


def run_all_tests():
    """Run all tests and show results"""
    tests = [
        test_basic_case_insensitive,
        test_exact_matches,
        test_partial_matches,
        test_no_matches,
        test_empty_and_edge_cases,
        test_email_subject_scenarios,
        test_bonus_email_function,
    ]
    
    print("🎯 EXERCISE 2 TEST RESULTS")
    print("=" * 50)
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_func in tests:
        try:
            test_func()
            passed_tests += 1
        except AssertionError as e:
            print(f"❌ {test_func.__name__} failed!")
            print(f"   Error: {str(e)}")
        except Exception as e:
            print(f"💥 {test_func.__name__} crashed!")
            print(f"   Error: {str(e)}")
    
    print("=" * 50)
    print(f"🏆 SCORE: {passed_tests}/{total_tests} tests passed!")
    
    if passed_tests >= total_tests - 1:  # Allow bonus function to be skipped
        print("🎉 EXCELLENT! You've mastered case-insensitive checking!")
        print("🚀 Ready for Exercise 3: Multiple Keywords")
        print("\n🎓 SKILLS UNLOCKED:")
        print("• Case-insensitive text searching")
        print("• String membership testing")
        print("• Email subject analysis")
        return True
    else:
        print("📚 Keep practicing! Check the failed tests above.")
        print("💡 Hint: Combine .lower() with the 'in' operator")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🏆 MASTERY LEVEL: INTERMEDIATE!")
        print("You're building the exact skills needed for email filtering!")
        print("\n➡️  Next: Move to exercise_03_multiple_keywords/")
    else:
        print("\n🔄 Need to improve? Run: python reset_exercise_02.py")
        print("Then edit problem.py and try again!")
