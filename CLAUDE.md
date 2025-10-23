# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python web scraper that extracts market diary tables from the Wall Street Journal's market data page and exports them to CSV files. The scraper uses Selenium for browser automation to handle dynamic content loading.

**Target URL**: `https://www.wsj.com/market-data/stocks/marketsdiary`

## Development Commands

### Running the Scraper

```bash
# Basic usage (headless mode)
python wsj_market_diary_scraper.py

# Using the Windows batch file
run_scraper.bat

# Run tests
python test_scraper.py

# View example usage
python example_usage.py
```

### Installation

```bash
pip install -r requirements.txt
```

## Architecture

### Core Class: WSJMarketDiaryScraper (wsj_market_diary_scraper.py)

The main scraper class uses a multi-step process:

1. **WebDriver Setup** (wsj_market_diary_scraper.py:57-104): Configures Microsoft Edge with headless mode, custom user agent, and anti-detection features. Tries system driver first, then falls back to downloading driver if needed.
2. **Page Loading & Waiting** (wsj_market_diary_scraper.py:106-144): Uses multiple wait strategies for table elements plus additional 5-second delay for dynamic content
3. **Data Extraction** (wsj_market_diary_scraper.py:146-205): Parses table HTML using BeautifulSoup, normalizes column counts, handles both `<th>` and `<td>` elements
4. **CSV Export** (wsj_market_diary_scraper.py:259+): Saves individual table files plus a combined file with separator rows

### Key Methods

- `setup_driver()`: Initializes Microsoft Edge WebDriver. Attempts system driver first (no download needed), falls back to webdriver-manager if necessary
- `wait_for_tables()`: Multi-strategy wait approach - tries TAG_NAME and CSS selectors, adds 5s buffer for JavaScript loading
- `extract_table_data(table_element)`: Returns table as `List[List[str]]` with all rows including headers
- `scrape_market_diary()`: Returns `List[List[List[str]]]` - list of tables, each table is list of rows. Saves page source for debugging if no tables found.
- `save_to_csv()`: Generates timestamped filenames in format `wsj_market_diary_table_{N}_{YYYYMMDD_HHMMSS}.csv`
- `run()`: Complete workflow - scrape, save, close driver (use in try/finally)

### Configuration Parameters

- `headless` (bool): Browser visibility. Use `False` for debugging page loading issues
- `wait_time` (int): Selenium explicit wait timeout in seconds. Default 10s, increase to 15-20s if tables not loading

## Output Structure

Files are saved to `output/` directory (or custom directory) with timestamp-based naming:

```
output/
├── wsj_market_diary_table_1_20250101_143022.csv    # Individual tables
├── wsj_market_diary_table_2_20250101_143022.csv
└── wsj_market_diary_combined_20250101_143022.csv   # All tables combined with separators
```

## Logging

All operations are logged to:
- **File**: `wsj_scraper.log` (persistent logs)
- **Console**: Real-time progress output
- **Format**: `%(asctime)s - %(levelname)s - %(message)s`

Access logger via `self.logger` in the WSJMarketDiaryScraper class.

## Common Issues & Debugging

### No Tables Found
- Increase `wait_time` parameter (try 15-20 seconds)
- Run with `headless=False` to observe browser behavior
- Check logs for timeout errors in `wait_for_tables()` method (wsj_market_diary_scraper.py:85-104)

### Table Extraction Failures
- WSJ may have changed HTML structure - inspect `extract_table_data()` logic (wsj_market_diary_scraper.py:106-158)
- Verify table rows have consistent column counts (normalization happens at lines 143-149)

### WebDriver Issues
- Scraper uses Microsoft Edge (pre-installed on Windows 10/11)
- System Edge driver is tried first (no download needed)
- Falls back to webdriver-manager if system driver not available
- Edge options configured for headless operation and anti-detection

## Testing

The `test_scraper.py` file contains three test functions:
1. `test_scraper_initialization()`: Validates constructor parameters
2. `test_driver_setup()`: Checks WebDriver initialization
3. `test_basic_scraping()`: End-to-end test with cleanup

Tests save to `test_output/` directory and clean up automatically.

## Dependencies

- `selenium>=4.15.0`: Browser automation
- `webdriver-manager>=4.0.0`: Automatic Edge driver management (fallback only)
- `beautifulsoup4>=4.12.0`: HTML parsing for table extraction
- `lxml>=4.9.0`: Fast XML/HTML parser for BeautifulSoup

## Ethical Considerations

This scraper includes rate limiting (3-second delays) and respects server load. When modifying:
- Do not remove delays in `wait_for_tables()` (wsj_market_diary_scraper.py:94)
- Maintain or increase wait times to avoid overwhelming WSJ servers
- This tool is for personal research/educational use only
