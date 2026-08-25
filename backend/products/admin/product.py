from django import forms
from django.contrib import admin
from django.db.models import Count

from unfold.admin import ModelAdmin, StackedInline, TabularInline

from ..models import (
    Product,
    Media, 
    Variant,
    Inventory,
    Option
)

class VariantInlineForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.product_id:
            self.fields["options"].queryset = (
                Option.objects
                .filter(product_id=self.instance.product_id)
                .select_related("option_variable")
            )
        else:
            self.fields["options"].queryset = Option.objects.none()

class InventoryInline(StackedInline):
    model = Inventory
    extra = 1
    max_num = 1

class VariantInline(StackedInline):
    model = Variant
    form = VariantInlineForm
    extra = 1

    inlines = (
        InventoryInline,
    )

class OptionInline(TabularInline):
    model = Option
    extra = 1

class MediaInline(TabularInline):
    model = Media
    extra = 0

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "name",
        "brand",
        "model",
        "category",
        "variant_count",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_display_links = (
        "name",
    )

    search_fields = (
        "name",
        "slug",
        "description",
        "brand__name",
        "model__name",
        "category__name",
    )

    list_filter = (
        "is_active",
        "brand",
        "category",
        "created_at",
        "updated_at",
    )

    list_editable = (
       "is_active",
    )

    autocomplete_fields = (
        "brand",
        "model",
        "category",
        "collections",
        "tags",
        "shipping_class",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 50

    filter_horizontal = ()

    inlines = (
        MediaInline,
        OptionInline,
        VariantInline,
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return (
            queryset
            .select_related(
                "brand",
                "model",
                "category",
            )
            .annotate(
                _variant_count=Count(
                    "variants",
                    distinct=True,
                ),
            )
        )

    @admin.display(
        description="Variants",
        ordering="_variant_count",
    )
    def variant_count(self, obj):
        return obj._variant_count