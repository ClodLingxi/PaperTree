"""
Semantic Scholar API client for fetching paper data.
"""

import warnings
import time
import requests
from typing import List, Dict, Optional
from .exceptions import APIError, RateLimitError


class SemanticScholarAPI:
    """Client for interacting with Semantic Scholar API."""

    BASE_URL = 'https://api.semanticscholar.org/graph/v1/paper/batch'
    DEFAULT_FIELDS = 'citationCount,title,paperId,abstract,references.paperId,year,authors'

    def __init__(
        self,
        api_key: Optional[str] = None,
        rate_limit_delay: float = 1.5,
        max_retries: int = 3
    ):
        """
        Initialize Semantic Scholar API client.

        Args:
            api_key: Optional API key for authenticated requests
            rate_limit_delay: Delay between requests in seconds
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.api_key = api_key

        if api_key is None or api_key == "":
            warnings.warn("Semantic Scholar has limit without API")

        self.rate_limit_delay = rate_limit_delay
        self.max_retries = max_retries
        self.session = requests.Session()

    def batch_fetch_papers(
        self,
        paper_ids: List[str],
        fields: Optional[str] = None,
        verbose: bool = True
    ) -> List[Dict]:
        """
        Fetch multiple papers in batches.

        Args:
            paper_ids: List of paper IDs to fetch
            fields: Comma-separated list of fields to retrieve
            verbose: Whether to print progress messages

        Returns:
            List of paper data dictionaries

        Raises:
            APIError: If API request fails
            RateLimitError: If rate limit is exceeded
        """
        if not fields:
            fields = self.DEFAULT_FIELDS

        all_results = []
        batch_size = 500

        for i in range(0, len(paper_ids), batch_size):
            batch = paper_ids[i:i + batch_size]

            if verbose:
                batch_num = i // batch_size + 1
                print(f"Fetching batch {batch_num}: {len(batch)} papers...")

            results = self._fetch_batch(batch, fields)
            all_results.extend(results)

            if verbose:
                print(f"Successfully fetched {len(results)} papers")

            # Rate limiting
            if i + batch_size < len(paper_ids):
                if verbose:
                    print(f"Waiting {self.rate_limit_delay} seconds before next request...")
                time.sleep(self.rate_limit_delay)

        return all_results

    def _fetch_batch(self, paper_ids: List[str], fields: str) -> List[Dict]:
        """
        Fetch a single batch of papers with retry logic.

        Args:
            paper_ids: List of paper IDs to fetch
            fields: Fields to retrieve

        Returns:
            List of paper data dictionaries

        Raises:
            APIError: If all retry attempts fail
            RateLimitError: If rate limit is exceeded
        """
        params = {'fields': fields}
        json_data = {"ids": paper_ids}
        headers = {}

        if self.api_key:
            headers['x-api-key'] = self.api_key

        for attempt in range(self.max_retries):
            try:
                response = self.session.post(
                    self.BASE_URL,
                    headers=headers,
                    params=params,
                    json=json_data
                )
                response.raise_for_status()

                results = response.json()
                # Filter out None results (papers not found)
                valid_results = [r for r in results if r is not None]
                return valid_results

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    # Rate limit exceeded
                    wait_time = 5 * (attempt + 1)  # Exponential backoff
                    print(f"Rate limit hit (429). Retrying in {wait_time} seconds... "
                          f"(Attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(wait_time)

                    if attempt == self.max_retries - 1:
                        raise RateLimitError(
                            f"Rate limit exceeded after {self.max_retries} attempts"
                        ) from e
                else:
                    raise APIError(f"HTTP error: {e}") from e

            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise APIError(f"Request failed: {e}") from e
                time.sleep(2)

        return []

    def fetch_single_paper(
        self,
        paper_id: str,
        fields: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Fetch a single paper by ID.

        Args:
            paper_id: Paper ID to fetch
            fields: Fields to retrieve

        Returns:
            Paper data dictionary or None if not found
        """
        results = self.batch_fetch_papers([paper_id], fields, verbose=False)
        return results[0] if results else None

    def close(self):
        """Close the session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
