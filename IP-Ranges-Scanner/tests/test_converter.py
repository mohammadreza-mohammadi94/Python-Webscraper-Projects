"""Tests for CIDR converter module."""

import pytest
from pathlib import Path
from ip_ranges.converter import CIDRConverter


class TestCIDRConverter:
    """Test cases for CIDRConverter class."""

    def test_cidr_to_ip_range_valid(self):
        """Test CIDR to IP range conversion with valid input."""
        converter = CIDRConverter()
        result = converter.cidr_to_ip_range("192.168.1.0/24")

        assert result is not None
        assert result["cidr"] == "192.168.1.0/24"
        assert result["start_ip"] == "192.168.1.0"
        assert result["end_ip"] == "192.168.1.255"
        assert result["total_ips"] == 256

    def test_cidr_to_ip_range_slash_32(self):
        """Test CIDR conversion for single IP (/32)."""
        converter = CIDRConverter()
        result = converter.cidr_to_ip_range("10.0.0.1/32")

        assert result is not None
        assert result["start_ip"] == "10.0.0.1"
        assert result["end_ip"] == "10.0.0.1"
        assert result["total_ips"] == 1

    def test_cidr_to_ip_range_slash_16(self):
        """Test CIDR conversion for /16 network."""
        converter = CIDRConverter()
        result = converter.cidr_to_ip_range("172.16.0.0/16")

        assert result is not None
        assert result["start_ip"] == "172.16.0.0"
        assert result["end_ip"] == "172.16.255.255"
        assert result["total_ips"] == 65536

    def test_cidr_to_ip_range_invalid(self):
        """Test CIDR conversion with invalid input."""
        converter = CIDRConverter()
        result = converter.cidr_to_ip_range("invalid")

        assert result is None

    def test_cidr_to_ip_range_empty(self):
        """Test CIDR conversion with empty string."""
        converter = CIDRConverter()
        result = converter.cidr_to_ip_range("")

        assert result is None

    def test_converter_initialization(self):
        """Test converter initialization with custom parameters."""
        converter = CIDRConverter(
            input_dir="custom_input", output_dir="custom_output", output_formats=["json"]
        )

        assert converter.input_dir == Path("custom_input")
        assert converter.output_dir == Path("custom_output")
        assert converter.output_formats == ["json"]

    def test_converter_all_formats(self):
        """Test converter with 'all' format option."""
        converter = CIDRConverter(output_formats=["all"])

        assert "json" in converter.output_formats
        assert "csv" in converter.output_formats
        assert "txt" in converter.output_formats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
