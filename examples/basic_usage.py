"""
Basic usage example for paper_tree library.

This example demonstrates:
1. Building a citation tree
2. Accessing tree statistics
3. Iterating through papers
"""

from paper_tree import CitationTreeBuilder


def main():
    """Run basic citation tree example."""

    # Initialize builder with API key (IMPORTANCE)
    # Get your API key from: https://www.semanticscholar.org/product/api
    api_key = ""  # Replace with your actual API key
    builder = CitationTreeBuilder(api_key=api_key)

    print("="*60)
    print("Building Citation Tree")
    print("="*60)

    # Build citation tree from "Attention is All you Need" paper
    root_paper_id = "ARXIV:1706.03762"
    max_depth = 2

    tree = builder.build_tree(
        root_paper_id=root_paper_id,
        max_depth=max_depth,
        verbose=True
    )

    # Get and display statistics
    print("\n" + "="*60)
    print("Tree Statistics")
    print("="*60)

    stats = tree.get_statistics()
    print(f"Root paper: {stats['root_title']}")
    print(f"Total papers: {stats['total_papers']}")
    print(f"Max depth: {stats['max_depth']}")

    print("\nPapers by depth:")
    for depth, count in sorted(stats['papers_by_depth'].items()):
        print(f"  Depth {depth}: {count} papers")

    # Get root paper details
    print("\n" + "="*60)
    print("Root Paper Details")
    print("="*60)

    root = tree.get_root_paper()
    if root:
        print(f"Title: {root.title}")
        print(f"Year: {root.year}")
        print(f"Citations: {root.citation_count:,}")
        print(f"Authors: {len(root.authors)} authors")
        print(f"References: {len(root.references)}")

        print("\nFirst 3 authors:")
        for i, author in enumerate(root.authors[:3], 1):
            print(f"  {i}. {author.name}")

    # Show sample papers from depth 1
    print("\n" + "="*60)
    print("Sample Papers (Depth 1)")
    print("="*60)

    depth_1_papers = tree.get_papers_by_depth(1)
    for i, paper in enumerate(depth_1_papers[:5], 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Year: {paper.year}")
        print(f"   Citations: {paper.citation_count:,}" if paper.citation_count else "   Citations: N/A")

    # Close the API session
    builder.close()

    print("\n" + "="*60)
    print("Example completed!")
    print("="*60)


if __name__ == "__main__":
    main()
