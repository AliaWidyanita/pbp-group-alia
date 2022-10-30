# Generated by Django 4.1 on 2022-10-29 10:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0003_event_delete_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='range',
            field=models.IntegerField(default=50, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(300)]),
        ),
    ]
