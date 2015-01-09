from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tiles.urls import load_namespaced_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'devdash.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'core.views.home', name='home'),
    url(r'^login$', 'core.views.login', name='login_start'),
    url(r'^login_continue$', 'core.views.login_continue', name='login_continue'),
    url(r'^logout', 'core.views.logout_view', name='logout'),
    url(r'^refresh', 'core.views.sync', name='sync'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)

load_namespaced_urls(urlpatterns, 'github', 'osw', 'jenkins', 'kratos')
