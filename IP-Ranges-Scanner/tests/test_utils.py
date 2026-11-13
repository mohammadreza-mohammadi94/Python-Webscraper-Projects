"""Tests for utility functions."""

import pytest
from ip_ranges.utils import validate_cidr, format_bytes, get_default_config


class TestUtils:
    """Test cases for utility functions."""

    def test_validate_cidr_valid(self):
        """Test CIDR validation with valid inputs."""
        assert validate_cidr("192.168.1.0/24") is True
        assert validate_cidr("10.0.0.0/8") is True
        assert validate_cidr("172.16.0.0/12") is True
        assert validate_cidr("8.8.8.8/32") is True

    def test_validate_cidr_invalid(self):
        """Test CIDR validation with invalid inputs."""
        assert validate_cidr("invalid") is False
        assert validate_cidr("192.168.1.0") is False
        assert validate_cidr("192.168.1.0/33") is False
        assert validate_cidr("") is False

    def test_format_bytes(self):
        """Test byte formatting."""
        assert format_bytes(0) == "0.0 B"
        assert format_bytes(1024) == "1.0 KB"
        assert format_bytes(1024 * 1024) == "1.0 MB"
        assert format_bytes(1024 * 1024 * 1024) == "1.0 GB"
        assert format_bytes(500) == "500.0 B"
        assert format_bytes(1536) == "1.5 KB"

    def test_get_default_config(self):
        """Test default configuration."""
        config = get_default_config()

        assert "scraper" in config
        assert "converter" in config
        assert "logging" in config

        assert config["scraper"]["source_url"] == "https://www.ipdeny.com/ipblocks/"
        assert config["converter"]["output_formats"] == ["json", "csv", "txt"]
        assert config["logging"]["level"] == "INFO"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
