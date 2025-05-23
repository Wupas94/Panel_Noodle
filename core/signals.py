from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile instance when a new User is created."""
    if created:
        Profile.objects.create(
            user=instance,
            rank='Nowy Pracownik',  # Default rank
            department='Security',  # Default department
            panel_role='Employee'  # Default role
        ) 