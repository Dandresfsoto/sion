from django.db import models
import uuid
from usuarios.models import Municipios, User, Departamentos, Corregimientos, Veredas, PueblosIndigenas, \
    ResguardosIndigenas, ComunidadesIndigenas, LenguasNativas, ConsejosAfro, ComunidadesAfro, CategoriaDiscapacidad, \
    DificultadesPermanentesDiscapacidad, ElementosDiscapacidad, TiposRehabilitacionDiscapacidad

from recursos_humanos import models as models_rh
from djmoney.models.fields import MoneyField
from django.db.models import Sum
from direccion_financiera.models import Bancos
from config.extrafields import ContentTypeRestrictedFileField
from django.db.models.signals import post_save
from django.dispatch import receiver
from pytz import timezone
from django.conf import settings
import json
from delta import html

settings_time_zone = timezone(settings.TIME_ZONE)

# Create your models here.

class Componentes(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    nombre = models.CharField(max_length=100)
    consecutivo = models.IntegerField()
    momentos = models.IntegerField()
    valor = models.IntegerField(default=0)
    ruta = models.TextField(default='')
    valor_pagado = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def get_numero_momentos(self):
        return Momentos.objects.filter(componente=self).count()


    def get_cantidad_instrumentos(self,hogar):
        return InstrumentosRutaObject.objects.filter(hogar = hogar,momento__componente = self).count()


    def get_valor_hogar(self, hogar):
        valor = CuposRutaObject.objects.filter(hogar=hogar, momento__componente = self,estado__in=['Reportado','Pagado']).aggregate(Sum('valor'))['valor__sum']
        return valor if valor != None else 0


    def get_ruta_hogar_componente(self, hogar):

        if self.consecutivo == 1:
            return hogar.ruta_1
        elif self.consecutivo == 2:
            return hogar.ruta_2
        elif self.consecutivo == 3:
            return hogar.ruta_3
        elif self.consecutivo == 4:
            return hogar.ruta_4
        else:
            return None

class Momentos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    componente = models.ForeignKey(Componentes,on_delete=models.DO_NOTHING,related_name='momentos_componente')
    nombre = models.CharField(max_length=100)
    consecutivo = models.IntegerField()
    instrumentos = models.IntegerField()
    tipo = models.CharField(max_length=100)
    valor_maximo = models.BooleanField(default=True)
    novedades = models.BooleanField(default=True)
    progreso = models.BooleanField(default=True)

    def __str__(self):
        return '{0} - {1}'.format(self.componente.nombre,self.nombre)


    def get_objetos_ruta(self,ruta):
        return CuposRutaObject.objects.filter(momento = self, ruta = ruta).count()


    def get_cantidad_instrumentos(self,hogar,componente):
        return InstrumentosRutaObject.objects.filter(hogar = hogar,momento__componente = componente, momento = self).count()

    def get_novedades_mis_rutas_actividades(self,ruta):
        return InstrumentosRutaObject.objects.filter(ruta = ruta, momento = self, estado = 'cargado').values_list('hogar__id',flat=True).distinct().count()

    def get_numero_instrumentos(self):
        return Instrumentos.objects.filter(momento=self).count()

    def get_consecutivo(self):
        return '{0}.{1}'.format(self.componente.consecutivo,self.consecutivo)

    def get_valor_maximo_momento(self,ruta):
        valor = CuposRutaObject.objects.filter(ruta = ruta, momento = self).aggregate(Sum('valor'))['valor__sum']
        if valor == None:
            valor = 0
        return float(valor)



    def get_valor_maximo_momento_corte(self,ruta,corte):
        valor = CuposRutaObject.objects.filter(ruta = ruta, momento = self, corte = corte).aggregate(Sum('valor'))['valor__sum']
        if valor == None:
            valor = 0
        return float(valor)


    def get_valor_reportado_momento(self,ruta):
        valor = CuposRutaObject.objects.filter(ruta = ruta, momento = self, estado = 'Reportado').aggregate(Sum('valor'))['valor__sum']
        if valor == None:
            valor = 0
        return float(valor)

    def get_valor_pagado_momento(self,ruta):
        valor = CuposRutaObject.objects.filter(ruta = ruta, momento = self, estado = 'Pagado').aggregate(Sum('valor'))['valor__sum']
        if valor == None:
            valor = 0
        return float(valor)

    def get_progreso_momento(self,ruta):
        valor_maximo = self.get_valor_maximo_momento(ruta)
        valor_reportado = self.get_valor_reportado_momento(ruta)
        valor_pagado = self.get_valor_pagado_momento(ruta)

        if valor_maximo != 0:
            progreso = ((valor_reportado + valor_pagado)/valor_maximo)*100.0
        else:
            progreso = 0.0

        return (progreso,valor_maximo,valor_reportado,valor_pagado)


    def get_valor_pagado(self,hogar):
        query = CuposRutaObject.objects.filter(momento = self, estado__in = ['Reportado','Pagado'], hogar = hogar)
        valor = query.aggregate(Sum('valor'))['valor__sum']
        if valor == None:
            valor = 0

        return valor

class Instrumentos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    momento = models.ForeignKey(Momentos,on_delete=models.DO_NOTHING,related_name='instrumento_omento')
    nombre = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    consecutivo = models.IntegerField()
    modelo = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def get_consecutivo(self):
        return '{0}.{1}.{2}'.format(self.momento.componente.consecutivo,self.momento.consecutivo,self.consecutivo)

class Rutas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    creation = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(unique=True, max_length=100)
    contrato = models.ForeignKey(models_rh.Contratos, on_delete=models.DO_NOTHING,
                                 related_name='contrato_ruta_fest_2019')
    valor = MoneyField(max_digits=10, decimal_places=2, default_currency='COP',default=0)
    valor_transporte = MoneyField(max_digits=10, decimal_places=2, default_currency='COP', default=0)

    novedades = models.IntegerField(default=0)
    progreso = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    usuario_creacion = models.ForeignKey(User, related_name="usuario_creacion_ruta_fest_2019", on_delete=models.DO_NOTHING)
    update_datetime = models.DateTimeField(auto_now=True)
    usuario_actualizacion = models.ForeignKey(User, related_name="usuario_actualizacion_ruta_fest_2019",
                                              on_delete=models.DO_NOTHING,
                                              blank=True, null=True)

    estado = models.CharField(max_length=100,blank=True)
    componente = models.ForeignKey(Componentes, on_delete=models.DO_NOTHING,blank=True,null=True)

    meta_vinculacion = models.IntegerField(default=0)
    valor_vinculacion = MoneyField(max_digits=10, decimal_places=2, default_currency='COP',default=0)
    valor_transporte_vinculacion = MoneyField(max_digits=10, decimal_places=2, default_currency='COP', default=0)

    peso_visitas = models.IntegerField(default=0)
    peso_encuentros = models.IntegerField(default=0)
    peso_otros = models.IntegerField(default=0)

    valor_actividades = MoneyField(max_digits=10, decimal_places=2, default_currency='COP',default=0)
    meta_hogares = models.IntegerField(default=0)
    hogares_inscritos = models.IntegerField(default=0)


    def __str__(self):
        return self.nombre


    def translado(self, hogar, componente):

        update = False

        momentos_ids = []

        for cupo in CuposRutaObject.objects.filter(hogar = hogar, estado__in = ['Pagado','Reportado'], translado = False,momento__componente = componente).exclude(ruta=self):

            if cupo.momento.id not in momentos_ids:

                update = True

                CuposRutaObject.objects.get_or_create(
                    ruta = self,
                    momento = cupo.momento,
                    tipo = cupo.tipo,
                    estado = 'Pagado',
                    valor = 0,
                    hogar = cupo.hogar,
                    translado = False
                )

            cupo.translado = True
            cupo.save()

        ruta = None

        if componente.consecutivo == 1:

            if hogar.ruta_1 != None:
                ruta = hogar.ruta_1

            hogar.ruta_1 = self
            hogar.save()

        elif componente.consecutivo == 2:

            if hogar.ruta_2 != None:
                ruta = hogar.ruta_2

            hogar.ruta_2 = self
            hogar.save()

        elif componente.consecutivo == 3:

            if hogar.ruta_3 != None:
                ruta = hogar.ruta_3

            hogar.ruta_3 = self
            hogar.save()

        elif componente.consecutivo == 4:

            if hogar.ruta_4 != None:
                ruta = hogar.ruta_4

            hogar.ruta_4 = self
            hogar.save()

        if ruta != None:
            ruta.update_hogares_inscritos()
            if update:
                ruta.actualizar_objetos()

        return update



    def translado_vinculacion(self, hogar):

        update = False

        momentos_ids = []

        for cupo in CuposRutaObject.objects.filter(hogar = hogar, estado__in = ['Pagado','Reportado'], translado = False, momento__tipo = 'vinculacion').exclude(ruta=self):

            if cupo.momento.id not in momentos_ids:

                update = True

                CuposRutaObject.objects.get_or_create(
                    ruta = self,
                    momento = cupo.momento,
                    tipo = cupo.tipo,
                    estado = 'Pagado',
                    valor = 0,
                    hogar = cupo.hogar,
                    translado = False
                )

            cupo.translado = True
            cupo.save()

        ruta = None


        if hogar.ruta_vinculacion != None:
            ruta = hogar.ruta_vinculacion

        hogar.ruta_vinculacion = self
        hogar.save()



        if ruta != None:
            ruta.update_hogares_inscritos()
            if update:
                ruta.actualizar_objetos()

        return update


    def update_visita_1(self):

        momento = Momentos.objects.filter(componente = self.componente).get(nombre = "Visita 1")
        valor_total = CuposRutaObject.objects.filter(ruta = self,momento = momento).aggregate(Sum('valor'))['valor__sum']
        CuposRutaObject.objects.filter(ruta = self, momento= momento, estado = "asignado").delete()
        asignados = CuposRutaObject.objects.filter(ruta=self,momento=momento).count()

        for i in range(0,self.meta_vinculacion-asignados):

            CuposRutaObject.objects.create(
                ruta=self,
                momento=momento,
                tipo=momento.tipo,
                estado='asignado',
                valor=0
            )

        objetos = CuposRutaObject.objects.filter(ruta=self,momento=momento)
        valor = valor_total/objetos.count()
        objetos.update(valor=valor)

        return '{0} - {1}'.format(self.meta_vinculacion,objetos.count())

    def update_progreso(self):
        progreso = 0
        cupos = CuposRutaObject.objects.filter(ruta = self)
        revisados = cupos.filter(estado__in = ['Reportado','Pagado'])

        try:
            progreso = (revisados.count()/cupos.count())*100.0
        except:
            pass

        self.progreso = progreso
        self.save()

        return self.progreso

    def set_novedades_ruta(self):
        novedades = 0
        for momento in Momentos.objects.filter(componente = self.componente):
            novedades += momento.get_novedades_mis_rutas_actividades(self)
        Rutas.objects.filter(id = self.id).update(novedades = novedades)
        self.update_progreso()
        return novedades

    def update_novedades(self):
        self.novedades = InstrumentosRutaObject.objects.filter(ruta=self, estado='cargado').values_list('hogar__id','momento__id').distinct().count()
        self.save()
        self.update_progreso()
        return 'Ok'

    def update_hogares_inscritos(self):

        if str(self.componente.consecutivo) == '1':
            objetos_hogares = Hogares.objects.filter(ruta_1 = self)

        elif str(self.componente.consecutivo) == '2':
            objetos_hogares = Hogares.objects.filter(ruta_2 = self)

        elif str(self.componente.consecutivo) == '3':
            objetos_hogares = Hogares.objects.filter(ruta_3 = self)

        elif str(self.componente.consecutivo) == '4':
            objetos_hogares = Hogares.objects.filter(ruta_4 = self)

        else:
            objetos_hogares = Hogares.objects.none()

        self.hogares_inscritos = objetos_hogares.count()
        self.save()

        return None

    def crear_objetos_momento(self,momento,procesados,meta,valor,cantidad_momentos,meta_vinculacion):

        valor = valor/cantidad_momentos

        valor_procesados = procesados.filter(momento=momento).aggregate(Sum('valor'))['valor__sum']
        if valor_procesados == None:
            valor_procesados = 0

        nueva_meta = (meta - procesados.filter(momento=momento).exclude(translado = True).count())



        try:
            nuevo_valor = (valor - float(valor_procesados)) / (nueva_meta)
        except:
            return (0,0)

        else:
            if momento.nombre == 'Visita 1':

                nueva_meta_visita_1 = (meta_vinculacion - procesados.filter(momento=momento).count())

                try:
                    nuevo_valor_visita_1 = (valor - float(valor_procesados)) / (nueva_meta_visita_1)
                except:
                    return (0, 0)

                for i in range(0, nueva_meta_visita_1):
                    CuposRutaObject.objects.create(
                        ruta=self,
                        momento=momento,
                        tipo=momento.tipo,
                        estado='asignado',
                        valor=nuevo_valor_visita_1
                    )
            else:
                for i in range(0, nueva_meta):
                    CuposRutaObject.objects.create(
                        ruta=self,
                        momento=momento,
                        tipo=momento.tipo,
                        estado='asignado',
                        valor=nuevo_valor
                    )

            return (nueva_meta,nuevo_valor)

    def clean_objetos(self,tipo):

        CuposRutaObject.objects.filter(ruta=self, estado = "asignado",momento__tipo = tipo).delete()
        procesados = CuposRutaObject.objects.filter(ruta = self, estado__in = ["Reportado","Pagado"], momento__tipo = tipo)

        return procesados

    def actualizar_objetos(self):

        tipos = {
            'vinculacion':{'meta':self.meta_vinculacion,'valor':float(self.valor_vinculacion.amount)},
            'visita': {'meta': self.meta_hogares, 'valor': (float(self.valor_actividades.amount)*self.peso_visitas)/100},
            'encuentro': {'meta': self.meta_hogares, 'valor': (float(self.valor_actividades.amount)*self.peso_encuentros)/100},
            'otros': {'meta': self.meta_hogares, 'valor': (float(self.valor_actividades.amount) * self.peso_otros)/100},
        }
        momentos = Momentos.objects.filter(componente=self.componente)

        #for key in tipos.keys():

        #    procesados = self.clean_objetos(key)

        #    cantidad_momentos = momentos.filter(tipo=key).count()

        #    for momento in momentos.filter(tipo=key):

        #        meta,valor = self.crear_objetos_momento(momento,procesados,tipos[key]['meta'],tipos[key]['valor'],cantidad_momentos,self.meta_vinculacion)


        if tipos['vinculacion']['meta'] > 0:

            for key in tipos.keys():

                valor_total = tipos[key]['valor'] # valor total del tipo de momento
                cantidad_momentos = momentos.filter(tipo=key).count() # cantidad total de momentos del componente
                procesados = self.clean_objetos(key) #query de objetos pagos o reportados
                valor_procesados = procesados.aggregate(Sum('valor'))['valor__sum']
                if valor_procesados == None:
                    valor_procesados = 0


                nueva_meta = (cantidad_momentos * tipos[key]['meta']) - procesados.filter(ruta = self).exclude(translado=True).count()
                nuevo_valor_total = valor_total - float(valor_procesados)




                try:
                    valor_momento = nuevo_valor_total / nueva_meta
                except:
                    pass

                else:

                    for momento in momentos.filter(tipo=key):

                        if momento.nombre == 'Visita 1':
                            nueva_meta_visita_1 = (tipos['vinculacion']['meta'] - procesados.filter(ruta = self,momento=momento).exclude(translado = True).count())

                            try:
                                nuevo_valor_visita_1 = (nuevo_valor_total/cantidad_momentos)/ nueva_meta_visita_1
                            except:
                                pass
                            else:

                                for i in range(0, nueva_meta_visita_1):
                                    CuposRutaObject.objects.create(
                                        ruta=self,
                                        momento=momento,
                                        tipo=momento.tipo,
                                        estado='asignado',
                                        valor=0
                                    )
                        else:
                            for i in range(0, tipos[key]['meta'] - procesados.filter(ruta = self,momento=momento).exclude(translado = True).count()):
                                CuposRutaObject.objects.create(
                                    ruta=self,
                                    momento=momento,
                                    tipo=momento.tipo,
                                    estado='asignado',
                                    valor=0
                                )


        else:

            for key in tipos.keys():

                valor_total = tipos[key]['valor']  # valor total del tipo de momento
                cantidad_momentos = momentos.filter(tipo=key).exclude(nombre = 'Visita 1').count()  # cantidad total de momentos del componente
                procesados = self.clean_objetos(key)  # query de objetos pagos o reportados
                valor_procesados = procesados.aggregate(Sum('valor'))['valor__sum']
                if valor_procesados == None:
                    valor_procesados = 0

                nueva_meta = (cantidad_momentos * tipos[key]['meta']) - procesados.filter(ruta=self).exclude(translado=True).exclude(momento__nombre="Visita 1").count()
                nuevo_valor_total = valor_total - float(valor_procesados)

                try:
                    valor_momento = nuevo_valor_total / nueva_meta
                except:
                    pass

                else:

                    print("Valor total: {0}".format(valor_total))

                    for momento in momentos.filter(tipo=key).exclude(nombre = 'Visita 1'):

                        for i in range(0,tipos[key]['meta'] - procesados.filter(ruta=self, momento=momento).exclude(translado=True).count()):
                            CuposRutaObject.objects.create(
                                ruta=self,
                                momento=momento,
                                tipo=momento.tipo,
                                estado='asignado',
                                valor=0
                            )


        for key in tipos.keys():

            valor_total = tipos[key]['valor']

            valor_pagados = CuposRutaObject.objects.filter(ruta = self, estado__in = ["Reportado","Pagado"], momento__tipo = key).aggregate(Sum('valor'))['valor__sum']


            if valor_pagados == None:
                valor_pagados = 0


            if valor_total > valor_pagados:

                valor_dividir = float(valor_total) - float(valor_pagados)

                objetos_creados = CuposRutaObject.objects.filter(ruta=self, estado = 'asignado', tipo = key)

                if objetos_creados.count() > 0:

                    valor_objeto = valor_dividir/objetos_creados.count()

                    objetos_creados.update(valor = valor_objeto)


        #valor_total = 0

        #for key in tipos.keys():
        #    valor_total += float(tipos[key]['valor'])


        #valor_objetos = CuposRutaObject.objects.filter(ruta = self).aggregate(Sum('valor'))['valor__sum']

        #if valor_objetos == None:
        #    valor_objetos = float(0)

        #else:
        #    valor_objetos = float(valor_objetos)


        #if valor_objetos < valor_total:

        #    adicional = valor_total - valor_objetos


        #    cantidad = CuposRutaObject.objects.filter(ruta = self, estado = 'asignado').count()


        #    if cantidad > 0:

        #        sumando = adicional / cantidad

        #        for cupo in CuposRutaObject.objects.filter(ruta = self, estado = 'asignado'):

        #            cupo.valor = float(cupo.valor.amount) + float(sumando)
        #            cupo.save()



        return 'Ok'

    def get_instrumentos_list(self,momento,hogar):

        instrumentos_return = []

        for instrumento in Instrumentos.objects.filter(momento = momento).order_by('consecutivo'):
            if InstrumentosRutaObject.objects.filter(ruta=self,momento = momento,hogar = hogar,instrumento = instrumento).count() == 0:
                instrumentos_return.append({
                    'id': instrumento.id,
                    'short_name': instrumento.short_name,
                    'icon': instrumento.icon,
                    'color': instrumento.color
                })

        return instrumentos_return

    def get_valor_corte(self):
        objetos = CuposRutaObject.objects.filter(estado = "Reportado", ruta = self).exclude(momento__tipo = 'vinculacion')
        valor = objetos.aggregate(Sum('valor'))['valor__sum']
        return valor if valor != None else 0

    def get_cupo_componente(self,componente):

        if componente.consecutivo == 1:
            cupos = self.meta_hogares - Hogares.objects.filter(ruta_1=self).count()

        elif componente.consecutivo == 2:
            cupos = self.meta_hogares - Hogares.objects.filter(ruta_2=self).count()

        elif componente.consecutivo == 3:
            cupos = self.meta_hogares - Hogares.objects.filter(ruta_3=self).count()

        elif componente.consecutivo == 4:
            cupos = self.meta_hogares - Hogares.objects.filter(ruta_4=self).count()

        else:
            cupos = 0

        return cupos


    def get_cupo_vinculacion(self):

        cupos = self.meta_vinculacion - Hogares.objects.filter(ruta_vinculacion=self).count()

        return cupos


class Hogares(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)

    documento = models.BigIntegerField(unique=True)
    municipio = models.ForeignKey(Municipios, on_delete=models.DO_NOTHING, related_name='hogares_municipio_inscripcion')

    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100,blank=True,null=True)
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100,blank=True,null=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=100,blank=True,null=True)
    celular1 = models.CharField(max_length=100,blank=True,null=True)
    celular2 = models.CharField(max_length=100,blank=True,null=True)
    municipio_residencia = models.ForeignKey(Municipios, on_delete=models.DO_NOTHING, related_name='hogares_municipio_residencia')

    ruta_1 = models.ForeignKey(Rutas,on_delete=models.DO_NOTHING, related_name='ruta1_hogares',blank=True,null=True)
    ruta_2 = models.ForeignKey(Rutas, on_delete=models.DO_NOTHING, related_name='ruta2_hogares', blank=True, null=True)
    ruta_3 = models.ForeignKey(Rutas, on_delete=models.DO_NOTHING, related_name='ruta3_hogares', blank=True, null=True)
    ruta_4 = models.ForeignKey(Rutas, on_delete=models.DO_NOTHING, related_name='ruta4_hogares', blank=True, null=True)
    ruta_vinculacion = models.ForeignKey(Rutas, on_delete=models.DO_NOTHING, related_name='ruta_vinculacion_hogares', blank=True, null=True)


    id_elegible = models.IntegerField(blank=True, null=True)
    id_archivo = models.IntegerField(blank=True, null=True)
    zona_microfocalizada = models.IntegerField(blank=True,null=True)
    id_tipo_documento = models.IntegerField(blank=True, null=True)
    genero = models.IntegerField(blank=True, null=True)
    id_zona = models.IntegerField(blank=True, null=True)

    codigo_corregimiento = models.IntegerField(blank=True,null=True)
    nombre_corregimiento = models.CharField(max_length=1000, blank=True, null=True)
    codigo_vereda = models.IntegerField(blank=True, null=True)
    nombre_vereda = models.CharField(max_length=1000, blank=True, null=True)
    ubicacion = models.CharField(max_length=1000, blank=True, null=True)
    barrio = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=1000, blank=True, null=True)

    cabeza_hogar = models.BooleanField(default=False)
    dependientes = models.IntegerField(blank=True, null=True)
    tiene_tierra = models.BooleanField(default=False)
    area_tierra = models.FloatField(blank=True, null=True)

    existe_mfa = models.IntegerField(blank=True, null=True)
    codigo_familia_mfa = models.IntegerField(blank=True, null=True)
    puntaje_mfa = models.FloatField(blank=True, null=True)

    existe_unidos = models.IntegerField(blank=True, null=True)
    area_unidos = models.FloatField(blank=True, null=True)
    puntaje_unidos = models.FloatField(blank=True, null=True)

    puntaje_sisben = models.FloatField(blank=True, null=True)

    folio = models.IntegerField(blank=True, null=True)

    hecho_victimizante = models.CharField(max_length=100, blank=True, null=True)
    fecha_hecho_victimizante = models.DateField(blank=True,null=True)

    puntaje_tiempo = models.FloatField(blank=True, null=True)
    puntaje_ssv = models.FloatField(blank=True, null=True)
    puntaje_total = models.FloatField(blank=True, null=True)


    def get_valor_ruta_vinculacion(self):
        valor = CuposRutaObject.objects.filter(hogar=self,momento__tipo='vinculacion',estado__in=['Reportado','Pagado']).aggregate(Sum('valor'))['valor__sum']
        return valor if valor != None else 0



    def get_nombre_ruta_componente(self,componente):


        ruta = ''


        if componente.consecutivo == 1:
            if self.ruta_1 != None:
                ruta = self.ruta_1.nombre

        elif componente.consecutivo == 2:
            if self.ruta_2 != None:
                ruta = self.ruta_2.nombre

        elif componente.consecutivo == 3:
            if self.ruta_3 != None:
                ruta = self.ruta_3.nombre

        elif componente.consecutivo == 4:
            if self.ruta_4 != None:
                ruta = self.ruta_4.nombre

        return ruta



    def get_ruta_componente(self,componente):


        ruta = None


        if componente.consecutivo == 1:
            if self.ruta_1 != None:
                ruta = self.ruta_1

        elif componente.consecutivo == 2:
            if self.ruta_2 != None:
                ruta = self.ruta_2

        elif componente.consecutivo == 3:
            if self.ruta_3 != None:
                ruta = self.ruta_3

        elif componente.consecutivo == 4:
            if self.ruta_4 != None:
                ruta = self.ruta_4

        return ruta



    def get_nombre_ruta_vinculacion(self):

        ruta = ''

        if self.ruta_vinculacion != None:
            ruta = self.ruta_vinculacion.nombre

        return ruta



    def get_ruta_vinculacion(self):

        ruta = None

        if self.ruta_vinculacion != None:
            ruta = self.ruta_vinculacion

        return ruta



    def get_vinculacion_ruta(self, ruta):
        respuesta = 'No'

        if self.ruta_vinculacion == ruta:
            respuesta = 'Si'

        return respuesta


    def get_estado_valor(self,ruta,momento):
        estado = ''
        try:
            obj = CuposRutaObject.objects.get(ruta=ruta,momento=momento,hogar=self)
        except:
            pass
        else:
            estado = str(obj.valor).replace('COL','')
        return estado


    def get_estado(self,ruta,momento):
        estado = ''
        try:
            obj = CuposRutaObject.objects.get(ruta=ruta,momento=momento,hogar=self)
        except:
            pass
        else:
            estado = obj.estado
        return estado


    def get_cantidad_instrumentos(self):
        return InstrumentosRutaObject.objects.filter(hogar = self).count()


    def get_novedades_mis_rutas_momento(self,ruta,momento):
        return InstrumentosRutaObject.objects.filter(ruta = ruta, momento = momento, hogar = self, estado__in = ['cargado','preaprobado']).count()


    def get_nombres(self):
        if self.segundo_nombre != None:
            nombres = '{0} {1}'.format(self.primer_nombre,self.segundo_nombre)
        else:
            nombres = self.primer_nombre
        return nombres

    def get_apellidos(self):
        if self.segundo_apellido != None:
            apellidos = '{0} {1}'.format(self.primer_apellido,self.segundo_apellido)
        else:
            apellidos = self.primer_apellido
        return apellidos

    def get_full_name(self):
        return '{0} {1}'.format(self.get_nombres(),self.get_apellidos())


    def get_gull_name(self):
        return '{0} {1}'.format(self.get_nombres(),self.get_apellidos())


    def get_cantidad_miembros(self):
        return MiembroNucleoHogar.objects.filter(hogar=self).count()


    def get_valor_total(self):
        valor = CuposRutaObject.objects.filter(hogar=self).aggregate(Sum('valor'))['valor__sum']
        return valor if valor != None else 0

    def get_cantidad_componentes(self):
        return CuposRutaObject.objects.filter(hogar=self).values_list('momento__componente__id',flat=True).distinct().count()

    def get_valor_vinculacion(self):
        valor = CuposRutaObject.objects.filter(hogar=self,momento__tipo='vinculacion').aggregate(Sum('valor'))['valor__sum']
        return valor if valor != None else 0





