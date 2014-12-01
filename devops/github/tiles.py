from __future__ import absolute_import
from github.models import Repo
from django.db.models import Q
from github.actions import gen_repo_context
from tiles.views import gen_context
from django.conf import settings

def gen_repos_context(request, context, actions, is_enterprise):
    admin_repos = Q(owner=request.user) | Q(teams__permission='admin', teams__members=request.user)
    qs = Repo.objects.filter(is_enterprise=is_enterprise).filter(admin_repos)
    repo_models = []
    for repo in qs:
        entry = {'model': repo}
        repo_models.append(entry)


    return gen_repo_context(request, context, actions, repo_models)

def gh_repos(request, context):
    out = {
        'template': 'github/tile.html',
        'name': 'gh_repos',
        'repos': gen_repos_context(request, context, settings.GH_REPO_ACTIONS, False),
        'title': 'GitHub Repos',
        'tiles': []
    }
    # import ipdb
    # ipdb.set_trace()
    out = gen_context(request, settings.GH_TILES, out, out['tiles'])
    return out

def ghe_repos(request, context):
    out = {
        'template': 'github/tile.html',
        'name': 'ghe_repos',
        'repos': gen_repos_context(request, context, settings.GHE_REPO_ACTIONS, True),
        'title': 'GitHub Enterprise Repos',
        'tiles': []
    }
    out = gen_context(request, settings.GHE_TILES, out, out['tiles'])
    return out
