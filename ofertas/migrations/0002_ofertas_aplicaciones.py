# Generated by Django 2.0.1 on 2018-04-27 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ofertas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertas',
            name='aplicaciones',
            field=models.IntegerField(default=0),
        ),
    ]
