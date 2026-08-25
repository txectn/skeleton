from django.db.models import (
    Case,
    Exists,
    FloatField,
    OuterRef,
    Q,
    Value,
    When,
)

from ...models.option import Option
from ...models.variant import Variant

from .scoring import SearchMatch

class ExactSearch:
    """
    Exact-match search block for the Product catalog.

    Searchable fields:

        Product
        ├── name
        └── slug

        Brand
        ├── name
        └── slug

        Model
        ├── name
        └── slug

        Category
        ├── name
        └── slug

        Variant
        └── sku

        Option
        └── value

        OptionVariable
        └── name

    Responsibilities:
        - Exact case-insensitive matching
        - Generate exact-match relevance signals

    Does not:
        - Normalize the query
        - Perform fuzzy matching
        - Perform synonym matching
        - Apply filters
        - Perform final ranking
    """

    SOURCE = "exact"

    FIELD_WEIGHTS = {
        "product_name": 100.0,
        "product_slug": 95.0,

        "variant_sku": 100.0,

        "brand_name": 90.0,
        "brand_slug": 85.0,

        "model_name": 90.0,
        "model_slug": 85.0,

        "category_name": 80.0,
        "category_slug": 75.0,

        "option_value": 70.0,
        "option_variable_name": 60.0,
    }

    def search(self, queryset, query):
        """
        Return SearchMatch objects for products containing
        an exact case-insensitive match.

        The strongest matching field determines the exact score.
        """

        if query is None:
            return []

        query = str(query).strip()

        if not query:
            return []

        # ---------------------------------------------------------
        # Reverse-relation existence checks
        # ---------------------------------------------------------

        variant_match = Variant.objects.filter(
            product_id=OuterRef("pk"),
            sku__iexact=query,
        )

        option_value_match = Option.objects.filter(
            product_id=OuterRef("pk"),
            value__iexact=query,
        )

        option_variable_match = Option.objects.filter(
            product_id=OuterRef("pk"),
            option_variable__name__iexact=query,
        )

        # ---------------------------------------------------------
        # Candidate filtering
        # ---------------------------------------------------------

        matches = queryset.filter(
            Q(name__iexact=query)
            | Q(slug__iexact=query)
            | Q(brand__name__iexact=query)
            | Q(brand__slug__iexact=query)
            | Q(model__name__iexact=query)
            | Q(model__slug__iexact=query)
            | Q(category__name__iexact=query)
            | Q(category__slug__iexact=query)
            | Exists(variant_match)
            | Exists(option_value_match)
            | Exists(option_variable_match)
        )

        # ---------------------------------------------------------
        # Exact relevance score
        # ---------------------------------------------------------
        #
        # Case is intentionally ordered from strongest to weakest.
        #
        # If a product matches multiple fields, the strongest
        # exact signal is used.
        # ---------------------------------------------------------

        matches = matches.annotate(
            exact_score=Case(
                When(
                    name__iexact=query,
                    then=Value(
                        self.FIELD_WEIGHTS["product_name"]
                    ),
                ),

                When(
                    slug__iexact=query,
                    then=Value(
                        self.FIELD_WEIGHTS["product_slug"]
                    ),
                ),

                When(
                    Exists(variant_match),
                    then=Value(
                        self.FIELD_WEIGHTS["variant_sku"]
                    ),
                ),

                When(
                    brand__name__iexact=query,
                    then=Value(
                        self.FIELD_WEIGHTS["brand_name"]
                    ),
                ),

                When(
                    brand__slug__iexact=query,
                    then=Value(
                        self.FIELD_WEIGHTS["brand_slug"]
                    ),
                ),

                When(
                    model__name__iexact=query,
                    then=Value(
                        self.FIELD_WEIGHTS["model_name"]
                    ),
                ),

                When(
                    model__slug__iexact=query,
                    then=Value(
                        self.FIELD_WEIGHTS["model_slug"]
                    ),
                ),

                When(
                    category__name__iexact=query,
                    then=Value(
                        self.FIELD_WEIGHTS["category_name"]
                    ),
                ),

                When(
                    category__slug__iexact=query,
                    then=Value(
                        self.FIELD_WEIGHTS["category_slug"]
                    ),
                ),

                When(
                    Exists(option_value_match),
                    then=Value(
                        self.FIELD_WEIGHTS["option_value"]
                    ),
                ),

                When(
                    Exists(option_variable_match),
                    then=Value(
                        self.FIELD_WEIGHTS["option_variable_name"]
                    ),
                ),

                default=Value(0.0),

                output_field=FloatField(),
            )
        )

        # ---------------------------------------------------------
        # Convert database results into SearchMatch objects
        # ---------------------------------------------------------

        return [
            SearchMatch(
                product_id=product.id,
                score=float(product.exact_score),
                source=self.SOURCE,
                signals={
                    "exact": float(product.exact_score),
                },
            )
            for product in matches
        ]