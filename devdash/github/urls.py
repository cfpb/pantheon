from django.conf.urls import patterns, url

urlpatterns = patterns('github.views',
    url(r'^enterprise_details', 'enterprise_details', name='enterprise_details'),
)
