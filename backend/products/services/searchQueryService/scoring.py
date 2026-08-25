from dataclasses import dataclass, field
from math import isfinite
from typing import Any, Iterable

@dataclass(frozen=True, slots=True)
class SearchMatch:
    """
    A single match produced by a search block.

    Each detachable search block can return SearchMatch objects.
    Multiple blocks may produce a match for the same product.
    """

    product_id: Any
    score: float
    source: str
    signals: dict[str, float] = field(default_factory=dict)


class SearchScorer:
    """
    Combines relevance signals produced by independent search blocks.

    Responsibilities:
    - Validate search matches
    - Combine duplicate product matches
    - Aggregate relevance scores
    - Preserve individual search signals

    This service does NOT:
    - Perform database searching
    - Normalize queries
    - Apply filters
    - Perform final ordering
    """

    def score(
        self,
        query: str,
        results: Iterable[Iterable[SearchMatch]],
    ) -> list[SearchMatch]:
        if not query or not results:
            return []

        aggregated: dict[Any, dict[str, Any]] = {}

        for block_results in results:
            if not block_results:
                continue

            for match in block_results:
                if not isinstance(match, SearchMatch):
                    continue

                if not isfinite(match.score):
                    continue

                if match.score < 0:
                    continue

                product_id = match.product_id

                if product_id not in aggregated:
                    aggregated[product_id] = {
                        "score": 0.0,
                        "signals": {},
                    }

                aggregated[product_id]["score"] += match.score

                for signal_name, signal_score in match.signals.items():
                    if not isinstance(signal_score, (int, float)):
                        continue

                    if not isfinite(signal_score):
                        continue

                    if signal_score < 0:
                        continue

                    aggregated[product_id]["signals"][signal_name] = (
                        aggregated[product_id]["signals"].get(signal_name, 0.0)
                        + float(signal_score)
                    )

        return [
            SearchMatch(
                product_id=product_id,
                score=data["score"],
                source="combined",
                signals=data["signals"],
            )
            for product_id, data in aggregated.items()
        ]