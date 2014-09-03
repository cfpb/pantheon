from github.models import Repo
from django.db.models import Q
from github.actions import gen_repo_context
from django.conf import settings

def get_context(request, context):
    admin_repos = Q(owner=request.user) | Q(teams__permission='admin', teams__members=request.user)
    github_qs = Repo.objects.filter(enterprise=False).filter(admin_repos)
    github = []
    for repo in github_qs:
        entry = {'model': repo}
        github.append(entry)

    github = gen_repo_context(request, context, settings.GITHUB_REPO_ACTIONS, github)

    enterprise = []
    enterprise_qs = Repo.objects.filter(enterprise=True).filter(admin_repos)
    for repo in enterprise_qs:
        entry = {'model': repo}
        enterprise.append(entry)

    enterprise = gen_repo_context(request, context, settings.GITHUB_ENTERPRISE_REPO_ACTIONS, enterprise)

    out = {
        'template': 'github/widget.html',
        'name': 'github',
        'github': github,
        'enterprise': enterprise,
    }


    return out
