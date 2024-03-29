import json

from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer


def get_admin_link(obj, app_name, model_name):
    link = reverse(
        f"admin:{app_name}_{model_name}_change",
        args=[obj.pk],
    )
    return format_html(
        '<a style="text-decoration: underline" href="{}" target="_blank">{}</a>',
        link,
        obj,
    )


def prettify_json(json_data):
    pretty_json = json.dumps(json_data, sort_keys=True, indent=2)

    formatter = HtmlFormatter(style="default")

    pretty_json = highlight(pretty_json, JsonLexer(), formatter)

    style = "<style>" + formatter.get_style_defs() + "</style><br>"

    return mark_safe(style + pretty_json)
