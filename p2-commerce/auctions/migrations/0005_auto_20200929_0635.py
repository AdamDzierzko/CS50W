# Generated by Django 3.1 on 2020-09-29 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listing_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
