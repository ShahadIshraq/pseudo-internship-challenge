"""
TEST SUITE FOR EXERCISE 3: Multiple Keywords Mastery - MAIN CHALLENGE SIMULATOR
===============================================================================

This is THE MOST IMPORTANT test file - it tests the exact logic you need for the main challenge!
Your family's future depends on mastering these concepts.

Run this file to check if your solution is correct.

Command to run: python test_exercise_03.py
"""

import sys
from problem import contains_all_keywords, contains_all_keywords_advanced, filter_emails_by_keywords


def test_basic_all_keywords():
    """Test basic ALL keywords functionality"""
    # Simple cases with all keywords present
    assert contains_all_keywords("PSEUDO INTERNSHIP INTEREST", ["pseudo", "internship", "interest"]) == True
    assert contains_all_keywords("pseudo internship interest", ["pseudo", "internship", "interest"]) == True
    
    # Mixed case scenarios
    assert contains_all_keywords("PSEUDO internship INTEREST application", ["pseudo", "internship", "interest"]) == True
    
    print("✅ Basic ALL keywords tests passed!")


def test_missing_keywords():
    """Test when keywords are missing - CRITICAL for filtering accuracy"""
    # Missing one keyword
    assert contains_all_keywords("PSEUDO INTERNSHIP PROGRAM", ["pseudo", "internship", "interest"]) == False
    assert contains_all_keywords("SOFTWARE INTERNSHIP INTEREST", ["pseudo", "internship", "interest"]) == False
    assert contains_all_keywords("PSEUDO DEVELOPER INTEREST", ["pseudo", "internship", "interest"]) == False
    
    # Missing multiple keywords
    assert contains_all_keywords("PSEUDO PROGRAM", ["pseudo", "internship", "interest"]) == False
    assert contains_all_keywords("SOFTWARE DEVELOPER", ["pseudo", "internship", "interest"]) == False
    
    print("✅ Missing keywords tests passed!")


def test_partial_matches():
    """Test partial word matches - should still work"""
    # Keywords within larger words (this should still match)
    assert contains_all_keywords("PSEUDO-INTERNSHIP-INTEREST", ["pseudo", "internship", "interest"]) == True
    assert contains_all_keywords("pseudocode internship interest", ["pseudo", "internship", "interest"]) == True
    
    print("✅ Partial match tests passed!")


def test_different_word_orders():
    """Test keywords in different orders"""
    assert contains_all_keywords("INTEREST in PSEUDO INTERNSHIP", ["pseudo", "internship", "interest"]) == True
    assert contains_all_keywords("INTERNSHIP interest PSEUDO program", ["pseudo", "internship", "interest"]) == True
    assert contains_all_keywords("Great INTEREST in our PSEUDO INTERNSHIP", ["pseudo", "internship", "interest"]) == True
    
    print("✅ Word order tests passed!")


def test_main_challenge_exact_scenarios():
    """Test EXACT scenarios from the main challenge - THIS IS CRITICAL!"""
    # These are the exact test cases from your main challenge
    main_challenge_cases = [
        ("pseudo internship interest", ["pseudo", "internship", "interest"], True),
        ("PSEUDO INTERNSHIP INTEREST APPLICATION", ["pseudo", "internship", "interest"], True),
        ("job application", ["pseudo", "internship", "interest"], False),
        ("Software Engineer Position", ["pseudo", "internship", "interest"], False),
        ("PSEUDO software internship high interest", ["pseudo", "internship", "interest"], True),
        ("internship program", ["pseudo", "internship", "interest"], False),
    ]
    
    for subject, keywords, expected in main_challenge_cases:
        result = contains_all_keywords(subject, keywords)
        assert result == expected, f"MAIN CHALLENGE FAILURE: '{subject}' should return {expected}, got {result}"
    
    print("✅ MAIN CHALLENGE scenarios passed! 🎯")


