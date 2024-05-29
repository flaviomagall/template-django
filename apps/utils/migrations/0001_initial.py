# Generated by Django 5.0.3 on 2024-05-28 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Nome do projeto', max_length=15, verbose_name='Nome')),
                ('sigla', models.CharField(help_text='Sigla do projeto', max_length=3, verbose_name='Sigla')),
            ],
            options={
                'verbose_name': 'Projeto',
                'verbose_name_plural': 'Projetos',
                'ordering': ['sigla'],
                'indexes': [models.Index(fields=['nome'], name='utils_proje_nome_04a631_idx'), models.Index(fields=['sigla'], name='utils_proje_sigla_f42d44_idx')],
            },
        ),
        migrations.CreateModel(
            name='UnidadeEstocagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Nome da unidade de estocagem', max_length=15, verbose_name='Nome')),
                ('sigla', models.CharField(help_text='Sigla da unidade de estocagem', max_length=3, verbose_name='Sigla')),
            ],
            options={
                'verbose_name': 'Unidade de estocagem',
                'verbose_name_plural': 'Unidades de estocagens',
                'ordering': ['sigla'],
                'indexes': [models.Index(fields=['nome'], name='utils_unida_nome_a9e55b_idx'), models.Index(fields=['sigla'], name='utils_unida_sigla_ae7cbc_idx')],
            },
        ),
        migrations.CreateModel(
            name='UnidadesFab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Nome da Organização militar', max_length=30, verbose_name='Nome da unidade')),
                ('foto', models.CharField(help_text='Sigla da Organização militar', max_length=3, verbose_name='Sigla da unidade')),
            ],
            options={
                'verbose_name': 'Unidade da FAB',
                'verbose_name_plural': 'Unidades da FAB',
                'ordering': ['nome'],
                'indexes': [models.Index(fields=['nome'], name='utils_unida_nome_33a6f1_idx'), models.Index(fields=['foto'], name='utils_unida_foto_3d6662_idx')],
            },
        ),
    ]