# Quick Start Guide

Get started with Paper Tree in 5 minutes!

## Installation

```bash
# Basic installation
pip install paper-tree

# With PostgreSQL support
pip install paper-tree[postgres]

# From source
git clone https://github.com/clodlingxi/paper_tree.git
cd paper_tree
pip install -e .
```

## 5-Minute Example

```python
from paper_tree import CitationTreeBuilder, JSONExporter

# 1. Create builder (API key optional but recommended)
builder = CitationTreeBuilder(api_key="your_api_key")

# 2. Build citation tree
tree = builder.build_tree("ARXIV:1706.03762", max_depth=2)

# 3. Get statistics
print(f"Total papers: {tree.size}")
print(f"Root: {tree.root_title}")

# 4. Export to JSON
JSONExporter.export(tree, "output.json")

# 5. Done!
builder.close()
```

## Common Use Cases

### 1. Simple Citation Tree

```python
from paper_tree import CitationTreeBuilder

builder = CitationTreeBuilder()
tree = builder.build_tree("ARXIV:1706.03762", max_depth=1)

# Access root paper
root = tree.get_root_paper()
print(f"{root.title} ({root.year})")
```

### 2. Export to Database

```python
from paper_tree import CitationTreeBuilder, PostgreSQLExporter

# Build tree
builder = CitationTreeBuilder()
tree = builder.build_tree("ARXIV:1706.03762", max_depth=2)

# Export to PostgreSQL
db = PostgreSQLExporter(
    database="paper_db",
    user="postgres",
    password="your_password"
)
db.export(tree)
```

### 3. Analyze Papers

```python
from paper_tree import CitationTreeBuilder

builder = CitationTreeBuilder()
tree = builder.build_tree("ARXIV:1706.03762", max_depth=2)

# Get most cited papers
papers = sorted(
    tree.papers.values(),
    key=lambda p: p.citation_count or 0,
    reverse=True
)

for paper in papers[:10]:
    print(f"{paper.citation_count:6,} - {paper.title}")
```

## Next Steps

- 📖 Read the [full documentation](README.md)
- 💡 Check out [examples/](examples) for more use cases
- 🔧 Learn about [API configuration](README.md#configuration)
- 🐛 Report issues on [GitHub](https://github.com/clodlingxi/paper_tree/issues)

## Getting an API Key

1. Visit [Semantic Scholar API](https://www.semanticscholar.org/product/api)
2. Sign up for a free API key
3. Higher rate limits with API key!

## Troubleshooting

### Rate Limit Errors

```python
# Increase delay between requests
from paper_tree import CitationTreeBuilder

builder = CitationTreeBuilder(rate_limit_delay=2.0)
```

### Database Connection Issues

```bash
# Install PostgreSQL support
pip install psycopg2-binary

# Check PostgreSQL is running
psql -U postgres -c "SELECT version();"
```

### Import Errors

```bash
# Reinstall package
pip uninstall paper-tree
pip install paper-tree
```

## Tips

1. **Use API Key**: Get faster, more reliable requests
2. **Start Small**: Test with `max_depth=1` first
3. **Save Progress**: Export to JSON frequently
4. **Context Manager**: Use `with` for automatic cleanup

```python
from paper_tree import CitationTreeBuilder
with CitationTreeBuilder() as builder:
    tree = builder.build_tree("ARXIV:1706.03762")
    # Automatically closes connection
```

Happy researching! 🎓📚
