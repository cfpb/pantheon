from appring import apps
from django.apps import apps as djangoapps
from django.template import RequestContext

def get_apps_with_widgets(app_labels):
    """
    Return a list of app modules with widgets whose labels are in app_labels

    :param app_names: list of app labels
    :returns: list of app labels filtered to include only those with widgets
    """
    out = []
    for app_label in app_labels:
        app = getattr(apps, app_label)
        if _has_widgets(app):
            out.append(app_label)
    return out

def _has_widgets(app):
    """
    :param module app: the module to check for widgets
    : returns bool: true if has widgets
    """
    try:
        app.widgets.get_context
    except:
        return False
    return True

def gen_context(request, widgets=None, context=None):
    """
    :param request request: Djange request object
    :param iterator widgets: tuple of app labels for which to display widgets
    :param context context: context
    :returns str: returns rendered html

    If widgets is None, will look through all apps looking for widgets
    If context is None, will create a RequestContext
    """
    if widgets is None:
        widgets = [app.label for app in djangoapps.get_app_configs()]
        widgets = get_apps_with_widgets(widgets)

    if context is None:
        context = RequestContext(request)

    context['widgets'] = []

    for app_label in widgets:
        app = getattr(apps, app_label)
        widget_ctx = app.widgets.get_context(request, context)
        context['widgets'].append(widget_ctx)

    return context

