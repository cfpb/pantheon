from social.pipeline.partial import partial
from django.shortcuts import redirect
from django.http import HttpResponse

@partial
def two_factor_audit(request, response, backend, details, user, **kwargs):
    if backend.name != 'github':
        return
    if not user:
        return HttpResponse('Unauthorized', status=401)

    if not request.session.get('github_details', {}).get('2fa_enabled'):
        return redirect('osw:two_factor_audit')


@partial
def github_details(request, response, backend, details, **kwargs):
    if backend.name != 'github':
        return
    if 'github_details' in request.session:
        return redirect('osw:github_details')
