from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include, re_path
from ninja import NinjaAPI

from apps.webhook_forwarder.api_1_0.views import router as webhook_forwarder_1_0


admin.site.site_header = f"PU Webhook Forwarder [{settings.ENVIRONMENT.upper()}]"

api = NinjaAPI()
api.add_router("/forwarder/1.0", webhook_forwarder_1_0)

urlpatterns = [
    path("api/", api.urls),
    path("sentry-debug/", lambda _: 1 / 0),
    path("admin/", admin.site.urls),
]

urlpatterns += [
    # path("404/", page_not_found, {"exception": Exception()}),
    # path("500/", server_error),
    re_path(r"^healthcheck/", lambda r: HttpResponse()),
]

if settings.DEBUG:
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        urlpatterns += [
            re_path(r"^__debug__/", include(debug_toolbar.urls)),
        ]
