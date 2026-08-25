from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db.models import F

from .scoring import SearchMatch

class FullTextSearch:
    """
    PostgreSQL full-text search block for the Product catalog.

    Searchable fields:
        Product
        ├── name
        └── description

        Brand
        └── name

        Model
        └── name

        Category
        ├── name
        └── description

        Variant
        └── sku

        Option
        └── value

        OptionVariable
        └── name

    This block:
        - uses PostgreSQL full-text search
        - calculates PostgreSQL relevance with SearchRank
        - returns SearchMatch objects
        - remains independent from other search blocks

    This block does not:
        - normalize the query
        - perform exact matching
        - perform fuzzy matching
        - perform synonym expansion
        - perform final ranking
        - apply product filters
        - paginate results
    """

    SOURCE = "fulltext"

    SEARCH_VECTOR = (
        SearchVector("name", weight="A")
        + SearchVector("description", weight="B")
        + SearchVector("brand__name", weight="A")
        + SearchVector("model__name", weight="A")
        + SearchVector("category__name", weight="B")
        + SearchVector("category__description", weight="C")
        + SearchVector("variants__sku", weight="A")
        + SearchVector("options__value", weight="B")
        + SearchVector(
            "options__option_variable__name",
            weight="C",
        )
    )

    def search(self, queryset, query):
        """
        Return SearchMatch objects for products matching the
        query through PostgreSQL full-text search.
        """

        if not query:
            return []

        query = query.strip()

        if not query:
            return []

        search_query = SearchQuery(
            query,
            search_type="websearch",
        )

        matches = (
            queryset
            .annotate(
                search_vector=self.SEARCH_VECTOR,
            )
            .annotate(
                fulltext_rank=SearchRank(
                    F("search_vector"),
                    search_query,
                )
            )
            .filter(
                search_vector=search_query,
                fulltext_rank__gt=0,
            )
            .order_by(
                "-fulltext_rank",
                "-id",
            )
            .distinct()
        )

        return [
            SearchMatch(
                product_id=product.id,
                score=float(product.fulltext_rank),
                source=self.SOURCE,
                signals={
                    "fulltext": float(product.fulltext_rank),
                },
            )
            for product in matches
        ]