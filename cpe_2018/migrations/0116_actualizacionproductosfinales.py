# Generated by Django 2.1.3 on 2018-12-03 15:38

import cpe_2018.models
from django.db import migrations, models
import config.extrafields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpe_2018', '0115_rutas_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActualizacionProductosFinales',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('tablero_control', config.extrafields.ContentTypeRestrictedFileField(max_length=255, upload_to=cpe_2018.models.upload_dinamic_actualizacion_productos_finales)),
                ('tablero_control_json', config.extrafields.ContentTypeRestrictedFileField(blank=True, max_length=255, null=True, upload_to=cpe_2018.models.upload_dinamic_actualizacion_productos_finales)),
                ('resultado', config.extrafields.ContentTypeRestrictedFileField(blank=True, max_length=255, null=True, upload_to=cpe_2018.models.upload_dinamic_actualizacion_productos_finales)),
            ],
        ),
    ]
