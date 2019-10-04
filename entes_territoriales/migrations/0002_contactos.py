# Generated by Django 2.0.1 on 2018-05-16 16:00

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('entes_territoriales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contactos',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=200)),
                ('cargo', models.CharField(max_length=200)),
                ('celular', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('observaciones', models.TextField(blank=True, max_length=500, null=True)),
                ('reunion', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='entes_territoriales.Reuniones')),
            ],
        ),
    ]
