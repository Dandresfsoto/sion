# Generated by Django 2.1.5 on 2020-04-17 16:02

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fest_2019', '0077_auto_20200415_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProyectosApi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('creation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]