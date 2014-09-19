from django.conf.urls import include, url
from django.apps import apps as djangoapps

def load_namespaced_urls(urlpatterns, *app_labels):
    """
    :param patterns urlpatterns: The django url patterns object

    add any urls.py for apps with tiles. namespaced to the app name.
    """
    for app_label in app_labels:
        app_name = djangoapps.get_app_config(app_label).name
        urlpatterns.append(url(app_label + '/', include( app_name + '.urls', namespace=app_label)))