class MiembroNucleoHogar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    hogar = models.ForeignKey(Hogares,on_delete=models.DO_NOTHING,related_name='hogar_miembro_nucleo')


    #Datos personales

    tipo_documento = models.CharField(max_length=100,blank=True,null=True)
    numero_documento = models.IntegerField(blank=True,null=True)
    primer_apellido = models.CharField(max_length=100,blank=True,null=True)
    segundo_apellido = models.CharField(max_length=100,blank=True, null=True)
    primer_nombre = models.CharField(max_length=100,blank=True,null=True)
    segundo_nombre = models.CharField(max_length=100,blank=True, null=True)
    celular_1 = models.CharField(max_length=100,blank=True,null=True)
    celular_2 = models.CharField(max_length=100,blank=True, null=True)
    correo_electronico = models.EmailField(max_length=100,blank=True, null=True)

    # Lugar y fecha de nacimiento

    departamento_nacimiento = models.ForeignKey(Departamentos, on_delete=models.DO_NOTHING,related_name='departamento_nacimiento_miembro_nucleo',blank=True,null=True)
    municipio_nacimiento = models.ForeignKey(Municipios, on_delete=models.DO_NOTHING,related_name='municipio_nacimiento_miembro_nucleo',blank=True,null=True)
    fecha_nacimiento = models.DateField(blank=True,null=True)

    # Lugar y fecha de expedición del documento

    departamento_expedicion = models.ForeignKey(Departamentos, on_delete=models.DO_NOTHING,related_name='departamento_expedicion_miembro_nucleo',blank=True,null=True)
    municipio_expedicion = models.ForeignKey(Municipios, on_delete=models.DO_NOTHING,related_name='municipio_expedicion_miembro_nucleo',blank=True,null=True)
    fecha_expedicion = models.DateField(blank=True,null=True)

    longitud = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    latitud = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    precision = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    altitud = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)

    # -------------------------------------------------------------

    # Caracteristicas generales

    sexo = models.CharField(max_length=100,blank=True,null=True)
    tiene_libreta = models.BooleanField(default=False,blank=True,null=True)
    numero_libreta = models.CharField(max_length=100, blank=True, null=True)

    identidad_genero = models.CharField(max_length=100, blank=True, null=True)
    condicion_sexual = models.CharField(max_length=100, blank=True, null=True)
    estado_civil = models.CharField(max_length=100,blank=True,null=True)
    etnia = models.CharField(max_length=100,blank=True,null=True)

    pueblo_indigena = models.ForeignKey(PueblosIndigenas, on_delete=models.DO_NOTHING, blank=True, null=True)#aparece si se selecciona "INDIGENA" en la etnia
    resguardo_indigena = models.ForeignKey(ResguardosIndigenas, on_delete=models.DO_NOTHING, blank=True, null=True)  # aparece si se selecciona "INDIGENA" en la etnia
    comunidad_indigena = models.ForeignKey(ComunidadesIndigenas, on_delete=models.DO_NOTHING, blank=True, null=True)  # aparece si se selecciona "INDIGENA" en la etnia
    lengua_nativa_indigena = models.BooleanField(blank=True,null=True)  # aparece si se selecciona "INDIGENA" en la etnia
    cual_lengua_indigena = models.ForeignKey(LenguasNativas, related_name='lengua_indigena_miembro_nucleo', on_delete=models.DO_NOTHING,blank=True,null=True)# aparece si se selecciona "INDIGENA" en la etnia y si se activa lengua nativa

    consejo_afro = models.ForeignKey(ConsejosAfro, on_delete=models.DO_NOTHING,blank=True,null=True)#aparece si se selecciona "AFROCOLOMBIANO" en la etnia
    comunidad_afro = models.ForeignKey(ComunidadesAfro, on_delete=models.DO_NOTHING, blank=True,null=True)  # aparece si se selecciona "AFROCOLOMBIANO" en la etnia
    lengua_nativa_afro = models.BooleanField(blank=True,null=True)  # aparece si se selecciona "AFROCOLOMBIANO" en la etnia
    cual_lengua_afro = models.ForeignKey(LenguasNativas, related_name='lengua_afro_miembro_nucleo', on_delete=models.DO_NOTHING, blank=True,null=True)  # aparece si se selecciona "AFROCOLOMBIANO" en la etnia y si se activa lengua nativa

    discapacidad = models.BooleanField(blank=True,null=True)

    registro_discapacidad = models.CharField(max_length=100,blank=True,null=True) #aparece si hay discapacidad
    categoria_discapacidad = models.ManyToManyField(CategoriaDiscapacidad, blank=True) #aparece si hay discapacidad
    dificultades_permanentes = models.ManyToManyField(DificultadesPermanentesDiscapacidad, blank=True) #aparece si hay discapacidad
    utiliza_actualmente = models.ManyToManyField(ElementosDiscapacidad, blank=True) #aparece si hay discapacidad
    rehabilitacion = models.ManyToManyField(TiposRehabilitacionDiscapacidad, blank=True) #aparece si hay discapacidad
    tiene_cuidador = models.BooleanField(blank=True,null=True) #aparece si hay discapacidad
    cuidador = models.CharField(max_length=100,blank=True,null=True)

    parentezco = models.CharField(max_length=100,blank=True,null=True)
    es_jefe = models.BooleanField(blank=True,null=True)

    nivel_escolaridad = models.CharField(max_length=100,blank=True,null=True)
    grado_titulo = models.CharField(max_length=100,blank=True,null=True)
    sabe_leer = models.BooleanField(blank=True,null=True)
    sabe_sumar_restar = models.BooleanField(blank=True,null=True)
    actualmente_estudia = models.BooleanField(blank=True,null=True)
    recibe_alimentos = models.BooleanField(blank=True,null=True)

    razon_no_estudia = models.CharField(max_length=100, blank=True, null=True)  # se activa si no estudia
    razon_no_estudia_otra = models.CharField(max_length=100, blank=True, null=True)  # se activa si no estudia y hay otra razon
    regimen_seguridad_social = models.CharField(max_length=100,blank=True,null=True)


    def get_str_list_categoria_discapacidad(self):
        string = ', '

        for categoria in self.categoria_discapacidad.all():
            string += categoria.nombre + ', '

        return string[:-2]

    def get_str_list_dificultades_permanentes(self):
        string = ', '

        for categoria in self.dificultades_permanentes.all():
            string += categoria.nombre + ', '

        return string[:-2]

    def get_str_list_utiliza_actualmente(self):
        string = ', '

        for categoria in self.utiliza_actualmente.all():
            string += categoria.nombre + ', '

        return string[:-2]

    def get_str_list_rehabilitacion(self):
        string = ', '

        for categoria in self.rehabilitacion.all():
            string += categoria.nombre + ', '

        return string[:-2]


    def get_fullname(self):
        return '{0} {1} {2} {3}'.format(self.primer_nombre,self.segundo_nombre,self.primer_apellido,self.segundo_apellido)



