"""Utility functions for IP Ranges tool."""

import yaml
import logging
import ipaddress
from pathlib import Path
from typing import Dict, Any, Optional


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary containing configuration settings

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    config_file = Path(config_path)

    if not config_file.exists():
        # Return default configuration
        return get_default_config()

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config


def get_default_config() -> Dict[str, Any]:
    """Get default configuration settings.

    Returns:
        Dictionary with default configuration
    """
    return {
        "scraper": {
            "source_url": "https://www.ipdeny.com/ipblocks/",
            "output_dir": "data/ip_zones",
            "delay_seconds": 0.1,
            "max_retries": 3,
            "timeout": 30,
        },
        "converter": {
            "input_dir": "data/ip_zones",
            "output_dir": "data/ip_ranges",
            "output_formats": ["json", "csv", "txt"],
            "batch_size": 100,
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "logs/ip_ranges.log",
        },
    }


def setup_logging(config: Optional[Dict[str, Any]] = None) -> None:
    """Configure logging for the application.

    Args:
        config: Configuration dictionary with logging settings
    """
    if config is None:
        config = get_default_config()

    log_config = config.get("logging", {})
    level = getattr(logging, log_config.get("level", "INFO"))
    log_format = log_config.get(
        "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    log_file = log_config.get("file")

    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configure logging
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(level=level, format=log_format, handlers=handlers)


def validate_cidr(cidr: str) -> bool:
    """Validate CIDR notation.

    Args:
        cidr: CIDR notation string (e.g., '192.168.1.0/24')

    Returns:
        True if valid CIDR notation, False otherwise
    """
    try:
        ipaddress.ip_network(cidr.strip(), strict=False)
        return True
    except (ValueError, AttributeError):
        return False


def ensure_directory(path: str) -> Path:
    """Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def format_bytes(size: int) -> str:
    """Format bytes to human-readable string.

    Args:
        size: Size in bytes

    Returns:
        Formatted string (e.g., '1.5 MB')
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"
