
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from unfold.admin import ModelAdmin

from ..models import OrderItem
from products.models import Media

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):

    list_display = (
        "id",
        "order_link",
        "product_link",
        "sku",
        "option_summary",
        "quantity",
        "unit_price",
        "discount",
        "total",
    )

    list_display_links = ("id",)

    list_filter = (
        "order",
        "variant__product",
    )

    search_fields = (
        "order__id",
        "variant__sku",
        "variant__product__name",
        "variant__product__slug",
        "variant__options__value",
        "variant__options__option_variable__name",
    )

    autocomplete_fields = (
        "order",
        "variant",
    )

    readonly_fields = (
        "order_link",
        "product_link",
        "product_brand",
        "product_category",
        "product_model",
        "product_media_preview",
        "sku",
        "option_summary",
        "variant_price",
        "variant_compare_at_price",
        "variant_cost_price",
        "variant_currency",
        "variant_purchase_limit",
        "variant_position",
        "variant_active",
    )

    fields = (
        "order",
        "order_link",
        "variant",
        "product_link",
        "product_brand",
        "product_category",
        "product_model",
        "product_media_preview",
        "sku",
        "option_summary",
        "variant_price",
        "variant_compare_at_price",
        "variant_cost_price",
        "variant_currency",
        "variant_purchase_limit",
        "variant_position",
        "variant_active",
        "quantity",
        "unit_price",
        "discount",
        "total",
    )

    list_select_related = (
        "order",
        "variant",
        "variant__product",
        "variant__product__brand",
        "variant__product__category",
        "variant__product__model",
        "variant__currency",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.prefetch_related(
            "variant__options__option_variable",
        )

    @admin.display(description="Order")
    def order_link(self, obj):
        if not obj or not obj.order_id:
            return "-"

        url = reverse(
            "admin:orders_order_change",
            args=[obj.order_id],
        )

        return format_html(
            '<a href="{}">Order #{}</a>',
            url,
            obj.order_id,
        )

    @admin.display(description="Product")
    def product_link(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        product = obj.variant.product

        url = reverse(
            "admin:products_product_change",
            args=[product.pk],
        )

        return format_html(
            '<a href="{}">{}</a>',
            url,
            product.name,
        )

    @admin.display(description="SKU")
    def sku(self, obj):
        return obj.variant.sku if obj and obj.variant_id else "-"

    @admin.display(description="Brand")
    def product_brand(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        return obj.variant.product.brand

    @admin.display(description="Category")
    def product_category(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        return obj.variant.product.category

    @admin.display(description="Model")
    def product_model(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        return obj.variant.product.model or "-"

    @admin.display(description="Selected Options")
    def option_summary(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        options = obj.variant.options.select_related(
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
                    (option.option_variable, option.value)
                    for option in options
                ),
            ),
        )

    @admin.display(description="Product Media")
    def product_media_preview(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        media_items = Media.objects.filter(
            product_id=obj.variant.product_id
        ).order_by("position", "id")

        previews = []

        for media in media_items:
            try:
                url = media.file.url
            except ValueError:
                continue

            if media.media_type == Media.MediaType.IMAGE:
                preview = format_html(
                    '<a href="{}" target="_blank" '
                    'rel="noopener noreferrer">'
                    '<img src="{}" alt="{}" loading="lazy" '
                    'style="display:block;width:80px;height:80px;'
                    'object-fit:cover;border-radius:6px;" />'
                    '</a>',
                    url,
                    url,
                    media.alt_text or obj.variant.product.name,
                )
            else:
                preview = format_html(
                    '<video src="{}" controls preload="metadata" '
                    'style="width:160px;height:90px;'
                    'object-fit:cover;border-radius:6px;"></video>',
                    url,
                )

            previews.append(
                format_html(
                    '<div style="display:flex;flex-direction:column;'
                    'gap:4px;max-width:160px;">'
                    '{}<span style="font-size:12px;opacity:.7;">'
                    '{}</span></div>',
                    preview,
                    media.alt_text or media.get_media_type_display(),
                )
            )

        if not previews:
            return "No media available."

        return format_html(
            '<div style="display:flex;flex-wrap:wrap;gap:12px;">{}</div>',
            format_html_join("", "{}", ((item,) for item in previews)),
        )

    @admin.display(description="Current Variant Price")
    def variant_price(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        return obj.variant.price

    @admin.display(description="Compare-at Price")
    def variant_compare_at_price(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        return obj.variant.compare_at_price or "-"

    @admin.display(description="Cost Price")
    def variant_cost_price(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        return obj.variant.cost_price or "-"

    @admin.display(description="Currency")
    def variant_currency(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        return obj.variant.currency

    @admin.display(description="Purchase Limit")
    def variant_purchase_limit(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        return obj.variant.purchase_limit or "-"

    @admin.display(description="Variant Position")
    def variant_position(self, obj):
        if not obj or not obj.variant_id:
            return "-"

        return obj.variant.position

    @admin.display(
        boolean=True,
        description="Variant Active",
    )
    def variant_active(self, obj):
        if not obj or not obj.variant_id:
            return False

        return obj.variant.is_active
