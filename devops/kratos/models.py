from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from django.conf import settings
UserModel = settings.AUTH_USER_MODEL


@python_2_unicode_compatible
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

    def is_admin(self, team_name=None):
        if self.stub:
            return False
        try:
            UserPermTeam.objects.get(user=self, perm__name='admin', team__name=team_name)
        except UserPermTeam.DoesNotExist:
            return False
        else:
            return True

    def __str__(self):
        return '<User: {}>'.format(self.username)

def remove_stubs(sender, instance, **kwargs):
    if instance.stub:
        return
    remove_stub(instance, gh_id=instance.gh_id)
    remove_stub(instance, ghe_id=instance.ghe_id)

def remove_stub(user, **stub_query):
    """ switch all relations from old user to new user """
    try:
        stub = User.objects.get(stub=True, **stub_query)
    except:
        return
    stub.perm_teams.all().update(user=user)
    stub.perm_repos.all().update(user=user)
    stub.delete()

post_save.connect(remove_stubs, User)

@python_2_unicode_compatible
class RepoExtension(models.Model):
    repo = models.OneToOneField('github.Repo', related_name='kratos_extension')
    team = models.ForeignKey('Team', related_name='repos')

    def __str__(self):
        return '<Kratos Repo Extension: {}>'.format(self.repo)

@python_2_unicode_compatible
class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '<Team: {}>'.format(self.name)

@python_2_unicode_compatible
class Perm(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '<Perm: {}>'.format(self.name)


@python_2_unicode_compatible
class UserPermTeam(models.Model):
    user = models.ForeignKey(UserModel, related_name='perm_teams')
    perm = models.ForeignKey(Perm, related_name='user_teams')
    team = models.ForeignKey(Team, related_name='user_perms')

    def __str__(self):
        return '<{} has {} for {}>'.format(self.user, self.perm, self.team)

@python_2_unicode_compatible
class UserPermRepo(models.Model):
    user = models.ForeignKey(UserModel, related_name='perm_repos')
    perm = models.ForeignKey(Perm, related_name='user_repos')
    repo = models.ForeignKey('github.Repo', related_name='user_perms')

    def __str__(self):
        return '<{} has {} for {}>'.format(self.user, self.perm, self.repo)
