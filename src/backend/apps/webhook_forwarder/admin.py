import json

from django.contrib import admin
from django.utils.html import format_html

from lib.utils import get_admin_link, prettify_json
from .models import WebhookIdentifier, WebhookForwardURL, WebhookPayload
from .tasks import forward_payload

class InlineWebhookForwardURL(admin.TabularInline):
    model = WebhookForwardURL


@admin.register(WebhookIdentifier)
class WebhookIdentifierAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "modified",
    ]
    readonly_fields = [
        "slug",
        "created",
        "modified",
    ]

    inlines = [
        InlineWebhookForwardURL,
    ]


@admin.register(WebhookForwardURL)
class WebhookForwardURLAdmin(admin.ModelAdmin):
    list_display = [
        "value",
        "origin",
    ]
    readonly_fields = [
        "created",
        "modified",
    ]
    list_filter = [
        "origin",
    ]


@admin.register(WebhookPayload)
class WebhookPayloadLAdmin(admin.ModelAdmin):
    search_fields = [
        "uuid",
        "origin__slug",
    ]
    list_display = [
        "uuid",
        "created",
        "origin",
        "http_method",
    ]
    list_filter = [
        "origin",
    ]
    readonly_fields = [
        "uuid",
        "created",
        "modified",
        "get_outgoing_requests",
        "get_http_headers",
        "get_http_query_params",
        "get_http_payload",
    ]
    exclude = ["outgoing_requests"]
    actions = ["resend_payload"]

    @staticmethod
    @admin.display(
        description="Outgoing requests",
    )
    def get_outgoing_requests(obj):
        links = []

        for request in obj.outgoing_requests.all():
            links.append(get_admin_link(request, "api_logging", "outgoingapicall"))

        return format_html("<br>".join(links))

    @staticmethod
    @admin.display(
        description="HTTP headers",
    )
    def get_http_headers(obj):
        return prettify_json(obj.http_headers)

    @staticmethod
    @admin.display(
        description="HTTP query params",
    )
    def get_http_query_params(obj):
        return prettify_json(obj.http_query_params)

    @staticmethod
    @admin.display(
        description="HTTP JSON payload",
    )
    def get_http_payload(obj):
        try:
            payload = json.loads(obj.http_payload)
        except json.decoder.JSONDecodeError:
            return None

        return prettify_json(payload)

    @staticmethod
    @admin.action(description="Resend payload")
    def resend_payload(self, request, queryset):
        for obj in queryset:

            for forward_url in obj.origin.forward_urls.active():
                forward_payload.send(obj.id, forward_url.id)