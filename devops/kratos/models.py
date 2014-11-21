from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from django.conf import settings
UserModel = settings.AUTH_USER_MODEL


class User(AbstractUser):
    gh_id = models.IntegerField(blank=True, null=True)
    ghe_id = models.IntegerField(blank=True, null=True)

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

def remove_stubs(sender, instance, **kwargs):
    if instance.stub:
        return
    try:
        User.objects.get(stub=True, gh_id=instance.gh_id).delete()
    except:
        pass

    try:
        User.objects.get(stub=True, ghe_id=instance.gh_id).delete()
    except:
        pass

post_save.connect(remove_stubs, User)

class RepoExtension(models.Model):
    repo = models.OneToOneField('github.Repo', related_name='kratos_extension')
    team = models.ForeignKey('Team', related_name='repos')

class Team(models.Model):
    name = models.CharField(max_length=100)

class Perm(models.Model):
    name = models.CharField(max_length=100)

class UserPermTeam(models.Model):
    user = models.ForeignKey(UserModel, related_name='perm_teams')
    perm = models.ForeignKey(Perm, related_name='user_teams')
    team = models.ForeignKey(Team, related_name='user_perms')

class UserPermRepo(models.Model):
    user = models.ForeignKey(UserModel, related_name='perm_repos')
    perm = models.ForeignKey(Perm, related_name='user_repos')
    repo = models.ForeignKey('github.Repo', related_name='user_perms')
