from django.db import models


class UnidadeEstocagem(models.Model):
    nome = models.CharField(max_length=15, verbose_name='Nome', help_text='Nome da unidade de estocagem')
    sigla = models.CharField(max_length=3, verbose_name='Sigla', help_text='Sigla da unidade de estocagem')

    def __str__(self) -> str:
        return self.sigla

    class Meta:
        verbose_name = 'Unidade de estocagem'
        verbose_name_plural = 'Unidades de estocagem'
        ordering = ['sigla']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['sigla']),
        ]
