import dramatiq
import requests

from apps.api_logging.helpers import OutgoingRequest
from .models import OutgoingWebhookCall, WebhookForwardURL, WebhookPayload


@dramatiq.actor
def forward_payload(webhook_payload_id, forward_url_id):
    webhook_payload = WebhookPayload.objects.get(pk=webhook_payload_id)

    forward_url = WebhookForwardURL.objects.get(pk=forward_url_id)

    request = OutgoingRequest(forward_url.value, "POST", webhook_payload.http_payload)

    with OutgoingWebhookCall.context(request, "forward_payload") as log:

        kwargs = dict(
            headers=webhook_payload.http_headers,
        )

        if webhook_payload.http_query_params:
            kwargs["params"] = webhook_payload.http_query_params

        if webhook_payload.http_payload:
            kwargs["data"] = webhook_payload.http_payload

        request_method = getattr(requests, webhook_payload.http_method)

        response = request_method(forward_url.value, **kwargs)

        log.method = webhook_payload.http_method
        log.destination = webhook_payload.origin.slug
        log.result = response

        webhook_payload.outgoing_requests.add(log)
