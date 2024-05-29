from django.db import models


class UnidadesFab(models.Model):
    nome = models.CharField(max_length=30, verbose_name='Nome da unidade', help_text='Nome da Organização militar')
    foto = models.ImageField(upload_to='fotos_unidades/', verbose_name='Sigla da unidade', help_text='Foto da Organização militar')

    def __str__(self) -> str:
        return self.nome

    class Meta:
        verbose_name = 'Unidade da FAB'
        verbose_name_plural = 'Unidades da FAB'
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['foto']),
        ]
