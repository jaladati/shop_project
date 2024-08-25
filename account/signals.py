from account.models import User

from django.dispatch import receiver
from django.db.models.signals import pre_save


@receiver(pre_save, sender=User)
def activate_superuser(sender, instance, **kwargs):
    if instance._state.adding is True and instance.is_superuser:
        instance.is_active = True
