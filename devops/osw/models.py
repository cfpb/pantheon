from django.db import models
import django_fsm as fsm
# Create your models here.
from django.conf import settings
User = settings.AUTH_USER_MODEL



class UserExtension(models.Model):
    CHOICES = (
        ('0', 'Link Public Github Account'),
        ('1', 'Add CFPB Email Address'),
        ('2', 'Pending Admin Approval'),
        ('3', ''),
        ('github account linked', ''),
    )

    user = models.OneToOneField(User, related_name='osw_extension')

