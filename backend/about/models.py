from django.db import models

# =====================================
# About Page
# =====================================

class AboutPage(models.Model):

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return "About Page"

# =====================================
# Image Position Choices
# =====================================

class ImagePosition(models.TextChoices):

    LEFT = "left", "Left"
    RIGHT = "right", "Right"
    NONE = "none", "None"


# ==========================================================================
# About Section
# About Us / Our Story / Our Values / Call To Action/ 
# ============================================================================

class AboutSection(models.Model):

    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="about_sections",
    )

    section_id = models.CharField(
        max_length=100,
    )

    title = models.CharField(
        max_length=255,
    )

    heading = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    cta_link = models.CharField(
        max_length=500,
        blank=True,
    )

    cta_label = models.CharField(
        max_length=100,
        blank=True,
    )

    position = models.PositiveIntegerField(
        default=0,
    )

    image_position = models.CharField(
        max_length=10,
        choices=ImagePosition.choices,
        default=ImagePosition.RIGHT,
    )

    image = models.ImageField(
        upload_to="about/story/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"

    constraints = [
        models.UniqueConstraint(
            fields=["about_page", "position"],
            name="unique_about_section_position",
        ),
    ]

    def __str__(self):
        return self.title

# =====================================
# About Item
# Individual Values / Features
# =====================================

class AboutItem(models.Model):

    about_section = models.ForeignKey(
        AboutSection,
        on_delete=models.CASCADE,
        related_name="items",
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "About Item"
        verbose_name_plural = "About Items"

    def __str__(self):
        return self.title
