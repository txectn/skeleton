from django.db.models import Q

from .scoring import SearchMatch
from ...models import SynonymTerm

class SynonymSearch:
    """
    Synonym-based search block for the Product catalog.

    This block expands the user's search query using known synonyms
    and searches the expanded terms against searchable product fields.

    Searchable fields:
        Product
        ├── name
        └── description

        Brand
        └── name

        Category
        └── name

        Option
        ├── value
        └── option_variable.name

        Tag
        └── name

        Collection
        └── name

    This block does not:
        - normalize the original query
        - perform exact matching
        - perform PostgreSQL full-text ranking
        - perform fuzzy matching
        - perform final ranking
        - apply filters
        - paginate results
    """

    SOURCE = "synonym"

    SEARCH_FIELDS = (
        "name",
        "description",
        "brand__name",
        "category__name",
        "options__value",
        "options__option_variable__name",
        "tags__name",
        "collections__name",
    )

    def search(self, queryset, query):
        """
        Return SearchMatch objects for products matching
        one or more synonym-expanded search terms.

        The original query itself is not handled here.
        ExactSearch and FullTextSearch are responsible for that.
        """

        if not query:
            return []

        query = query.strip().lower()

        if not query:
            return []

        synonym_term = (
            SynonymTerm.objects
            .filter(
                term=query,
                is_active=True,
                group__is_active=True,
            )
            .select_related("group")
            .first()
        )

        if not synonym_term:
            return []

        synonym_terms = (
            SynonymTerm.objects
            .filter(
                group=synonym_term.group,
                is_active=True,
            )
            .values_list("term", flat=True)
        )

        matches = Q()

        for term in synonym_terms:
            term_query = Q()

            for field in self.SEARCH_FIELDS:
                term_query |= Q(
                    **{f"{field}__icontains": term}
                )

            matches |= term_query

        products = (
            queryset
            .filter(matches)
            .distinct()
        )

        return [
            SearchMatch(
                product_id=product.id,
                score=1.0,
                source=self.SOURCE,
                signals={
                    "synonym": 1.0,
                },
            )
            for product in products
        ]