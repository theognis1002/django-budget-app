# Generated by Django 3.0.8 on 2020-07-07 17:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0004_auto_20200707_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='client',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='project',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2020, 7, 21, 13, 26, 5, 284601)),
        ),
    ]
