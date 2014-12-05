from django.conf.urls import patterns, url

urlpatterns = patterns('osw.views',
    url(r'^start', 'start_new', name='start_new'),
    url(r'^release', 'release_existing', name='release_existing'),
    url(r'^gh_details', 'gh_details', name='gh_details'),
    url(r'^join_org', 'join_org', name='join_org'),
    url(r'^enable_2fa', 'enable_2fa', name='enable_2fa'),
)
