"""CIDR to IP Range Converter.

This module provides functionality to convert CIDR notation from .zone files
to IP ranges in multiple formats (JSON, CSV, TXT).
"""

import concurrent.futures
import json
import logging
import random
import ipaddress
from pathlib import Path
from typing import List, Dict, Optional, Set, Union

from .utils import ensure_directory, validate_cidr


logger = logging.getLogger(__name__)


class CIDRConverter:
    """Converter for transforming CIDR notation to IP ranges."""

    def __init__(
        self,
        input_path: Union[str, Path] = "data/ip_zones",
        output_dir: Union[str, Path] = "data/ip_ranges",
        output_formats: Optional[List[str]] = None,
        sample_rate: float = 1.0,
        max_workers: int = 1,
        timeout: Optional[int] = None,
        output_file_name: Optional[str] = None,
    ):
        """Initialize the CIDR Converter.

        Args:
            input_path: Directory containing .zone files OR path to a single .zone file
            output_dir: Directory to save converted files
            output_formats: List of output formats ('json', 'csv', 'txt', or 'all')
            sample_rate: Percentage of IPs to sample (0.0 to 1.0, default: 1.0)
            max_workers: Number of threads to use for processing
            timeout: Timeout in seconds for efficient processing
            output_file_name: Optional explicit filename for output (only for single file input)
        """
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.sample_rate = max(0.0, min(1.0, sample_rate))
        self.max_workers = max(1, max_workers)
        self.timeout = timeout
        self.output_file_name = output_file_name

        if output_formats is None:
            output_formats = ["json", "csv", "txt"]
        elif "all" in output_formats:
            output_formats = ["json", "csv", "txt"]

        self.output_formats = output_formats

        # Statistics
        self.total_ranges = 0
        self.total_ips = 0
        self.processed_files = 0
        self.failed_files = 0

    def cidr_to_ip_range(self, cidr: str) -> Optional[Dict[str, any]]:
        """Convert a CIDR notation to an IP range.

        Args:
            cidr: CIDR notation string (e.g., '192.168.1.0/24')

        Returns:
            Dictionary containing start_ip, end_ip, and total_ips, or None if invalid
        """
        if not validate_cidr(cidr):
            return None

        try:
            network = ipaddress.ip_network(cidr.strip(), strict=False)
            return {
                "cidr": cidr.strip(),
                "start_ip": str(network.network_address),
                "end_ip": str(network.broadcast_address),
                "total_ips": network.num_addresses,
            }
        except ValueError as e:
            logger.warning(f"Error processing CIDR {cidr}: {e}")
            return None

    def process_zone_file(self, zone_file_path: Path) -> List[Dict[str, any]]:
        """Process a single .zone file and convert all CIDR entries.

        Args:
            zone_file_path: Path to the .zone file

        Returns:
            List of dictionaries containing IP range information
        """
        ip_ranges = []

        try:
            with open(zone_file_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    # Convert CIDR to IP range
                    ip_range = self.cidr_to_ip_range(line)
                    if ip_range:
                        ip_ranges.append(ip_range)
                    else:
                        logger.debug(
                            f"Skipping invalid line {line_num} in {zone_file_path.name}: {line}"
                        )

        except Exception as e:
            logger.error(f"Error reading file {zone_file_path}: {e}")

        return ip_ranges

    def save_ranges_json(self, base_name: str, ip_ranges: List[Dict[str, any]]) -> None:
        """Save IP ranges to a JSON file.

        Args:
            base_name: Base name for the output file
            ip_ranges: List of IP range dictionaries
        """
        if self.output_file_name and len(self.output_formats) == 1:
            output_file = self.output_dir / self.output_file_name
        else:
            output_file = self.output_dir / f"{base_name}_ranges.json"

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "source": base_name.upper(),
                        "total_ranges": len(ip_ranges),
                        "total_ips": sum(r["total_ips"] for r in ip_ranges),
                        "sample_rate": self.sample_rate,
                        "ranges": ip_ranges,
                    },
                    f,
                    indent=2,
                )

            logger.debug(f"Saved JSON: {output_file.name}")

        except Exception as e:
            logger.error(f"Error saving JSON file for {base_name}: {e}")

    def save_ranges_csv(self, base_name: str, ip_ranges: List[Dict[str, any]]) -> None:
        """Save IP ranges to a CSV file.

        Args:
            base_name: Base name for the output file
            ip_ranges: List of IP range dictionaries
        """
        if self.output_file_name and len(self.output_formats) == 1:
            output_file = self.output_dir / self.output_file_name
        else:
            output_file = self.output_dir / f"{base_name}_ranges.csv"

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                # Write header
                f.write("CIDR,Start_IP,End_IP,Total_IPs\n")

                # Write data
                for ip_range in ip_ranges:
                    f.write(
                        f"{ip_range['cidr']},{ip_range['start_ip']},{ip_range['end_ip']},{ip_range['total_ips']}\n"
                    )

            logger.debug(f"Saved CSV: {output_file.name}")

        except Exception as e:
            logger.error(f"Error saving CSV file for {base_name}: {e}")

    def save_ranges_txt(self, base_name: str, ip_ranges: List[Dict[str, any]]) -> None:
        """Save IP ranges to a simple text file with one IP per line.

        Supports sampling based on self.sample_rate.

        Args:
            base_name: Base name for the output file
            ip_ranges: List of IP range dictionaries
        """
        if self.output_file_name and len(self.output_formats) == 1:
            output_file = self.output_dir / self.output_file_name
        else:
            output_file = self.output_dir / f"{base_name}_ranges.txt"

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                for ip_range in ip_ranges:
                    try:
                        # Reconstruct network object
                        network = ipaddress.ip_network(ip_range["cidr"], strict=False)

                        if self.sample_rate >= 1.0:
                            # Write all IPs
                            for ip in network:
                                f.write(f"{ip}\n")
                        elif self.sample_rate > 0.0:
                            # Random sampling logic
                            total_ips = network.num_addresses
                            k = max(1, int(total_ips * self.sample_rate))

                            if k >= total_ips:
                                # Write all if sample size covers everything
                                for ip in network:
                                    f.write(f"{ip}\n")
                            else:
                                # Efficient random sampling using indices
                                # random.sample on range() is efficient in Python 3
                                indices = sorted(random.sample(range(total_ips), k))
                                network_int = int(network.network_address)

                                for idx in indices:
                                    ip_int = network_int + idx
                                    f.write(f"{ipaddress.IPv4Address(ip_int)}\n")

                    except ValueError:
                        logger.warning(f"Could not expand CIDR: {ip_range['cidr']} for {base_name}")

            logger.debug(f"Saved TXT: {output_file.name}")

        except Exception as e:
            logger.error(f"Error saving TXT file for {base_name}: {e}")

    def convert_file(self, zone_file: Path) -> Optional[dict]:
        """Convert a single zone file to IP ranges.

        Args:
            zone_file: Path to the .zone file

        Returns:
            Stats dict if successful, None if failed
        """
        base_name = zone_file.stem

        logger.info(f"Processing {base_name.upper()}...")

        # Convert CIDR to IP ranges
        ip_ranges = self.process_zone_file(zone_file)

        if not ip_ranges:
            logger.warning(f"No valid ranges found for {base_name.upper()}")
            return None

        # Update statistics (thread-safe updates might be needed if this were shared state,
        # but we are returning values to be aggregated)
        file_ranges = len(ip_ranges)
        file_ips = sum(r["total_ips"] for r in ip_ranges)

        # Save in requested format(s)
        if "json" in self.output_formats:
            self.save_ranges_json(base_name, ip_ranges)

        if "csv" in self.output_formats:
            self.save_ranges_csv(base_name, ip_ranges)

        if "txt" in self.output_formats:
            self.save_ranges_txt(base_name, ip_ranges)

        logger.info(f"[OK] {base_name.upper()} - {file_ranges} ranges, {file_ips:,} IPs")

        return {"ranges": file_ranges, "ips": file_ips}

    def convert_all(self) -> dict:
        """Convert all .zone files to IP ranges.

        Returns:
            Dictionary with conversion statistics
        """
        # Ensure output directory exists
        ensure_directory(self.output_dir)
        logger.info(f"Output directory: {self.output_dir.absolute()}")
        if self.sample_rate < 1.0:
            logger.info(f"Sampling enabled: {self.sample_rate*100:.2f}%")

        # Determine files to process
        zone_files = []
        if self.input_path.is_file():
            zone_files = [self.input_path]
            logger.info(f"Processing single file: {self.input_path.name}")
        elif self.input_path.is_dir():
            zone_files = list(self.input_path.glob("*.zone"))
            logger.info(f"Found {len(zone_files)} .zone files in {self.input_path}")
        else:
            logger.error(f"Input path not found: {self.input_path}")
            return {
                "total_files": 0,
                "processed_files": 0,
                "total_ranges": 0,
                "total_ips": 0,
            }

        if not zone_files:
            logger.warning(f"No files to process")
            return {
                "total_files": 0,
                "processed_files": 0,
                "total_ranges": 0,
                "total_ips": 0,
            }

        logger.info("=" * 60)

        # Reset statistics
        self.total_ranges = 0
        self.total_ips = 0
        self.processed_files = 0
        self.failed_files = 0

        # Process files using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {executor.submit(self.convert_file, zf): zf for zf in zone_files}

            try:
                # Iterate over completed futures, potentially with a timeout
                for future in concurrent.futures.as_completed(future_to_file, timeout=self.timeout):
                    zf = future_to_file[future]
                    try:
                        stats = future.result()
                        if stats:
                            self.processed_files += 1
                            self.total_ranges += stats["ranges"]
                            self.total_ips += stats["ips"]
                        else:
                            self.failed_files += 1
                    except Exception as exc:
                        logger.error(f"{zf.name} generated an exception: {exc}")
                        self.failed_files += 1

            except concurrent.futures.TimeoutError:
                logger.error(f"Operation timed out after {self.timeout} seconds")
                # Cancel remaining futures
                for future in future_to_file:
                    future.cancel()

        # Summary
        logger.info("=" * 60)
        logger.info("Conversion Summary:")
        logger.info(f"  Total files processed: {self.processed_files}")
        if self.failed_files > 0:
            logger.info(f"  Failed files: {self.failed_files}")
        logger.info(f"  Total IP ranges: {self.total_ranges:,}")
        logger.info(f"  Total IP addresses: {self.total_ips:,}")
        if self.sample_rate < 1.0:
            logger.info(f"  Sampling Rate: {self.sample_rate*100:.2f}%")
        logger.info(f"  Output saved to: {self.output_dir.absolute()}")

        return {
            "total_files": len(zone_files),
            "processed_files": self.processed_files,
            "failed_files": self.failed_files,
            "total_ranges": self.total_ranges,
            "total_ips": self.total_ips,
        }


