"""
Data models for papers and citation trees.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict


@dataclass
class Author:
    """Represents a paper author."""
    author_id: str
    name: str

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class Paper:
    """Represents an academic paper with its metadata and relationships."""

    paper_id: str
    title: str
    depth: int
    year: Optional[int] = None
    citation_count: Optional[int] = None
    abstract: Optional[str] = None
    authors: List[Author] = field(default_factory=list)
    references: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert paper to dictionary format."""
        return {
            'paperId': self.paper_id,
            'title': self.title,
            'year': self.year,
            'citationCount': self.citation_count,
            'abstract': self.abstract,
            'authors': [author.to_dict() for author in self.authors],
            'depth': self.depth,
            'references': self.references
        }

    @classmethod
    def from_api_response(cls, data: Dict[str, Any], depth: int) -> 'Paper':
        """Create Paper instance from API response."""
        authors = [
            Author(author_id=a.get('authorId', ''), name=a.get('name', ''))
            for a in data.get('authors', [])
        ]

        references = [
            ref.get('paperId')
            for ref in data.get('references', [])
            if ref and ref.get('paperId')
        ]

        return cls(
            paper_id=data.get('paperId', ''),
            title=data.get('title', ''),
            year=data.get('year'),
            citation_count=data.get('citationCount'),
            abstract=data.get('abstract'),
            authors=authors,
            depth=depth,
            references=references
        )


class CitationTree:
    """Represents a citation tree with papers at different depths."""

    def __init__(self, root_paper_id: str):
        """
        Initialize citation tree.

        Args:
            root_paper_id: The ID of the root paper
        """
        self.root_paper_id = root_paper_id
        self.papers: Dict[str, Paper] = {}
        self._root_title: Optional[str] = None

    def add_paper(self, paper: Paper) -> None:
        """Add a paper to the tree."""
        self.papers[paper.paper_id] = paper
        if paper.depth == 0:
            self._root_title = paper.title

    def get_paper(self, paper_id: str) -> Optional[Paper]:
        """Get a paper by ID."""
        return self.papers.get(paper_id)

    def get_papers_by_depth(self, depth: int) -> List[Paper]:
        """Get all papers at a specific depth."""
        return [p for p in self.papers.values() if p.depth == depth]

    def get_root_paper(self) -> Optional[Paper]:
        """Get the root paper (depth 0)."""
        papers = self.get_papers_by_depth(0)
        return papers[0] if papers else None

    @property
    def root_title(self) -> str:
        """Get the title of the root paper."""
        if self._root_title:
            return self._root_title
        root = self.get_root_paper()
        return root.title if root else "Unknown"

    @property
    def size(self) -> int:
        """Get the total number of papers in the tree."""
        return len(self.papers)

    @property
    def max_depth(self) -> int:
        """Get the maximum depth in the tree."""
        if not self.papers:
            return 0
        return max(p.depth for p in self.papers.values())

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """Convert tree to dictionary format."""
        return {
            paper_id: paper.to_dict()
            for paper_id, paper in self.papers.items()
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the citation tree."""
        depth_count = {}
        for paper in self.papers.values():
            depth_count[paper.depth] = depth_count.get(paper.depth, 0) + 1

        return {
            'total_papers': self.size,
            'root_title': self.root_title,
            'max_depth': self.max_depth,
            'papers_by_depth': depth_count
        }

    def __len__(self) -> int:
        """Return the number of papers in the tree."""
        return self.size

    def __contains__(self, paper_id: str) -> bool:
        """Check if a paper is in the tree."""
        return paper_id in self.papers
