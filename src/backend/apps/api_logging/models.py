import datetime
import json
import logging
from contextlib import contextmanager
from json import JSONDecodeError

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class RequestData:
    def __init__(self, request):
        if hasattr(request, "url"):
            self.url = request.url
        else:
            self.url = request.path

        self.method = request.method
        try:
            try:
                self.body = json.dumps(json.loads(request.body), indent=2)
            except:
                self.body = json.dumps(getattr(request, request.method), indent=2)
        except AttributeError:
            try:
                self.body = json.dumps(request.body, indent=2)
            except:
                self.body = request.body


class BaseAPICall(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False)

    source = models.CharField(max_length=64, db_index=True)
    destination = models.CharField(max_length=64, db_index=True)
    call_type = models.CharField(max_length=64, db_index=True, null=True, default=None)

    url = models.CharField(max_length=1024)
    method = models.CharField(max_length=16, default="GET")
    body = models.TextField(default="")
    error = models.TextField(default="")

    status_code = models.PositiveIntegerField(null=True, db_index=True)

    request_duration = models.DecimalField(max_digits=6, decimal_places=3)

    response = models.TextField(default="")

    def __str__(self):
        return "[{}] {}.{}".format(
            self.created.strftime("%d-%m-%Y %H:%M:%S"), self.destination, self.call_type
        )

    def __init__(self, *args, **kwargs):
        self._started = datetime.datetime.now()
        self._result = None

        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        elapsed = datetime.datetime.now() - self._started

        # Reduce elapsed precision from microseconds to milliseconds before saving
        self.request_duration = int(elapsed.total_seconds() * 1000) / 1000.0

        return super().save(*args, **kwargs)

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = result

    @classmethod
    @contextmanager
    def context(cls, request, call_type, save_changes=True):
        log = cls(
            call_type=call_type,
            **vars(RequestData(request)),
        )

        if save_changes is True:
            log.save()

        try:
            yield log
        except Exception as exc:
            logger.error(exc, exc_info=True)

            try:
                log.error = str(exc)
                log.status_code = getattr(exc, "status_code", 500)

                if log.result is not None:
                    log.status_code = log.result.status_code
                    log.response = log.result.content

                log.save()
            except Exception as e:
                logger.exception(e)
                pass  # Don't fail on inability to save log instance

            # Raise original exception
            raise exc
        else:
            if log.result is not None:
                log.status_code = log.result.status_code
                try:
                    log.response = json.dumps(log.result.json(), indent=2)
                except JSONDecodeError:
                    log.response = log.result.content

            if save_changes is True:
                log.save()


class IncomingAPICall(BaseAPICall):
    def save(self, *args, **kwargs):
        if not self.destination:
            self.destination = settings.API_LOCAL_NAME

        super().save(*args, **kwargs)


class OutgoingAPICall(BaseAPICall):
    def save(self, *args, **kwargs):
        if not self.source:
            self.source = settings.API_LOCAL_NAME

        super().save(*args, **kwargs)
