# Generated by Django 2.1.5 on 2019-12-15 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fest_2019', '0056_rutas_valores_actividades'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuposrutaobject',
            name='hogar',
        ),
        migrations.RemoveField(
            model_name='documento',
            name='hogar',
        ),
        migrations.AddField(
            model_name='cuposrutaobject',
            name='hogares',
            field=models.ManyToManyField(blank=True, related_name='cupo_hogares', to='fest_2019.Hogares'),
        ),
        migrations.AddField(
            model_name='documento',
            name='hogares',
            field=models.ManyToManyField(blank=True, related_name='hogar_documento', to='fest_2019.Hogares'),
        ),
        migrations.AddField(
            model_name='documento',
            name='ruta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ruta_documento', to='fest_2019.Rutas'),
        ),
    ]