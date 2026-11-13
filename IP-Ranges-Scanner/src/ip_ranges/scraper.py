"""IP Range Scraper for ipdeny.com.

This module provides functionality to scrape and download IP ranges
from ipdeny.com in .zone format.
"""

import re
import time
import logging
from pathlib import Path
from typing import List, Tuple, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .utils import ensure_directory, format_bytes


logger = logging.getLogger(__name__)


class IPRangeScraper:
    """Scraper for downloading IP range zone files from ipdeny.com."""

    def __init__(
        self,
        source_url: str = "https://www.ipdeny.com/ipblocks/",
        output_dir: str = "data/ip_zones",
        delay_seconds: float = 0.1,
        max_retries: int = 3,
        timeout: int = 30,
    ):
        """Initialize the IP Range Scraper.

        Args:
            source_url: Base URL to scrape zone files from
            output_dir: Directory to save downloaded files
            delay_seconds: Delay between requests (seconds)
            max_retries: Maximum number of retry attempts
            timeout: Request timeout (seconds)
        """
        self.source_url = source_url
        self.output_dir = Path(output_dir)
        self.delay_seconds = delay_seconds
        self.max_retries = max_retries
        self.timeout = timeout

        # Statistics
        self.successful_downloads = 0
        self.failed_downloads = 0

    def scrape_zone_files(self) -> List[Tuple[str, str]]:
        """Scrape the website and extract all .zone file URLs.

        Returns:
            List of tuples containing (country_code, zone_url)
        """
        logger.info(f"Fetching page: {self.source_url}")

        try:
            response = requests.get(self.source_url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all links that end with .zone
        zone_links = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            # Match links to .zone files in the countries directory
            if href.endswith(".zone") and "/countries/" in href:
                # Extract country code from the filename
                match = re.search(r"/([a-z]{2})\.zone$", href)
                if match:
                    country_code = match.group(1)
                    full_url = urljoin(self.source_url, href)
                    zone_links.append((country_code, full_url))

        logger.info(f"Found {len(zone_links)} zone files")
        return zone_links

    def download_zone_file(self, country_code: str, url: str) -> bool:
        """Download a single zone file with retry logic.

        Args:
            country_code: Two-letter country code
            url: URL of the zone file

        Returns:
            True if successful, False otherwise
        """
        filename = f"{country_code}.zone"
        filepath = self.output_dir / filename

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(
                    f"Downloading {country_code.upper()} (attempt {attempt}/{self.max_retries})..."
                )

                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()

                with open(filepath, "wb") as f:
                    f.write(response.content)

                file_size = len(response.content)
                logger.info(
                    f"✓ {country_code.upper()} downloaded ({format_bytes(file_size)})"
                )

                self.successful_downloads += 1
                return True

            except requests.RequestException as e:
                logger.warning(
                    f"Attempt {attempt} failed for {country_code.upper()}: {e}"
                )

                if attempt < self.max_retries:
                    # Exponential backoff
                    wait_time = self.delay_seconds * (2 ** (attempt - 1))
                    time.sleep(wait_time)
                else:
                    logger.error(
                        f"✗ Failed to download {country_code.upper()} after {self.max_retries} attempts"
                    )
                    self.failed_downloads += 1
                    return False

        return False

    def download_all(self) -> dict:
        """Download all zone files.

        Returns:
            Dictionary with download statistics
        """
        # Ensure output directory exists
        ensure_directory(self.output_dir)
        logger.info(f"Output directory: {self.output_dir.absolute()}")

        # Scrape zone file URLs
        zone_files = self.scrape_zone_files()

        if not zone_files:
            logger.warning("No zone files found")
            return {"total": 0, "successful": 0, "failed": 0}

        logger.info(f"Starting download of {len(zone_files)} files...")
        logger.info("-" * 60)

        # Reset statistics
        self.successful_downloads = 0
        self.failed_downloads = 0

        # Download each zone file
        for country_code, url in zone_files:
            self.download_zone_file(country_code, url)
            time.sleep(self.delay_seconds)

        # Summary
        logger.info("-" * 60)
        logger.info("Download Summary:")
        logger.info(f"  ✓ Successful: {self.successful_downloads}")
        logger.info(f"  ✗ Failed: {self.failed_downloads}")
        logger.info(f"  Total: {len(zone_files)}")
        logger.info(f"Files saved to: {self.output_dir.absolute()}")

        return {
            "total": len(zone_files),
            "successful": self.successful_downloads,
            "failed": self.failed_downloads,
        }


def scrape_ip_ranges(
    output_dir: Optional[str] = None, config: Optional[dict] = None
) -> dict:
    """Convenience function to scrape IP ranges.

    Args:
        output_dir: Output directory (overrides config)
        config: Configuration dictionary

    Returns:
        Dictionary with download statistics
    """
    if config is None:
        from .utils import get_default_config

        config = get_default_config()

    scraper_config = config.get("scraper", {})

    scraper = IPRangeScraper(
        source_url=scraper_config.get("source_url", "https://www.ipdeny.com/ipblocks/"),
        output_dir=output_dir or scraper_config.get("output_dir", "data/ip_zones"),
        delay_seconds=scraper_config.get("delay_seconds", 0.1),
        max_retries=scraper_config.get("max_retries", 3),
        timeout=scraper_config.get("timeout", 30),
    )

    return scraper.download_all()
