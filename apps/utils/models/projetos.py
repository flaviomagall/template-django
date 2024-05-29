from django.db import models


"""
PROJETOS:
A2 - C-97
A6 - IU-93A
A7 - C-95
T1 - T-27
T2 - A-29
T9 - T-25
U2 - G-19
U8 - C-98

"""


class Projeto(models.Model):
    nome = models.CharField(max_length=15, verbose_name='Nome', help_text='Nome do projeto')
    sigla = models.CharField(max_length=3, verbose_name='Sigla', help_text='Sigla do projeto')

    def __str__(self) -> str:
        return self.sigla

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ['sigla']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['sigla']),
        ]
