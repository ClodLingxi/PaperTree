"""
JSON export example for paper_tree library.

This example demonstrates:
1. Building a citation tree
2. Exporting to JSON
3. Loading from JSON
"""

from paper_tree import CitationTreeBuilder, JSONExporter


def main():
    """Run JSON export example."""

    # Build citation tree
    print("Building citation tree...")
    builder = CitationTreeBuilder(api_key="your_api_key_here")

    tree = builder.build_tree(
        root_paper_id="ARXIV:1706.03762",
        max_depth=1,  # Smaller depth for faster example
        verbose=True
    )

    # Export to JSON
    print("\n" + "="*60)
    print("Exporting to JSON")
    print("="*60)

    output_file = "citation_tree_example.json"
    exporter = JSONExporter()

    exporter.export(
        tree=tree,
        filename=output_file,
        indent=2,
        ensure_ascii=False
    )

    print(f"\n✓ Exported {tree.size} papers to {output_file}")

    # Load back from JSON
    print("\n" + "="*60)
    print("Loading from JSON")
    print("="*60)

    loaded_data = JSONExporter.load(output_file)
    print(f"✓ Loaded {len(loaded_data)} papers from {output_file}")

    # Verify data
    print("\nVerifying data...")
    print(f"Root paper in loaded data: {'Yes' if any(p['depth'] == 0 for p in loaded_data.values()) else 'No'}")

    # Show sample paper
    sample_id = list(loaded_data.keys())[0]
    sample_paper = loaded_data[sample_id]

    print(f"\nSample paper:")
    print(f"  Title: {sample_paper['title']}")
    print(f"  Depth: {sample_paper['depth']}")
    print(f"  Citations: {sample_paper.get('citationCount', 'N/A')}")

    builder.close()

    print("\n" + "="*60)
    print("JSON export example completed!")
    print("="*60)


if __name__ == "__main__":
    main()
