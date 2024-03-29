import uuid

from django.db import models
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel,
)

from apps.api_logging.models import IncomingAPICall, OutgoingAPICall
from lib.models import SingletonModel, Choices


class OutgoingWebhookCall(OutgoingAPICall):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        # kwargs["destination"] = kwargs.get("destination", "forwarded_location")

        super().__init__(*args, **kwargs)


class IncomingWebhookCall(IncomingAPICall):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        kwargs["source"] = kwargs.get("source", "webhook_forwarder_api")
        super().__init__(*args, **kwargs)


class WebhookIdentifier(TimeStampedModel, TitleSlugDescriptionModel):
    def __str__(self):
        return self.slug


class WebhookForwardURL(ActivatorModel, TimeStampedModel):
    origin = models.ForeignKey(
        WebhookIdentifier,
        on_delete=models.CASCADE,
        related_name="forward_urls",
    )
    value = models.URLField("URL")

    def __str__(self):
        return self.value


class WebhookPayload(TimeStampedModel):

    class HttpMethods(Choices):
        GET = "get"
        POST = "post"

    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    origin = models.ForeignKey(
        WebhookIdentifier,
        on_delete=models.CASCADE,
        related_name="payloads",
    )
    http_method = models.CharField(
        choices=HttpMethods.as_choices(),
        default=HttpMethods.GET,
    )
    http_headers = models.JSONField(default=dict)
    http_query_params = models.JSONField(default=dict)
    http_payload = models.TextField(null=True, blank=True)

    outgoing_requests = models.ManyToManyField(OutgoingWebhookCall)

    def __str__(self):
        return str(self.uuid)
