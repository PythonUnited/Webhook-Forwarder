from .core import *

from environ import environ

SOURCE_DIR = environ.Path(__file__) - 2
BASE_DIR = environ.Path(__file__) - 3
ROOT_DIR = environ.Path(__file__) - 4

env = environ.Env()
try:
    env.read_env(ROOT_DIR.file(".env"))
except FileNotFoundError:
    pass


SECRET_KEY = env.str("SECRET_KEY", None)
DEBUG = env.bool("DJANGO_DEBUG", False)
ENVIRONMENT = env.str("ENVIRONMENT", None)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "[::1]"])

# -- Installed apps ------------------------------------------------------------
_EXTERNAL_APPS = [
    "django_extensions",
    "django_dramatiq",
    "django_periodiq",
]

_PROJECT_APPS = [
    "apps.api_logging",
    "apps.webhook_forwarder",
]

INSTALLED_APPS += _EXTERNAL_APPS + _PROJECT_APPS

# -- Database ------------------------------------------------------------------
DATABASES = {"default": env.db("DATABASE_URL", "sqlite:///sqlite.db")}

# -- Internationalization ------------------------------------------------------
LANGUAGE_CODE = "nl"
TIME_ZONE = "Europe/Amsterdam"
USE_I18N = True
USE_TZ = True
USE_L10N = True

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    # SOURCE_DIR("static"),
]

MEDIA_ROOT = env.str("MEDIA_ROOT", BASE_DIR("mediafiles"))
MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR("staticfiles")
STATIC_URL = "/static/"

# -- Dramatiq message queue --------------------------------------------------------------------------------------------
DRAMATIQ_BROKER_URL = env("DRAMATIQ_BROKER_URL", default="amqp://localhost:5672")
DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "OPTIONS": {
        "url": DRAMATIQ_BROKER_URL,
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
        "django_dramatiq.middleware.AdminMiddleware",
        "periodiq.PeriodiqMiddleware",
    ],
}


# Defines which database should be used to persist Task objects when the
# AdminMiddleware is enabled.  The default value is "default".
DRAMATIQ_TASKS_DATABASE = "default"


# -- Logging ----------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

API_LOCAL_NAME = "webhook_forwarder"
