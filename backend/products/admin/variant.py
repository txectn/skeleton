from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from unfold.admin import ModelAdmin, TabularInline

from ..models import Variant, Inventory, Option, Media
from promotions.models import PromotionVariant

class VariantAdminForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = "__all__"
        widgets = {
            "options": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        product_id = (
            self.data.get(self.add_prefix("product"))
            if self.is_bound
            else None
        )

        if not product_id and self.instance and self.instance.product_id:
            product_id = self.instance.product_id

        if product_id:
            self.fields["options"].queryset = (
                Option.objects.filter(product_id=product_id)
                .select_related("option_variable")
            )
        else:
            self.fields["options"].queryset = Option.objects.none()


class InventoryInline(TabularInline):
    model = Inventory
    extra = 0
    max_num = 1


class PromotionVariantInline(TabularInline):
    model = PromotionVariant
    extra = 0


@admin.register(Variant)
class VariantAdmin(ModelAdmin):
    form = VariantAdminForm

    list_display = (
        "id",
        "sku",
        "product_link",
        "option_summary",
        "price",
        "compare_at_price",
        "cost_price",
        "purchase_limit",
        "position",
        "is_active",
        "created_at",
    )

    list_display_links = (
        "id",
        "sku",
    )

    list_filter = (
        "is_active",
        "product",
    )

    search_fields = (
        "id",
        "sku",
        "product__name",
        "options__value",
        "options__option_variable__name",
    )

    autocomplete_fields = (
        "product",
        "currency",
    )

    readonly_fields = (
        "product_link",
        "product_brand",
        "product_category",
        "product_model",
        "product_media_preview",
        "option_summary",
        "created_at",
    )

    fields = (
        "product",
        "product_link",
        "product_brand",
        "product_category",
        "product_model",
        "product_media_preview",
        "sku",
        "options",
        "option_summary",
        "price",
        "compare_at_price",
        "cost_price",
        "currency",
        "position",
        "purchase_limit",
        "is_active",
        "created_at",
    )

    ordering = (
        "product",
        "position",
        "id",
    )

    inlines = (
        InventoryInline,
        PromotionVariantInline,
    )

    @admin.display(description="Product")
    def product_link(self, obj):
        if not obj or not obj.product_id:
            return "-"

        url = reverse(
            "admin:products_product_change",
            args=[obj.product_id],
        )

        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.product.name,
        )

    @admin.display(description="Brand")
    def product_brand(self, obj):
        if not obj or not obj.product_id:
            return "-"

        return obj.product.brand

    @admin.display(description="Category")
    def product_category(self, obj):
        if not obj or not obj.product_id:
            return "-"

        return obj.product.category

    @admin.display(description="Model")
    def product_model(self, obj):
        if not obj or not obj.product_id:
            return "-"

        return obj.product.model or "-"

    @admin.display(description="Selected Options")
    def option_summary(self, obj):
        if not obj or not obj.pk:
            return "-"

        options = obj.options.select_related(
            "option_variable"
        ).all()

        if not options.exists():
            return "No options selected"

        return format_html(
            '<div style="display:flex;flex-wrap:wrap;gap:6px;">{}</div>',
            format_html_join(
                "",
                '<span style="padding:4px 8px;'
                'border-radius:6px;'
                'background:rgba(128,128,128,.12);">'
                '<strong>{}</strong>: {}</span>',
                (
                    (
                        option.option_variable,
                        option.value,
                    )
                    for option in options
                ),
            ),
        )

    @admin.display(description="Product Media")
    def product_media_preview(self, obj):
        if not obj or not obj.product_id:
            return "Save the variant with a product to preview its media."

        media_items = Media.objects.filter(
            product_id=obj.product_id
        ).order_by("position", "id")

        if not media_items.exists():
            return "No media available for this product."

        previews = []

        for media in media_items:
            try:
                url = media.file.url
            except ValueError:
                continue

            if media.media_type == Media.MediaType.IMAGE:
                preview = format_html(
                    '<a href="{}" target="_blank" rel="noopener noreferrer">'
                    '<img src="{}" alt="{}" loading="lazy" '
                    'style="display:block;width:80px;height:80px;'
                    'object-fit:cover;border-radius:6px;" />'
                    '</a>',
                    url,
                    url,
                    media.alt_text or media.product.name,
                )
            else:
                preview = format_html(
                    '<video src="{}" controls preload="metadata" '
                    'style="display:block;width:160px;height:90px;'
                    'object-fit:cover;border-radius:6px;">'
                    '</video>',
                    url,
                )

            previews.append(
                format_html(
                    '<div style="display:flex;flex-direction:column;'
                    'gap:4px;max-width:160px;">'
                    '{}'
                    '<span style="font-size:12px;opacity:.7;'
                    'overflow-wrap:anywhere;">{}</span>'
                    '</div>',
                    preview,
                    media.alt_text or media.get_media_type_display(),
                )
            )

        if not previews:
            return "No accessible media files available."

        return format_html(
            '<div style="display:flex;flex-wrap:wrap;gap:12px;">{}</div>',
            format_html_join("", "{}", ((item,) for item in previews)),
        )

    @admin.display(
        boolean=True,
        description="Active",
        ordering="is_active",
    )
    def is_active_display(self, obj):
        return obj.is_active
