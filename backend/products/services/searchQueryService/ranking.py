from collections.abc import Iterable

from .scoring import SearchMatch

class SearchRanker:
    """
    Order scored search results by relevance.

    Responsibilities:
    - Validate scored results
    - Sort by relevance score
    - Apply deterministic tie-breaking
    - Preserve the SearchMatch contract

    This service does NOT:
    - Search the database
    - Normalize queries
    - Calculate relevance scores
    - Apply filters
    """

    def rank(
        self,
        query: str,
        results: Iterable[SearchMatch],
    ) -> list[SearchMatch]:
        if not query or not results:
            return []

        valid_results = [
            result
            for result in results
            if isinstance(result, SearchMatch)
        ]

        return sorted(
            valid_results,
            key=lambda result: (
                -result.score,
                str(result.product_id),
            ),
        )