from osw import models

def join_org(request, context):
    out = {
        'template': 'osw/tile_join_org.html',
        'name': 'join_org',
    }
    try:
        models.UserExtension.objects.get(user=request.user)
    except:
        return out
    else:
        return {}
