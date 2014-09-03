from osw.forms import ReleaseForm, StartForm
from github.client import GitHubEnterprise

def get_context(request, context):
    return {}
    ghe = GitHubEnterprise(request.user)
    user_repos = [repo['full_name'] for repo in ghe.user.repos.get().json()]
    user_orgs = [org['login'] for org in ghe.user.orgs.get().json()]
    org_repos = [ghe.orgs._(org).repos.get().json() for org in user_orgs]
    repos = user_repos + [repo['full_name'] for org in org_repos for repo in org]
    choices = [(repo, repo,) for repo in repos]
    release_form = ReleaseForm()
    release_form.fields['repo'].choices = choices
    return {
        'template': 'osw/widget.html',
        'name': 'osw',
        'start_form': StartForm(),
        'release_form':release_form,
    }
