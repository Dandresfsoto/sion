# Generated by Django 2.0.1 on 2018-07-03 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpe_2018', '0041_documentolegalizacionterminales_radicado'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuenticostallerapertura',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dibuartetallercontenidoseducativos',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ecoraeetallerraee',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='infotictalleradministratic',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrofotograficotalleradministratic',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrofotograficotallerapertura',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrofotograficotallercontenidoseducativos',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registrofotograficotallerraee',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatoriatalleradministratic',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatoriatallerapertura',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatoriatallercontenidoseducativos',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='relatoriatallerraee',
            name='radicado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Radicados'),
            preserve_default=False,
        ),
    ]
