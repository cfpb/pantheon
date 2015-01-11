from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib.auth.models import AbstractUser


@python_2_unicode_compatible
class User(AbstractUser):
    gh_id = models.IntegerField(blank=True, null=True)
    ghe_id = models.IntegerField(blank=True, null=True)
    kratos_id = models.CharField(max_length=32, blank=True, null=True)
    stub = models.BooleanField(default=False)
    contractor = models.BooleanField(default=True)

    def is_authenticated(self):
        """
        whether the user is authenticated AND has linked their
        github enterprise account
        """
        if not super(User, self).is_authenticated():
            return False
        try:
            self.social_auth.get(provider='github-enterprise')
        except:
            return False
        return True

    def is_gh_linked(self):
        """
        whether the user has linked github.com account
        """
        try:
            self.social_auth.get(provider='github')
        except:
            return False
        return True

    def __str__(self):
        return '<User: {}>'.format(self.username)
