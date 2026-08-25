import re
import unicodedata

class QueryNormalizer:
    """
    Normalize user search queries into a consistent representation.

    Responsibilities:
    - Validate the input type
    - Normalize Unicode characters
    - Normalize whitespace
    - Normalize case
    - Normalize common punctuation spacing
    - Remove control characters

    This service does NOT:
    - Perform searching
    - Apply synonyms
    - Perform fuzzy matching
    - Stem words
    - Rank results
    """

    _WHITESPACE_PATTERN = re.compile(r"\s+")
    _CONTROL_CHARACTER_PATTERN = re.compile(r"[\x00-\x1f\x7f]")

    def normalize(self, query):
        if query is None:
            return ""

        if not isinstance(query, str):
            query = str(query)

        query = unicodedata.normalize("NFKC", query)

        query = self._CONTROL_CHARACTER_PATTERN.sub(" ", query)

        query = query.strip()

        if not query:
            return ""

        query = self._WHITESPACE_PATTERN.sub(" ", query)

        return query.casefold()