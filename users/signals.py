from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


# @receiver(post_save,sender=User)
def profile_create(sender, instance, created, **kwargs):
    if created:
        print("we are creating new user.")
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            name=user.first_name,
            email=user.email,
        )
        subject="Welcome Message!"
        body=f"Hi {profile.name} , We are glad to see you here we wish you the best."
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def user_update(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.username = profile.username
        user.first_name = profile.name
        user.email = profile.email
        user.save()


def user_delete(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(profile_create, sender=User)
post_save.connect(user_update,sender=Profile)
post_delete.connect(user_delete, sender=Profile)
