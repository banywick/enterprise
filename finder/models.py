from re import T
from django.db import models
from sqlalchemy import null


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


class UserIP(models.Model):
    ip_address = models.CharField(max_length=12)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} {self.ip_address}"



class Data_Table(models.Model):
    index_remains = models.IntegerField(null=True, default=1)
    article = models.CharField(max_length=50, null=True)
    party = models.CharField(max_length=20, null=True)
    title = models.TextField(null=True)
    base_unit = models.CharField(max_length=10, null=True)
    comment = models.TextField(null=True)
    date = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.article
    
    def save(self, *args, **kwargs):
        # Обрезаем пробелы в начале и конце строки поля my_field
        self.my_field = self.article.strip()
        super(Data_Table, self).save(*args, **kwargs)


    
