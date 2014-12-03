from django.conf.urls import patterns, url

urlpatterns = patterns('kratos.views',
    url(r'^teams/(?P<team_name>\w+)/members/(?P<perm_name>read|write)/(?P<user_id>\d+)/$', 'team_members', name="team-members"),
    url(r'^teams/$', 'teams', name='teams'),
)
