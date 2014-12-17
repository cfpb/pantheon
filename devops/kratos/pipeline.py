from django.conf import settings
from universalclient import Client

kratos = Client(settings.KRATOS_URL).auth(('admin', settings.KRATOS_ADMIN_PWD))

def register_kratos(request, response, user, **kwargs):
    if not user or not user.gh_id:
        return
    kratos_data = kratos.users.get(params={'gh': user.gh_id}).json()
    
    if kratos_data.get('error') == 'not_found':
        # TODO: create new user
        pass
    else:
        kratos_id = kratos_data.get('name')
    
        if kratos_id and kratos_id != user.kratos_id:
            user.kratos_id = kratos_id
            user.save()

        if kratos_id and 'gh|user' not in kratos_data.get('roles', []):
            kratos.users._(kratos_id).roles.gh.user.put()
