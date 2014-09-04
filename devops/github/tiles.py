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

    github_repos_ctx = gen_repo_context(request, context, settings.GITHUB_REPO_ACTIONS, github_repo_models)

    enterprise_repo_models = []
    enterprise_qs = Repo.objects.filter(is_enterprise=True).filter(admin_repos)
    for repo in enterprise_qs:
        entry = {'model': repo}
        enterprise_repo_models.append(entry)

    enterprise_repos_ctx = gen_repo_context(request, context, settings.GITHUB_ENTERPRISE_REPO_ACTIONS, enterprise_repo_models)
    out = {
        'template': 'github/tile.html',
        'name': 'github',
        'github': github_repos_ctx,
        'enterprise': enterprise_repos_ctx,
    }


    return out
