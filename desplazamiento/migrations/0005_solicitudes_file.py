# Generated by Django 2.0.1 on 2018-05-30 13:33

import desplazamiento.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desplazamiento', '0004_auto_20180529_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudes',
            name='file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=desplazamiento.models.upload_dinamic_dir_file),
        ),
    ]
