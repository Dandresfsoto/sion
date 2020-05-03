# Generated by Django 2.1.5 on 2020-05-03 04:18

import config.extrafields
from django.db import migrations
import fest_2019.models


class Migration(migrations.Migration):

    dependencies = [
        ('fest_2019', '0085_auto_20200502_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyectosapi',
            name='file2',
            field=config.extrafields.ContentTypeRestrictedFileField(blank=True, max_length=255, null=True, upload_to=fest_2019.models.upload_dinamic_ficha_proyecto),
        ),
        migrations.AlterField(
            model_name='proyectosapi',
            name='file3',
            field=config.extrafields.ContentTypeRestrictedFileField(blank=True, max_length=255, null=True, upload_to=fest_2019.models.upload_dinamic_ficha_proyecto),
        ),
        migrations.AlterField(
            model_name='proyectosapi',
            name='file4',
            field=config.extrafields.ContentTypeRestrictedFileField(blank=True, max_length=255, null=True, upload_to=fest_2019.models.upload_dinamic_ficha_proyecto),
        ),
        migrations.AlterField(
            model_name='proyectosapi',
            name='file5',
            field=config.extrafields.ContentTypeRestrictedFileField(blank=True, max_length=255, null=True, upload_to=fest_2019.models.upload_dinamic_ficha_proyecto),
        ),
    ]
