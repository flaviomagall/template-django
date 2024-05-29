import os
from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def user_directory_path(instance, filename):
    # Extrai a extensão do arquivo original e gera o nome do arquivo
    base_filename, file_extension = os.path.splitext(filename)
    # Você pode querer adicionar slugify se o username tiver caracteres especiais
    new_filename = f"{slugify(instance.usuario.username)}_profile{file_extension}"
    # Monta o caminho completo para o arquivo
    return os.path.join('fotos_perfil', new_filename)

class Perfil(models.Model):
    """
    Modelo de Perfil do Usuário
    """

    CARGO_CHOICES = [
        ('usuario', 'Usuário'),
        ('solicitante', 'Solicitante'),
        ('demanda', 'Demanda'),
        ('obtencao', 'Obtenção'),
        ('administrador', 'Administrador'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    setor = models.CharField(max_length=30, choices=CARGO_CHOICES, verbose_name='Cargo')
    foto = models.ImageField(upload_to=user_directory_path, default='avatars/default.png', blank=True, null=True, verbose_name='Foto do Usuário')

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos Usuários'
        ordering = ['usuario']
        indexes = [
            models.Index(fields=['usuario']),
            models.Index(fields=['setor']),
            models.Index(fields=['foto']),
        ]