class PermisosCuentasRutas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING)
    rutas_ver = models.ManyToManyField(Rutas,related_name="permisos_cuentas_ver",blank=True)
    rutas_preaprobar = models.ManyToManyField(Rutas,related_name="permisos_cuentas_preaprobar",blank=True)
    rutas_aprobar = models.ManyToManyField(Rutas,related_name="permisos_cuentas_aprobar",blank=True)

    def __str__(self):
        return self.user.email



class InstrumentosRutaObject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='instrumento_usuario_creacion',blank=True,null=True)

    ruta = models.ForeignKey(Rutas, on_delete=models.DO_NOTHING, related_name='instrumento_ruta')
    momento = models.ForeignKey(Momentos, on_delete=models.DO_NOTHING, related_name='instrumento_momento')
    hogar = models.ForeignKey(Hogares, on_delete=models.DO_NOTHING, related_name='instrumento_hogar')
    instrumento = models.ForeignKey(Instrumentos, on_delete=models.DO_NOTHING, related_name='instrumento_instrumento',blank=True,null=True)

    modelo = models.CharField(max_length=100)
    soporte = models.UUIDField(blank=True,null=True)
    observacion = models.TextField(blank=True,null=True)
    fecha_actualizacion = models.DateTimeField(blank=True,null=True)
    usuario_actualizacion = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='instrumento_usuario_actualizacion',blank=True,null=True)
    estado = models.CharField(max_length=100,blank=True,null=True)
    nombre = models.CharField(max_length=100,blank=True,null=True)
    consecutivo = models.IntegerField(blank=True,null=True)


