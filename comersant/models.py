from django.db import models

class TableData(models.Model):
    row = models.IntegerField()
    col = models.IntegerField()
    value = models.TextField()

    class Meta:
        unique_together = ('row', 'col')

class Comment(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Leading(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name        
