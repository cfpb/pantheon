from social.pipeline.partial import partial
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from github.client import GitHubAdmin, get_org_name, is_org_member, is_2fa_enabled

gha = GitHubAdmin()

@partial
def join_org(request, backend, user, details, **kwargs):
    if backend.name != 'github':
        return
    if not user:
        return HttpResponse('Unauthorized', status=401)

    gh_details = request.session.get('gh_details', {})

    if not gh_details.get('org_name'):
        gh_details['org_name'] = get_org_name(gha, settings.GH_ORG_IDS[0])
        request.session['gh_details'] = gh_details

    if not gh_details.get('is_member'):
        gh_details['is_member'] = is_org_member(gha, details['username'], gh_details['org_name'])
        request.session['gh_details'] = gh_details

    if gh_details['is_member']:
        return None
    else:
        return redirect('osw:join_org')

@partial
def enable_2fa(request, backend, user, details, **kwargs):
    if backend.name != 'github':
        return
    if not user:
        return HttpResponse('Unauthorized', status=401)

    gh_details = request.session['gh_details']

    if not gh_details.get('is_2fa_enabled'):
        gh_details['is_2fa_enabled'] = is_2fa_enabled(gha, details['username'], gh_details['org_name'])
        request.session['gh_details'] = gh_details

    if gh_details['is_2fa_enabled']:
        gh_details['is_public_member'] = is_org_member(gha, details['username'], gh_details['org_name'], public=True)
        request.session['gh_details'] = gh_details
        return None
    else:
        return redirect('osw:enable_2fa')

@partial
def github_details(request, backend, user, details, **kwargs):
    if backend.name != 'github':
        return
    if not user:
        return HttpResponse('Unauthorized', status=401)

    gh_details = request.session.get('gh_details', {})

    if gh_details:
        return redirect('osw:gh_details')
    else:
        return None