def convert_cidr_ranges(
    input_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    output_formats: Optional[List[str]] = None,
    sample_rate: Optional[float] = None,
    max_workers: int = 1,
    timeout: Optional[int] = None,
    output_file_name: Optional[str] = None,
    config: Optional[dict] = None,
) -> dict:
    """Convenience function to convert CIDR ranges.

    Args:
        input_path: Input directory or file (overrides config)
        output_dir: Output directory (overrides config)
        output_formats: Output formats (overrides config)
        sample_rate: Sampling rate (overrides config)
        max_workers: Number of threads (default: 1)
        timeout: Timeout in seconds
        output_file_name: Explicit output filename (only for single file input)
        config: Configuration dictionary

    Returns:
        Dictionary with conversion statistics
    """
    if config is None:
        from .utils import get_default_config

        config = get_default_config()

    converter_config = config.get("converter", {})

    if sample_rate is None:
        sample_rate = converter_config.get("sample_rate", 1.0)

    converter = CIDRConverter(
        input_path=input_path or converter_config.get("input_dir", "data/ip_zones"),
        output_dir=output_dir or converter_config.get("output_dir", "data/ip_ranges"),
        output_formats=output_formats
        or converter_config.get("output_formats", ["json", "csv", "txt"]),
        sample_rate=float(sample_rate),
        max_workers=max_workers,
        timeout=timeout,
        output_file_name=output_file_name,
    )

    return converter.convert_all()
