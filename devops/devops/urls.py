from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tiles.urls import load_tile_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'devops.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'core.views.home', name='home'),
    url(r'^logout', 'core.views.logout_view', name='logout'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)

load_tile_urls(urlpatterns)