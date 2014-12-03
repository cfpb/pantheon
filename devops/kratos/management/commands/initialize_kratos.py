from django.core.management.base import BaseCommand
from django.conf import settings
from github import client
from github.models import Repo
from kratos import models
import random
import string

from django.contrib.auth import get_user_model
User = get_user_model()

class Command(BaseCommand):
    help = 'Initialize Kratos enforcement based on existing repos/teams in GH/GHE'

    def handle(self, *args, **kwargs):
        GH_ORGS = getattr(settings, 'KRATOS_ENFORCE_GH_ORGS', [])
#        GHE = getattr(settings, 'KRATOS_ENFORCE_GH_ORGS', False)

        gha = client.GitHubAdmin()
#        ghea = client.GitHubEnterpriseAdmin()

        print 'syncing github.com'
        for org_id in GH_ORGS:
            org_name = client.get_org_name(gha, org_id)
            print 'syncing {} org'.format(org_name)
            sync_gh_repos(gha, org_name)
            sync_gh_users(gha, org_name)
            sync_gh_teams(gha, org_name)
        print('done.')
    # TODO: implement GHE support

def sync_gh_repos(gha, org_name):
    print('syncing repos...')
    req = gha.orgs._(org_name).repos
    for repo_data in client.iter_get(req):
        Repo.objects.sync_repo(repo_data)

def generate_username(login_name):
    random_length = 30 - len(login_name) - 1
    filler = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random_length))
    return login_name + '_' + filler

def sync_gh_users(gha, org_name):
    print('syncing users...')
    req = gha.orgs._(org_name).members
    for user_data in client.iter_get(req):
        User.objects.get_or_create(gh_id=user_data['id'], defaults={'stub': True, 'username': generate_username(user_data['login'])})


def get_users_for_team(gha, team_id):
    req = gha.teams._(str(team_id)).members
    for user_data in client.iter_get(req):
        user = User.objects.get(gh_id=user_data['id'])
        yield user

def get_repos_for_team(gha, team_id):
    req = gha.teams._(str(team_id)).repos
    for repo_data in client.iter_get(req):
        print(repo_data['full_name'])
        repo = Repo.objects.get(full_name=repo_data['full_name'], is_enterprise=False)
        yield repo

def sync_gh_teams(gha, org_name):
    print('syncing teams...')
    req = gha.orgs._(org_name).teams
    for team_data in client.iter_get(req):
        full_name = team_data['name']
        if full_name == 'Owners' or team_data['id'] == getattr(settings, 'GH_WELCOME_TEAM', None):
            continue
        name, typ, perm_name = full_name.split()
        perm, created = models.Perm.objects.get_or_create(name=perm_name)
        if typ == 'team':
            team, created = models.Team.objects.get_or_create(name=name)
            for user in get_users_for_team(gha, team_data['id']):
                models.UserPermTeam.objects.get_or_create(user=user, perm=perm, team=team)
            for repo in get_repos_for_team(gha, team_data['id']):
                models.RepoExtension.objects.get_or_create(repo=repo, team=team)
        elif typ == 'repo':
            repo_full_name = '{}/{}'.format(org_name, name)
            repo = Repo.objects.get(full_name=repo_full_name, is_enterprise=False)
            for user in get_users_for_team(gha, team_data['id']):
                models.UserPermRepo.objects.get_or_create(user=user, perm=perm, repo=repo)





