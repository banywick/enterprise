from django.db import models


class Comment(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Leading(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name        

class Supler(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  
    
class Status(models.Model):
    name = models.CharField(max_length=100, default='Запрос') 

    def __str__(self):
        return self.name      

class Specialist(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  
    
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20)
    date = models.DateField()
    supplier = models.ForeignKey(Supler, on_delete=models.CASCADE)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, default='шт')
    quantity = models.IntegerField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    leading = models.ForeignKey(Leading, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,  default=1)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.invoice_number    
