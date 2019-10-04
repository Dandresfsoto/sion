# Generated by Django 2.0.1 on 2018-03-20 20:19

from django.db import migrations, models
import uuid
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from usuarios.models import ContentTypeSican


def create_permissions(apps, schema_editor):

    content_type = ContentType.objects.get_for_model(ContentTypeSican)

    db_alias = schema_editor.connection.alias

    Permission.objects.using(db_alias).bulk_create([
        Permission(name="Dirección financiera, ver aplicación", content_type = content_type, codename = 'direccion_financiera.ver'),

        Permission(name="Dirección financiera, ver bancos", content_type=content_type, codename='direccion_financiera.bancos.ver'),
        Permission(name="Dirección financiera, editar bancos", content_type=content_type, codename='direccion_financiera.bancos.editar'),
        Permission(name="Dirección financiera, crear bancos", content_type=content_type, codename='direccion_financiera.bancos.crear'),
        Permission(name="Dirección financiera, eliminar bancos", content_type=content_type, codename='direccion_financiera.bancos.eliminar'),
    ])

def create_groups(apps, schema_editor):

    #Consulta de bancos
    consulta_bancos, created = Group.objects.get_or_create(name = 'Dirección financiera, consulta bancos')
    permisos_consulta_bancos = Permission.objects.filter(codename__in = [
        'direccion_financiera.bancos.ver',
        'direccion_financiera.ver'
    ])
    consulta_bancos.permissions.add(*permisos_consulta_bancos)

    #Edicion de bancos
    edicion_bancos, created = Group.objects.get_or_create(name='Dirección financiera, edición bancos')
    permisos_edicion_bancos = Permission.objects.filter(codename__in=[
        'direccion_financiera.ver',
        'direccion_financiera.bancos.ver',
        'direccion_financiera.bancos.crear',
        'direccion_financiera.bancos.editar',
        'direccion_financiera.bancos.eliminar'
    ])
    edicion_bancos.permissions.add(*permisos_edicion_bancos)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bancos',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('codigo', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),

        migrations.RunPython(create_permissions),
        migrations.RunPython(create_groups),
    ]
