from github.models import Repo

def sync(user=None):
    """
    We do not yet support batch sync.
    """
    if not user:
        return
    Repo.objects.sync_user(user)
