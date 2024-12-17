from django.db import models
from django.contrib.auth.models import User

class Remains(models.Model):
    comment = models.CharField(max_length=50, null=True, verbose_name='Комментарий')
    code = models.CharField(max_length=50, null=True, verbose_name='Код')
    article = models.TextField(null=True, verbose_name='Артикул')
    party = models.CharField(max_length=9, null=True, verbose_name='Партия')
    title = models.TextField(null=True, verbose_name='Наименование')
    base_unit = models.CharField(max_length=10, null=True, verbose_name='Единица')
    project = models.CharField(max_length=30, null=True, verbose_name='Проект')
    quantity = models.FloatField(blank=True, null=True, verbose_name='Количество')
    price = models.IntegerField(null=True, blank=True, verbose_name='Цена')


    def __str__(self):
        return f"{self.article}"

    def save(self, *args, **kwargs):
        # Обрезаем пробелы в начале и конце строки поля my_field
        self.my_field = self.article.strip()
        super(Remains, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Остаток'
        verbose_name_plural = 'Остатки'    


class Data_Table(models.Model):
    index_remains = models.IntegerField(null=True, default=1)
    article = models.CharField(max_length=60, null=True)
    party = models.CharField(max_length=20, null=True)
    title = models.TextField(null=True)
    base_unit = models.CharField(max_length=10, null=True)
    comment = models.TextField(null=True)
    date = models.DateTimeField(null=True)
    address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.article

    def save(self, *args, **kwargs):
        # Обрезаем пробелы в начале и конце строки поля my_field
        self.my_field = self.article.strip()
        super(Data_Table, self).save(*args, **kwargs)


class History(models.Model):
    data_table = models.ForeignKey(Data_Table, on_delete=models.CASCADE)
    article = models.TextField(null=True)
    party = models.CharField(max_length=9, null=True)
    title = models.TextField(null=True)
    comment = models.TextField(null=True)
    date = models.DateTimeField(null=True)
    address = models.CharField(max_length=100, null=True)


class Deleted(models.Model):
    article = models.TextField(null=True)
    party = models.CharField(max_length=9, null=True)
    title = models.TextField(null=True)
    comment = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100, null=True)



class Review(models.Model):
    user = models.CharField(null=True, blank=True, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f'{self.user} {self.created_at} {self.text}'
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'    





