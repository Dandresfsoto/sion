# Generated by Django 2.0.1 on 2018-03-22 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('direccion_financiera', '0005_auto_20180321_1511'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pagos',
            old_name='update',
            new_name='update_datetime',
        ),
        migrations.RenameField(
            model_name='reportes',
            old_name='update',
            new_name='update_datetime',
        ),
    ]
