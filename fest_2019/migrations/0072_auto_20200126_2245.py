# Generated by Django 2.1.5 on 2020-01-27 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fest_2019', '0071_auto_20200112_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hogares',
            name='documento',
            field=models.BigIntegerField(),
        ),
    ]
