"""Setup configuration for IP Ranges package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="ip-ranges",
    version="1.0.0",
    author="IP Ranges Contributors",
    description="A tool for scraping and converting IP ranges from ipdeny.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mohammadreza-mohammadi94/IP-Ranges-Scanner",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Internet",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ip-ranges=ip_ranges.__main__:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
