# Paper Tree

A Python library for building and analyzing academic paper citation trees using the Semantic Scholar API.

## Features

- 🌳 **Build Citation Trees**: Construct citation networks starting from any paper
- 🔍 **Automatic Deduplication**: Efficiently handle papers cited multiple times
- 📊 **Flexible Depth Control**: Customize how deep to traverse the citation network
- 💾 **Multiple Export Formats**: Save to JSON or PostgreSQL
- 🚀 **Rate Limit Handling**: Built-in retry logic and rate limiting
- 📈 **Rich Metadata**: Track depth, citations, authors, and references

## Installation

### Basic Installation

```bash
pip install paper-tree
```

### With PostgreSQL Support

```bash
pip install paper-tree[postgres]
```

### Development Installation

```bash
git clone https://github.com/yourusername/paper_tree.git
cd paper_tree
pip install -e .[dev]
```

## Quick Start

### Building a Citation Tree

```python
from paper_tree import CitationTreeBuilder

# Initialize builder with API key (optional but recommended)
builder = CitationTreeBuilder(api_key="your_semantic_scholar_api_key")

# Build citation tree starting from a paper
tree = builder.build_tree("ARXIV:1706.03762", max_depth=2)

print(f"Built tree with {len(tree)} papers")
print(f"Root paper: {tree.root_title}")
```

### Exporting to JSON

```python
from paper_tree import JSONExporter

tree = {""} # Your Json

# Export to JSON file
exporter = JSONExporter()
exporter.export(tree, "citation_tree.json")
```

### Exporting to PostgreSQL

```python
from paper_tree import PostgreSQLExporter

tree = {""} # Your Json

# Configure database connection
db_exporter = PostgreSQLExporter(
    host="localhost",
    database="paper_db",
    user="postgres",
    password="your_password",
    table_name="citation_tree"
)

# Export to database
db_exporter.export(tree, drop_existing=True)
```

## Usage Examples

### Basic Citation Tree

```python
from paper_tree import CitationTreeBuilder, JSONExporter

# Create builder
builder = CitationTreeBuilder(api_key="your_api_key")

# Build tree from "Attention is All you Need" paper
tree = builder.build_tree("ARXIV:1706.03762", max_depth=2)

# Get statistics
stats = tree.get_statistics()
print(f"Total papers: {stats['total_papers']}")
print(f"Max depth: {stats['max_depth']}")
print(f"Papers by depth: {stats['papers_by_depth']}")

# Export to JSON
JSONExporter.export(tree, "attention_tree.json")
```

### Building Multiple Trees

```python
from paper_tree import CitationTreeBuilder

builder = CitationTreeBuilder(api_key="your_api_key")

# Build trees from multiple root papers
root_papers = [
    "ARXIV:1706.03762",  # Attention is All you Need
    "ARXIV:1512.03385",  # ResNet
    "ARXIV:1409.0473",   # GoogLeNet
]

trees = builder.build_tree_from_multiple_roots(root_papers, max_depth=1)

for tree in trees:
    print(f"{tree.root_title}: {len(tree)} papers")
```

### Working with Papers

```python

tree = {""} # Your Json

# Get root paper
root = tree.get_root_paper()
print(f"Title: {root.title}")
print(f"Year: {root.year}")
print(f"Citations: {root.citation_count}")

# Get papers at specific depth
depth_1_papers = tree.get_papers_by_depth(1)
print(f"Found {len(depth_1_papers)} papers at depth 1")

# Check if paper exists in tree
if "some_paper_id" in tree:
    paper = tree.get_paper("some_paper_id")
    print(f"Found: {paper.title}")
```

### Context Manager Usage

```python
from paper_tree import CitationTreeBuilder

# Use context manager for automatic cleanup
with CitationTreeBuilder(api_key="your_api_key") as builder:
    tree = builder.build_tree("ARXIV:1706.03762", max_depth=2)
    # API session is automatically closed
```

## API Reference

### CitationTreeBuilder

Main class for building citation trees.

