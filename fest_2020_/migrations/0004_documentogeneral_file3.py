# Generated by Django 2.1.5 on 2021-02-10 02:55

import config.extrafields
from django.db import migrations
import fest_2020_.models


class Migration(migrations.Migration):

    dependencies = [
        ('fest_2020_', '0003_auto_20210126_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentogeneral',
            name='file3',
            field=config.extrafields.ContentTypeRestrictedFileField(blank=True, max_length=255, null=True, upload_to=fest_2020_.models.upload_dinamic_documento_general),
        ),
    ]