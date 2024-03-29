_INTERNAL_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django_dramatiq",
    "django_periodiq",
]

_EXTERNAL_APPS = []

_PROJECT_APPS = [
    "apps.example",
]

INSTALLED_APPS = _INTERNAL_APPS + _EXTERNAL_APPS + _PROJECT_APPS
