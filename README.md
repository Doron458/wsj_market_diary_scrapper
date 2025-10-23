# WSJ Market Diary Scraper

A Python web scraper that extracts market diary tables from the Wall Street Journal's market data page and exports them to CSV files.

## Features

- **Automated Data Extraction**: Scrapes 6+ market diary tables from WSJ
- **CSV Export**: Saves individual and combined CSV files with timestamps
- **Headless Mode**: Runs invisibly in the background
- **Robust Error Handling**: Multiple wait strategies and debugging output
- **Windows Compatible**: Uses Microsoft Edge (pre-installed on Windows 10/11)

## Requirements

- Python 3.7+
- Microsoft Edge browser (pre-installed on Windows 10/11)
- Internet connection

## Installation

```bash
# Clone or download this repository
cd wsj_market_diary_scrapper

# Install dependencies
pip install -r requirements.txt
```

**Note**: No browser driver download needed! The scraper automatically uses the Microsoft Edge browser that comes with Windows.

## Quick Start

### Basic Usage

```bash
# Run the scraper (headless mode)
python wsj_market_diary_scraper.py
```

This will:
1. Launch Microsoft Edge in headless mode
2. Navigate to WSJ market diary page
3. Extract all market tables
4. Save CSV files to the `output/` directory

### Output Files

Files are saved with timestamps:
```
output/
├── wsj_market_diary_table_1_20251023_130259.csv
├── wsj_market_diary_table_2_20251023_130259.csv
├── ...
└── wsj_market_diary_combined_20251023_130259.csv
```

## Usage Examples

### Python Script

```python
from wsj_market_diary_scraper import WSJMarketDiaryScraper

# Basic usage
scraper = WSJMarketDiaryScraper(headless=True, wait_time=15)
try:
    saved_files = scraper.run(output_dir="output")
    print(f"Saved {len(saved_files)} files")
finally:
    scraper.close()
```

### Visible Browser Mode (for debugging)

```python
# Run with visible browser
scraper = WSJMarketDiaryScraper(headless=False, wait_time=20)
saved_files = scraper.run()
```

### Advanced Usage

```python
# Step-by-step control
scraper = WSJMarketDiaryScraper()
try:
    scraper.setup_driver()
    table_data = scraper.scrape_market_diary()

    # Process data before saving
    print(f"Found {len(table_data)} tables")
    for i, table in enumerate(table_data):
        print(f"Table {i+1}: {len(table)} rows")

    # Save to custom directory
    scraper.save_to_csv(table_data, output_dir="my_data")
finally:
    scraper.close()
```

## Testing

Run the test suite to verify everything works:

```bash
python test_scraper.py
```

See more examples:
```bash
python example_usage.py
```

## Configuration

### Scraper Parameters

- `headless` (bool): Run browser invisibly (default: `True`)
- `wait_time` (int): Maximum seconds to wait for page load (default: `15`)

### Increasing Wait Time

If tables aren't loading, increase wait time:

```python
scraper = WSJMarketDiaryScraper(headless=True, wait_time=20)
```

## Data Extracted

The scraper extracts the following market diary tables:
1. NYSE Trading Statistics (Issues, Advances, Declines, Volumes)
2. NASDAQ Trading Statistics
3. Market Indices Performance
4. Sector Performance
5. Options Statistics
6. Volume Leaders

## Logging

All operations are logged to:
- **File**: `wsj_scraper.log` (persistent logs)
- **Console**: Real-time progress output

## Troubleshooting

### No Tables Found

1. Increase wait time: `wait_time=20`
2. Run with visible browser: `headless=False`
3. Check `debug_page_source.html` file (created when scraping fails)
4. Check logs in `wsj_scraper.log`

### Edge Driver Issues

The scraper automatically uses the system Edge driver (no download needed). If you get driver errors:

1. Ensure Microsoft Edge is installed (comes with Windows 10/11)
2. Update Edge to the latest version
3. Check `wsj_scraper.log` for detailed error messages

### Network/Loading Issues

If the page isn't loading:
- Check your internet connection
- WSJ may have updated their site structure (check logs)
- Try increasing wait_time to 20+ seconds

## Ethical Use

This scraper includes rate limiting and respects server load:
- 5-second delay between operations
- Minimal resource usage
- For personal research/educational use only
- Respects WSJ's terms of service

## License

For educational and personal use only. Respect Wall Street Journal's terms of service.

## Support

For issues or questions:
1. Check `wsj_scraper.log` for errors
2. Run tests: `python test_scraper.py`
3. Try visible mode: `headless=False`
4. Review the CLAUDE.md file for technical details
