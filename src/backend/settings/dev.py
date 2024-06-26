from .base import *

ENVIRONMENT = "development"
DEBUG = True

USE_X_FORWARDED_HOST = True
# INTERNAL_IPS = ('127.0.0.1',)

# SECURITY WARNING: keep the secret key used in production secret!
INSTALLED_APPS += [
    "debug_toolbar",
    "django_pdb",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # 'django_pdb.middleware.PdbMiddleware',
]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    # Profifing:
    # 'debug_toolbar.panels.timer.TimerDebugPanel',
    # 'debug_toolbar.panels.profiling.ProfilingDebugPanel',
]


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *
except ImportError:
    pass
