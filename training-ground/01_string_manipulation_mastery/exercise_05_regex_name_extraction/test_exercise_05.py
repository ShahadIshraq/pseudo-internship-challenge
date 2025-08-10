"""
TEST SUITE: Exercise 5 - Regex Name Extraction Basics
====================================================

This test suite validates your regex name extraction skills.
These are the EXACT patterns you need for the main challenge!

Command to run: python test_exercise_05.py
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from problem import extract_name_basic, extract_name_multiple_patterns, extract_name_advanced, validate_extracted_name


def test_basic_extraction():
    """Test basic 'Best regards,' pattern extraction"""
    print("📝 Testing basic extraction...")
    
    test_cases = [
        ("Email content\n\nBest regards,\nJohn Smith", "John Smith"),
        ("Dear Sir,\n\nI am interested.\n\nBest regards,\nEmily Johnson", "Emily Johnson"),
        ("Message body\nBest regards,\n  Michael Brown  ", "Michael Brown"),  # Test whitespace
        ("Email content\n\nSincerely,\nJane Doe", None),  # Should not match
        ("Email content\n\nThanks,\nBob Wilson", None),  # Should not match
        ("Email with no signature", None),
    ]
    
    passed = 0
    for email_body, expected in test_cases:
        result = extract_name_basic(email_body)
        if result == expected:
            passed += 1
            print(f"  ✅ PASS: '{email_body[:20]}...' → '{result}'")
        else:
            print(f"  ❌ FAIL: '{email_body[:20]}...' → '{result}' (expected '{expected}')")
    
    print(f"Basic extraction: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_multiple_patterns():
    """Test extraction from multiple signature formats"""
    print("\n📝 Testing multiple patterns...")
    
    test_cases = [
        ("Email\n\nBest regards,\nJohn Smith", "John Smith"),
        ("Email\n\nSincerely,\nEmily Johnson", "Emily Johnson"),
        ("Email\n\nThanks,\nMichael Brown", "Michael Brown"),
        ("Email\n\nRegards,\nSarah Davis", "Sarah Davis"),
        ("Email\n\nBest,\nDavid Wilson", "David Wilson"),
        ("Email with no signature", None),
        ("Email\nKind regards,\nUnknown Pattern", None),  # Unsupported pattern
    ]
    
    passed = 0
    for email_body, expected in test_cases:
        result = extract_name_multiple_patterns(email_body)
        if result == expected:
            passed += 1
            print(f"  ✅ PASS: '{email_body[:20]}...' → '{result}'")
        else:
            print(f"  ❌ FAIL: '{email_body[:20]}...' → '{result}' (expected '{expected}')")
    
    print(f"Multiple patterns: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_advanced_extraction():
    """Test advanced extraction - main challenge simulation"""
    print("\n📝 Testing advanced extraction (main challenge simulation)...")
    
    # These are the EXACT test cases from the main challenge!
    test_cases = [
        ("Email body\nBest regards,\nJohn Smith", "John Smith"),
        ("Email body\nSincerely,\nEmily Johnson", "Emily Johnson"),
        ("Email body\nThanks,\nMichael Brown", "Michael Brown"),
        ("Email body\nRegards,\nSarah Davis", "Sarah Davis"),
        ("Email body\nBest,\nDavid Wilson", "David Wilson"),
        ("Email body with no signature", None),
    ]
    
    passed = 0
    for email_body, expected in test_cases:
        result = extract_name_advanced(email_body)
        if result == expected:
            passed += 1
            print(f"  ✅ PASS: '{email_body[:20]}...' → '{result}'")
        else:
            print(f"  ❌ FAIL: '{email_body[:20]}...' → '{result}' (expected '{expected}')")
    
    print(f"Advanced extraction: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_complex_email_bodies():
    """Test extraction from complex, realistic email bodies"""
    print("\n📝 Testing complex email bodies...")
    
    complex_email = """Dear Hiring Manager,

I am writing to express my strong interest in the pseudo internship position at your company. I believe this opportunity would be perfect for my career development.

I have relevant experience in software development and am eager to contribute to your team. My skills include:
- Python programming
- Web development
- Database management

I would love to discuss this opportunity further at your convenience.

