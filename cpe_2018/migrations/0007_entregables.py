# Generated by Django 2.0.1 on 2018-06-08 17:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpe_2018', '0006_momentos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entregables',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=200)),
                ('numero', models.IntegerField()),
                ('cantidad', models.IntegerField(default=0)),
                ('momento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cpe_2018.Momentos')),
            ],
        ),
    ]
