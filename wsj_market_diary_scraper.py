#!/usr/bin/env python3
"""
WSJ Market Diary Scraper

This script scrapes market diary tables from the Wall Street Journal's
market data page and exports them to CSV files.

Author: AI Assistant
Date: 2025
"""

import os
import time
import logging
import csv
from datetime import datetime
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup


class WSJMarketDiaryScraper:
    """Scraper for WSJ Market Diary tables using Microsoft Edge."""

    def __init__(self, headless: bool = True, wait_time: int = 15):
        """
        Initialize the scraper.

        Args:
            headless: Whether to run browser in headless mode
            wait_time: Maximum wait time for elements to load
        """
        self.url = "https://www.wsj.com/market-data/stocks/marketsdiary"
        self.headless = headless
        self.wait_time = wait_time
        self.driver = None
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('wsj_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_driver(self):
        """Setup Microsoft Edge WebDriver with appropriate options."""
        try:
            edge_options = EdgeOptions()

            # Headless mode configuration
            if self.headless:
                edge_options.add_argument("--headless=new")  # Use new headless mode

            # Essential options for stability
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--window-size=1920,1080")
            edge_options.add_argument("--disable-blink-features=AutomationControlled")
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            edge_options.add_experimental_option('useAutomationExtension', False)

            # Modern user agent
            edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")

            # Disable notifications for cleaner operation
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
            }
            edge_options.add_experimental_option("prefs", prefs)

            # Try to use system Edge driver first (no download needed)
            try:
                self.logger.info("Attempting to use system Microsoft Edge driver...")
                self.driver = webdriver.Edge(options=edge_options)
                self.logger.info("Microsoft Edge WebDriver initialized successfully using system driver")
            except Exception as e1:
                self.logger.warning(f"Could not use system driver: {e1}")
                self.logger.info("Attempting to download Edge driver...")
                # Fallback to downloading driver
                try:
                    from webdriver_manager.microsoft import EdgeChromiumDriverManager
                    service = EdgeService(EdgeChromiumDriverManager().install())
                    self.driver = webdriver.Edge(service=service, options=edge_options)
                    self.logger.info("Microsoft Edge WebDriver initialized successfully using downloaded driver")
                except Exception as e2:
                    self.logger.error(f"Failed to download driver: {e2}")
                    raise Exception(f"Could not initialize Edge driver. System driver error: {e1}, Download error: {e2}")

        except Exception as e:
            self.logger.error(f"Failed to setup WebDriver: {e}")
            raise
            
    def wait_for_tables(self) -> List:
        """Wait for tables to load and return them."""
        try:
            self.logger.info("Waiting for page content to load...")

            # Wait for the page to fully load - try multiple strategies
            # Strategy 1: Wait for table elements
            try:
                WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located((By.TAG_NAME, "table"))
                )
                self.logger.info("Tables found using TAG_NAME strategy")
            except:
                self.logger.warning("No tables found with TAG_NAME, trying CSS selectors...")
                # Strategy 2: Try common WSJ table selectors
                try:
                    WebDriverWait(self.driver, self.wait_time).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "table, .WSJTheme--table--3oVG0Bt4"))
                    )
                    self.logger.info("Tables found using CSS selector strategy")
                except:
                    self.logger.warning("No tables found with CSS selectors either")

            # Additional wait for JavaScript to finish loading
            time.sleep(5)

            # Try to find tables using multiple methods
            tables = []

            # Method 1: Standard table tags
            tables_by_tag = self.driver.find_elements(By.TAG_NAME, "table")
            if tables_by_tag:
                tables.extend(tables_by_tag)
                self.logger.info(f"Found {len(tables_by_tag)} tables using TAG_NAME")

            # Method 2: CSS selectors for WSJ-specific classes
            try:
                wsj_tables = self.driver.find_elements(By.CSS_SELECTOR, "[class*='table']")
                for table in wsj_tables:
                    if table not in tables and table.tag_name == 'table':
                        tables.append(table)
                if wsj_tables:
                    self.logger.info(f"Found {len(wsj_tables)} additional tables using CSS selectors")
            except:
                pass

            self.logger.info(f"Total tables found: {len(tables)}")
            return tables

        except Exception as e:
            self.logger.error(f"Error waiting for tables: {e}")
            return []
            
    def extract_table_data(self, table_element) -> Optional[List[List[str]]]:
        """
        Extract data from a table element and return as list of rows.

        Args:
            table_element: Selenium WebElement representing a table

        Returns:
            List of lists containing table data [headers, row1, row2, ...]
        """
        try:
            # Get table HTML
            table_html = table_element.get_attribute('outerHTML')
            soup = BeautifulSoup(table_html, 'html.parser')

            # Find all rows
            rows = soup.find_all('tr')
            if not rows:
                self.logger.debug("No rows found in table")
                return None

            all_data = []

            # Extract all rows (including headers and data)
            for row in rows:
                row_data = []
                # Get all cells (th and td)
                cells = row.find_all(['th', 'td'])
                for cell in cells:
                    # Get text and clean it
                    text = cell.get_text(strip=True)
                    # Replace special characters if needed
                    text = text.replace('\n', ' ').replace('\r', ' ')
                    row_data.append(text)

                # Only add non-empty rows
                if row_data and any(cell.strip() for cell in row_data):
                    all_data.append(row_data)

            if not all_data:
                self.logger.debug("No data extracted from table")
                return None

            # Normalize column counts - make all rows have the same number of columns
            if all_data:
                max_cols = max(len(row) for row in all_data)
                for row in all_data:
                    while len(row) < max_cols:
                        row.append('')
                    # Trim if too long
                    if len(row) > max_cols:
                        del row[max_cols:]

            return all_data

        except Exception as e:
            self.logger.error(f"Error extracting table data: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return None
            
    def scrape_market_diary(self) -> List[List[List[str]]]:
        """
        Scrape all market diary tables from WSJ.

        Returns:
            List of table data (each table is a list of rows)
        """
        try:
            self.logger.info(f"Starting to scrape: {self.url}")

            # Setup driver if not already done
            if not self.driver:
                self.setup_driver()

            # Navigate to the page
            self.driver.get(self.url)
            self.logger.info("Page loaded successfully")

            # Wait for tables to load
            tables = self.wait_for_tables()

            if not tables:
                self.logger.warning("No tables found on the page")
                # Save page source for debugging
                try:
                    with open('debug_page_source.html', 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                    self.logger.info("Page source saved to debug_page_source.html for debugging")
                except:
                    pass
                return []

            # Extract data from each table
            table_data = []
            for i, table in enumerate(tables):
                self.logger.info(f"Processing table {i+1}/{len(tables)}")
                data = self.extract_table_data(table)
                if data is not None and len(data) >= 1:  # At least 1 row
                    table_data.append(data)
                    self.logger.info(f"Table {i+1} extracted successfully: {len(data)} rows, {len(data[0]) if data else 0} columns")
                else:
                    self.logger.warning(f"Table {i+1} is empty or could not be extracted")

            self.logger.info(f"Successfully extracted {len(table_data)} tables")
            return table_data

        except Exception as e:
            self.logger.error(f"Error during scraping: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return []
            
    def save_to_csv(self, table_data: List[List[List[str]]], output_dir: str = "output") -> List[str]:
        """
        Save table data to a single combined CSV file.

        Args:
            table_data: List of table data (each table is a list of rows)
            output_dir: Directory to save CSV file

        Returns:
            List containing the saved file path
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Generate timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Save combined file with all tables
            combined_filename = f"wsj_market_diary_{timestamp}.csv"
            combined_filepath = os.path.join(output_dir, combined_filename)

            # Combine all tables with a separator row
            with open(combined_filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for i, table in enumerate(table_data):
                    if i > 0:
                        # Add separator row between tables
                        writer.writerow([])  # Empty row for separation
                        writer.writerow(['---', f'Table {i+1}', '---'] + [''] * max(0, len(table[0]) - 3 if table else 0))
                    writer.writerows(table)

            self.logger.info(f"Saved combined data ({len(table_data)} tables) to: {combined_filepath}")
            return [combined_filepath]

        except Exception as e:
            self.logger.error(f"Error saving to CSV: {e}")
            return []
            
    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed")
            
    def run(self, output_dir: str = "output") -> List[str]:
        """
        Run the complete scraping process.
        
        Args:
            output_dir: Directory to save CSV files
            
        Returns:
            List of saved file paths
        """
        try:
            # Scrape the data
            table_data = self.scrape_market_diary()
            
            if not table_data:
                self.logger.warning("No data was scraped")
                return []
            
            # Save to CSV
            saved_files = self.save_to_csv(table_data, output_dir)
            
            self.logger.info(f"Scraping completed successfully. {len(saved_files)} files saved.")
            return saved_files
            
        except Exception as e:
            self.logger.error(f"Error in run method: {e}")
            return []
        finally:
            self.close()


def main():
    """Main function to run the scraper."""
    scraper = WSJMarketDiaryScraper(headless=True, wait_time=15)
    
    try:
        print("Starting WSJ Market Diary scraper...")
        saved_files = scraper.run()
        
        if saved_files:
            print(f"\nScraping completed successfully!")
            print(f"Files saved:")
            for file in saved_files:
                print(f"  - {file}")
        else:
            print("No files were saved. Check the logs for details.")
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
