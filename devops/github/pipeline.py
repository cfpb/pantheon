from social.pipeline.partial import partial
from django.shortcuts import redirect
from github.client import GitHubEnterprise

@partial
def enterprise_details(request, response, backend, details, is_new, **kwargs):
    if backend.name != 'github-enterprise':
        return
    if not is_new:
        return
    enterprise_details = request.session.pop('enterprise_details', None)
    if enterprise_details is None:
        return redirect('github:enterprise_details')
    details.update(enterprise_details)
    ghe = GitHubEnterprise(access_token=response['access_token'])
    updated_user_data = {
        'name': details['fullname'],
        'email': details['email'],
        'location': details['location'],
    }
    ghe.user.patch(data=updated_user_data)
