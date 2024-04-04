# Generated by Django 5.0.2 on 2024-04-03 14:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.TextField(null=True)),
                ('party', models.CharField(max_length=9, null=True)),
                ('title', models.TextField(null=True)),
                ('comment', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('data_table', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finder.data_table')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]