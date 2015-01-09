import core.sync

def sync(user, new_association, **kwargs):
    """
    A social auth pipeline function. new_association is true if a
    user has never logged in with this github credential before.
    Since it is a new credential, we will sync the user so that
    any repos associated with this credential are in the system.
    """
    if new_association:
        core.sync.sync(user)
