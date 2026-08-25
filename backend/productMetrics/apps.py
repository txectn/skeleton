from django.apps import AppConfig

class ProductMetricsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "productMetrics"

    def ready(self) -> None:
        from . import signals  # noqa: F401