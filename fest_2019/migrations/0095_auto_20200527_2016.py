# Generated by Django 2.1.5 on 2020-05-28 01:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fest_2019', '0094_proyectosapi_actualizar_app'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observacionesproyectosapi',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]