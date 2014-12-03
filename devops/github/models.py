from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from github.client import GitHubEnterprise, GitHub
from django.conf import settings

User = settings.AUTH_USER_MODEL

class RepoManager(models.Manager):
    def sync_user(self, user):
        if not user.is_authenticated():
            return
        dirty = False
        ghe = GitHubEnterprise(user)
        gh = GitHub(user)

        teams_data = ghe.user.teams.get().json()
        Team.objects.sync_teams(teams_data, ghe)

        repos_data = ghe.user.repos.get().json()
        self.sync_repos(repos_data, user)

        if gh:
            teams_data = gh.user.teams.get().json()
            teams_data = [td for td in teams_data if td['organization']['id'] in settings.GH_ORG_IDS]
            Team.objects.sync_teams(teams_data, gh)

    def sync_repos(self, repos_data, owner=None):
        repo_models = []
        for repo_data in repos_data:
            repo_models.append(self.sync_repo(repo_data, owner))
        return repo_models

    def sync_repo(self, repo_data, owner=None):
        is_enterprise = not repo_data['html_url'].startswith('https://github.com/')
        try:
            repo_model = self.get(gh_id=repo_data['id'], is_enterprise=is_enterprise, gh_updated_at=repo_data['updated_at'])
        except self.model.DoesNotExist:
            default_keys = ('full_name', 'description', 'fork', 'html_url',)
            defaults = {
                'gh_updated_at': repo_data['updated_at'],
                'owner': owner
            }
            defaults.update({k: v for k, v in repo_data.items() if k in default_keys})
            repo_model, created = self.update_or_create(gh_id=repo_data['id'], is_enterprise=is_enterprise, defaults=defaults)
        return repo_model

# Create your models here.
@python_2_unicode_compatible
class Repo(models.Model):
    gh_id = models.IntegerField()
    full_name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, blank=True, default="")
    fork = models.BooleanField(default=False)
    is_enterprise = models.BooleanField(default=True)
    html_url = models.URLField()
    gh_updated_at = models.DateTimeField()
    teams = models.ManyToManyField('Team', related_name='repos')
    owner = models.ForeignKey(User, blank=True, null=True, related_name='repos')
    objects = RepoManager()

    class Meta:
        ordering = ['fork']

    def __str__(self):
        return '<Repo: {} ({})>'.format(self.full_name, 'enterprise' if self.is_enterprise else 'public')

    def save(self, *args, **kwargs):
        if self.description is None:
            self.description = ''
        super(Repo, self).save(*args, **kwargs)

class Org(models.Model):
    gh_id = models.IntegerField()
    gh_updated_at = models.DateTimeField()
    name = models.CharField(max_length=100)


class TeamManager(models.Manager):
    def sync_teams(self, teams_data, client):
        out = []
        for team_data in teams_data:
            out.append(self.sync_team(team_data, client))
        return out

    def sync_team(self, team_data, client):
        gh_id = team_data['id']
        is_enterprise = not team_data['url'].startswith('https://api.github.com/')
        default_keys = ('url', 'permission', 'slug',)
        defaults = {k: v for k, v in team_data.items() if k in default_keys}

        team, created = self.update_or_create(gh_id=gh_id, is_enterprise=is_enterprise, defaults=defaults)

        #if this isn't an admin team, we don't care about repos or members
        if defaults['permission'] != 'admin':
            return team

        # Members and Repositories
        team_client = client.teams._(str(gh_id))

        members_data = team_client.members.get().json()
        member_gh_ids = [m['id'] for m in members_data]
        # get all members in the database
        fltr = {'ghe_id__in': member_gh_ids} if is_enterprise else {'gh_id__in': member_gh_ids}
        from django.contrib.auth import get_user_model
        User = get_user_model()
        member_models = User.objects.filter(**fltr)
        team.members = member_models
        repos_data = team_client.repos.get().json()
        repo_models = Repo.objects.sync_repos(repos_data)
        team.repos = repo_models
        return team


class Team(models.Model):
    gh_id = models.IntegerField()
    url = models.URLField()
    permission = models.CharField(max_length=6)
    slug = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='teams')
    is_enterprise = models.BooleanField(default=True)
#    org = models.ForeignKey('Org')

    objects = TeamManager()


