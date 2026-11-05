from django.contrib import admin
from django.utils.html import format_html

from unfold.admin import ModelAdmin

from ..models import ReturnActionToken

@admin.register(ReturnActionToken)
class ReturnActionTokenAdmin(ModelAdmin):
    list_display = (
        "id",
        "return_request",
        "token",
        "expires_at",
        "used_at",
        "created_at",
    )

    list_display_links = (
        "id",
        "return_request",
    )

    readonly_fields = (
        "token_field",
        "created_at",
    )

    list_filter = (
        "used_at",
        "created_at",
    )

    search_fields = (
        "=return_request__id",
    )

    autocomplete_fields = ("return_request",)

    list_per_page = 25

    fieldsets = (
        (
            "Token Information",
            {
                "fields": (
                    "return_request",
                    "token_field",
                    "expires_at",
                    "used_at",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                ),
            },
        ),
    )
    
    @admin.display(description="Token")
    def token_field(self, obj):
        if not obj or not obj.token:
            return "-"

        token = str(obj.token)

        return format_html(
            """
            <div style="display: flex; align-items: center; gap: 10px;">
                <div
                    class="token-value border border-base-200 dark:border-base-700 rounded-default px-3 py-2 text-sm"
                    style="font-family: monospace; word-break: break-all;"
                >
                    {}
                </div>

                <button
                    type="button"
                    class="token-copy-button"
                    data-token="{}"
                    class="border"
                    style="cursor: pointer; padding: 10px; min-height: 41px; -webkit-tap-highlight-color: transparent; -ms-touch-action: manipulation; touch-action: manipulation;"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-copy preview-icon"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                </button>
            </div>

            <script>
                document.querySelectorAll('.token-copy-button').forEach(button => {{
                    if (button.dataset.initialized) return;
                    button.dataset.initialized = 'true';

                    button.addEventListener('click', async () => {{
                        const token = button.dataset.token;

                        try {{
                            if (navigator.clipboard && navigator.clipboard.writeText) {{
                                await navigator.clipboard.writeText(token);
                            }} else {{
                                const textarea = document.createElement('textarea');
                                textarea.value = token;
                                textarea.style.position = 'fixed';
                                textarea.style.opacity = '0';
                                document.body.appendChild(textarea);
                                textarea.select();

                                const copied = document.execCommand('copy');
                                textarea.remove();

                                if (!copied) {{
                                    throw new Error('Copy failed');
                                }}
                            }}

                            button.textContent = 'Copied!';

                            setTimeout(() => {{
                                button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-copy preview-icon"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>';
                            }}, 1000);

                        }} catch (error) {{
                            console.error('Copy failed:', error);
                            button.textContent = 'Copy failed';

                            setTimeout(() => {{
                                button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-copy preview-icon"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>';
                            }}, 1000);
                        }}
                    }});
                }});
            </script>
            """,
            str(obj.token),
            str(obj.token),
        )