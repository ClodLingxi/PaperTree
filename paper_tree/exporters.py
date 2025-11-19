"""
Exporters for saving citation trees to various formats.
"""

import json
from typing import Optional, Dict
from pathlib import Path

try:
    import psycopg2
    from psycopg2.extras import Json
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

from .models import CitationTree
from .exceptions import ExportError, DatabaseError


class JSONExporter:
    """Export citation tree to JSON format."""

    @staticmethod
    def export(
        tree: CitationTree,
        filename: str,
        indent: int = 2,
        ensure_ascii: bool = False
    ) -> None:
        """
        Export citation tree to JSON file.

        Args:
            tree: CitationTree to export
            filename: Output filename
            indent: JSON indentation level
            ensure_ascii: Whether to escape non-ASCII characters

        Raises:
            ExportError: If export fails
        """
        try:
            tree_dict = tree.to_dict()

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tree_dict, f, ensure_ascii=ensure_ascii, indent=indent)

            print(f"Citation tree exported to {filename}")
            print(f"Total papers: {tree.size}")

        except Exception as e:
            raise ExportError(f"Failed to export to JSON: {e}") from e

    @staticmethod
    def load(filename: str) -> Dict:
        """
        Load citation tree from JSON file.

        Args:
            filename: JSON file to load

        Returns:
            Dictionary representation of the tree

        Raises:
            ExportError: If loading fails
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise ExportError(f"Failed to load from JSON: {e}") from e


class PostgreSQLExporter:
    """Export citation tree to PostgreSQL database."""

    def __init__(
        self,
        host: str = 'localhost',
        port: int = 5432,
        database: str = 'paper_db',
        user: str = 'postgres',
        password: str = '',
        table_name: str = 'citation_tree'
    ):
        """
        Initialize PostgreSQL exporter.

        Args:
            host: Database host
            port: Database port
            database: Database name
            user: Database user
            password: Database password
            table_name: Table name for storing papers

        Raises:
            DatabaseError: If psycopg2 is not installed
        """
        if not PSYCOPG2_AVAILABLE:
            raise DatabaseError(
                "psycopg2 is not installed. Install it with: pip install psycopg2-binary"
            )

        self.config = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self.table_name = table_name

    def export(
        self,
        tree: CitationTree,
        drop_existing: bool = False,
        verbose: bool = True
    ) -> None:
        """
        Export citation tree to PostgreSQL.

        Args:
            tree: CitationTree to export
            drop_existing: Whether to drop existing table
            verbose: Whether to print progress messages

        Raises:
            DatabaseError: If database operation fails
        """
        try:
            conn = psycopg2.connect(**self.config)
            cursor = conn.cursor()

            if verbose:
                print("Connected to PostgreSQL successfully")

            # Drop existing table if requested
            if drop_existing:
                if verbose:
                    print(f"Dropping existing table '{self.table_name}'...")
                cursor.execute(f"DROP TABLE IF EXISTS {self.table_name} CASCADE;")

            # Create table
            self._create_table(cursor, verbose)

            # Insert papers
            self._insert_papers(cursor, tree, verbose)

            # Commit transaction
            conn.commit()

            if verbose:
                print("\n" + "="*60)
                print("Export Statistics")
                print("="*60)
                print(f"Total papers exported: {tree.size}")
                print(f"Root title: {tree.root_title}")

            cursor.close()
            conn.close()

            if verbose:
                print("\nDatabase connection closed")
                print("✓ Export completed successfully!")

        except psycopg2.Error as e:
            raise DatabaseError(f"Database error: {e}") from e
        except Exception as e:
            raise DatabaseError(f"Export failed: {e}") from e

    def _create_table(self, cursor, verbose: bool = True) -> None:
        """Create the papers table with indexes."""
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
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
        """

        # Create indexes
        indexes = [
            f"CREATE INDEX IF NOT EXISTS idx_{self.table_name}_depth ON {self.table_name}(depth);",
            f"CREATE INDEX IF NOT EXISTS idx_{self.table_name}_year ON {self.table_name}(year);",
            f"CREATE INDEX IF NOT EXISTS idx_{self.table_name}_citation_count ON {self.table_name}(citation_count);",
            f"CREATE INDEX IF NOT EXISTS idx_{self.table_name}_root_title ON {self.table_name}(root_title);",
            f"CREATE INDEX IF NOT EXISTS idx_{self.table_name}_title ON {self.table_name} USING gin(to_tsvector('english', title));",
        ]

        if verbose:
            print("Creating table...")
        cursor.execute(create_table_sql)

        if verbose:
            print("Creating indexes...")
        for idx_sql in indexes:
            cursor.execute(idx_sql)

        if verbose:
            print(f"Table '{self.table_name}' created successfully!")

    def _insert_papers(self, cursor, tree: CitationTree, verbose: bool = True) -> None:
        """Insert papers into the database."""
        insert_sql = f"""
        INSERT INTO {self.table_name}
        (paper_id, title, year, citation_count, abstract, authors, depth, "references", root_title)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (paper_id) DO UPDATE SET
            title = EXCLUDED.title,
            year = EXCLUDED.year,
            citation_count = EXCLUDED.citation_count,
            abstract = EXCLUDED.abstract,
            authors = EXCLUDED.authors,
            depth = EXCLUDED.depth,
            "references" = EXCLUDED."references",
            root_title = EXCLUDED.root_title;
        """

        papers_data = []
        for paper in tree.papers.values():
            papers_data.append((
                paper.paper_id,
                paper.title,
                paper.year,
                paper.citation_count,
                paper.abstract,
                Json([a.to_dict() for a in paper.authors]),
                paper.depth,
                Json(paper.references),
                tree.root_title
            ))

        if verbose:
            print(f"\nInserting {len(papers_data)} papers...")

        cursor.executemany(insert_sql, papers_data)

        if verbose:
            print(f"Successfully inserted {len(papers_data)} papers!")

    @classmethod
    def from_config(cls, config: Dict) -> 'PostgreSQLExporter':
        """
        Create exporter from configuration dictionary.

        Args:
            config: Configuration dictionary

        Returns:
            PostgreSQLExporter instance
        """
        return cls(**config)
