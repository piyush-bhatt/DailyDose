from django.db import models
from django.contrib.auth.models import User


class Subreddits(models.Model):
    subreddit_name = models.TextField(null=True)
    user = models.ForeignKey(User, default='')



