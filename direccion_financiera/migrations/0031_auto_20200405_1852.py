# Generated by Django 2.1.5 on 2020-04-05 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('direccion_financiera', '0030_auto_20191204_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='RubroPresupuestal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='reportes',
            name='observacion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reportes',
            name='rubro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='direccion_financiera.RubroPresupuestal'),
        ),
    ]