class ObservacionesInstrumentoRutaObject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    instrumento = models.ForeignKey(InstrumentosRutaObject, on_delete=models.DO_NOTHING)
    creacion = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='instrumento_observacion_usuario_creacion',blank=True, null=True)
    observacion = models.TextField(blank=True,null=True)


    def pretty_creation_datetime(self):
        return self.creacion.astimezone(settings_time_zone).strftime('%d/%m/%Y - %I:%M:%S %p')



class InstrumentosTrazabilidadRutaObject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    instrumento = models.ForeignKey(InstrumentosRutaObject,on_delete=models.DO_NOTHING,related_name="trazabilidad_instrumento")
    creacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='trazabilidad_instrumento_usuario')
    observacion = models.TextField()



class Cortes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    consecutivo = models.IntegerField()
    creation = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='cortes_usuario_creacion_fest')
    valor = MoneyField(max_digits=10, decimal_places=2, default_currency='COP', default=0, blank=True, null=True)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion


    def pretty_creation_datetime(self):
        return self.creation.astimezone(settings_time_zone).strftime('%d/%m/%Y - %I:%M:%S %p')


    def get_valor(self):
        valor = CuposRutaObject.objects.filter(corte = self).aggregate(Sum('valor'))['valor__sum']
        return valor if valor != None else 0


    def get_novedades(self):
        cuentas_cobro = CuentasCobro.objects.filter(corte = self, estado__in = ['Creado', 'Cargado'])
        return cuentas_cobro.count()

    def get_cantidad_cuentas_cobro(self):
        return CuentasCobro.objects.filter(corte = self).count()

    def create_cuentas_cobro(self, user):
        objetos = CuposRutaObject.objects.filter(corte = self, estado = "Pagado")
        rutas_ids = objetos.values_list('ruta__id', flat=True).distinct()
        for ruta_id in rutas_ids:
            ruta = Rutas.objects.get(id = ruta_id)

            try:
                cuenta_cobro = CuentasCobro.objects.get(
                    ruta = ruta,
                    corte = self
                )
            except:

                valor = objetos.filter(ruta = ruta).aggregate(Sum('valor'))['valor__sum']

                if valor == None:
                    valor = 0

                cuenta_cobro = CuentasCobro.objects.create(
                    ruta = ruta,
                    corte = self,
                    usuario_creacion = user,
                    estado = 'Creado',
                    valor = valor
                )

            else:
                pass


        return None





