from appring import apps
from django.apps import apps as djangoapps
from django.template import RequestContext

def filter_app_labels_with_tiles(app_labels):
    """
    Given a list of app labels, return a list of those app labels whose apps
    contain tiles.

    :param app_names: list of app labels
    :returns: list of app labels filtered to include only those with tiles
    """
    out = []
    for app_label in app_labels:
        app = getattr(apps, app_label)
        if _has_tiles(app):
            out.append(app_label)
    return out

def _has_tiles(app):
    """
    :param module app: the module to check for tiles
    : returns bool: true if has tiles
    """
    try:
        app.tiles
    except:
        return False
    return True

def gen_context(request, tile_names, context, tile_contexts):
    """
    :param request request: Djange request object
    :param iterator tile_names: tuple of "app.function" tile name
    :param context context: context
    :param iterator tile_contexts: pointer into context to a list
        where tile contexts will be inserted
    :returns str: returns rendered html
    """
    for tile_name in tile_names:
        app_label, tile_label = tile_name.split('.')
        app = getattr(apps, app_label)
        tile = getattr(app.tiles, tile_label)
        tile_contexts.append(tile(request, context))

    return context

