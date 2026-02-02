"""
Setup configuration for Qualtrics SDK
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read version from package
about = {}
with open(this_directory / "qualtrics_sdk" / "__init__.py") as f:
    exec(f.read(), about)

setup(
    name="qualtrics-sdk",
    version=about["__version__"],
    author=about["__author__"],
    author_email="your.email@example.com",
    description="A comprehensive Python SDK for the Qualtrics REST API v3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/qualtrics-sdk",
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "qualtrics=qualtrics_sdk.cli:main",
        ],
    },
    keywords="qualtrics api survey research data-collection",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/qualtrics-sdk/issues",
        "Source": "https://github.com/yourusername/qualtrics-sdk",
        "Documentation": "https://github.com/yourusername/qualtrics-sdk/blob/main/README.md",
    },
)
