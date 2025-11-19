"""
Citation tree builder for constructing paper citation networks.
"""

from collections import deque
from typing import Set, Dict, List, Optional
from .api import SemanticScholarAPI
from .models import Paper, CitationTree


class CitationTreeBuilder:
    """Builds citation trees from paper references using BFS traversal."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        rate_limit_delay: float = 1.5,
        max_retries: int = 3
    ):
        """
        Initialize citation tree builder.

        Args:
            api_key: Semantic Scholar API key
            rate_limit_delay: Delay between API requests in seconds
            max_retries: Maximum retry attempts for failed requests
        """
        self.api = SemanticScholarAPI(
            api_key=api_key,
            rate_limit_delay=rate_limit_delay,
            max_retries=max_retries
        )

    def build_tree(
        self,
        root_paper_id: str,
        max_depth: int = 2,
        verbose: bool = True
    ) -> CitationTree:
        """
        Build a citation tree starting from a root paper.

        Args:
            root_paper_id: Starting paper ID (e.g., 'ARXIV:1706.03762')
            max_depth: Maximum depth to traverse
            verbose: Whether to print progress messages

        Returns:
            CitationTree object containing all papers

        Example:
            >>> builder = CitationTreeBuilder(api_key="your_key")
            >>> tree = builder.build_tree("ARXIV:1706.03762", max_depth=2)
            >>> print(f"Built tree with {len(tree)} papers")
        """
        tree = CitationTree(root_paper_id)
        visited: Set[str] = set()
        visited.add(root_paper_id)

        # Group papers by depth for batch fetching
        depth_batches: Dict[int, List[str]] = {0: [root_paper_id]}

        if verbose:
            print(f"Starting citation tree build from {root_paper_id}")
            print(f"Max depth: {max_depth}\n")

        current_depth = 0

        while current_depth <= max_depth and depth_batches.get(current_depth):
            if verbose:
                print(f"\n{'='*60}")
                print(f"Processing Depth {current_depth}")
                print('='*60)

            current_ids = depth_batches[current_depth]

            # Fetch papers at current depth
            papers_data = self.api.batch_fetch_papers(current_ids, verbose=verbose)

            # Process fetched papers and collect references
            next_level_ids = []

            for paper_data in papers_data:
                if not paper_data or 'paperId' not in paper_data:
                    continue

                paper = Paper.from_api_response(paper_data, current_depth)
                tree.add_paper(paper)

                # Collect references for next depth
                if current_depth < max_depth:
                    for ref_id in paper.references:
                        if ref_id and ref_id not in visited:
                            visited.add(ref_id)
                            next_level_ids.append(ref_id)

            if verbose:
                print(f"Depth {current_depth}: Processed {len(papers_data)} papers")
                print(f"Found {len(next_level_ids)} new references for next depth")

            # Prepare next depth
            if next_level_ids and current_depth < max_depth:
                depth_batches[current_depth + 1] = next_level_ids

            current_depth += 1

        if verbose:
            print(f"\n{'='*60}")
            print("Citation Tree Built")
            print('='*60)
            print(f"Total papers collected: {tree.size}")
            print(f"Total unique papers visited: {len(visited)}")

        return tree

    def build_tree_from_multiple_roots(
        self,
        root_paper_ids: List[str],
        max_depth: int = 2,
        verbose: bool = True
    ) -> List[CitationTree]:
        """
        Build multiple citation trees from a list of root papers.

        Args:
            root_paper_ids: List of root paper IDs
            max_depth: Maximum depth for each tree
            verbose: Whether to print progress messages

        Returns:
            List of CitationTree objects
        """
        trees = []

        for i, paper_id in enumerate(root_paper_ids, 1):
            if verbose:
                print(f"\n{'#'*60}")
                print(f"Building tree {i}/{len(root_paper_ids)}")
                print('#'*60)

            tree = self.build_tree(paper_id, max_depth, verbose)
            trees.append(tree)

        return trees

    def close(self):
        """Close the API session."""
        self.api.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
