from django import template
from django.template.loader import get_template

register = template.Library()

@register.simple_tag(takes_context=True)
def tile_container(context, tiles=None):
    tiles = tiles if tiles is not None else context['tiles']
    tile_html = '<div class="tile_container">'
    for tile_ctx in tiles:
        if not tile_ctx:
            continue
        context['tile'] = tile_ctx
        tmplt = get_template(tile_ctx['template'])
        rendered = tmplt.render(context)
        tile_html += '<div class="tile {}">{}</div>'.format(tile_ctx['name'], rendered)
    tile_html += '</div>'
    return tile_html