def upload_dinamic_cuentas_cobro(instance, filename):
    return '/'.join(['FEST 2019', 'Cuentas de Cobro', str(instance.id), filename])

class CuentasCobro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    ruta = models.ForeignKey(Rutas, on_delete=models.DO_NOTHING)
    creation = models.DateTimeField(auto_now_add=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True,related_name='cuentas_cobro_usuario_creacion_fest')

    fecha_actualizacion = models.DateTimeField(blank=True,null=True)
    usuario_actualizacion = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='usuario_actualizacion_cuentas_cobro_fest')

    corte = models.ForeignKey(Cortes, on_delete = models.DO_NOTHING, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    valor = MoneyField(max_digits=10, decimal_places=2, default_currency='COP', default=0, blank=True, null=True)
    file = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_cuentas_cobro,
        content_types=['application/pdf'],
        max_upload_size=5242880,
        max_length=255,
        blank=True,
        null=True
    )
    file2 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_cuentas_cobro,
        content_types=['application/pdf'],
        max_upload_size=5242880,
        max_length=255,
        blank=True,
        null=True
    )
    html = models.FileField(upload_to=upload_dinamic_cuentas_cobro, blank=True, null=True)
    delta = models.TextField(blank=True, null=True)
    data_json = models.TextField(blank=True,null=True)
    valores_json = models.TextField(default='[]',blank=True,null=True)
    observaciones = models.TextField(default='',blank=True,null=True)



    def pretty_creation_datetime(self):
        return self.creation.astimezone(settings_time_zone).strftime('%d/%m/%Y - %I:%M:%S %p')

    def create_delta(self):
        from fest_2019.functions import delta_cuenta_cobro
        self.delta = json.dumps(delta_cuenta_cobro(self))
        self.save()
        return None

    def get_html_delta(self):
        delta = json.loads(self.delta)
        return html.render(delta['ops'])

    def url_file(self):
        url = None
        try:
            url = self.file.url
        except:
            pass
        return url

    def url_file2(self):
        url = None
        try:
            url = self.file2.url
        except:
            pass
        return url

    def pretty_print_url_file2(self):
        try:
            url = self.file2.url
        except:
            return '<p style="display:inline;margin-left:5px;">No hay archivos cargados.</p>'
        else:
            return '<a href="'+ url +'"> '+ str(self.file2.name) +'</a>'



