from django.conf.urls import patterns, url

urlpatterns = patterns('github.views',
    url(r'^refresh', 'refresh', name='refresh'),
)
