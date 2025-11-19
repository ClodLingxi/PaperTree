# Examples

This directory contains example scripts demonstrating various features of the paper_tree library.

## Quick Start

Before running examples, make sure to:
1. Install the library: `pip install -e ..`
2. Replace `"your_api_key_here"` with your actual Semantic Scholar API key
3. For PostgreSQL examples, ensure database is running and credentials are correct

## Available Examples

### 1. basic_usage.py
**Basic citation tree building and exploration**

```bash
python basic_usage.py
```

**What it demonstrates:**
- Building a citation tree
- Accessing tree statistics
- Getting papers by depth
- Iterating through papers and authors

**Duration:** ~30 seconds (max_depth=2)

---

### 2. export_json.py
**JSON export and import**

```bash
python export_json.py
```

**What it demonstrates:**
- Exporting tree to JSON
- Loading tree from JSON
- Verifying exported data

**Duration:** ~15 seconds (max_depth=1)
**Output:** `citation_tree_example.json`

---

### 3. export_postgres.py
**PostgreSQL database export**

```bash
python export_postgres.py
```

**What it demonstrates:**
- Configuring database connection
- Exporting tree to PostgreSQL
- Creating tables and indexes
- Example SQL queries

**Duration:** ~15 seconds (max_depth=1)
**Requirements:**
- PostgreSQL running
- Database `paper_db` exists
- `psycopg2-binary` installed

---

### 4. analyze_tree.py
**Citation tree analysis and statistics**

```bash
python analyze_tree.py
```

**What it demonstrates:**
- Computing tree statistics
- Finding most cited papers
- Analyzing year distribution
- Identifying prolific authors
- Reference analysis
- Depth vs citations correlation

**Duration:** ~45 seconds (max_depth=2)

---

## Configuration

### API Key

All examples use a placeholder API key. To use your own:

```python
# Replace this line in each example
api_key = "your_api_key_here"

# With your actual key
api_key = "abc123xyz456"
```

Get your API key: https://www.semanticscholar.org/product/api

### Adjusting Parameters

You can modify these parameters in the examples:

```python
# Control tree depth (smaller = faster)
tree = builder.build_tree("ARXIV:1706.03762", max_depth=1)

# Change rate limiting
builder = CitationTreeBuilder(
    api_key="your_key",
    rate_limit_delay=2.0,  # Wait 2 seconds between requests
    max_retries=5          # Retry up to 5 times
)

# Use different root paper
tree = builder.build_tree("ARXIV:1512.03385")  # ResNet paper
```

## Common Papers to Try

Here are some interesting papers to build trees from:

```python
papers = {
    # Deep Learning
    "ARXIV:1706.03762": "Attention is All you Need (Transformer)",
    "ARXIV:1512.03385": "Deep Residual Learning (ResNet)",
    "ARXIV:1409.1556": "Very Deep Networks (VGG)",

    # NLP
    "ARXIV:1810.04805": "BERT",
    "ARXIV:1910.03771": "BART",

    # Computer Vision
    "ARXIV:2010.11929": "Vision Transformer",
    "ARXIV:1506.01497": "Faster R-CNN",
}
```

## Running All Examples

```bash
# Run all examples sequentially
for file in *.py; do
    echo "Running $file..."
    python "$file"
    echo "---"
done
```

## Troubleshooting

### Rate Limit Errors
```python
# Increase delay between requests
builder = CitationTreeBuilder(rate_limit_delay=2.5)
```

### Out of Memory
```python
# Reduce max_depth
tree = builder.build_tree("ARXIV:1706.03762", max_depth=1)
```

### Database Connection Failed
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Create database
createdb paper_db
```

## Output Files

Examples may create these files:
- `citation_tree_example.json` - Example JSON export
- Various analysis outputs to console

## Next Steps

After running the examples:
1. Modify them for your use case
2. Try different papers
3. Combine multiple features
4. Build your own analysis tools

## Support

- Issues: https://github.com/yourusername/paper_tree/issues
- Documentation: ../README.md
- API Docs: ../docs/
