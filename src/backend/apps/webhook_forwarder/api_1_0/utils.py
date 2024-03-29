import uuid

from ninja.errors import HttpError

from apps.webhook_forwarder.models import WebhookIdentifier


def get_webhook_identifier(webhook_slug):
    try:
        return WebhookIdentifier.objects.get(slug=webhook_slug)
    except WebhookIdentifier.DoesNotExist:
        raise HttpError(401, "Unknown webhook slug")
