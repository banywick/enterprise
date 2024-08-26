from django.db import models
from django.contrib.auth.models import User

class RemainsInventory(models.Model):
    article = models.CharField(max_length=70, null=True, verbose_name='Артикул')
    title = models.TextField(null=True, verbose_name='Наименование')
    base_unit = models.CharField(max_length=10, null=True, verbose_name='Единица')
    status = models.CharField(blank=True, null=True, verbose_name='Статус')

    def __str__(self):
        return f'{self.article}{self.title}{self.base_unit}'
    
    class Meta:
        verbose_name = 'Инвентаризация'
        verbose_name_plural = 'Инвентаризация'  


class OrderInventory(models.Model):
    product = models.ForeignKey(RemainsInventory, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_ord = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100,blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'OrderInventory (id: {self.id}, product: {self.product.title} {self.product.article}'        



