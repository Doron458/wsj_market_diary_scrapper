#!/usr/bin/env python3
"""
Test script for the WSJ Market Diary Scraper

This script performs basic tests to ensure the scraper is working correctly.
"""

import os
import sys
from wsj_market_diary_scraper import WSJMarketDiaryScraper


def test_scraper_initialization():
    """Test scraper initialization."""
    print("Testing scraper initialization...")
    try:
        scraper = WSJMarketDiaryScraper(headless=True, wait_time=5)
        assert scraper.url == "https://www.wsj.com/market-data/stocks/marketsdiary"
        assert scraper.headless == True
        assert scraper.wait_time == 5
        print("[PASS] Scraper initialization test passed")
        return True
    except Exception as e:
        print(f"[FAIL] Scraper initialization test failed: {e}")
        return False


def test_driver_setup():
    """Test WebDriver setup."""
    print("Testing WebDriver setup...")
    try:
        scraper = WSJMarketDiaryScraper(headless=True, wait_time=5)
        scraper.setup_driver()
        assert scraper.driver is not None
        print("[PASS] WebDriver setup test passed")
        scraper.close()
        return True
    except Exception as e:
        print(f"[FAIL] WebDriver setup test failed: {e}")
        return False


def test_basic_scraping():
    """Test basic scraping functionality."""
    print("Testing basic scraping...")
    try:
        scraper = WSJMarketDiaryScraper(headless=True, wait_time=10)

        # Test the scraping process
        dataframes = scraper.scrape_market_diary()

        if dataframes:
            print(f"[PASS] Basic scraping test passed - found {len(dataframes)} tables")

            # Test CSV saving
            saved_files = scraper.save_to_csv(dataframes, output_dir="test_output")
            if saved_files:
                print(f"[PASS] CSV saving test passed - saved {len(saved_files)} files")

                # Clean up test files
                for file in saved_files:
                    if os.path.exists(file):
                        os.remove(file)
                if os.path.exists("test_output"):
                    os.rmdir("test_output")

                return True
            else:
                print("[FAIL] CSV saving test failed")
                return False
        else:
            print("[FAIL] Basic scraping test failed - no tables found")
            return False

    except Exception as e:
        print(f"[FAIL] Basic scraping test failed: {e}")
        return False
    finally:
        scraper.close()


def run_all_tests():
    """Run all tests."""
    print("WSJ Market Diary Scraper - Test Suite")
    print("=" * 40)
    
    tests = [
        test_scraper_initialization,
        test_driver_setup,
        test_basic_scraping
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"[FAIL] Test {test.__name__} failed with exception: {e}")
        print()

    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("SUCCESS: All tests passed! The scraper is ready to use.")
        return True
    else:
        print("WARNING: Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