**Parameters:**
- `api_key` (str, optional): Semantic Scholar API key
- `rate_limit_delay` (float): Delay between API requests in seconds (default: 1.5)
- `max_retries` (int): Maximum retry attempts for failed requests (default: 3)

**Methods:**
- `build_tree(root_paper_id, max_depth=2, verbose=True)`: Build a citation tree
- `build_tree_from_multiple_roots(root_paper_ids, max_depth=2, verbose=True)`: Build multiple trees
- `close()`: Close the API session

### CitationTree

Represents a citation tree structure.

**Properties:**
- `root_title`: Title of the root paper
- `size`: Total number of papers
- `max_depth`: Maximum depth in the tree

**Methods:**
- `get_paper(paper_id)`: Get a paper by ID
- `get_papers_by_depth(depth)`: Get all papers at a specific depth
- `get_root_paper()`: Get the root paper
- `to_dict()`: Convert to dictionary format
- `get_statistics()`: Get tree statistics

### JSONExporter

Export citation trees to JSON format.

**Methods:**
- `export(tree, filename, indent=2, ensure_ascii=False)`: Export tree to JSON file
- `load(filename)`: Load tree from JSON file (returns dict)

### PostgreSQLExporter

Export citation trees to PostgreSQL database.

**Parameters:**
- `host` (str): Database host (default: 'localhost')
- `port` (int): Database port (default: 5432)
- `database` (str): Database name (default: 'paper_db')
- `user` (str): Database user (default: 'postgres')
- `password` (str): Database password
- `table_name` (str): Table name (default: 'citation_tree')

**Methods:**
- `export(tree, drop_existing=False, verbose=True)`: Export tree to database

## Data Structure

### Paper Object

Each paper contains:
- `paper_id`: Unique identifier
- `title`: Paper title
- `year`: Publication year
- `citation_count`: Number of citations
- `abstract`: Paper abstract
- `authors`: List of authors (with id and name)
- `depth`: Depth in the citation tree (0 = root)
- `references`: List of referenced paper IDs

### Database Schema

When exporting to PostgreSQL, the following table is created:

```sql
CREATE TABLE citation_tree (
    paper_id VARCHAR(255) PRIMARY KEY,
    title TEXT,
    year INTEGER,
    citation_count INTEGER,
    abstract TEXT,
    authors JSONB,
    depth INTEGER NOT NULL,
    "references" JSONB,
    root_title TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Configuration

### API Rate Limits

The library automatically handles Semantic Scholar API rate limits:
- Default delay: 1.5 seconds between requests
- Automatic retry with exponential backoff on 429 errors
- Batch requests up to 500 papers per call

### Getting an API Key

While optional, using an API key provides higher rate limits:

1. Visit [Semantic Scholar API](https://www.semanticscholar.org/product/api)
2. Sign up for an API key
3. Use it when initializing the builder:

```python
from paper_tree import CitationTreeBuilder
builder = CitationTreeBuilder(api_key="your_api_key_here")
```

## Examples

See the `examples/` directory for more detailed examples:
- `examples/basic_usage.py`: Basic citation tree building
- `examples/export_json.py`: JSON export example
- `examples/export_postgres.py`: PostgreSQL export example
- `examples/analyze_tree.py`: Tree analysis and statistics

## Requirements

- Python >= 3.8
- requests >= 2.28.0
- psycopg2-binary >= 2.9.0 (for PostgreSQL support)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this library in your research, please cite:

```bibtex
@software{paper_tree,
  title = {Paper Tree: A Python Library for Citation Tree Analysis},
  author = {Paper Tree Contributors},
  year = {2025},
  url = {https://github.com/clodlingxi/paper_tree}
}
```

## Acknowledgments

- Data provided by [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- Inspired by the need for better citation network analysis tools

## Support

- 📫 Issues: [GitHub Issues](https://github.com/yourusername/paper_tree/issues)
- 📖 Documentation: [GitHub Wiki](https://github.com/yourusername/paper_tree/wiki)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/paper_tree/discussions)
