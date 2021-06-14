# Generated by Django 3.1 on 2021-04-02 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0003_auto_20210402_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genere',
            name='movie_id',
        ),
        migrations.AddField(
            model_name='movie',
            name='genere',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='genere', to='capstone.genere'),
        ),
    ]
