# Generated by Django 5.0.3 on 2024-06-06 17:20

import apps.authentication.models.perfil
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setor', models.CharField(choices=[('usuario', 'Usuário'), ('solicitante', 'Solicitante'), ('demanda', 'Demanda'), ('obtencao', 'Obtenção'), ('administrador', 'Administrador')], max_length=30, verbose_name='Cargo')),
                ('foto', models.ImageField(blank=True, default='avatars/default.png', null=True, upload_to=apps.authentication.models.perfil.user_directory_path, verbose_name='Foto do Usuário')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil do Usuário',
                'verbose_name_plural': 'Perfis dos Usuários',
                'ordering': ['usuario'],
                'indexes': [models.Index(fields=['usuario'], name='authenticat_usuario_6e1471_idx'), models.Index(fields=['setor'], name='authenticat_setor_3a5fce_idx'), models.Index(fields=['foto'], name='authenticat_foto_14eaa4_idx')],
            },
        ),
    ]
