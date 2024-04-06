from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import History, Data_Table


@receiver(post_save, sender=Data_Table)
def create_history_entry(sender, instance, created, **kwargs):
    if created:
        History.objects.create(
                data_table=instance,
                article=instance.article,
                party=instance.party,
                title=instance.title,
                comment=instance.comment,
                address=instance.address,
                date=instance.date
            )

    if not created:
        History.objects.create(
            data_table=instance,
            article=instance.article,
            party=instance.party,
            title=instance.title,
            comment=instance.comment,
            address=instance.address,
            date=datetime.now()
        )
