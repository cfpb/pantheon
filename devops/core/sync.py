from django.conf import settings
from appring import apps

def sync(user=None):
    """
    If a user is passed, then sync just records involved with that user.
    If user is None, then sync all records in DB.

    Calls app.sync.sync(user) for each app in settings.SYNC.
    """
    for app_name in settings.SYNC:
        app = getattr(apps, app_name)
        app.sync.sync(user)
