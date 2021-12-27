# Generated by Django 3.2.9 on 2021-12-23 02:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_auto_20211223_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='warning_amount',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='expense',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 23, 2, 11, 2, 104954, tzinfo=utc), editable=False),
        ),
    ]
