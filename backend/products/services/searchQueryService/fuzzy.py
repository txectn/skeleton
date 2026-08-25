import re

from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import Case, FloatField, Value, When
from django.db.models.functions import Greatest

from .scoring import SearchMatch

class FuzzySearch:
    """
    Fuzzy search block for the Product catalog using PostgreSQL
    Trigram Word Similarity.
    """

    SOURCE = "fuzzy"

    # Trigram math drops steeply on short words. 0.35 safely catches 1-2 character typos.
    SIMILARITY_THRESHOLD = 0.50

    # Prevent very short words from producing noisy matches.
    MIN_WORD_LENGTH = 1

    FIELD_WEIGHTS = {
        "name": 100.0,
        "brand_name": 90.0,
        "model_name": 90.0,
        "category_name": 80.0,
        "slug": 70.0,
        "brand_slug": 65.0,
        "model_slug": 65.0,
        "category_slug": 60.0,
    }

    WORD_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)

    def search(self, queryset, query):
        if not query or not query.strip():
            return []

        query_words = [
            word for word in self._extract_words(query)
            if len(word) >= self.MIN_WORD_LENGTH
        ]

        if not query_words:
            return []

        results_by_product = {}

        for query_word in query_words:
            # Query DB for matches against this word
            matches = self._search_word(
                queryset=queryset,
                query_word=query_word
            )

            for product in matches:
                similarity = float(
                    getattr(product, "fuzzy_similarity", 0.0) or 0.0
                )
                field = getattr(product, "fuzzy_field", None)

                if not field or similarity < self.SIMILARITY_THRESHOLD:
                    continue

                field_weight = self.FIELD_WEIGHTS.get(field, 50.0)
                score = similarity * field_weight
                product_id = product.id

                candidate = SearchMatch(
                    product_id=product_id,
                    score=score,
                    source=self.SOURCE,
                    signals={
                        "fuzzy": score,
                        "similarity": similarity,
                        "query_word": query_word,
                        "matched_field": field,
                    },
                )

                current = results_by_product.get(product_id)

                if current is None or candidate.score > current.score:
                    results_by_product[product_id] = candidate

        return list(results_by_product.values())

    def _search_word(self, queryset, query_word):
        field_annotations = {}
        when_branches = []

        # 1. Annotate each field's similarity
        for field_key, field_path in self._fields().items():
            sim_expr = TrigramWordSimilarity(
                Value(query_word),
                field_path
            )

            field_annotations[f"_sim_{field_key}"] = sim_expr

            # Use gte filter in Case/When to prevent exact float equality failures
            when_branches.append(
                When(
                    **{
                        f"_sim_{field_key}__gte": self.SIMILARITY_THRESHOLD,
                        "then": Value(field_key),
                    }
                )
            )

        qs = queryset.annotate(**field_annotations)

        # 2. Get maximum similarity across all fields
        similarity_expressions = list(field_annotations.values())

        max_similarity = Greatest(
            *similarity_expressions,
            output_field=FloatField()
        )

        qs = qs.annotate(fuzzy_similarity=max_similarity)

        # 3. Resolve matched field using priority ordering
        # defined in _fields
        qs = qs.annotate(
            fuzzy_field=Case(
                *when_branches,
                default=None
            )
        )

        return (
            qs.filter(
                fuzzy_similarity__gte=self.SIMILARITY_THRESHOLD
            )
            .only("id")
            .distinct()
        )

    @classmethod
    def _fields(cls):
        # Order matters! Priority goes from top to bottom if scores are tied.

        return {
            "name": "name",
            "brand_name": "brand__name",
            "model_name": "model__name",
            "category_name": "category__name",
            "slug": "slug",
            "brand_slug": "brand__slug",
            "model_slug": "model__slug",
            "category_slug": "category__slug",
        }

    @classmethod
    def _extract_words(cls, value):
        return [
            word.lower()
            for word in cls.WORD_PATTERN.findall(value)
            if word
        ]