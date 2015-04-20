from django.conf import settings
from universalclient import Client, jsonFilter
import requests
import json

kratos = Client(settings.KRATOS_URL, dataFilter=jsonFilter, auth=('admin', settings.KRATOS_ADMIN_PWD), headers={'Content-Type': 'application/json'})

def register_kratos(request, response, user, **kwargs):
    if not user or not user.gh_id:
        return
    social_auth = user.social_auth.get(provider='github').extra_data
    kratos_data = kratos.users.get(params={'gh': user.gh_id}).json()

    if kratos_data.get('error') == 'not_found':
        kratos_user = {
            "data": {
                "username": user.username,
                "contractor": user.contractor,
            },
            "roles": ["gh|user", "kratos|enabled"],
            "rsrcs": {
                "gh": {
                    "username": social_auth['username'],
                    "id": social_auth['id'],
                },
            },
        }
#        resp = requests.post(settings.KRATOS_URL '/users', data=json.dumps(kratos_user), auth=auth=('admin', settings.KRATOS_ADMIN_PWD))
        resp = kratos.users.post(data=kratos_user)
        kratos_id = resp.json()['name']
    else:
        kratos_id = kratos_data.get('name')
        
        if not kratos_id:
            return

        if user.contractor != kratos_data.get('data', {}).get('contractor') or \
           user.username != kratos_data.get('data', {}).get('username'):
            resp = kratos.users._(kratos_id).data.put(data={'contractor': user.contractor, 'username': user.username})
            print resp, resp.text

        if 'kratos|enabled' not in kratos_data.get('roles', []):
            resp = kratos.users._(kratos_id).put()
            print resp, resp.text

        if 'gh|user' not in kratos_data.get('roles', []):
            resp = kratos.users._(kratos_id).roles.gh.user.put()
            print resp, resp.text

    if kratos_id != user.kratos_id:
        user.kratos_id = kratos_id
        user.save()
