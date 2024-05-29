import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.authentication.models import Perfil

User = get_user_model()
logger = logging.getLogger('requestlogs')

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance, setor='usuario')  # Use a string diretamente ou o índice correto
        logger.info(f'Perfil created for user {instance.username}')
    else:
        instance.perfil.save()
        logger.info(f'Perfil updated for user {instance.username}')
