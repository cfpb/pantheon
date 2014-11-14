from osw import models

def join_org(request, context):
    out = {
        'template': 'osw/tile_join_org.html',
        'name': 'join_org',
    }
    try:
        ue = models.UserExtension.objects.get(user=request.user)
    except:
        return out

    if ue.state == 'approved':
        return {}
    else:
        out['state'] = ue.state
        return out
