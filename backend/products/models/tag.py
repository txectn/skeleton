from django.db import models

class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    class Meta:
        db_table = "product_tags"
        ordering = ["name"]

    def __str__(self):
        return self.name