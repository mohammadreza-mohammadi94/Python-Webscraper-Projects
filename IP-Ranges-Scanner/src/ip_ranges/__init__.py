"""IP Ranges - A tool for scraping and converting IP ranges.

This package provides functionality to:
- Scrape IP ranges from ipdeny.com
- Convert CIDR notation to IP ranges
- Export data in multiple formats (JSON, CSV, TXT)
"""

__version__ = "1.0.0"
__author__ = "IP Ranges Contributors"

from .scraper import IPRangeScraper
from .converter import CIDRConverter

__all__ = ["IPRangeScraper", "CIDRConverter", "__version__"]
