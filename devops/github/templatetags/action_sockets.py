from django import template
import datetime
from django.template.loader import get_template

register = template.Library()

@register.simple_tag(takes_context=True)
def repo_socket(context, namespace):
    widgets = context['widgets']
    widget_html = '<div class="widget_container">'
    for widget_ctx in widgets:
        context['widget'] = widget_ctx
        tmplt = get_template(widget_ctx['template'])
        rendered = tmplt.render(context)
        widget_html += '<div class="widget {}">{}</div>'.format(widget_ctx['name'], rendered)
    widget_html += '</div>'
    return widget_html
