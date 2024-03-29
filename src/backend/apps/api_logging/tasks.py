from datetime import timedelta

import dramatiq
from django.conf import settings
from django.utils import timezone
from periodiq import cron

from apps.api_logging.models import IncomingAPICall, OutgoingAPICall


@dramatiq.actor(periodic=cron("0 1 * * *"))
def scrub_api_logs():
    now = timezone.now()
    from_date = now - timedelta(days=settings.DATA_SCRUB_DAYS)

    qry = dict(created__lte=from_date)
    IncomingAPICall.objects.filter(**qry).delete()
    OutgoingAPICall.objects.filter(**qry).delete()
