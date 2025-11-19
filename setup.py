"""
Setup script for paper_tree package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="paper_tree",
    version="0.1.0",
    author="Paper Tree Contributors",
    author_email="",
    description="A Python library for building and analyzing academic paper citation trees",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/paper_tree",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "postgres": ["psycopg2-binary>=2.9.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
        "all": [
            "psycopg2-binary>=2.9.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
    },
    entry_points={
        "console_scripts": [
            "paper-tree=paper_tree.cli:main",
        ],
    },
    keywords="citation tree academic papers semantic scholar research",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/paper_tree/issues",
        "Source": "https://github.com/yourusername/paper_tree",
    },
)
