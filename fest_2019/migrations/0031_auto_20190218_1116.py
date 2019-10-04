# Generated by Django 2.1.3 on 2019-02-18 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0027_categoriadiscapacidad_dificultadespermanentesdiscapacidad'),
        ('fest_2019', '0030_auto_20190214_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caracterizacioninicial',
            name='categoria_discapacidad',
        ),
        migrations.AddField(
            model_name='caracterizacioninicial',
            name='categoria_discapacidad',
            field=models.ManyToManyField(blank=True, null=True, to='usuarios.CategoriaDiscapacidad'),
        ),
        migrations.RemoveField(
            model_name='caracterizacioninicial',
            name='dificultades_permanentes',
        ),
        migrations.AddField(
            model_name='caracterizacioninicial',
            name='dificultades_permanentes',
            field=models.ManyToManyField(blank=True, null=True, to='usuarios.DificultadesPermanentesDiscapacidad'),
        ),
    ]
