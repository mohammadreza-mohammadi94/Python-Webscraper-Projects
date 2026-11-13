# IP Ranges

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional Python package for scraping and converting IP ranges from [ipdeny.com](https://www.ipdeny.com/ipblocks/).

## Features

- 🌍 **Scrape IP Ranges**: Download IP ranges for all countries in `.zone` format
- 🔄 **Convert CIDR**: Convert CIDR notation to IP ranges in multiple formats
- 📊 **Multiple Formats**: Export as JSON, CSV, or TXT
- ⚙️ **Configurable**: Centralized YAML configuration
- 🖥️ **CLI Interface**: Professional command-line interface
- 📝 **Logging**: Comprehensive logging with file and console output
- 🧪 **Tested**: Unit tests with pytest
- 🛡️ **Robust**: Retry logic, error handling, and validation

## Installation

### Prerequisites
- Python 3.6 or higher
- Git (optional, for cloning)

### Initial Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohammadreza-mohammadi94/IP-Ranges-Scanner.git
   cd IP-Ranges
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the package:**
   ```bash
   # Install dependencies and the package
   pip install -e .
   
   # Or install from requirements directly
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   ip-ranges --version
   ```



## Quick Start

### Scrape IP Zones

Download all country IP ranges from ipdeny.com:

```bash
ip-ranges scrape
```

This will download all `.zone` files to `data/ip_zones/`.

### Convert to IP Ranges

Convert CIDR notation to IP ranges:

```bash
ip-ranges convert
```

This will convert all zone files and save them in `data/ip_ranges/` in JSON, CSV, and TXT formats.

### Custom Options

```bash
# Scrape to custom directory
ip-ranges scrape --output custom_zones

# Turn on verbose logging
ip-ranges --verbose convert

# 🚀 NEW: Convert using multiple threads (faster for many files)
ip-ranges convert --threads 4

# 🚀 NEW: Convert a single zone file to a specific output file
ip-ranges convert --input data/ip_zones/cn.zone --output-file cn_ips.json --format json

# 🚀 NEW: Set a timeout for long-running operations (seconds)
ip-ranges convert --timeout 60

# Convert with specific format(s)
ip-ranges convert --format json csv

# Convert with random sampling (e.g. 1%)
ip-ranges convert --sample-rate 0.01

# Convert with custom directories
ip-ranges convert --input custom_zones --output custom_ranges
```

## Configuration

Create a `config.yaml` file to customize settings:

```yaml
scraper:
  source_url: "https://www.ipdeny.com/ipblocks/"
  output_dir: "data/ip_zones"
  delay_seconds: 0.1
  max_retries: 3
  timeout: 30

converter:
  input_dir: "data/ip_zones"
  output_dir: "data/ip_ranges"
  output_formats:
    - json
    - csv
    - txt

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/ip_ranges.log"
```

## Output Formats

### JSON Format

```json
{
  "country_code": "US",
  "total_ranges": 69358,
  "total_ips": 1610095968,
  "ranges": [
    {
      "cidr": "14.1.64.0/19",
      "start_ip": "14.1.64.0",
      "end_ip": "14.1.95.255",
      "total_ips": 8192
    }
  ]
}
```

### CSV Format

```csv
CIDR,Start_IP,End_IP,Total_IPs
14.1.64.0/19,14.1.64.0,14.1.95.255,8192
27.100.36.0/22,27.100.36.0,27.100.39.255,1024
```

### TXT Format

```
14.1.64.0
14.1.64.1
14.1.64.2
...
```

> **Warning**: The TXT format lists **every single IP address** on a new line. For large countries, this can result in extremely large files (GBs).

## Project Structure

```
IP-Ranges/
├── src/
│   └── ip_ranges/          # Main package
│       ├── __init__.py     # Package initialization
│       ├── __main__.py     # CLI entry point
│       ├── scraper.py      # Scraping functionality
│       ├── converter.py    # CIDR conversion
│       └── utils.py        # Utility functions
├── tests/                  # Unit tests
├── data/
│   ├── ip_zones/          # Downloaded zone files
│   └── ip_ranges/         # Converted IP ranges
├── docs/                   # Documentation
├── logs/                   # Application logs
├── config.yaml            # Configuration file
├── setup.py               # Package setup
├── pyproject.toml         # Modern Python config
└── README.md              # This file
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/ip_ranges --cov-report=html

# Run specific test file
pytest tests/test_converter.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## Usage as Library

You can also use IP Ranges as a Python library:

```python
from ip_ranges import IPRangeScraper, CIDRConverter

# Scrape IP ranges
scraper = IPRangeScraper(output_dir="my_zones")
stats = scraper.download_all()
print(f"Downloaded {stats['successful']} files")

# Convert CIDR to IP ranges
converter = CIDRConverter(
    input_dir="my_zones",
    output_dir="my_ranges",
    output_formats=["json"]
)
stats = converter.convert_all()
print(f"Converted {stats['total_ranges']} ranges")
```

## Statistics

Example output for 233 countries:

```
✅ Conversion Complete!
   Total countries processed: 233
   Total IP ranges: 1,234,567
   Total IP addresses: 3,456,789,012
   
   Output saved to: data/ip_ranges
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- IP range data sourced from [ipdeny.com](https://www.ipdeny.com/ipblocks/)
- Please respect ipdeny.com's [usage limits](https://www.ipdeny.com/usagelimits.php) and [copyright policy](https://www.ipdeny.com/copyright.php)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/IP-Ranges/issues) on GitHub.
