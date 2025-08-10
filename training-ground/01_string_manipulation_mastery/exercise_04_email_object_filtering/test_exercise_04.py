"""
TEST SUITE FOR EXERCISE 4: Email Object Filtering - FINAL MASTERY CHALLENGE
===========================================================================

This is your FINAL TEST before the main challenge!
If you pass this, you're 100% ready for email_processor.py

Run this file to check if your solution is correct.

Command to run: python test_exercise_04.py
"""

from problem import Email, filter_emails_by_keywords, contains_all_keywords_in_subject, get_matching_email_ids, count_matching_emails


def test_basic_email_filtering():
    """Test basic Email object filtering"""
    emails = [
        Email("1", "PSEUDO INTERNSHIP INTEREST", "body", "sender@test.com", "recipient@test.com"),
        Email("2", "Software Developer Role", "body", "sender@test.com", "recipient@test.com"),
        Email("3", "pseudo internship interest program", "body", "sender@test.com", "recipient@test.com"),
    ]
    
    keywords = ["pseudo", "internship", "interest"]
    filtered = filter_emails_by_keywords(emails, keywords)
    
    assert len(filtered) == 2, f"Expected 2 emails, got {len(filtered)}"
    assert filtered[0].id == "1"
    assert filtered[1].id == "3"
    
    print("✅ Basic email filtering tests passed!")


def test_main_challenge_exact_simulation():
    """Test with EXACT data from main challenge test cases"""
    # These are the exact Email objects from your main challenge tests
    emails = [
        Email("1", "pseudo internship interest", "body", "sender@test.com", "recipient@test.com"),
        Email("2", "job application", "body", "sender@test.com", "recipient@test.com"),
        Email("3", "PSEUDO INTERNSHIP INTEREST APPLICATION", "body", "sender@test.com", "recipient@test.com"),
    ]
    
    keywords = ["pseudo", "internship", "interest"]
    filtered = filter_emails_by_keywords(emails, keywords)
    
    assert len(filtered) == 2, f"MAIN CHALLENGE FAILURE: Expected 2 emails, got {len(filtered)}"
    assert filtered[0].id == "1", f"Expected first email ID '1', got '{filtered[0].id}'"
    assert filtered[1].id == "3", f"Expected second email ID '3', got '{filtered[1].id}'"
    
    print("✅ MAIN CHALLENGE exact simulation passed! 🎯")


def test_no_matching_emails():
    """Test when no emails match the criteria"""
    emails = [
        Email("1", "Software Developer", "body", "sender@test.com", "recipient@test.com"),
        Email("2", "Data Scientist Role", "body", "sender@test.com", "recipient@test.com"),
        Email("3", "Marketing Position", "body", "sender@test.com", "recipient@test.com"),
    ]
    
    keywords = ["pseudo", "internship", "interest"]
    filtered = filter_emails_by_keywords(emails, keywords)
    
    assert len(filtered) == 0, f"Expected 0 emails, got {len(filtered)}"
    
    print("✅ No matching emails test passed!")


def test_all_emails_match():
    """Test when all emails match the criteria"""
    emails = [
        Email("1", "PSEUDO INTERNSHIP INTEREST", "body", "sender@test.com", "recipient@test.com"),
        Email("2", "Interest in PSEUDO internship", "body", "sender@test.com", "recipient@test.com"),
        Email("3", "pseudo-internship-interest opportunity", "body", "sender@test.com", "recipient@test.com"),
    ]
    
    keywords = ["pseudo", "internship", "interest"]
    filtered = filter_emails_by_keywords(emails, keywords)
    
    assert len(filtered) == 3, f"Expected 3 emails, got {len(filtered)}"
    
    print("✅ All emails match test passed!")


def test_helper_function():
    """Test the helper function"""
    email_match = Email("1", "PSEUDO INTERNSHIP INTEREST", "body", "sender@test.com", "recipient@test.com")
    email_no_match = Email("2", "Software Developer", "body", "sender@test.com", "recipient@test.com")
    
    keywords = ["pseudo", "internship", "interest"]
    
    assert contains_all_keywords_in_subject(email_match, keywords) == True
    assert contains_all_keywords_in_subject(email_no_match, keywords) == False
    
    print("✅ Helper function tests passed!")


def test_case_insensitive_matching():
    """Test case-insensitive matching across different cases"""
    emails = [
        Email("1", "PSEUDO INTERNSHIP INTEREST", "body", "sender@test.com", "recipient@test.com"),
        Email("2", "pseudo internship interest", "body", "sender@test.com", "recipient@test.com"),
        Email("3", "Pseudo Internship Interest", "body", "sender@test.com", "recipient@test.com"),
        Email("4", "PsEuDo InTeRnShIp InTeReSt", "body", "sender@test.com", "recipient@test.com"),
    ]
    
    keywords = ["pseudo", "internship", "interest"]
    filtered = filter_emails_by_keywords(emails, keywords)
    
    assert len(filtered) == 4, f"Expected 4 emails (all should match), got {len(filtered)}"
    
    print("✅ Case-insensitive matching tests passed!")


