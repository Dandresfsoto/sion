# Generated by Django 2.0.1 on 2018-06-14 20:57

from django.db import migrations, models
import recursos_humanos.models


class Migration(migrations.Migration):

    dependencies = [
        ('recursos_humanos', '0051_auto_20180608_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hv',
            name='excel',
            field=models.FileField(blank=True, max_length=250, null=True, upload_to=recursos_humanos.models.upload_dinamic_dir_excel),
        ),
    ]
