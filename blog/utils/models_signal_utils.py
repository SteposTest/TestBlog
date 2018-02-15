import threading

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Post, Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.is_superuser:
        return
    if created:
        Profile.objects.create(
            user=instance,
            viewed=[]
        )
    instance.profile.save()


@receiver(post_save, sender=Post)
def send_notification(sender, instance, created, **kwargs):
    user = instance.user_profile.user
    users = instance.user_profile.profile_set.all()
    recipient_list = [i.user.email for i in users if i.user.email]
    subject = 'New post'
    body = f'{user.username} created new post {settings.BASE_URL}/post/{instance.pk}/'
    EmailThread(subject, body, settings.EMAIL, recipient_list).start()


class EmailThread(threading.Thread):
    def __init__(self, subject, body, sender, recipient_list):
        self.subject = subject
        self.body = body
        self.sender = sender
        self.recipient_list = recipient_list

        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(self.subject, self.body, self.sender, self.recipient_list)
        except Exception as e:
            return
