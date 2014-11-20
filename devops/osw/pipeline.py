from social.pipeline.partial import partial
from django.shortcuts import redirect
from django.http import HttpResponse

@partial
def two_factor_audit(request, response, backend, details, user, **kwargs):
    if backend.name != 'github':
        return
    if not user:
        return HttpResponse('Unauthorized', status=401)
    github_details = request.session.get('github_details', {})
    if not github_details or (github_details['is_member'] and not github_details['2fa_enabled']):
        return redirect('osw:two_factor_audit')

@partial
def github_details(request, response, backend, details, **kwargs):
    if backend.name != 'github':
        return
    if 'github_details' in request.session:
        return redirect('osw:github_details')
