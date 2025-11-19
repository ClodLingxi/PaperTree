"""
Custom exceptions for the paper_tree library.
"""


class PaperTreeError(Exception):
    """Base exception for paper_tree library."""
    pass


class APIError(PaperTreeError):
    """Raised when API request fails."""
    pass


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded."""
    pass


class ExportError(PaperTreeError):
    """Raised when export operation fails."""
    pass


class DatabaseError(ExportError):
    """Raised when database operation fails."""
    pass
