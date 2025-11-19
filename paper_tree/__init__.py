"""
Paper Tree - A Python library for building and analyzing academic paper citation trees.

This library provides tools to:
- Fetch paper data from Semantic Scholar API
- Build citation trees with customizable depth
- Export to JSON and PostgreSQL
- Analyze citation networks

Basic usage:
    >>> from paper_tree import CitationTreeBuilder
    >>> builder = CitationTreeBuilder(api_key="your_api_key")
    >>> tree = builder.build_tree("ARXIV:1706.03762", max_depth=2)
    >>> tree.to_json("output.json")
"""

__version__ = "0.1.0"
__author__ = "Paper Tree Contributors"
__license__ = "MIT"

from .tree_builder import CitationTreeBuilder
from .models import Paper, CitationTree
from .exporters import JSONExporter, PostgreSQLExporter
from .api import SemanticScholarAPI

__all__ = [
    "CitationTreeBuilder",
    "Paper",
    "CitationTree",
    "JSONExporter",
    "PostgreSQLExporter",
    "SemanticScholarAPI",
]
