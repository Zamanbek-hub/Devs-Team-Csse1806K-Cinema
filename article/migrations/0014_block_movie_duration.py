# Generated by Django 2.2.6 on 2019-11-28 11:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_auto_20191128_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='movie_duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
