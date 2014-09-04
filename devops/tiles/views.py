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
        app.tiles.get_context
    except:
        return False
    return True

def gen_context(request, app_labels=None, context=None):
    """
    :param request request: Djange request object
    :param iterator app_labels: tuple of app labels for which to display tiles
    :param context context: context
    :returns str: returns rendered html

    If app_labels is None, will look through all apps looking for tiles
    If context is None, will create a RequestContext
    """
    if app_labels is None:
        app_labels = [app.label for app in djangoapps.get_app_configs()]

    app_labels = filter_app_labels_with_tiles(app_labels)

    if context is None:
        context = RequestContext(request)

    context['tiles'] = []

    for app_label in app_labels:
        app = getattr(apps, app_label)
        tile_ctx = app.tiles.get_context(request, context)
        context['tiles'].append(tile_ctx)

    return context

