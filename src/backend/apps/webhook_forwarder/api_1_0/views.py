from django.http import HttpRequest
from ninja import Router, Schema, Field
from ninja.errors import HttpError

from .utils import get_webhook_identifier
from ..models import IncomingWebhookCall, WebhookForwardURL, WebhookPayload
from ..tasks import forward_payload

router = Router()


@router.get("/webhooks/{webhook_slug}")
@router.post("/webhooks/{webhook_slug}")
def queue_payload_to_forward(
    request: HttpRequest,
    webhook_slug: str,
):
    with IncomingWebhookCall.context(request, "queue_payload_to_forward") as log:
        webhook_identifier = get_webhook_identifier(webhook_slug)

        http_method = request.method.lower()

        try:
            http_payload = request.body.decode("utf-8")
        except UnicodeDecodeError:
            http_payload = request.body

        webhook_payload = WebhookPayload.objects.create(
            origin=webhook_identifier,
            http_method=http_method,
            http_headers=dict(request.headers),
            http_query_params=dict(request.GET),
            http_payload=http_payload,
        )

        forward_urls = webhook_identifier.forward_urls.active()

        if not forward_urls:
            raise HttpError(404, "No URLs found to forward payload to")

        for forward_url in forward_urls:
            forward_payload.send(webhook_payload.id, forward_url.id)

        response = dict(
            uuid=webhook_payload.uuid,
            message="Queued tasks to forward webhook payload upstream",
            urls=list(forward_urls.values_list("value", flat=True)),
        )
        log.destination = webhook_identifier.slug
        log.response = response
        log.status_code = 200
        log.method = http_method
        log.save()

    return response


# @router.get("/webhooks/{uuid}")
# def check_ticket_status(request: HttpRequest, uuid: str):
#     if not is_valid_uuid(uuid):
#         raise HttpError(400, "Webhook identifier is not an UUID4 value")
#
#     nerds_ticket = NerdsTicket.objects.get(uuid=uuid)
#
#     response = dict(
#         created=nerds_ticket.created,
#         modified=nerds_ticket.modified,
#         status=dict(
#             support_request=nerds_ticket.status,
#         ),
#     )
#     if nerds_ticket.hubspot_ticket:
#         response["status"]["hubspot"] = nerds_ticket.hubspot_ticket.status
#
#     return response