class CuposRutaObject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)

    ruta = models.ForeignKey(Rutas,on_delete=models.DO_NOTHING,related_name='cupo_ruta')
    momento = models.ForeignKey(Momentos,on_delete=models.DO_NOTHING,related_name='cupo_momento')
    tipo = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    valor = MoneyField(max_digits=10, decimal_places=2, default_currency='COP', default=0)
    hogar = models.ForeignKey(Hogares,on_delete=models.DO_NOTHING,related_name='cupo_hogar',blank=True,null=True)
    corte = models.ForeignKey(Cortes, on_delete=models.DO_NOTHING, blank=True, null=True)
    translado = models.BooleanField(default=False)




def upload_dinamic_fest(instance, filename):
    return '/'.join(['FEST 2019', str(instance.hogar.id), instance.nombre, filename])

class Documento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    hogar = models.ForeignKey(Hogares,on_delete=models.DO_NOTHING,related_name='hogar_documento')
    instrumento = models.ForeignKey(Instrumentos,on_delete=models.DO_NOTHING,related_name='instrumento_documento',blank=True,null=True)
    nombre = models.CharField(max_length=100)

    file = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'application/pdf',
        ],
        max_upload_size=10485760,
        max_length=255
    )



    def url_file(self):
        url = None
        try:
            url = self.file.url
        except:
            pass
        return url


    def get_extension(self):
        return self.file.name.split('.')[-1]


class DocumentoExcel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    hogar = models.ForeignKey(Hogares,on_delete=models.DO_NOTHING,related_name='hogar_documento_excel')
    instrumento = models.ForeignKey(Instrumentos,on_delete=models.DO_NOTHING,related_name='instrumento_documento_excel',blank=True,null=True)
    nombre = models.CharField(max_length=100)

    file = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ],
        max_upload_size=10485760,
        max_length=255
    )



    def url_file(self):
        url = None
        try:
            url = self.file.url
        except:
            pass
        return url


    def get_extension(self):
        return self.file.name.split('.')[-1]


class Fotos4(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    hogar = models.ForeignKey(Hogares,on_delete=models.DO_NOTHING,related_name='hogar_fotos4')
    instrumento = models.ForeignKey(Instrumentos,on_delete=models.DO_NOTHING,related_name='instrumento_fotos4',blank=True,null=True)
    nombre = models.CharField(max_length=100)

    foto1 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255,
    )
    foto2 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255
    )
    foto3 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255
    )
    foto4 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255
    )



    def url_foto1(self):
        url = None
        try:
            url = self.foto1.url
        except:
            pass
        return url

    def url_foto2(self):
        url = None
        try:
            url = self.foto2.url
        except:
            pass
        return url

    def url_foto3(self):
        url = None
        try:
            url = self.foto3.url
        except:
            pass
        return url

    def url_foto4(self):
        url = None
        try:
            url = self.foto4.url
        except:
            pass
        return url

