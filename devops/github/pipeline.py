from github.models import Repo

def sync(user, new_association, **kwargs):
    if new_association:
        Repo.objects.sync_user(user)