# Generated by Django 2.0.1 on 2018-08-08 20:44

import cpe_2018.models
from django.db import migrations
import config.extrafields


class Migration(migrations.Migration):

    dependencies = [
        ('cpe_2018', '0069_cuentascobro'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentascobro',
            name='file2',
            field=config.extrafields.ContentTypeRestrictedFileField(blank=True, max_length=255, null=True, upload_to=cpe_2018.models.upload_dinamic_cuentas_cobro),
        ),
    ]
