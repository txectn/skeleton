from django.db import models

class OptionVariable(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ("name",)
        indexes = (
            models.Index(fields=("name",)),
        )

    def __str__(self):
        return self.name