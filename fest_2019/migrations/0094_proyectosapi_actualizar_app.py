# Generated by Django 2.1.5 on 2020-05-27 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fest_2019', '0093_permisoscuentasdepartamentos'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyectosapi',
            name='actualizar_app',
            field=models.BooleanField(default=True),
        ),
    ]