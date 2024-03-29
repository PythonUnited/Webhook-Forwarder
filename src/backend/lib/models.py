from abc import ABC

from django.utils.translation import gettext_lazy as _


class Choices(ABC):
    """Usage:

    class Statuses(Choices):
        NEW = "new"
        IN_PROGRESS = "in_progress"
        READY = "ready"

    status = models.CharField(
        max_length=50,
        choices=Statuses.as_choices(),
        default=Statuses.NEW,
    )
    """

    @classmethod
    def as_list(cls):
        return [getattr(cls, state) for state in vars(cls).keys() if state[0].isupper()]

    @classmethod
    def as_choices(cls):
        return ((state, _(state.capitalize())) for state in cls.as_list())

