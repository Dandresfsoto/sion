# Generated by Django 2.0.1 on 2018-04-29 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ofertas', '0010_auto_20180429_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertas',
            name='vacantes',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
