"""
Unit tests for data models.
"""

from paper_tree.models import Author, Paper, CitationTree


class TestAuthor:
    """Test Author model."""

    def test_author_creation(self):
        """Test creating an author."""
        author = Author(author_id="123", name="John Doe")
        assert author.author_id == "123"
        assert author.name == "John Doe"

    def test_author_to_dict(self):
        """Test converting author to dict."""
        author = Author(author_id="123", name="John Doe")
        data = author.to_dict()
        assert data == {'author_id': '123', 'name': 'John Doe'}


class TestPaper:
    """Test Paper model."""

    def test_paper_creation(self):
        """Test creating a paper."""
        paper = Paper(
            paper_id="paper123",
            title="Test Paper",
            depth=1,
            year=2023,
            citation_count=100
        )
        assert paper.paper_id == "paper123"
        assert paper.title == "Test Paper"
        assert paper.depth == 1
        assert paper.year == 2023
        assert paper.citation_count == 100

    def test_paper_to_dict(self):
        """Test converting paper to dict."""
        author = Author(author_id="123", name="John Doe")
        paper = Paper(
            paper_id="paper123",
            title="Test Paper",
            depth=1,
            authors=[author],
            references=["ref1", "ref2"]
        )

        data = paper.to_dict()
        assert data['paperId'] == "paper123"
        assert data['title'] == "Test Paper"
        assert data['depth'] == 1
        assert len(data['authors']) == 1
        assert len(data['references']) == 2

    def test_paper_from_api_response(self):
        """Test creating paper from API response."""
        api_data = {
            'paperId': 'paper123',
            'title': 'Test Paper',
            'year': 2023,
            'citationCount': 100,
            'abstract': 'Test abstract',
            'authors': [
                {'authorId': '123', 'name': 'John Doe'},
                {'authorId': '456', 'name': 'Jane Smith'}
            ],
            'references': [
                {'paperId': 'ref1'},
                {'paperId': 'ref2'}
            ]
        }

        paper = Paper.from_api_response(api_data, depth=1)

        assert paper.paper_id == 'paper123'
        assert paper.title == 'Test Paper'
        assert paper.depth == 1
        assert len(paper.authors) == 2
        assert len(paper.references) == 2
        assert paper.authors[0].name == 'John Doe'


class TestCitationTree:
    """Test CitationTree model."""

    def test_tree_creation(self):
        """Test creating a citation tree."""
        tree = CitationTree("root123")
        assert tree.root_paper_id == "root123"
        assert tree.size == 0
        assert len(tree) == 0

    def test_add_paper(self):
        """Test adding papers to tree."""
        tree = CitationTree("root123")

        paper1 = Paper(paper_id="root123", title="Root Paper", depth=0)
        paper2 = Paper(paper_id="paper2", title="Paper 2", depth=1)

        tree.add_paper(paper1)
        tree.add_paper(paper2)

        assert tree.size == 2
        assert len(tree) == 2
        assert tree.root_title == "Root Paper"

    def test_get_paper(self):
        """Test getting a paper by ID."""
        tree = CitationTree("root123")
        paper = Paper(paper_id="paper1", title="Test Paper", depth=1)
        tree.add_paper(paper)

        retrieved = tree.get_paper("paper1")
        assert retrieved is not None
        assert retrieved.title == "Test Paper"

        not_found = tree.get_paper("nonexistent")
        assert not_found is None

    def test_get_papers_by_depth(self):
        """Test getting papers by depth."""
        tree = CitationTree("root123")

        root = Paper(paper_id="root123", title="Root", depth=0)
        paper1 = Paper(paper_id="p1", title="Paper 1", depth=1)
        paper2 = Paper(paper_id="p2", title="Paper 2", depth=1)
        paper3 = Paper(paper_id="p3", title="Paper 3", depth=2)

        tree.add_paper(root)
        tree.add_paper(paper1)
        tree.add_paper(paper2)
        tree.add_paper(paper3)

        depth_0 = tree.get_papers_by_depth(0)
        assert len(depth_0) == 1
        assert depth_0[0].title == "Root"

        depth_1 = tree.get_papers_by_depth(1)
        assert len(depth_1) == 2

        depth_2 = tree.get_papers_by_depth(2)
        assert len(depth_2) == 1

    def test_get_root_paper(self):
        """Test getting root paper."""
        tree = CitationTree("root123")

        root = Paper(paper_id="root123", title="Root Paper", depth=0)
        paper1 = Paper(paper_id="p1", title="Paper 1", depth=1)

        tree.add_paper(root)
        tree.add_paper(paper1)

        root_paper = tree.get_root_paper()
        assert root_paper is not None
        assert root_paper.title == "Root Paper"
        assert root_paper.depth == 0

    def test_max_depth(self):
        """Test getting maximum depth."""
        tree = CitationTree("root123")

        tree.add_paper(Paper(paper_id="p0", title="P0", depth=0))
        tree.add_paper(Paper(paper_id="p1", title="P1", depth=1))
        tree.add_paper(Paper(paper_id="p2", title="P2", depth=2))

        assert tree.max_depth == 2

    def test_contains(self):
        """Test checking if paper exists in tree."""
        tree = CitationTree("root123")
        paper = Paper(paper_id="paper1", title="Test", depth=0)
        tree.add_paper(paper)

        assert "paper1" in tree
        assert "nonexistent" not in tree

    def test_get_statistics(self):
        """Test getting tree statistics."""
        tree = CitationTree("root123")

        tree.add_paper(Paper(paper_id="root", title="Root", depth=0))
        tree.add_paper(Paper(paper_id="p1", title="P1", depth=1))
        tree.add_paper(Paper(paper_id="p2", title="P2", depth=1))
        tree.add_paper(Paper(paper_id="p3", title="P3", depth=2))

        stats = tree.get_statistics()

        assert stats['total_papers'] == 4
        assert stats['root_title'] == "Root"
        assert stats['max_depth'] == 2
        assert stats['papers_by_depth'][0] == 1
        assert stats['papers_by_depth'][1] == 2
        assert stats['papers_by_depth'][2] == 1
