# Generated by Django 3.1 on 2020-11-06 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20201008_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
