"""
PostgreSQL export example for paper_tree library.

This example demonstrates:
1. Building a citation tree
2. Exporting to PostgreSQL database
3. Database configuration
"""

from paper_tree import CitationTreeBuilder, PostgreSQLExporter


def main():
    """Run PostgreSQL export example."""

    # Build citation tree
    print("Building citation tree...")
    builder = CitationTreeBuilder(api_key="your_api_key_here")

    tree = builder.build_tree(
        root_paper_id="ARXIV:1706.03762",
        max_depth=1,  # Smaller depth for faster example
        verbose=True
    )

    # Configure database connection
    print("\n" + "="*60)
    print("Configuring PostgreSQL Connection")
    print("="*60)

    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'paper_db',
        'user': 'postgres',
        'password': 'your_password',  # Replace with your password
        'table_name': 'citation_tree'
    }

    print(f"Host: {db_config['host']}")
    print(f"Database: {db_config['database']}")
    print(f"Table: {db_config['table_name']}")

    # Create exporter
    exporter = PostgreSQLExporter(**db_config)

    # Export to database
    print("\n" + "="*60)
    print("Exporting to PostgreSQL")
    print("="*60)

    try:
        exporter.export(
            tree=tree,
            drop_existing=True,  # Drop and recreate table
            verbose=True
        )

        print("\n✓ Successfully exported to PostgreSQL!")

        # Example SQL queries to run
        print("\n" + "="*60)
        print("Example SQL Queries")
        print("="*60)

        queries = [
            ("Get root paper", """
SELECT title, year, citation_count
FROM citation_tree
WHERE depth = 0;
            """),

            ("Count papers by depth", """
SELECT depth, COUNT(*) as paper_count
FROM citation_tree
GROUP BY depth
ORDER BY depth;
            """),

            ("Top 10 most cited", """
SELECT title, citation_count, depth
FROM citation_tree
WHERE citation_count IS NOT NULL
ORDER BY citation_count DESC
LIMIT 10;
            """),
        ]

        for i, (title, query) in enumerate(queries, 1):
            print(f"\n{i}. {title}:")
            print(query.strip())

    except Exception as e:
        print(f"\n✗ Export failed: {e}")
        print("\nMake sure:")
        print("1. PostgreSQL is running")
        print("2. Database 'paper_db' exists")
        print("3. Credentials are correct")
        print("4. psycopg2-binary is installed: pip install psycopg2-binary")

    finally:
        builder.close()

    print("\n" + "="*60)
    print("PostgreSQL export example completed!")
    print("="*60)


if __name__ == "__main__":
    main()
