from django.db import models
from django.contrib.auth.models import User

class RemainsInventory(models.Model):
    article = models.CharField(max_length=70, null=True, verbose_name='Артикул')
    title = models.TextField(null=True, verbose_name='Наименование')
    base_unit = models.CharField(max_length=10, null=True, verbose_name='Единица')

    def __str__(self):
        return f'{self.article}{self.title}{self.base_unit}'
    
    class Meta:
        verbose_name = 'Инвентаризация'
        verbose_name_plural = 'Инвентаризация'  



