# Generated by Django 2.0.1 on 2018-03-09 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recursos_humanos', '0002_auto_20180308_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratistas',
            name='cedula',
            field=models.BigIntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
