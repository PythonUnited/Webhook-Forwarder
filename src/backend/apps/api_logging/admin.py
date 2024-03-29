import json

from django.contrib import admin

# from lib.utils import prettify_json
from . import models


class APICallAdmin(admin.ModelAdmin):
    list_display = [
        "created",
        "source",
        "destination",
        "call_type",
        "status_code",
        "request_duration",
    ]

    list_filter = [
        "source",
        "destination",
        "call_type",
        "status_code",
        "method",
        "created",
    ]
    search_fields = ["url", "body", "response"]
    exclude = ["body", "response"]

    readonly_fields = [
        "source",
        "destination",
        "call_type",
        "url",
        "method",
        "status_code",
        "request_duration",
        "get_body",
        "get_response",
        "error",
    ]

    @staticmethod
    def get_body(instance):
        # try:
        #     return prettify_json(json.loads(instance.body))
        # except json.JSONDecodeError:
        return instance.body

    @staticmethod
    def get_response(instance):
        # try:
        #     return prettify_json(json.loads(instance.response))
        # except json.JSONDecodeError:
        return instance.response


admin.site.register(models.IncomingAPICall, APICallAdmin)
admin.site.register(models.OutgoingAPICall, APICallAdmin)
