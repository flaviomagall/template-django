# apps/accounts/signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rolepermissions.roles import assign_role, clear_roles
from apps.authentication.models import Perfil

User = get_user_model()

@receiver(pre_save, sender=Perfil)
def update_user_role(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Perfil.objects.get(pk=instance.pk)
        if old_instance.setor != instance.setor:
            clear_roles(instance.usuario)
            assign_role(instance.usuario, instance.setor.lower())  # Assume que o nome da role é igual ao cargo em minúsculas

