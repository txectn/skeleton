import re
from django import forms

from django.utils.html import format_html

from django.contrib import admin
from django.db.models import Count
from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe

from django.contrib.admin import RelatedFieldListFilter

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms.formsets import BaseFormSet

from unfold.admin import ModelAdmin, StackedInline, TabularInline

from ..models import (
    Product,
    Media, 
    Variant,
    Inventory,
    Option,
    Metafield,
)
from promotions.models import PromotionVariant

class MetafieldInline(TabularInline):
    model = Metafield
    extra = 0

class InventoryInline(StackedInline):
    model = Inventory
    extra = 1
    max_num = 1

class PromotionVariantInline(TabularInline):
    model = PromotionVariant
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        original_clean = formset.clean

        def clean(self):
            original_clean(self)
            # bubble up per-form errors to formset non-field errors
            for form in self.forms:
                if form.errors:
                    for field, errs in form.errors.items():
                        for err in errs:
                            self._non_form_errors.append(err)  # see note
        formset.clean = clean
        return formset

class OptionInline(TabularInline):
    model = Option
    extra = 1
    classes = ["option-inline"]
    fields = (
        "option_variable",
        "value",
        "position",
    )

class VariantInlineForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = "__all__"
        widgets = {
            "options": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.product_id:
            self.fields["options"].queryset = (
                Option.objects.filter(product_id=self.instance.product_id)
                .select_related("option_variable")
            )
        else:
            self.fields["options"].queryset = Option.objects.none()

class VariantInline(StackedInline):
    model = Variant
    form = VariantInlineForm
    extra = 0    

    fields = (
        "sku",
        "price",
        "compare_at_price",
        "cost_price",
        "currency",
        "options",
        "position",
        "purchase_limit",
        "is_active",
    )

    inlines = (
        InventoryInline,
        PromotionVariantInline,
    )

# --- CONDITIONAL MEDIA FILE WIDGET ---

class MediaFileAdminWidget(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        widget_output = super().render(name, value, attrs, renderer)
        
        if value and hasattr(value, "url"):
            url = value.url.lower()
            image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg")
            video_extensions = (".mp4", ".webm", ".ogg", ".mov", ".avi", ".mkv", ".m4v")
            
            is_image = url.endswith(image_extensions)
            is_video = url.endswith(video_extensions)
            
            if is_image or is_video:
                # 1. Remove the redundant "Currently: <filename><br>" text
                widget_output = re.sub(
                    r'Currently:\s*<a[^>]*>.*?</a>(<br\s*/?>)?', 
                    '', 
                    widget_output, 
                    flags=re.IGNORECASE
                )
                
                # 2. Clean up old text labels preceding the file input
                widget_output = re.sub(
                    r'(Change:|<label[^>]*>.*?</label>)\s*', 
                    '', 
                    widget_output, 
                    flags=re.IGNORECASE
                )
                
                # 3. Use custom clean wrapper with the line clamping styles on the file name span
                unique_id = attrs.get('id', f'id_{name}') if attrs else f'id_{name}'
                widget_output = f'''
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <label style="display: inline-block; cursor: pointer; font-size: 12px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-cloud-upload preview-icon"><path d="M12 13v8"/><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="m8 17 4-4 4 4"/></svg>
                            <input type="file" name="{name}" id="{unique_id}" style="display: none;" onchange="document.getElementById('filename-{unique_id}').textContent = this.files[0] ? this.files[0].name : ''">
                        </label>
                        <span id="filename-{unique_id}" style="font-size: 12px; opacity: 0.8; display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 1; overflow: hidden;"></span>
                    </div>
                '''
                
                # 4. Build the preview (image or video) with the same 40x40 sizing
                if is_image:
                    preview_html = f'''
                        <a href="{value.url}" target="_blank">
                            <img src="{value.url}" style="display: block; width: 40px; max-width: 40px; height: 40px; object-fit: cover;" />
                        </a>
                    '''
                else:  # is_video
                    preview_html = f'''
                        <a href="{value.url}" target="_blank" style="display: block; width: 40px; height: 40px;">
                            <video src="{value.url}" muted playsinline preload="metadata"
                                style="display: block; width: 40px; max-width: 40px; height: 40px; object-fit: cover; pointer-events: none;">
                            </video>
                        </a>
                    '''
                
                return mark_safe(f'''
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="flex-shrink: 0;">
                            {preview_html}
                        </div>
                        <div>
                            {widget_output}
                        </div>
                    </div>
                ''')
                
        return widget_output

class MediaAdminForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = "__all__"
        widgets = {
            "file": MediaFileAdminWidget(),
        }

class MediaInline(TabularInline):
    model = Media
    form = MediaAdminForm
    extra = 0
# ------------------------------------

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "thumbnail",
        "id",
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
        "thumbnail",
        "id",
        "name",
    )

    search_fields = (
        "=id",
        "name",
        "=slug",
        "description",
        "brand__name",
        "model__name",
        "category__name",
    )

    list_filter = (
        "is_active",
        "brand",
        "category",
        "model",
        "collections",
        "tags",
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
        "shipping_class_rates",
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
        MetafieldInline,
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

    @admin.display(description="Thumbnail")
    def thumbnail(self, obj):

        media = obj.media.filter(
            media_type=Media.MediaType.IMAGE,
        ).first()

        if not media:
            return "NO IMAGE"

        return format_html(
            '<img src="{}" style="width:45px; height:45px; '
            'object-fit:cover; border-radius:6px;" />',
            media.file.url,
        )
        