Best regards,
Sarah Connor"""
    
    expected_name = "Sarah Connor"
    result = extract_name_advanced(complex_email)
    
    if result == expected_name:
        print(f"  ✅ PASS: Complex email → '{result}'")
        return True
    else:
        print(f"  ❌ FAIL: Complex email → '{result}' (expected '{expected_name}')")
        return False


def test_name_validation():
    """Test name validation logic"""
    print("\n📝 Testing name validation...")
    
    test_cases = [
        ("John Smith", True),           # Valid name
        ("Emily Rose Johnson", True),   # Valid three-part name
        ("A B", True),                  # Minimal valid name
        ("Emily", False),               # Single name (invalid)
        ("", False),                    # Empty string
        ("  ", False),                  # Whitespace only
        ("John123", False),             # Contains numbers
        ("John@Smith", False),          # Contains symbols
        ("VeryLongFirstNameThatExceedsReasonableLimits LastName", False),  # Too long
    ]
    
    passed = 0
    for name, expected in test_cases:
        result = validate_extracted_name(name)
        if result == expected:
            passed += 1
            print(f"  ✅ PASS: '{name}' → {result}")
        else:
            print(f"  ❌ FAIL: '{name}' → {result} (expected {expected})")
    
    print(f"Name validation: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_edge_cases():
    """Test edge cases and error conditions"""
    print("\n📝 Testing edge cases...")
    
    edge_cases = [
        ("Best regards,\n\n", None),     # Missing name
        ("Best regards,\n123", None),   # Non-alphabetic name
        ("BEST REGARDS,\nJohn Smith", None),  # Case sensitive (should not match)
        ("Email\nBest regards,John Smith", "John Smith"),  # No newline
        ("Email\nBest regards,\nJohn   Smith  ", "John   Smith"),  # Extra spaces
    ]
    
    passed = 0
    for email_body, expected in edge_cases:
        result = extract_name_advanced(email_body)
        if result == expected:
            passed += 1
            print(f"  ✅ PASS: Edge case → '{result}'")
        else:
            print(f"  ❌ FAIL: Edge case → '{result}' (expected '{expected}')")
    
    print(f"Edge cases: {passed}/{len(edge_cases)} tests passed")
    return passed == len(edge_cases)


def test_main_challenge_compatibility():
    """Test compatibility with main challenge patterns"""
    print("\n📝 Testing main challenge compatibility...")
    
    # Import the actual patterns from the main challenge
    main_challenge_patterns = [
        r"Best regards,\s*([A-Za-z\s]+)",
        r"Sincerely,\s*([A-Za-z\s]+)",
        r"Thanks,\s*([A-Za-z\s]+)",
        r"Regards,\s*([A-Za-z\s]+)",
        r"Best,\s*([A-Za-z\s]+)",
    ]
    
    print(f"  ✅ Main challenge uses {len(main_challenge_patterns)} patterns")
    print(f"  ✅ Your implementation should handle all these patterns")
    
    # Test that our function produces the same results as the main challenge would
    test_email = "Email content\n\nBest regards,\nTest User"
    result = extract_name_advanced(test_email)
    
    if result == "Test User":
        print("  ✅ PASS: Compatible with main challenge implementation")
        return True
    else:
        print(f"  ❌ FAIL: Not compatible - got '{result}' expected 'Test User'")
        return False


if __name__ == "__main__":
    print("🧪 EXERCISE 5: Regex Name Extraction - Test Suite")
    print("=" * 60)
    
    tests = [
        test_basic_extraction,
        test_multiple_patterns,
        test_advanced_extraction,
        test_complex_email_bodies,
        test_name_validation,
        test_edge_cases,
        test_main_challenge_compatibility,
    ]
    
    passed_tests = 0
    for test in tests:
        if test():
            passed_tests += 1
    
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS: {passed_tests}/{len(tests)} test suites passed")
    
    if passed_tests == len(tests):
        print("🎉 CONGRATULATIONS! You've mastered regex name extraction!")
        print("🚀 You're now ready for the extract_name_from_email() method in the main challenge!")
    else:
        print("❌ Some tests failed. Review your implementations and try again.")
        print("💡 Focus on the failed test cases and check your regex patterns.")
    
    print("\nNext steps:")
    print("1. Complete Exercise 6: API Method Integration")
    print("2. Complete Exercise 7: String Processing Pipeline")
    print("3. Move on to 02_regex_mastery for advanced regex skills")