"""
Citation tree analysis example.

This example demonstrates:
1. Building a citation tree
2. Analyzing tree structure
3. Computing statistics
4. Finding influential papers
"""

from paper_tree import CitationTreeBuilder
from collections import Counter


def main():
    """Run citation tree analysis example."""

    # Build citation tree
    print("Building citation tree...")
    builder = CitationTreeBuilder(api_key="your_api_key_here")

    tree = builder.build_tree(
        root_paper_id="ARXIV:1706.03762",
        max_depth=2,
        verbose=True
    )

    # Basic statistics
    print("\n" + "="*60)
    print("Basic Statistics")
    print("="*60)

    stats = tree.get_statistics()
    print(f"Total papers: {stats['total_papers']}")
    print(f"Root paper: {stats['root_title']}")
    print(f"Max depth: {stats['max_depth']}")

    print("\nDepth distribution:")
    for depth in sorted(stats['papers_by_depth'].keys()):
        count = stats['papers_by_depth'][depth]
        percentage = (count / stats['total_papers']) * 100
        bar = "█" * int(percentage / 2)
        print(f"  Depth {depth}: {count:4d} papers ({percentage:5.1f}%) {bar}")

    # Most cited papers
    print("\n" + "="*60)
    print("Top 10 Most Cited Papers")
    print("="*60)

    papers_with_citations = [
        p for p in tree.papers.values()
        if p.citation_count is not None
    ]
    papers_with_citations.sort(key=lambda x: x.citation_count, reverse=True)

    for i, paper in enumerate(papers_with_citations[:10], 1):
        print(f"{i:2d}. [{paper.citation_count:6,} citations] [Depth {paper.depth}]")
        print(f"    {paper.title}")

    # Year distribution
    print("\n" + "="*60)
    print("Publication Year Distribution")
    print("="*60)

    years = [p.year for p in tree.papers.values() if p.year]
    year_counts = Counter(years)

    print(f"Year range: {min(years) if years else 'N/A'} - {max(years) if years else 'N/A'}")
    print(f"\nMost common years:")

    for year, count in year_counts.most_common(10):
        percentage = (count / len(years)) * 100
        bar = "█" * int(percentage)
        print(f"  {year}: {bar} {count:3d} papers ({percentage:4.1f}%)")

    # Author analysis
    print("\n" + "="*60)
    print("Most Prolific Authors (in this tree)")
    print("="*60)

    all_authors = []
    for paper in tree.papers.values():
        all_authors.extend([author.name for author in paper.authors])

    author_counts = Counter(all_authors)

    for i, (author, count) in enumerate(author_counts.most_common(10), 1):
        print(f"{i:2d}. {author}: {count} papers")

    # Reference analysis
    print("\n" + "="*60)
    print("Reference Statistics")
    print("="*60)

    ref_counts = [len(p.references) for p in tree.papers.values()]
    total_refs = sum(ref_counts)
    avg_refs = total_refs / len(tree.papers) if tree.papers else 0

    print(f"Total references: {total_refs}")
    print(f"Average references per paper: {avg_refs:.2f}")
    print(f"Max references: {max(ref_counts) if ref_counts else 0}")
    print(f"Papers with no references: {ref_counts.count(0)}")

    # Most referenced paper
    paper_with_most_refs = max(tree.papers.values(), key=lambda p: len(p.references))
    print(f"\nPaper with most references:")
    print(f"  {paper_with_most_refs.title}")
    print(f"  References: {len(paper_with_most_refs.references)}")

    # Depth vs Citations correlation
    print("\n" + "="*60)
    print("Average Citations by Depth")
    print("="*60)

    depth_citations = {}
    for paper in tree.papers.values():
        if paper.citation_count is not None:
            if paper.depth not in depth_citations:
                depth_citations[paper.depth] = []
            depth_citations[paper.depth].append(paper.citation_count)

    for depth in sorted(depth_citations.keys()):
        citations = depth_citations[depth]
        avg = sum(citations) / len(citations)
        max_cite = max(citations)
        print(f"  Depth {depth}: avg={avg:8,.1f}, max={max_cite:8,}")

    builder.close()

    print("\n" + "="*60)
    print("Analysis completed!")
    print("="*60)


if __name__ == "__main__":
    main()
