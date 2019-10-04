# Generated by Django 2.0.1 on 2018-03-20 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('direccion_financiera', '0001_initial'),
        ('recursos_humanos', '0015_auto_20180313_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratistas',
            name='banco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='direccion_financiera.Bancos'),
        ),
        migrations.AddField(
            model_name='contratistas',
            name='cuenta',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
