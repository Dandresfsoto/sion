# Generated by Django 2.0.1 on 2018-08-17 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desplazamiento', '0009_auto_20180618_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desplazamiento',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
    ]
