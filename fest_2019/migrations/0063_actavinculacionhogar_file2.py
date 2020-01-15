# Generated by Django 2.1.5 on 2019-12-18 03:25

import config.extrafields
from django.db import migrations
import fest_2019.models


class Migration(migrations.Migration):

    dependencies = [
        ('fest_2019', '0062_auto_20191217_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='actavinculacionhogar',
            name='file2',
            field=config.extrafields.ContentTypeRestrictedFileField(default='', max_length=255, upload_to=fest_2019.models.upload_dinamic_acta_vinculacion_hogar),
            preserve_default=False,
        ),
    ]