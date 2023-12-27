from urllib import request

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def update_user_rank(sender, instance, **kwargs):
    """
       Signal handler to update the user ranks after a User instance (profile) is saved.

       This function is connected to the post_save signal of the User model.

       Args:
           sender: The sender model class.
           instance: The instance of the User model that was saved.
           kwargs: Additional keyword arguments.

       Returns: None thanks CHATGPT<3 YES IT'S CALLED EVERY TIME A USER IS SAVEZ BECAUSE I NEEDED IT TO ACTUALISE EVERY
       TIME YES IT'S NOT EFFICIENT OR POWER EFFICIENT BUT THAT'S OK
    """
    profiles = Profile.objects.all().order_by('-user_score')

    for index, profile in enumerate(profiles, start=1):
        profile.user_rank = index
        profile.save()
