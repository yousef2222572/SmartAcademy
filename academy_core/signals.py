from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_permissions(sender, instance, created, **kwargs):
    """Every user must have a UserPermissions row.

    Code such as ``UserPermissions.objects.get(user=...)`` assumes the row
    already exists, so create it right after the user is created.
    """
    if created:
        models.UserPermissions.objects.get_or_create(user=instance)
