# Generated by Django 2.0.1 on 2018-10-10 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpe_2018', '0111_actualizacionlupaap_red'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actualizacionlupaap',
            name='red',
        ),
        migrations.AddField(
            model_name='actualizacionlupaap',
            name='red_r2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='red_r2_actualizacion', to='cpe_2018.Red'),
        ),
        migrations.AddField(
            model_name='actualizacionlupaap',
            name='red_r3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='red_r3_actualizacion', to='cpe_2018.Red'),
        ),
    ]
