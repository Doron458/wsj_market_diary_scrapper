#!/usr/bin/env python3
"""
Example usage of the WSJ Market Diary Scraper

This script demonstrates how to use the scraper with different options.
"""

from wsj_market_diary_scraper import WSJMarketDiaryScraper


def example_basic_usage():
    """Basic usage example."""
    print("=== Basic Usage Example ===")
    
    # Create scraper instance
    scraper = WSJMarketDiaryScraper(headless=True, wait_time=15)
    
    try:
        # Run the scraper
        saved_files = scraper.run(output_dir="market_data")
        
        if saved_files:
            print(f"Successfully saved {len(saved_files)} files:")
            for file in saved_files:
                print(f"  - {file}")
        else:
            print("No files were saved.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        scraper.close()


def example_custom_options():
    """Example with custom options."""
    print("\n=== Custom Options Example ===")
    
    # Create scraper with custom options
    scraper = WSJMarketDiaryScraper(
        headless=False,  # Show browser window
        wait_time=20     # Wait longer for content to load
    )
    
    try:
        # Scrape data
        table_data = scraper.scrape_market_diary()
        
        if table_data:
            print(f"Found {len(table_data)} tables:")
            for i, table in enumerate(table_data):
                print(f"  Table {i+1}: {len(table)-1} rows × {len(table[0])} columns")
                print(f"    Columns: {table[0]}")
                print(f"    First few rows:")
                for j, row in enumerate(table[:4]):  # Show first 4 rows (including header)
                    print(f"      {row}")
                print()
        
        # Save with custom directory
        saved_files = scraper.save_to_csv(table_data, output_dir="custom_output")
        print(f"Saved to: {saved_files}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        scraper.close()


def example_step_by_step():
    """Example showing step-by-step usage."""
    print("\n=== Step-by-Step Example ===")
    
    scraper = WSJMarketDiaryScraper()
    
    try:
        # Step 1: Setup driver
        print("Setting up browser...")
        scraper.setup_driver()
        
        # Step 2: Scrape data
        print("Scraping market diary data...")
        table_data = scraper.scrape_market_diary()
        
        # Step 3: Process results
        if table_data:
            print(f"Successfully scraped {len(table_data)} tables")
            
            # Step 4: Save to CSV
            print("Saving to CSV files...")
            saved_files = scraper.save_to_csv(table_data)
            
            print(f"Files saved: {saved_files}")
        else:
            print("No data was scraped")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    # Run examples
    example_basic_usage()
    example_custom_options()
    example_step_by_step()
