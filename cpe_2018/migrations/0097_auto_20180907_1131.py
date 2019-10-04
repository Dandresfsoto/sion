# Generated by Django 2.0.1 on 2018-09-07 16:31

import cpe_2018.models
from django.db import migrations, models
import config.extrafields
import storages.backends.ftp


class Migration(migrations.Migration):

    dependencies = [
        ('cpe_2018', '0096_auto_20180830_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='cortes',
            name='file',
            field=models.FileField(blank=True, null=True, storage=storages.backends.ftp.FTPStorage(), upload_to=cpe_2018.models.upload_dinamic_dir_corte),
        ),
        migrations.AlterField(
            model_name='red',
            name='file',
            field=config.extrafields.ContentTypeRestrictedFileField(blank=True, max_length=255, null=True, storage=storages.backends.ftp.FTPStorage(), upload_to=cpe_2018.models.upload_dinamic_red),
        ),
    ]