class Fotos5(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    hogar = models.ForeignKey(Hogares,on_delete=models.DO_NOTHING,related_name='hogar_fotos5')
    instrumento = models.ForeignKey(Instrumentos,on_delete=models.DO_NOTHING,related_name='instrumento_fotos5',blank=True,null=True)
    nombre = models.CharField(max_length=100)

    foto1 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255,
    )
    foto2 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255
    )
    foto3 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255
    )
    foto4 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255
    )
    foto5 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255
    )


    def url_foto1(self):
        url = None
        try:
            url = self.foto1.url
        except:
            pass
        return url

    def url_foto2(self):
        url = None
        try:
            url = self.foto2.url
        except:
            pass
        return url

    def url_foto3(self):
        url = None
        try:
            url = self.foto3.url
        except:
            pass
        return url

    def url_foto4(self):
        url = None
        try:
            url = self.foto4.url
        except:
            pass
        return url

    def url_foto5(self):
        url = None
        try:
            url = self.foto5.url
        except:
            pass
        return url


class Fotos6(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    hogar = models.ForeignKey(Hogares,on_delete=models.DO_NOTHING,related_name='hogar_fotos6')
    instrumento = models.ForeignKey(Instrumentos,on_delete=models.DO_NOTHING,related_name='instrumento_fotos6',blank=True,null=True)
    nombre = models.CharField(max_length=100)

    foto1 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255,
    )
    foto2 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255
    )
    foto3 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255
    )
    foto4 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255
    )
    foto5 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255
    )
    foto6 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255,
    )


    def url_foto1(self):
        url = None
        try:
            url = self.foto1.url
        except:
            pass
        return url

    def url_foto2(self):
        url = None
        try:
            url = self.foto2.url
        except:
            pass
        return url

    def url_foto3(self):
        url = None
        try:
            url = self.foto3.url
        except:
            pass
        return url

    def url_foto4(self):
        url = None
        try:
            url = self.foto4.url
        except:
            pass
        return url

    def url_foto5(self):
        url = None
        try:
            url = self.foto5.url
        except:
            pass
        return url

    def url_foto6(self):
        url = None
        try:
            url = self.foto6.url
        except:
            pass
        return url


class Fotos1(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    hogar = models.ForeignKey(Hogares,on_delete=models.DO_NOTHING,related_name='hogar_fotos1')
    instrumento = models.ForeignKey(Instrumentos,on_delete=models.DO_NOTHING,related_name='instrumento_fotos1',blank=True,null=True)
    nombre = models.CharField(max_length=100)

    foto1 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255,
    )


    def url_foto1(self):
        url = None
        try:
            url = self.foto1.url
        except:
            pass
        return url




class ArchivoRarZip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    hogar = models.ForeignKey(Hogares,on_delete=models.DO_NOTHING,related_name='hogar_rar_zip')
    instrumento = models.ForeignKey(Instrumentos,on_delete=models.DO_NOTHING,related_name='instrumento_rar_zip',blank=True,null=True)
    nombre = models.CharField(max_length=100)

    file = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'application/x-rar-compressed',
            'application/zip',
            'application/x-7z-compressed'
        ],
        max_upload_size=10485760,
        max_length=255,
    )


    def url_file(self):
        url = None
        try:
            url = self.file.url
        except:
            pass
        return url



class Fotos2(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    hogar = models.ForeignKey(Hogares,on_delete=models.DO_NOTHING,related_name='hogar_fotos2')
    instrumento = models.ForeignKey(Instrumentos,on_delete=models.DO_NOTHING,related_name='instrumento_fotos2',blank=True,null=True)
    nombre = models.CharField(max_length=100)

    foto1 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255,
    )

    foto2 = ContentTypeRestrictedFileField(
        upload_to=upload_dinamic_fest,
        content_types=[
            'image/jpg',
            'image/jpeg',
            'image/png'
        ],
        max_upload_size=10485760,
        max_length=255,
    )


    def url_foto1(self):
        url = None
        try:
            url = self.foto1.url
        except:
            pass
        return url

    def url_foto2(self):
        url = None
        try:
            url = self.foto2.url
        except:
            pass
        return url

