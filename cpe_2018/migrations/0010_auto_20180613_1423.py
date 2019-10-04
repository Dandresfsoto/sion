# Generated by Django 2.0.1 on 2018-06-13 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpe_2018', '0009_entregables_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentes',
            name='modelo',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='componentes',
            name='tipo',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estrategias',
            name='modelo',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estrategias',
            name='tipo',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='momentos',
            name='modelo',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='momentos',
            name='tipo',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
