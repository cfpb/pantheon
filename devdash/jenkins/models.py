from django.db import models

class JobManager(models.Manager):
    pass

class Job(models.Model):
    repo = models.ForeignKey("github.Repo")
