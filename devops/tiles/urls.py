from appring import apps
from django.apps import apps as djangoapps
from django.conf.urls import include, url
from tiles.views import filter_app_labels_with_tiles

def load_tile_urls(urlpatterns):
    """
    :param patterns urlpatterns: The django url patterns object

    add any urls.py for apps with tiles. namespaced to the app name.
    """
    all_app_labels = [app.label for app in djangoapps.get_app_configs()]
    app_labels = filter_app_labels_with_tiles(all_app_labels)
    for app_label in app_labels:
        app = getattr(apps, app_label)
        try:
            app.urls
        except AttributeError:
            continue
        app_name = djangoapps.get_app_config(app_label).name
        urlpatterns.append(url(app_label + '/', include( app_name + '.urls', namespace=app_label)))
