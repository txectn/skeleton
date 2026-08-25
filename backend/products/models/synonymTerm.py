from django.db import models

from .synonymGroup import SynonymGroup

class SynonymTerm(models.Model):
    group = models.ForeignKey(
        SynonymGroup,
        on_delete=models.CASCADE,
        related_name="terms",
    )
    term = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["term"]
        constraints = [
            models.UniqueConstraint(
                fields=["group", "term"],
                name="unique_synonym_term_per_group",
            ),
        ]

    def __str__(self):
        return self.term