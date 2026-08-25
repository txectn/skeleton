class ProductSortOrdering:
    """
    Central source of truth for product queryset ordering definitions.
    """

    MOST_VIEWED = (
        "-metrics__view_count",
        "-id",
    )

    MOST_SOLD = (
        "-metrics__sold_count",
        "-id",
    )

    TRENDING = (
        "-metrics__trending_score",
        "-id",
    )

    POPULARITY = (
        "-metrics__popularity_score",
        "-id",
    )

    SORT_ORDERINGS = {
        "most_viewed": MOST_VIEWED,
        "most_sold": MOST_SOLD,
        "trending": TRENDING,
        "popularity": POPULARITY,
    }