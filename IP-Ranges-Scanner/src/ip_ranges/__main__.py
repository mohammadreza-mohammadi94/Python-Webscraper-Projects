"""Command-line interface for IP Ranges tool."""

import argparse
import sys
import logging
from pathlib import Path

from . import __version__
from .scraper import scrape_ip_ranges
from .converter import convert_cidr_ranges
from .utils import load_config, setup_logging, get_default_config


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="ip-ranges",
        description="IP Ranges - Scrape and convert IP ranges from ipdeny.com",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape all zone files
  ip-ranges scrape
  
  # Convert zone files to IP ranges (all formats)
  ip-ranges convert
  
  # Convert to only JSON format
  ip-ranges convert --format json
  
  # Use custom directories
  ip-ranges scrape --output custom_zones
  ip-ranges convert --input custom_zones --output custom_ranges
        """,
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    parser.add_argument(
        "--config",
        "-c",
        help="Path to configuration file (default: config.yaml)",
        default="config.yaml",
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape IP zone files from ipdeny.com")
    scrape_parser.add_argument(
        "--output",
        "-o",
        help="Output directory for zone files (default: data/ip_zones)",
    )

    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert CIDR notation to IP ranges")
    convert_parser.add_argument(
        "--input",
        "-i",
        help="Input directory containing .zone files or path to a single .zone file (default: data/ip_zones)",
    )
    convert_parser.add_argument(
        "--output",
        "-o",
        help="Output directory for converted files (default: data/ip_ranges)",
    )
    convert_parser.add_argument(
        "--output-file",
        help="Explicit output filename (only for single file input and single format).",
    )
    convert_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv", "txt", "all"],
        nargs="+",
        help="Output format(s) (default: all)",
    )

    convert_parser.add_argument(
        "--sample-rate",
        "-s",
        type=float,
        help="Percentage of IPs to sample (0.0 to 1.0, e.g. 0.01 for 1%%)",
    )

    convert_parser.add_argument(
        "--threads",
        "-t",
        type=int,
        default=1,
        help="Number of threads to use for processing (default: 1)",
    )

    convert_parser.add_argument(
        "--timeout",
        type=int,
        help="Timeout in seconds for total operation",
    )

    return parser


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Warning: Could not load config file '{args.config}': {e}")
        print("Using default configuration...")
        config = get_default_config()

    # Setup logging
    if args.verbose:
        config["logging"]["level"] = "DEBUG"

    setup_logging(config)
    logger = logging.getLogger(__name__)

    # Execute command
    if args.command == "scrape":
        logger.info("=" * 60)
        logger.info("IP Ranges Scraper")
        logger.info("=" * 60)

        try:
            stats = scrape_ip_ranges(output_dir=args.output, config=config)

            if stats["failed"] > 0:
                sys.exit(1)

        except Exception as e:
            logger.error(f"Error during scraping: {e}", exc_info=args.verbose)
            sys.exit(1)

    elif args.command == "convert":
        logger.info("=" * 60)
        logger.info("CIDR to IP Range Converter")
        logger.info("=" * 60)

        # Basic validation for output-file
        if args.output_file and args.input and Path(args.input).is_dir():
            logger.error("--output-file can only be used when --input is a single file")
            sys.exit(1)

        try:
            stats = convert_cidr_ranges(
                input_path=args.input,
                output_dir=args.output,
                output_formats=args.format,
                sample_rate=args.sample_rate,
                max_workers=args.threads,
                timeout=args.timeout,
                output_file_name=args.output_file,
                config=config,
            )

            if stats["processed_files"] == 0:
                logger.warning("No files were processed")
                sys.exit(1)

        except Exception as e:
            logger.error(f"Error during conversion: {e}", exc_info=args.verbose)
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
