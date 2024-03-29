from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = "apps.webhook_forwarder"
    label = "webhook_forwarder"
    verbose_name = _("Webhook forwarder")
