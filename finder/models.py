from pyclbr import Class
from unittest.util import _MAX_LENGTH
from django.db import models


class Remains(models.Model):
    comment = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=50, null=True)
    article = models.TextField(null=True)
    party = models.CharField(max_length=9, null=True)
    title = models.TextField(null=True)
    base_unit = models.CharField(max_length=10, null=True)
    project = models.CharField(max_length=30, null=True)
    quantity = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.article}"

    def save(self, *args, **kwargs):
        # Обрезаем пробелы в начале и конце строки поля my_field
        self.my_field = self.article.strip()
        super(Remains, self).save(*args, **kwargs)


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


class Standart(models.Model):
    din = models.CharField("ДИН", max_length=20)
    gost = models.CharField("ГОСТ", max_length=20)
    iso = models.CharField("ISO", max_length=20)
    another = models.CharField("Другое", max_length=20)

    def __str__(self) -> str:
        return f"{self.din}{self.gost}"


class Metiz(models.Model):
    description = models.TextField()
    standards = models.ManyToManyField(Standart)  # Многие-ко-многим отношение


    def __str__(self) -> str:
        return f"{self.description}"
