from django.shortcuts import render
from kratos import models
from github.models import Repo
import json

def teams(req=None):
    out = {}
    teams = models.Team.objects.all()
    for team in teams:
        out[team.name] = {'name': team.name, 'permissions': {}, 'repos': {}}

    team_perms = models.UserPermTeam.objects.all()
    for team_perm in team_perms:
        team_name = team_perm.team.name
        perm_name = team_perm.perm.name
        user_name = team_perm.user.username.split('_')[0]
        out[team_name]['permissions'].setdefault(perm_name, []).append(user_name)

    repos = {}
    repo_perms = models.UserPermRepo.objects.all()
    for repo_perm in repo_perms:
        repo_name = repo_perm.repo.full_name.split('/')[1]
        perm_name = repo_perm.perm.name
        user_name = repo_perm.user.username.split('_')[0]
        repos.setdefault(repo_perm, {'name': repo_name, 'permissions': {}})['permissions'].setdefault(perm_name, []).append(user_name)


    all_repos = models.RepoExtension.objects.all()
    for repo in all_repos:
        repo_name = repo.repo.full_name.split('/')[1]
        repo_data = repos.pop(repo_name, {'name': repo_name, 'permissions': {}})
        team_name = repo.team.name
        out[team_name]['repos'][repo_name] = repo_data

    with open('repo-groups.json', 'w') as f:
        json.dump(out, f)

