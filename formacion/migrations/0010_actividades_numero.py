# Generated by Django 2.0.1 on 2018-05-10 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formacion', '0009_auto_20180510_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividades',
            name='numero',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
