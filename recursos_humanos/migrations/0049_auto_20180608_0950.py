# Generated by Django 2.0.1 on 2018-06-08 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recursos_humanos', '0048_contratos_cargo'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratos',
            name='fecha_liquidacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contratos',
            name='fecha_renuncia',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
