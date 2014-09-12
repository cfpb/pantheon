from github.models import Repo
from django.db.models import Q
from github.actions import gen_repo_context
from django.conf import settings

def get_context(request, context):
    admin_repos = Q(owner=request.user) | Q(teams__permission='admin', teams__members=request.user)
    github_qs = Repo.objects.filter(is_enterprise=False).filter(admin_repos)
    github_repo_models = []
    for repo in github_qs:
        entry = {'model': repo}
        github_repo_models.append(entry)

    github_repos_ctx = gen_repo_context(request, context, settings.GH_REPO_ACTIONS, github_repo_models)

    enterprise_repo_models = []
    enterprise_qs = Repo.objects.filter(is_enterprise=True).filter(admin_repos)
    for repo in enterprise_qs:
        entry = {'model': repo}
        enterprise_repo_models.append(entry)

    enterprise_repos_ctx = gen_repo_context(request, context, settings.GHE_REPO_ACTIONS, enterprise_repo_models)
    out = {
        'template': 'github/tile.html',
        'name': 'github',
        'github': github_repos_ctx,
        'enterprise': enterprise_repos_ctx,
    }


    return out

def gh_repos(request, context):
    admin_repos = Q(owner=request.user) | Q(teams__permission='admin', teams__members=request.user)
    qs = Repo.objects.filter(is_enterprise=False).filter(admin_repos)
    repo_models = []
    for repo in qs:
        entry = {'model': repo}
        repo_models.append(entry)

    repos_ctx = gen_repo_context(request, context, settings.GH_REPO_ACTIONS, repo_models)

    out = {
        'template': 'github/tile.html',
        'name': 'gh_repos',
        'repos': repos_ctx,
        'title': 'GitHub Repos',
    }


    return out

def ghe_repos(request, context):
    admin_repos = Q(owner=request.user) | Q(teams__permission='admin', teams__members=request.user)
    repo_models = []
    qs = Repo.objects.filter(is_enterprise=True).filter(admin_repos)
    for repo in qs:
        entry = {'model': repo}
        repo_models.append(entry)

    repos_ctx = gen_repo_context(request, context, settings.GHE_REPO_ACTIONS, repo_models)
    out = {
        'template': 'github/tile.html',
        'name': 'ghe_repos',
        'repos': repos_ctx,
        'title': 'GitHub Enterprise Repos',
    }


    return out
