from django.db import models
import django_fsm as fsm
# Create your models here.
from django.conf import settings
User = settings.AUTH_USER_MODEL


def can_approve():
    """
    Whether the user can approve a member for the org.
    """
    return True

class UserExtension(models.Model):
    CHOICES = (
        ('0', 'Link Public Github Account'),
        ('1', 'Add CFPB Email Address'),
        ('2', 'Pending Admin Approval'),
        ('3', ''),
        ('github account linked', ''),
    )

    user = models.OneToOneField(User, related_name='osw_extension')
    state = fsm.FSMField(default='pending', protected=True)
    publicize_membership = models.BooleanField(default=False)

    @fsm.transition(
        field=state,
        source='pending',
        target='approved',
    )
    def existing_approval(self):
        pass

    @fsm.transition(
        field=state,
        source='pending',
        target='approved',
        conditions=[can_approve],
    )
    def approve(self):
        pass
