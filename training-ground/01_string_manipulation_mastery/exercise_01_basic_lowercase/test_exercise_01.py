"""
TEST SUITE FOR EXERCISE 1: Basic Lowercase Conversion
=====================================================

This file contains comprehensive tests for your lowercase conversion function.
Run this file to check if your solution is correct.

Command to run: python test_exercise_01.py
"""

import sys
from problem import convert_to_lowercase


def test_basic_lowercase():
    """Test basic lowercase conversion"""
    assert convert_to_lowercase("HELLO") == "hello"
    assert convert_to_lowercase("WORLD") == "world"
    print("✅ Basic lowercase tests passed!")


def test_mixed_case():
    """Test mixed case strings"""
    assert convert_to_lowercase("HeLLo WoRLd") == "hello world"
    assert convert_to_lowercase("PyThOn") == "python"
    assert convert_to_lowercase("JavaScript") == "javascript"
    print("✅ Mixed case tests passed!")


def test_already_lowercase():
    """Test strings that are already lowercase"""
    assert convert_to_lowercase("already lowercase") == "already lowercase"
    assert convert_to_lowercase("python") == "python"
    print("✅ Already lowercase tests passed!")


def test_empty_and_special():
    """Test edge cases"""
    assert convert_to_lowercase("") == ""
    assert convert_to_lowercase("123ABC") == "123abc"
    assert convert_to_lowercase("HELLO-WORLD_TEST") == "hello-world_test"
    assert convert_to_lowercase("SPECIAL!@#$%CHARS") == "special!@#$%chars"
    print("✅ Edge case tests passed!")


def test_email_filtering_context():
    """Test in the context of email filtering - real-world scenarios"""
    # These are actual email subjects you might encounter
    email_subjects = [
        "PSEUDO INTERNSHIP INTEREST APPLICATION",
        "Pseudo Internship Interest Program",
        "URGENT: PSEUDO-INTERNSHIP-INTEREST"
    ]
    
    expected_results = [
        "pseudo internship interest application",
        "pseudo internship interest program", 
        "urgent: pseudo-internship-interest"
    ]
    
    for i, subject in enumerate(email_subjects):
        result = convert_to_lowercase(subject)
        assert result == expected_results[i], f"Failed on email subject: {subject}"
    
    print("✅ Email filtering context tests passed!")


def run_all_tests():
    """Run all tests and show results"""
    tests = [
        test_basic_lowercase,
        test_mixed_case,
        test_already_lowercase,
        test_empty_and_special,
        test_email_filtering_context,
    ]
    
    print("🎯 EXERCISE 1 TEST RESULTS")
    print("=" * 40)
    
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
    
    print("=" * 40)
    print(f"🏆 SCORE: {passed_tests}/{total_tests} tests passed!")
    
    if passed_tests == total_tests:
        print("🎉 PERFECT! You've mastered basic lowercase conversion!")
        print("🚀 Ready for Exercise 2: Case-Insensitive Checking")
        return True
    else:
        print("📚 Keep practicing! Check the failed tests above.")
        print("💡 Hint: Look at Python's string methods documentation")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🎓 MASTERY ACHIEVED!")
        print("You now understand:")
        print("• How to convert strings to lowercase")
        print("• Why case normalization is crucial for text processing")
        print("• How this applies to email filtering")
        print("\n➡️  Next: Move to exercise_02_case_insensitive_check/")
    else:
        print("\n🔄 Need to improve? Run: python reset_exercise_01.py")
        print("Then edit problem.py and try again!")
