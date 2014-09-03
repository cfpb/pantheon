from django.conf.urls import patterns, url

urlpatterns = patterns('osw.views',
    url(r'^start', 'start_new', name='start_new'),
    url(r'^release', 'release_existing', name='release_existing')
)
