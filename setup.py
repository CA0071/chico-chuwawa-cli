"""
Setup script for Chico Chuwawa AI CLI
Built by Max van Heerden
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="chico-cli",
    version="3.0.0",
    author="Max van Heerden",
    author_email="",
    description="A comprehensive AI CLI tool with multi-provider support and integrations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CA0071/chico-chuwawa-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "openai>=1.0.0",
        "ollama>=0.1.0",
        "requests>=2.31.0",
        "pygments>=2.15.0",
        "colorama>=0.4.6",
        "rich>=13.0.0",
        "pyfiglet>=0.8.0",
        "qrcode>=7.4.0",
        "pillow>=10.0.0",
        "duckduckgo-search>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "chico=chico-cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.png", "*.json"],
    },
)
