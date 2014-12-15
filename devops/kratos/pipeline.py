from django.conf import settings
from universalclient import Client

kratos = Client(settings.KRATOS_URL)

def register_kratos(request, response, user, **kwargs):
    if not user or not user.gh_id:
        return
    kratos_id = kratos.users.get(params={'gh': user.gh_id}).json().get('name')
    if kratos_id and kratos_id != user.kratos_id:
        user.kratos_id = kratos_id
        user.save()
