# Paper Tree - Package Structure

Complete package structure documentation.

## Directory Tree

```
paper_tree/
├── paper_tree/              # Main package directory
│   ├── __init__.py         # Package initialization & exports
│   ├── api.py              # Semantic Scholar API client
│   ├── models.py           # Data models (Paper, Author, CitationTree)
│   ├── tree_builder.py     # Citation tree builder
│   ├── exporters.py        # JSON & PostgreSQL exporters
│   └── exceptions.py       # Custom exceptions
│
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_models.py      # Unit tests for models
│
├── examples/                # Usage examples
│   ├── README.md           # Examples documentation
│   ├── basic_usage.py      # Basic tree building
│   ├── export_json.py      # JSON export example
│   ├── export_postgres.py  # PostgreSQL export example
│   └── analyze_tree.py     # Tree analysis example
│
├── docs/                    # Documentation (optional)
│
├── setup.py                 # Setup script
├── pyproject.toml          # Modern Python project config
├── requirements.txt        # Dependencies
├── MANIFEST.in            # Include additional files in dist
├── .gitignore             # Git ignore patterns
├── LICENSE                # MIT License
├── README.md              # Main documentation
└── QUICKSTART.md          # Quick start guide
```

## Module Descriptions

### Core Modules

#### `__init__.py`
- Package initialization
- Public API exports
- Version information

**Exports:**
- `CitationTreeBuilder`
- `Paper`, `CitationTree`
- `JSONExporter`, `PostgreSQLExporter`
- `SemanticScholarAPI`

#### `models.py`
Data models for papers and citation trees.

**Classes:**
- `Author`: Represents a paper author
- `Paper`: Represents an academic paper
- `CitationTree`: Represents a citation tree structure

**Key Features:**
- Dataclass-based models
- Type hints
- Conversion methods (`to_dict()`, `from_api_response()`)

#### `api.py`
Semantic Scholar API client.

**Classes:**
- `SemanticScholarAPI`: HTTP client for S2 API

**Features:**
- Batch fetching (up to 500 papers)
- Rate limiting
- Automatic retry with exponential backoff
- Context manager support

#### `tree_builder.py`
Citation tree construction logic.

**Classes:**
- `CitationTreeBuilder`: Builds citation trees via BFS

**Features:**
- Breadth-first traversal
- Automatic deduplication
- Depth control
- Progress reporting

#### `exporters.py`
Export citation trees to various formats.

**Classes:**
- `JSONExporter`: Export to JSON files
- `PostgreSQLExporter`: Export to PostgreSQL database

**Features:**
- JSON with pretty printing
- Database table creation
- Index creation
- Batch insertion

#### `exceptions.py`
Custom exception classes.

**Exceptions:**
- `PaperTreeError`: Base exception
- `APIError`: API-related errors
- `RateLimitError`: Rate limit exceeded
- `ExportError`: Export failures
- `DatabaseError`: Database errors

## Configuration Files

### `setup.py`
Classic setuptools configuration.

**Includes:**
- Package metadata
- Dependencies
- Entry points
- Classifiers

### `pyproject.toml`
Modern Python project configuration.

**Sections:**
- `[build-system]`: Build requirements
- `[project]`: Project metadata
- `[project.optional-dependencies]`: Optional deps
- `[tool.black]`: Code formatter config
- `[tool.pytest]`: Test configuration
- `[tool.mypy]`: Type checker config

### `requirements.txt`
Runtime dependencies.

**Core:**
- `requests>=2.28.0`

**Optional:**
- `psycopg2-binary>=2.9.0` (PostgreSQL)

## Installation Methods

### 1. From PyPI (when published)
```bash
pip install paper-tree
pip install paper-tree[postgres]  # With PostgreSQL
pip install paper-tree[dev]       # Development tools
```

### 2. From Source
```bash
git clone https://github.com/yourusername/paper_tree.git
cd paper_tree
pip install -e .                  # Editable install
pip install -e .[dev]            # With dev tools
```

### 3. From Local Directory
```bash
cd paper_tree
pip install .
```

## Testing

### Run Tests
```bash
# Install with dev dependencies
pip install -e .[dev]

# Run all tests
pytest

# Run with coverage
pytest --cov=paper_tree

# Run specific test file
pytest tests/test_models.py
```

### Run Examples
```bash
cd examples
python basic_usage.py
```

## Development Workflow

### 1. Setup Development Environment
```bash
git clone <repo>
cd paper_tree
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e .[dev]
```

### 2. Make Changes
```bash
# Edit files in paper_tree/
vim paper_tree/models.py
```

### 3. Format Code
```bash
black paper_tree/
```

### 4. Run Tests
```bash
pytest
```

### 5. Check Types
```bash
mypy paper_tree/
```

## Distribution

### Build Package
```bash
python -m build
```

**Creates:**
- `dist/paper_tree-0.1.0.tar.gz` (source distribution)
- `dist/paper_tree-0.1.0-py3-none-any.whl` (wheel)

### Upload to PyPI
```bash
pip install twine
twine upload dist/*
```

## API Usage Patterns

### Basic Pattern
```python
from paper_tree import CitationTreeBuilder, JSONExporter

builder = CitationTreeBuilder(api_key="key")
tree = builder.build_tree("ARXIV:1706.03762", max_depth=2)
JSONExporter.export(tree, "output.json")
builder.close()
```

### Context Manager Pattern
```python
from paper_tree import CitationTreeBuilder

with CitationTreeBuilder(api_key="key") as builder:
    tree = builder.build_tree("ARXIV:1706.03762")
    # Automatically closes
```

### Multiple Trees Pattern
```python
from paper_tree import CitationTreeBuilder

builder = CitationTreeBuilder()
papers = ["ARXIV:1706.03762", "ARXIV:1512.03385"]
trees = builder.build_tree_from_multiple_roots(papers)
builder.close()
```

## Dependencies Graph

```
paper_tree
├── requests (required)
│   └── urllib3, certifi, charset-normalizer, idna
│
├── psycopg2-binary (optional, for PostgreSQL)
│
└── Development tools (optional)
    ├── pytest (testing)
    ├── pytest-cov (coverage)
    ├── black (formatting)
    ├── flake8 (linting)
    └── mypy (type checking)
```

## Version History

### 0.1.0 (Initial Release)
- Citation tree building
- JSON export
- PostgreSQL export
- BFS traversal
- Rate limiting
- Basic documentation

## Future Enhancements

Potential features for future versions:
- [ ] More export formats (CSV, SQLite, MongoDB)
- [ ] Visualization tools
- [ ] Advanced analytics
- [ ] Caching layer
- [ ] Async API support
- [ ] CLI tool
- [ ] Graph analysis features
- [ ] Network visualization

## Contributing

See `CONTRIBUTING.md` for:
- Code style guidelines
- Pull request process
- Issue reporting
- Development setup

## License

MIT License - see `LICENSE` file for details.

## Support

- GitHub Issues: Report bugs and request features
- GitHub Discussions: Ask questions and share ideas
- Documentation: Full docs in `README.md`
- Examples: See `examples/` directory
