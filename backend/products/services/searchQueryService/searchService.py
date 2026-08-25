from django.db.models import Case, When, IntegerField

# Core Services
from .normalize import QueryNormalizer
from .scoring import SearchScorer
from .ranking import SearchRanker

# Detachable Services
from .exact import ExactSearch
from .fulltext import FullTextSearch
from .synonyms import SynonymSearch
from .fuzzy import FuzzySearch

class ProductSearchService:

    def __init__(self):
        # Core pipeline
        self.normalizer = QueryNormalizer()
        self.scorer = SearchScorer()
        self.ranker = SearchRanker()

        # Detachable search blocks
        self.search_blocks = [
            ExactSearch(),
            FullTextSearch(),
            SynonymSearch(),
            FuzzySearch(),
        ]

    def search(self, queryset, query=None):
        if not query:
            return queryset

        # 1. Normalize query
        query = self.normalizer.normalize(query)

        if not query:
            return queryset

        # 2. Collect candidates/signals from each search block
        search_results = []

        for block in self.search_blocks:
            results = block.search(
                queryset=queryset,
                query=query,
            )

            if results:
                search_results.extend(results)

        if not search_results:
            return queryset.none()

        # 3. Calculate relevance
        scored_results = self.scorer.score(
            query=query,
            results=[search_results],
        )

        # 4. Apply final ranking
        ranked_results = self.ranker.rank(
            query=query,
            results=scored_results,
        )

        if not ranked_results:
            return queryset.none()

        # 5. Extract Product IDs in ranked order
        product_ids = [
            result.product_id
            for result in ranked_results
        ]

        # 6. Preserve ranking at database level
        ranking_order = Case(
            *[
                When(
                    id=product_id,
                    then=position,
                )
                for position, product_id in enumerate(product_ids)
            ],
            output_field=IntegerField(),
        )

        # 7. Return Product QuerySet
        return (
            queryset
            .filter(id__in=product_ids)
            .order_by(ranking_order)
        )
