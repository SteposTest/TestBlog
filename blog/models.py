from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField

MAX_LENGTH = 255


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)
    viewed = JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.pk}: {self.user.username}'


class Post(models.Model):
    title = models.CharField(max_length=MAX_LENGTH, unique=True)
    text = models.TextField(max_length=MAX_LENGTH)
    created = models.TimeField(auto_created=True)

    def __str__(self):
        return f'{self.pk}: {self.title}'