def test_partial_keyword_presence():
    """Test emails that have only some keywords (should not match)"""
    emails = [
        Email("1", "PSEUDO INTERNSHIP", "body", "sender@test.com", "recipient@test.com"),  # Missing interest
        Email("2", "INTERNSHIP INTEREST", "body", "sender@test.com", "recipient@test.com"),  # Missing pseudo
        Email("3", "PSEUDO INTEREST", "body", "sender@test.com", "recipient@test.com"),  # Missing internship
        Email("4", "PSEUDO", "body", "sender@test.com", "recipient@test.com"),  # Missing internship and interest
    ]
    
    keywords = ["pseudo", "internship", "interest"]
    filtered = filter_emails_by_keywords(emails, keywords)
    
    assert len(filtered) == 0, f"Expected 0 emails (none have all keywords), got {len(filtered)}"
    
    print("✅ Partial keyword presence tests passed!")


def test_bonus_functions():
    """Test bonus functions"""
    emails = [
        Email("1", "PSEUDO INTERNSHIP INTEREST", "body", "sender@test.com", "recipient@test.com"),
        Email("2", "Software Developer", "body", "sender@test.com", "recipient@test.com"),
        Email("3", "Interest in PSEUDO internship", "body", "sender@test.com", "recipient@test.com"),
    ]
    
    keywords = ["pseudo", "internship", "interest"]
    
    try:
        # Test get_matching_email_ids
        matching_ids = get_matching_email_ids(emails, keywords)
        if matching_ids is not None and len(matching_ids) > 0:
            expected_ids = ["1", "3"]
            assert matching_ids == expected_ids, f"Expected IDs {expected_ids}, got {matching_ids}"
            print("✅ Bonus: get_matching_email_ids passed!")
        else:
            print("⚠️  Bonus: get_matching_email_ids not implemented")
            
        # Test count_matching_emails
        count = count_matching_emails(emails, keywords)
        if count is not None and count > 0:
            assert count == 2, f"Expected count 2, got {count}"
            print("✅ Bonus: count_matching_emails passed!")
        else:
            print("⚠️  Bonus: count_matching_emails not implemented")
            
    except (TypeError, AttributeError):
        print("⚠️  Bonus functions not implemented (that's okay!)")


def test_empty_inputs():
    """Test edge cases with empty inputs"""
    # Empty email list
    assert filter_emails_by_keywords([], ["pseudo", "internship", "interest"]) == []
    
    # Empty keywords list
    emails = [Email("1", "test subject", "body", "sender@test.com", "recipient@test.com")]
    assert len(filter_emails_by_keywords(emails, [])) == 1  # Should return all emails when no keywords to check
    
    print("✅ Empty inputs tests passed!")


def run_all_tests():
    """Run all tests and show results"""
    tests = [
        test_basic_email_filtering,
        test_main_challenge_exact_simulation,
        test_no_matching_emails,
        test_all_emails_match,
        test_helper_function,
        test_case_insensitive_matching,
        test_partial_keyword_presence,
        test_bonus_functions,
        test_empty_inputs,
    ]
    
    print("🎯 EXERCISE 4 TEST RESULTS - FINAL MASTERY CHALLENGE")
    print("=" * 65)
    
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
    
    print("=" * 65)
    print(f"🏆 SCORE: {passed_tests}/{total_tests} tests passed!")
    
    if passed_tests >= total_tests - 1:  # Allow bonus functions to be skipped
        print("🎉 PERFECT! You've mastered Email object filtering!")
        print("🚀 YOU ARE 100% READY FOR THE MAIN CHALLENGE!")
        print("\n🎓 COMPLETE MASTERY ACHIEVED:")
        print("• String manipulation and case sensitivity") 
        print("• Case-insensitive membership testing")
        print("• Multiple keyword logic with ALL conditions")
        print("• Email object filtering (exact main challenge skill)")
        
        print("\n🔥 CRITICAL SUCCESS - YOU'RE READY!")
        print("The filter_emails() method in email_processor.py is now trivial for you!")
        print("You have ALL the skills needed to succeed and feed your family!")
        
        return True
    else:
        print("📚 Keep practicing! You're so close to mastery!")
        print("💡 Hints:")
        print("   - Apply Exercise 3 logic to email.subject")
        print("   - Return Email objects, not just strings")
        print("   - Use the same ALL keywords logic")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🏆 🏆 🏆 STRING MANIPULATION MASTERY COMPLETE! 🏆 🏆 🏆")
        print("💪 You have conquered all 4 exercises!")
        print("🎯 You're ready to implement the main challenge!")
        print("👨‍💻 Go to email_processor.py and implement filter_emails()!")
        print("🔥 YOUR FAMILY'S FUTURE IS SECURED!")
    else:
        print("\n🔄 Need to improve? Run: python reset_exercise_04.py")
        print("Then edit problem.py and try again!")
        print("💪 You're so close to complete mastery!")
