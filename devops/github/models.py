from django.db import models
from core.models import User
from github.client import GitHubEnterprise, GitHub
from django.conf import settings


class RepoManager(models.Manager):
    def sync_user(self, user):
        if not user.is_authenticated():
            return
        dirty = False
        ghe = GitHubEnterprise(user)
        gh = GitHub(user)
        if not user.ghe_id:
            user_data = ghe.user.get().json()
            user.ghe_id = user_data['id']
            dirty = True
        if gh and not user.gh_id:
            user_data = gh.user.get().json()
            user.gh_id = user_data['id']
            dirty = True
        if dirty:
            user.save()

        teams_data = ghe.user.teams.get().json()
        Team.objects.sync_teams(teams_data, ghe)

        repos_data = ghe.user.repos.get().json()
        self.sync_repos(repos_data, user)

        if gh:
            teams_data = gh.user.teams.get().json()
            teams_data = [td for td in teams_data if td['organization']['id'] in settings.GITHUB_ORG_IDS]
            Team.objects.sync_teams(teams_data, gh)

    def sync_repos(self, repos_data, owner=None):
        out = []
        for repo_data in repos_data:
            out.append(self.sync_repo(repo_data, owner))
        return out

    def sync_repo(self, repo_data, owner=None):
        try:
            repo = self.get(html_url=repo_data['html_url'], gh_updated_at=repo_data['updated_at'])
        except self.model.DoesNotExist:
            default_keys = ('full_name', 'description', 'fork', 'html_url',)
            defaults = {k: v for k, v in repo_data.items() if k in default_keys}
            defaults['gh_updated_at'] = repo_data['updated_at']
            defaults['enterprise'] = not repo_data['html_url'].startswith('https://github.com/')
            defaults['owner'] = owner
            repo, created = self.update_or_create(html_url=repo_data['html_url'], defaults=defaults)
        return repo

# Create your models here.
class Repo(models.Model):
    full_name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, blank=True, default="")
    fork = models.BooleanField()
    enterprise = models.BooleanField(default=True)
    html_url = models.URLField()
    gh_updated_at = models.DateTimeField()
    teams = models.ManyToManyField('Team', related_name='repos')
    owner = models.ForeignKey('core.User', blank=True, null=True)

    objects = RepoManager()

    class Meta:
        ordering = ['fork']


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
        default_keys = ('url', 'permission', 'slug',)
        defaults = {k: v for k, v in team_data.items() if k in default_keys}
        defaults['gh_id'] = team_data['id']
        defaults['enterprise'] = not team_data['url'].startswith('https://api.github.com/')

        team, created = self.update_or_create(url=team_data['url'], defaults=defaults)

        #if this isn't an admin team, we don't care about repos or members
        if defaults['permission'] != 'admin':
            return team
        # Members and Repositories
        team_client = client.teams._(str(defaults['gh_id']))

        members_data = team_client.members.get().json()
        member_gh_ids = [m['id'] for m in members_data]
        # get all members in the database
        fltr = {'ghe_id__in': member_gh_ids} if defaults['enterprise'] else {'gh_id__in': member_gh_ids}
        members = User.objects.filter(**fltr)
        team.members = members
        repos_data = team_client.repos.get().json()
        repos = Repo.objects.sync_repos(repos_data)
        team.repos = repos
        return team


class Team(models.Model):
    gh_id = models.IntegerField()
    url = models.URLField()
    permission = models.CharField(max_length=6)
    slug = models.CharField(max_length=100)
    members = models.ManyToManyField('core.User', related_name='teams')
    enterprise = models.BooleanField(default=True)
#    org = models.ForeignKey('Org')

    objects = TeamManager()
