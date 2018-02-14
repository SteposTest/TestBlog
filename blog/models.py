from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField

MAX_LENGTH = 255


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ManyToManyField('self', blank=True, symmetrical=False)
    viewed = JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.pk}: {self.user.username}'


class Post(models.Model):
    title = models.CharField(max_length=MAX_LENGTH, unique=True)
    text = models.TextField(max_length=MAX_LENGTH)
    pub_date = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f'{self.pk}: {self.user_profile} - {self.title}'

    class Meta:
        ordering = ['-pub_date']
