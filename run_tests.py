#!/usr/bin/env python3
"""
1024 Game - Test Runner
Run all tests using unittest
"""

import sys
import os
import unittest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_all_tests():
    """Run all test suites"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Discover all tests
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    all_tests = loader.discover(test_dir, pattern='test_*.py')

    suite.addTests(all_tests)

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_specific_test(test_module):
    """Run a specific test module"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_module)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 60)
    print("1024 Game - Running Test Suite")
    print("=" * 60)
    print()

    if len(sys.argv) > 1:
        # Run specific test
        test_module = sys.argv[1]
        print(f"Running specific test: {test_module}")
        print()
        success = run_specific_test(test_module)
    else:
        # Run all tests
        print("Running all tests...")
        print()
        success = run_all_tests()

    print()
    print("=" * 60)
    if success:
        print("All tests passed! ✓")
    else:
        print("Some tests failed! ✗")
        sys.exit(1)
    print("=" * 60)
