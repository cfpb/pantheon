from django.conf.urls import patterns, url

urlpatterns = patterns('osw.views',
    url(r'^start', 'start_new', name='start_new'),
    url(r'^release', 'release_existing', name='release_existing'),
    url(r'^github_details', 'github_details', name='github_details'),
    url(r'^two_factor_audit', 'two_factor_audit', name='two_factor_audit')
)
