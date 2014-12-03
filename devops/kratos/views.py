from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from kratos import models
from github.models import Repo
import json

from django.contrib.auth import get_user_model
User = get_user_model()

def team_members(req, team_name, perm_name, user_id):
    if not req.user.is_admin(team_name=team_name):
        msg = '{} is not an admin for the {} team.'.format(req.user.username, team_name)
        return HttpResponseForbidden(json.dumps({'status': 'error', 'msg': msg}), content_type="application/json")

    team = get_object_or_404(models.Team, name=team_name)
    user = get_object_or_404(User, id=int(user_id), stub=False)

    if req.method == 'PUT':
        perm = models.Perm.objects.get(name=perm_name)
        models.UserPermTeam.objects.get_or_create(user=user, perm=perm, team=team)
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")        
    elif req.method == 'DELETE':
        try:
            upt = models.UserPermTeam.objects.get(user=user, perm__name=perm_name, team=team)
        except models.UserPermTeam.DoesNotExist:
            pass
        else:
            upt.delete()
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
    else:
        return HttpResponseNotAllowed(['DELETE', 'PUT'])



def teams(req):
    if not req.user.is_authenticated():
        return HttpResponseForbidden()
    out = {}
    teams = models.Team.objects.all()
    for team in teams:
        out[team.name] = {'name': team.name, 'permissions': {}, 'repos': {}}

    team_perms = models.UserPermTeam.objects.all()
    for team_perm in team_perms:
        team_name = team_perm.team.name
        perm_name = team_perm.perm.name
        user_name = team_perm.user.id
        out[team_name]['permissions'].setdefault(perm_name, []).append(user_name)

    repos = {}
    repo_perms = models.UserPermRepo.objects.all()
    for repo_perm in repo_perms:
        repo_name = repo_perm.repo.full_name.split('/')[1]
        perm_name = repo_perm.perm.name
        user_name = repo_perm.user.id
        repos.setdefault(repo_name, {'name': repo_name, 'id': repo_perm.repo.id, 'is_enterprise': repo_perm.repo.is_enterprise, 'permissions': {}})['permissions'].setdefault(perm_name, []).append(user_name)

    all_repos = models.RepoExtension.objects.all()
    for repo in all_repos:
        repo_name = repo.repo.full_name.split('/')[1]
        repo_data = repos.pop(repo_name, {'name': repo_name, 'id': repo.repo.id, 'is_enterprise': repo.repo.is_enterprise, 'permissions': {}})
        team_name = repo.team.name
        out[team_name]['repos'][repo_name] = repo_data

    for team, team_data in out.items():
        team_data['repos'] = team_data['repos'].values()

    out = {
        "permission": "admin",
        "groups": out.values(),
        "ungrouped": [{'name': repo.full_name.split('/')[1]} for repo in Repo.objects.filter(kratos_extension=None)],
        "user": req.user.id,
        "users": {user.id: {'username': user.username.split('_')[0], 'stub': user.stub} for user in User.objects.all()}
    }

    return HttpResponse(json.dumps(out), content_type="application/json")