def test_email_filtering_function():
    """Test the email filtering function - EXACT main challenge simulation"""
    email_subjects = [
        "pseudo internship interest application",
        "Software Engineer Position",
        "PSEUDO INTERNSHIP INTEREST APPLICATION", 
        "job application",
        "PSEUDO software internship high interest",
        "internship program",
        "Interest in PSEUDO INTERNSHIP program",
        "pseudo coding challenge",
    ]
    
    required_keywords = ["pseudo", "internship", "interest"]
    filtered = filter_emails_by_keywords(email_subjects, required_keywords)
    
    expected_subjects = [
        "pseudo internship interest application",
        "PSEUDO INTERNSHIP INTEREST APPLICATION",
        "PSEUDO software internship high interest", 
        "Interest in PSEUDO INTERNSHIP program",
    ]
    
    assert len(filtered) == len(expected_subjects), f"Expected {len(expected_subjects)} emails, got {len(filtered)}"
    
    # Check that all expected subjects are in the result
    for expected_subject in expected_subjects:
        assert expected_subject in filtered, f"Missing expected subject: '{expected_subject}'"
    
    print("✅ Email filtering function tests passed! 📧")


def test_advanced_function():
    """Test the advanced implementation (bonus)"""
    try:
        # Test the advanced version if implemented
        result1 = contains_all_keywords_advanced("PSEUDO INTERNSHIP INTEREST", ["pseudo", "internship", "interest"])
        result2 = contains_all_keywords_advanced("PSEUDO INTERNSHIP PROGRAM", ["pseudo", "internship", "interest"])
        
        if result1 is not None and result2 is not None:
            assert result1 == True
            assert result2 == False
            print("✅ Advanced function tests passed! 🚀")
        else:
            print("⚠️  Advanced function not implemented (that's okay!)")
    except (TypeError, AttributeError):
        print("⚠️  Advanced function not implemented (that's okay!)")


def test_edge_cases():
    """Test edge cases that might break your code"""
    # Empty inputs
    assert contains_all_keywords("", ["pseudo"]) == False
    assert contains_all_keywords("pseudo internship interest", []) == True  # No keywords to check
    
    # Single keyword
    assert contains_all_keywords("PSEUDO", ["pseudo"]) == True
    assert contains_all_keywords("PSEUDO", ["internship"]) == False
    
    print("✅ Edge case tests passed!")


def run_all_tests():
    """Run all tests and show results"""
    tests = [
        test_basic_all_keywords,
        test_missing_keywords,
        test_partial_matches,
        test_different_word_orders,
        test_main_challenge_exact_scenarios,
        test_email_filtering_function,
        test_advanced_function,
        test_edge_cases,
    ]
    
    print("🎯 EXERCISE 3 TEST RESULTS - MAIN CHALLENGE SIMULATOR")
    print("=" * 60)
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_func in tests:
        try:
            test_func()
            passed_tests += 1
        except AssertionError as e:
            print(f"❌ {test_func.__name__} failed!")
            print(f"   Error: {str(e)}")
            print("   This means your main challenge solution will also fail!")
        except Exception as e:
            print(f"💥 {test_func.__name__} crashed!")
            print(f"   Error: {str(e)}")
    
    print("=" * 60)
    print(f"🏆 SCORE: {passed_tests}/{total_tests} tests passed!")
    
    if passed_tests >= total_tests - 1:  # Allow advanced function to be skipped
        print("🎉 OUTSTANDING! You've mastered multiple keywords checking!")
        print("🚀 YOU ARE READY FOR THE MAIN CHALLENGE!")
        print("\n🎓 SKILLS MASTERED:")
        print("• Case-insensitive multiple keyword detection")
        print("• Email subject filtering logic") 
        print("• Boolean logic with ALL conditions")
        print("• The EXACT logic needed for filter_emails() method")
        
        print("\n🔥 CRITICAL SUCCESS:")
        print("You now have the CORE SKILL needed for your main challenge!")
        print("The filter_emails() method is just this logic applied to Email objects!")
        
        return True
    else:
        print("📚 Keep practicing! This is CRITICAL for your main challenge success!")
        print("💡 Hints:")
        print("   - Use .lower() on both text and keywords")
        print("   - Use 'in' operator to check if keyword exists in text")
        print("   - Check ALL keywords - if ANY is missing, return False")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🏆 MASTERY ACHIEVED!")
        print("💪 You're ready to implement the main challenge filter_emails() method!")
        print("📧 This exact logic will make you succeed!")
        print("\n➡️  Next: Apply this to your main email_processor.py!")
        print("     The filter_emails() method should use the exact same logic!")
    else:
        print("\n🔄 Need to improve? Run: python reset_exercise_03.py")
        print("Then edit problem.py and try again!")
        print("🔥 YOUR FAMILY'S FUTURE DEPENDS ON MASTERING THIS!")
