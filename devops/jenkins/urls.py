from django.conf.urls import patterns, url

urlpatterns = patterns('jenkins.views',
    url(r'^initialize', 'initialize_ci', name='initialize_ci'),
)
