# Generated by Django 2.0.1 on 2018-04-11 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recursos_humanos', '0024_auto_20180410_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificaciones',
            name='word',
        ),
        migrations.AddField(
            model_name='certificaciones',
            name='delta',
            field=models.CharField(default='', max_length=10000),
            preserve_default=False,
        ),
    ]
