from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OnboardingConfig(AppConfig):
    name = "apps.api_logging"
    verbose_name = _("API logging")

    def ready(self):
        pass
