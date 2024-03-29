# Generated by Django 2.1.5 on 2019-12-04 15:19

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('direccion_financiera', '0029_auto_20191113_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagos',
            name='valor',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='COP', max_digits=20),
        ),
        migrations.AlterField(
            model_name='reportes',
            name='valor',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='COP', max_digits=20),
        ),
    ]