class CaracterizacionInicial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    hogar = models.ForeignKey(Hogares,on_delete=models.DO_NOTHING,related_name='hogar_caracterizacion_inicial')
    instrumento = models.ForeignKey(Instrumentos,on_delete=models.DO_NOTHING,related_name='instrumento_caracterizacion_inicial',blank=True,null=True)
    nombre = models.CharField(max_length=100,blank=True,null=True)

    # -------------------------------------------------------------

    #lugar de atencion
    departamento_atencion = models.ForeignKey(Departamentos,on_delete=models.DO_NOTHING,related_name='departamento_atencion_caracterizacion_inicial',blank=True,null=True)
    municipio_atencion = models.ForeignKey(Municipios, on_delete=models.DO_NOTHING,related_name='municipio_atencion_caracterizacion_inicial',blank=True,null=True)

    #lugar de residencia
    departamento_residencia = models.ForeignKey(Departamentos, on_delete=models.DO_NOTHING,related_name='departamento_residencia_caracterizacion_inicial',blank=True,null=True)
    municipio_residencia = models.ForeignKey(Municipios, on_delete=models.DO_NOTHING,related_name='municipio_residencia_caracterizacion_inicial',blank=True,null=True)
    zona_residencia = models.CharField(max_length=100,blank=True,null=True)

    localidad = models.CharField(max_length=1000,blank=True,null=True) #aparece si se selecciona "cabecera municipal" en la zona de residencia
    barrio = models.CharField(max_length=1000,blank=True,null=True) #aparece si se selecciona "cabecera municipal" en la zona de residencia
    direccion_predio = models.CharField(max_length=1000,blank=True,null=True) #aparece si se selecciona "cabecera municipal" en la zona de residencia

    corregimiento = models.ForeignKey(Corregimientos,on_delete=models.DO_NOTHING,blank=True,null=True) #aparece si se selecciona las opciones "centro poblado" o "rural disperso"
    vereda = models.ForeignKey(Veredas,on_delete=models.DO_NOTHING, blank=True,null=True)  # aparece si se selecciona las opciones "centro poblado" o "rural disperso"
    ubicacion_predio = models.CharField(max_length=1000, blank=True,null=True)  # aparece si se selecciona las opciones "centro poblado" o "rural disperso"

    telefono_fijo = models.CharField(max_length=100,blank=True,null=True)


    tipo_vivienda = models.CharField(max_length=100,blank=True,null=True)
    otro_tipo_vivienda = models.CharField(max_length=100,blank=True,null=True)#aparece si se selecciona "Otro tipo de vivienda"

    propiedad_vivienda = models.CharField(max_length=100,blank=True,null=True)
    estrato_vivienda = models.CharField(max_length=100,blank=True,null=True)

    #-------------------------------------------------------------

    #información sobre la familia

    otro_telefono = models.CharField(max_length=100, blank=True, null=True)
    descripcion_direccion = models.CharField(max_length=100, blank=True, null=True)
    numero_personas_familia = models.IntegerField(blank=True,null=True)
    menores_5_anios = models.IntegerField(blank=True,null=True)
    mayores_60_anios = models.IntegerField(blank=True,null=True)
    mujeres_gestantes_lactantes = models.IntegerField(blank=True,null=True)
    discapacitados_familia = models.IntegerField(blank=True,null=True)

    # -------------------------------------------------------------

    #Datos personales

    tipo_documento = models.CharField(max_length=100,blank=True,null=True)
    numero_documento = models.IntegerField(blank=True,null=True)
    primer_apellido = models.CharField(max_length=100,blank=True,null=True)
    segundo_apellido = models.CharField(max_length=100,blank=True, null=True)
    primer_nombre = models.CharField(max_length=100,blank=True,null=True)
    segundo_nombre = models.CharField(max_length=100,blank=True, null=True)
    celular_1 = models.CharField(max_length=100,blank=True,null=True)
    celular_2 = models.CharField(max_length=100,blank=True, null=True)
    correo_electronico = models.EmailField(max_length=100,blank=True, null=True)

    # Lugar y fecha de nacimiento

    departamento_nacimiento = models.ForeignKey(Departamentos, on_delete=models.DO_NOTHING,related_name='departamento_nacimiento_caracterizacion_inicial',blank=True,null=True)
    municipio_nacimiento = models.ForeignKey(Municipios, on_delete=models.DO_NOTHING,related_name='municipio_nacimiento_caracterizacion_inicial',blank=True,null=True)
    fecha_nacimiento = models.DateField(blank=True,null=True)

    # Lugar y fecha de expedición del documento

    departamento_expedicion = models.ForeignKey(Departamentos, on_delete=models.DO_NOTHING,related_name='departamento_expedicion_caracterizacion_inicial',blank=True,null=True)
    municipio_expedicion = models.ForeignKey(Municipios, on_delete=models.DO_NOTHING,related_name='municipio_expedicion_caracterizacion_inicial',blank=True,null=True)
    fecha_expedicion = models.DateField(blank=True,null=True)

    longitud = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    latitud = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    precision = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    altitud = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)

    # -------------------------------------------------------------

    # Caracteristicas generales

    sexo = models.CharField(max_length=100,blank=True,null=True)
    tiene_libreta = models.BooleanField(default=False,blank=True,null=True)
    numero_libreta = models.CharField(max_length=100, blank=True, null=True)

    identidad_genero = models.CharField(max_length=100, blank=True, null=True)
    condicion_sexual = models.CharField(max_length=100, blank=True, null=True)
    estado_civil = models.CharField(max_length=100,blank=True,null=True)
    etnia = models.CharField(max_length=100,blank=True,null=True)

    pueblo_indigena = models.ForeignKey(PueblosIndigenas, on_delete=models.DO_NOTHING, blank=True, null=True)#aparece si se selecciona "INDIGENA" en la etnia
    resguardo_indigena = models.ForeignKey(ResguardosIndigenas, on_delete=models.DO_NOTHING, blank=True, null=True)  # aparece si se selecciona "INDIGENA" en la etnia
    comunidad_indigena = models.ForeignKey(ComunidadesIndigenas, on_delete=models.DO_NOTHING, blank=True, null=True)  # aparece si se selecciona "INDIGENA" en la etnia
    lengua_nativa_indigena = models.BooleanField(blank=True,null=True)  # aparece si se selecciona "INDIGENA" en la etnia
    cual_lengua_indigena = models.ForeignKey(LenguasNativas, related_name='lengua_indigena', on_delete=models.DO_NOTHING,blank=True,null=True)# aparece si se selecciona "INDIGENA" en la etnia y si se activa lengua nativa

    consejo_afro = models.ForeignKey(ConsejosAfro, on_delete=models.DO_NOTHING,blank=True,null=True)#aparece si se selecciona "AFROCOLOMBIANO" en la etnia
    comunidad_afro = models.ForeignKey(ComunidadesAfro, on_delete=models.DO_NOTHING, blank=True,null=True)  # aparece si se selecciona "AFROCOLOMBIANO" en la etnia
    lengua_nativa_afro = models.BooleanField(blank=True,null=True)  # aparece si se selecciona "AFROCOLOMBIANO" en la etnia
    cual_lengua_afro = models.ForeignKey(LenguasNativas, related_name='lengua_afro', on_delete=models.DO_NOTHING, blank=True,null=True)  # aparece si se selecciona "AFROCOLOMBIANO" en la etnia y si se activa lengua nativa

    discapacidad = models.BooleanField(blank=True,null=True)

    registro_discapacidad = models.CharField(max_length=100,blank=True,null=True) #aparece si hay discapacidad
    categoria_discapacidad = models.ManyToManyField(CategoriaDiscapacidad, blank=True) #aparece si hay discapacidad
    dificultades_permanentes = models.ManyToManyField(DificultadesPermanentesDiscapacidad, blank=True) #aparece si hay discapacidad
    utiliza_actualmente = models.ManyToManyField(ElementosDiscapacidad, blank=True) #aparece si hay discapacidad
    rehabilitacion = models.ManyToManyField(TiposRehabilitacionDiscapacidad, blank=True) #aparece si hay discapacidad
    tiene_cuidador = models.BooleanField(blank=True,null=True) #aparece si hay discapacidad
    cuidador = models.CharField(max_length=100,blank=True,null=True)

    parentezco = models.CharField(max_length=100,blank=True,null=True)
    es_jefe = models.BooleanField(blank=True,null=True)
    es_representante_hogar = models.BooleanField(blank=True,null=True)

    bancarizacion = models.BooleanField(blank=True,null=True)
    banco = models.ForeignKey(Bancos,on_delete=models.DO_NOTHING,blank=True,null=True) # se activa si hay bancarizacion
    tipo_cuenta = models.CharField(max_length=100, blank=True, null=True) # se activa si hay bancarizacion
    numero_cuenta = models.CharField(max_length=100, blank=True, null=True) # se activa si hay bancarizacion

    nivel_escolaridad = models.CharField(max_length=100,blank=True,null=True)
    grado_titulo = models.CharField(max_length=100,blank=True,null=True)
    sabe_leer = models.BooleanField(blank=True,null=True)
    sabe_sumar_restar = models.BooleanField(blank=True,null=True)
    actualmente_estudia = models.BooleanField(blank=True,null=True)
    recibe_alimentos = models.BooleanField(blank=True,null=True)

    razon_no_estudia = models.CharField(max_length=100, blank=True, null=True)  # se activa si no estudia
    razon_no_estudia_otra = models.CharField(max_length=100, blank=True, null=True)  # se activa si no estudia y hay otra razon
    regimen_seguridad_social = models.CharField(max_length=100,blank=True,null=True)


    def get_str_list_categoria_discapacidad(self):
        string = ', '

        for categoria in self.categoria_discapacidad.all():
            string += categoria.nombre + ', '

        return string[:-2]

    def get_str_list_dificultades_permanentes(self):
        string = ', '

        for categoria in self.dificultades_permanentes.all():
            string += categoria.nombre + ', '

        return string[:-2]

    def get_str_list_utiliza_actualmente(self):
        string = ', '

        for categoria in self.utiliza_actualmente.all():
            string += categoria.nombre + ', '

        return string[:-2]

    def get_str_list_rehabilitacion(self):
        string = ', '

        for categoria in self.rehabilitacion.all():
            string += categoria.nombre + ', '

        return string[:-2]




class Contactos(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    municipio = models.ForeignKey(Municipios, on_delete=models.DO_NOTHING, related_name='hcontactos_municipio')
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    celular = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    resguardo = models.CharField(max_length=100)
    comunidad = models.CharField(max_length=100)
    lenguas = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.nombres