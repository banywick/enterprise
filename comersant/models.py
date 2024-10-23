from django.db import models

class TableData(models.Model):
    row = models.IntegerField()
    col = models.IntegerField()
    value = models.TextField()

    class Meta:
        unique_together = ('row', 'col')
