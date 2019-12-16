#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from fest_2019 import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Fieldset
from crispy_forms_materialize.layout import Layout, Row, Column, Submit, HTML, Button
from recursos_humanos import models as rh_models
from recursos_humanos.models import Contratistas, Contratos
from django.db.models import Q
from django.conf import settings
import openpyxl
from dal import autocomplete
from django.forms.fields import Field, FileField
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
import json
from cpe_2018.widgets import SelectWithDisabled
from django.utils import timezone
from usuarios.models import Municipios,Departamentos, Corregimientos, Veredas, PueblosIndigenas, ResguardosIndigenas, \
    ComunidadesIndigenas ,LenguasNativas, ConsejosAfro, ComunidadesAfro, CategoriaDiscapacidad, \
    DificultadesPermanentesDiscapacidad, ElementosDiscapacidad, TiposRehabilitacionDiscapacidad
from direccion_financiera.models import Bancos
from django.db.models import Sum


class HogarCreateForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(HogarCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Información del hogar',
                )
            ),
            Row(
                Column(
                    'documento',css_class="s12 m6 l4"
                ),
                Column(
                    'primer_nombre', css_class="s12 m6 l4"
                ),
                Column(
                    'segundo_nombre', css_class="s12 m6 l4"
                ),
            ),
            Row(
                Column(
                    'primer_apellido', css_class="s12 m6 l4"
                ),
                Column(
                    'segundo_apellido', css_class="s12 m6 l4"
                ),
                Column(
                    'fecha_nacimiento', css_class="s12 m6 l4"
                )
            ),
            Row(
                Column(
                    'municipio', css_class="s12 m6 "
                ),
                Column(
                    'municipio_residencia', css_class="s12 m6 "
                ),
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )

    class Meta:
        model = models.Hogares
        fields = ['documento','municipio','primer_nombre','segundo_nombre','primer_apellido','segundo_apellido','fecha_nacimiento',
                  'municipio_residencia']
        widgets = {
        }

class HogarUpdateForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(HogarUpdateForm, self).__init__(*args, **kwargs)


        hogar = models.Hogares.objects.get(id = self.initial['pk'])

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Información del hogar',
                )
            ),
            Row(
                Column(
                    HTML("""<p>Cedula: {0}</p>""".format(hogar.documento))
                ),
            ),
            Row(
                Column(
                    'primer_nombre', css_class="s12 m6 l6"
                ),
                Column(
                    'segundo_nombre', css_class="s12 m6 l6"
                ),
            ),
            Row(
                Column(
                    'primer_apellido', css_class="s12 m6 l4"
                ),
                Column(
                    'segundo_apellido', css_class="s12 m6 l4"
                ),
                Column(
                    'fecha_nacimiento', css_class="s12 m6 l4"
                )
            ),
            Row(
                Column(
                    'municipio', css_class="s12 m6 "
                ),
                Column(
                    'municipio_residencia', css_class="s12 m6 "
                ),
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )

    class Meta:
        model = models.Hogares
        fields = ['municipio','primer_nombre','segundo_nombre','primer_apellido','segundo_apellido','fecha_nacimiento',
                  'municipio_residencia']
        widgets = {
        }

class RutasCreateForm(forms.Form):

    contrato = forms.ModelChoiceField(label='Contrato', queryset=rh_models.Contratos.objects.none())
    nombre = forms.CharField(label='Código ruta', max_length=100)
    componente = forms.ModelChoiceField(label='Componente', queryset=models.Componentes.objects.all())
    valor_transporte = forms.CharField(label='Valor transporte del contrato',max_length=100)
    tipo_pago = forms.CharField(label="Tipo de pago",widget=forms.Select(choices=[('completo','Al completar todas las actividades'),('actividad','Por actividad')]))


    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            if name not in ['contrato','nombre']:
                if field.disabled:
                    value = self.get_initial_for_field(field, name)
                else:
                    value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
                try:
                    if isinstance(field, FileField):
                        initial = self.get_initial_for_field(field, name)
                        value = field.clean(value, initial)
                    else:
                        value = field.clean(value)

                        if name == 'nombre':
                            try:
                                models.Rutas.objects.get(nombre = value)
                            except:
                                pass
                            else:
                                self.add_error(name, 'El nombre de la ruta ya existe')

                    self.cleaned_data[name] = value
                    if hasattr(self, 'clean_%s' % name):
                        value = getattr(self, 'clean_%s' % name)()
                        self.cleaned_data[name] = value
                except ValidationError as e:
                    self.add_error(name, e)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
                self.cleaned_data[name] = value


    def __init__(self, *args, **kwargs):
        super(RutasCreateForm, self).__init__(*args, **kwargs)
        ruta = None

        if 'pk' in kwargs['initial']:
            ruta = models.Rutas.objects.get(id = kwargs['initial']['pk'])
            self.fields['nombre'].initial = ruta.nombre
            self.fields['contrato'].queryset = rh_models.Contratos.objects.filter(id = ruta.contrato.id)
            self.fields['contrato'].initial = ruta.contrato
            self.fields['valor_transporte'].initial = str(ruta.valor_transporte.amount)
            self.fields['componente'].initial = ruta.componente
            self.fields['tipo_pago'].initial = ruta.tipo_pago




        else:
            self.fields['contrato'].queryset = rh_models.Contratos.objects.none()

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Información de la ruta:',
                )
            ),
            Row(
                Column(
                    'contrato',
                    css_class='s12'
                )
            ),
            Row(
                Column(
                    'nombre',
                    css_class='s12 m6 l3'
                ),
                Column(
                    'componente',
                    css_class='s12 m6 l3'
                ),
                Column(
                    'valor_transporte',
                    css_class='s12 m6 l3'
                ),
                Column(
                    'tipo_pago',
                    css_class='s12 m6 l3'
                )
            ),

            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )






class ValoresActividadesForm(forms.Form):



    def clean(self):
        cleaned_data = super().clean()
        ruta = models.Rutas.objects.get(id=self.initial['pk_ruta'])

        valor_total = 0

        for momento in models.Momentos.objects.filter(componente = ruta.componente):


            valor_total += float(cleaned_data['valor_' + str(momento.id)].replace('$ ','').replace(',',''))


            if models.CuposRutaObject.objects.filter(ruta = ruta,momento = momento).count() > cleaned_data['cantidad_' + str(momento.id)]:
                self.add_error('cantidad_' + str(momento.id), 'La cantidad de actividades no puede ser reducida')


            valor_pago = models.CuposRutaObject.objects.filter(ruta=ruta, momento=momento).aggregate(Sum('valor'))['valor__sum']

            if valor_pago == None:
                valor_pago = 0

            else:
                float(valor_pago)

            if valor_pago > float(cleaned_data['valor_' + str(momento.id)].replace('$ ','').replace(',','')):
                self.add_error('valor_' + str(momento.id), 'El valor de las actividdes no puede ser reducido')



        if valor_total != float(ruta.valor.amount) - float(ruta.valor_transporte.amount):
            self.add_error(None,"El valor total de las actividades debe ser $ {:20,.2f}".format(float(ruta.valor.amount) - float(ruta.valor_transporte.amount)))


    def __init__(self, *args, **kwargs):
        super(ValoresActividadesForm, self).__init__(*args, **kwargs)

        ruta = models.Rutas.objects.get(id = kwargs['initial']['pk_ruta'])

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Componente: {0}'.format(ruta.componente),
                )
            ),
            Row(

            ),

            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )


        initial = []

        try:
            initial = json.loads(ruta.valores_actividades)
        except:
            pass


        for momento in models.Momentos.objects.filter(componente = ruta.componente):

            self.fields['cantidad_' + str(momento.id)] = forms.IntegerField(label = 'Cantidad de soportes: {0}'.format(momento.nombre))

            if 'cantidad_' + str(momento.id) in initial:
                self.fields['cantidad_' + str(momento.id)].initial = initial['cantidad_' + str(momento.id)]


            self.fields['valor_' + str(momento.id)] = forms.CharField(max_length=200,label = 'Valor total actividades: {0}'.format(momento.nombre))




            if 'valor_' + str(momento.id) in initial:
                self.fields['valor_' + str(momento.id)].initial = initial['valor_' + str(momento.id)]



            self.helper.layout.fields[1].fields.append(
                Column(
                    Column(
                        'cantidad_' + str(momento.id),
                        css_class='s12 m6'
                    ),
                    Column(
                        'valor_' + str(momento.id),
                        css_class='s12 m6'
                    ),
                    css_class='s12'
                )
            )







class RutasHogaresForm(forms.Form):

    file = forms.FileField(widget=forms.FileInput(attrs={'accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}))


    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")

        if file.name.split('.')[-1] == 'xlsx':
            pass
        else:
            self.add_error('file', 'El archivo cargado no tiene un formato valido')


    def __init__(self, *args, **kwargs):
        super(RutasHogaresForm, self).__init__(*args, **kwargs)
        ruta = None

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Archivo XLSX:',
                )
            ),
            Row(
                Column(
                    'file',
                    css_class='s12'
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )



class RutasInstrumentosRechazarForm(forms.Form):

    observacion = forms.CharField(widget=forms.Textarea())



    def __init__(self, *args, **kwargs):
        super(RutasInstrumentosRechazarForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Observación de rechazo',
                )
            ),
            Row(
                Column(
                    'observacion',
                    css_class='s12'
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )



class CortesCreateForm(forms.Form):

    descripcion = forms.CharField(max_length = 200)

    def __init__(self, *args, **kwargs):
        super(CortesCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Rutas con momentos reportados',
                )
            ),
            Row(
                Column(
                    'descripcion',
                    css_class = 's12'
                )
            ),
            Row(

            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )

        rutas_ids = models.CuposRutaObject.objects.exclude(momento__tipo = 'vinculacion').filter(estado = "Reportado").values_list('ruta__id',flat=True).distinct()

        for ruta_id in rutas_ids:

            ruta = models.Rutas.objects.get(id = ruta_id)
            self.fields['ruta_' + str(ruta.id)] = forms.BooleanField(
                label = '{0} Ruta: {1} - {2}'.format('$ {:20,.2f}'.format(ruta.get_valor_corte()),ruta.nombre,ruta.contrato.contratista),
                required = False
            )
            self.fields['ruta_' + str(ruta.id)].widget.attrs['class'] = 'filled-in'

            self.helper.layout.fields[2].fields.append(
                Div(
                    Div(
                        Column(
                            'ruta_' + str(ruta.id),
                            css_class='s12'
                        )
                    )
                )
            )


class CuentaCobroForm(forms.Form):
    valores = forms.CharField(widget=forms.HiddenInput())
    valores_inicial = forms.CharField(widget=forms.HiddenInput())
    mes = forms.MultipleChoiceField(choices=[
        ('Enero','Enero'),
        ('Febrero', 'Febrero'),
        ('Marzo', 'Marzo'),
        ('Abril', 'Abril'),
        ('Mayo', 'Mayo'),
        ('Junio', 'Junio'),
        ('Julio', 'Julio'),
        ('Agosto', 'Agosto'),
        ('Septiembre', 'Septiembre'),
        ('Octubre', 'Octubre'),
        ('Noviembre', 'Noviembre'),
        ('Diciembre', 'Diciembre')
    ])
    year = forms.ChoiceField(label='Año')


    def clean(self):
        cleaned_data = super().clean()
        cuenta_cobro = models.CuentasCobro.objects.get(id = self.initial['pk_cuenta_cobro'])
        valores_meses_json = json.loads(cleaned_data['valores'])
        valor_total = 0

        if len(valores_meses_json) > 1:

            for valor_mes in valores_meses_json:
                valor = valor_mes.get('valor')
                if valor == None or valor == '':
                    pass
                else:
                    valor_total += float(valor.replace('$ ','').replace(',',''))

            if round(valor_total) != round(cuenta_cobro.valor.amount):
                self.add_error('mes', 'No coinciden los valores')




    def __init__(self, *args, **kwargs):
        super(CuentaCobroForm, self).__init__(*args, **kwargs)

        cuenta_cobro = models.CuentasCobro.objects.get(id=kwargs['initial']['pk_cuenta_cobro'])
        fecha = timezone.now()
        year = fecha.strftime('%Y')
        year_1 = str(int(year)-1)
        mes = fecha.strftime('%B').capitalize()

        self.fields['valores_inicial'].initial = cuenta_cobro.valores_json

        self.fields['year'].choices = [(year_1,year_1),(year,year)]
        self.fields['year'].initial = year

        if cuenta_cobro.data_json == '' or cuenta_cobro.data_json == None:
            self.fields['mes'].initial = mes
        else:
            self.fields['mes'].initial = json.loads(cuenta_cobro.data_json)['mes']
            self.fields['year'].initial = json.loads(cuenta_cobro.data_json)['year']

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Cuenta de cobro',
                )
            ),
            Row(
                HTML(
                    """
                    <div class="col s12">{{ cuentas| safe }}</div>
                    """
                )
            ),
            Row(
                HTML(
                    """
                    <div class="col s12 m6"><p><b>Valor:</b> {{valor}}</p></div>
                    <div class="col s12 m6"><p><b>Corte:</b> {{corte}}</p></div>
                    <div class="col s12 m6"><p><b>Contratista:</b> {{contratista}}</p></div>
                    <div class="col s12 m6"><p><b>Contrato:</b> {{contrato}}</p></div>
                    <div class="col s12 m6"><p><b>Inicio:</b> {{inicio}}</p></div>
                    <div class="col s12 m6"><p><b>Fin:</b> {{fin}}</p></div>
                    """
                )
            ),
            Row(),
            Row(
                Column(
                    'mes',
                    css_class="s12 m6"
                ),
                Column(
                    'year',
                    css_class="s12 m6"
                ),
                Column(
                    HTML(
                        """
                        <div id="container_meses"></div>
                        """
                    ),
                    css_class="s12"
                ),
            ),
            Row(
                Column(
                    'valores',
                    'valores_inicial',
                    css_class = 's12'
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )


class CuentaCobroCargarForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(CuentaCobroCargarForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Cargar cuenta de cobro',
                )
            ),
            Row(
                HTML(
                    """
                    <p style="display:inline;margin-left: 10px;"><b>Actualmente:</b>{{ file_url | safe }}</p>
                    """
                )
            ),
            Row(
                Column(
                    'file2',
                    css_class="s12"
                ),
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )

    class Meta:
        model = models.CuentasCobro
        fields = ['file2']
        widgets = {
            'file2': forms.FileInput(attrs={'data-max-file-size': "50M",'accept': 'application/pdf'})
        }


class CuentaCobroEstadoForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        estado = cleaned_data.get("estado")
        observaciones = cleaned_data.get("observaciones")

        if estado == 'Pendiente':
            if observaciones == None or observaciones == '':
                self.add_error('observaciones', 'Por favor escriba una observación')


    def __init__(self, *args, **kwargs):
        super(CuentaCobroEstadoForm, self).__init__(*args, **kwargs)

        self.fields['estado'].widget = forms.Select(choices = [
            ('','----------'),
            ('Reportado', 'Reportado'),
            ('Pendiente', 'Pendiente'),
            ('Liquidación', 'Liquidación'),
            ('Pagado', 'Pagado')
        ])

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Cargar cuenta de cobro',
                )
            ),
            Row(
                Column(
                    'estado',
                    css_class="s12"
                ),
                Column(
                    'observaciones',
                    css_class="s12"
                ),
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )

    class Meta:
        model = models.CuentasCobro
        fields = ['estado','observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }


class DocumentoForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")

        if file.name.split('.')[-1] == 'pdf':
            pass
        else:
            self.add_error('file', 'El archivo cargado no tiene un formato valido')


    def __init__(self, *args, **kwargs):
        super(DocumentoForm, self).__init__(*args, **kwargs)


        instrumento = models.Instrumentos.objects.get(id = kwargs['initial']['pk_instrumento'])



        if instrumento.nivel == 'ruta':


            self.helper = FormHelper(self)
            self.helper.layout = Layout(

                Row(
                    Fieldset(
                        kwargs['initial'].get('short_name'),
                    )
                ),
                Row(
                    Column(
                        'file',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        Div(
                            Submit(
                                'submit',
                                'Guardar',
                                css_class='button-submit'
                            ),
                            css_class="right-align"
                        ),
                        css_class="s12"
                    ),
                )
            )

        elif instrumento.nivel == 'individual':
            self.fields['hogares'] = forms.ModelChoiceField(label = "Hogar",queryset = models.Hogares.objects.filter(rutas=kwargs['initial']['pk_ruta']))

            if 'pk_instrumento_object' in kwargs['initial']:

                instrumento_object = models.InstrumentosRutaObject.objects.get(id = kwargs['initial']['pk_instrumento_object'])

                try:
                    self.fields['hogares'].initial = instrumento_object.hogares.all()[0]
                except:
                    pass

            self.helper = FormHelper(self)
            self.helper.layout = Layout(

                Row(
                    Fieldset(
                        kwargs['initial'].get('short_name'),
                    )
                ),
                Row(
                    Column(
                        'file',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'hogares',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        Div(
                            Submit(
                                'submit',
                                'Guardar',
                                css_class='button-submit'
                            ),
                            css_class="right-align"
                        ),
                        css_class="s12"
                    ),
                )
            )

        else:
            self.fields['hogares'] = forms.ModelMultipleChoiceField(queryset=models.Hogares.objects.filter(rutas=kwargs['initial']['pk_ruta']))

            if 'pk_instrumento_object' in kwargs['initial']:
                instrumento_object = models.InstrumentosRutaObject.objects.get(id=kwargs['initial']['pk_instrumento_object'])

                self.fields['hogares'].initial = instrumento_object.hogares.all()

            self.helper = FormHelper(self)
            self.helper.layout = Layout(

                Row(
                    Fieldset(
                        kwargs['initial'].get('short_name'),
                    )
                ),
                Row(
                    Column(
                        'file',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'hogares',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        Div(
                            Submit(
                                'submit',
                                'Guardar',
                                css_class='button-submit'
                            ),
                            css_class="right-align"
                        ),
                        css_class="s12"
                    ),
                )
            )


    class Meta:
        model = models.Documento
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'data-max-file-size': "10M",
                'accept': 'application/pdf,application/x-pdf'}
            ),
        }








class ActaSocializacionComunidadesForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")

        if file.name.split('.')[-1] == 'pdf':
            pass
        else:
            self.add_error('file', 'El archivo cargado no tiene un formato valido')


    def __init__(self, *args, **kwargs):
        super(ActaSocializacionComunidadesForm, self).__init__(*args, **kwargs)


        instrumento = models.Instrumentos.objects.get(id = kwargs['initial']['pk_instrumento'])



        if instrumento.nivel == 'ruta':


            self.helper = FormHelper(self)
            self.helper.layout = Layout(

                Row(
                    Fieldset(
                        kwargs['initial'].get('short_name'),
                    )
                ),
                Row(
                    Column(
                        'nombre_comunidad',
                        css_class='s12 m6'
                    ),
                    Column(
                        'resguado_indigena_consejo_comunitario',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'municipio',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'nombre_representante',
                        css_class='s12 m6'
                    ),
                    Column(
                        'documento_representante',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'cargo_representante',
                        css_class='s12 m6'
                    ),
                    Column(
                        'fecha_firma',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'file',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        Div(
                            Submit(
                                'submit',
                                'Guardar',
                                css_class='button-submit'
                            ),
                            css_class="right-align"
                        ),
                        css_class="s12"
                    ),
                )
            )

        elif instrumento.nivel == 'individual':
            self.fields['hogares'] = forms.ModelChoiceField(label = "Hogar",queryset = models.Hogares.objects.filter(rutas=kwargs['initial']['pk_ruta']))

            if 'pk_instrumento_object' in kwargs['initial']:

                instrumento_object = models.InstrumentosRutaObject.objects.get(id = kwargs['initial']['pk_instrumento_object'])

                try:
                    self.fields['hogares'].initial = instrumento_object.hogares.all()[0]
                except:
                    pass

            self.helper = FormHelper(self)
            self.helper.layout = Layout(

                Row(
                    Fieldset(
                        kwargs['initial'].get('short_name'),
                    )
                ),
                Row(
                    Column(
                        'nombre_comunidad',
                        css_class='s12 m6'
                    ),
                    Column(
                        'resguado_indigena_consejo_comunitario',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'municipio',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'nombre_representante',
                        css_class='s12 m6'
                    ),
                    Column(
                        'documento_representante',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'cargo_representante',
                        css_class='s12 m6'
                    ),
                    Column(
                        'fecha_firma',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'file',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'hogares',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        Div(
                            Submit(
                                'submit',
                                'Guardar',
                                css_class='button-submit'
                            ),
                            css_class="right-align"
                        ),
                        css_class="s12"
                    ),
                )
            )

        else:
            self.fields['hogares'] = forms.ModelMultipleChoiceField(queryset=models.Hogares.objects.filter(rutas=kwargs['initial']['pk_ruta']))

            if 'pk_instrumento_object' in kwargs['initial']:
                instrumento_object = models.InstrumentosRutaObject.objects.get(id=kwargs['initial']['pk_instrumento_object'])

                self.fields['hogares'].initial = instrumento_object.hogares.all()

            self.helper = FormHelper(self)
            self.helper.layout = Layout(

                Row(
                    Fieldset(
                        kwargs['initial'].get('short_name'),
                    )
                ),
                Row(
                    Column(
                        'nombre_comunidad',
                        css_class='s12 m6'
                    ),
                    Column(
                        'resguado_indigena_consejo_comunitario',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'municipio',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'nombre_representante',
                        css_class='s12 m6'
                    ),
                    Column(
                        'documento_representante',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'cargo_representante',
                        css_class='s12 m6'
                    ),
                    Column(
                        'fecha_firma',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'file',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'hogares',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        Div(
                            Submit(
                                'submit',
                                'Guardar',
                                css_class='button-submit'
                            ),
                            css_class="right-align"
                        ),
                        css_class="s12"
                    ),
                )
            )


    class Meta:
        model = models.ActaSocializacionComunidades
        fields = ['file','nombre_comunidad','resguado_indigena_consejo_comunitario','municipio','nombre_representante',
                  'documento_representante','cargo_representante','fecha_firma']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'data-max-file-size': "10M",
                'accept': 'application/pdf,application/x-pdf'}
            ),
        }

        labels = {
            'nombre_comunidad': 'Nombre de la comunidad',
            'resguado_indigena_consejo_comunitario': 'Resguardo indigena o consejo comunitario',
            'fecha_firma': 'Fecha firma del acta'
        }




class ActaVinculacionHogarForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")

        if file.name.split('.')[-1] == 'pdf':
            pass
        else:
            self.add_error('file', 'El archivo cargado no tiene un formato valido')


    def __init__(self, *args, **kwargs):
        super(ActaVinculacionHogarForm, self).__init__(*args, **kwargs)


        instrumento = models.Instrumentos.objects.get(id = kwargs['initial']['pk_instrumento'])



        if instrumento.nivel == 'ruta':


            self.helper = FormHelper(self)
            self.helper.layout = Layout(

                Row(
                    Fieldset(
                        kwargs['initial'].get('short_name'),
                    )
                ),
                Row(
                    Column(
                        'fecha_diligenciamiento',
                        css_class='s12 m6 l4'
                    ),
                    Column(
                        'nombre_comunidad',
                        css_class='s12 m6 l4'
                    ),
                    Column(
                        'resguado_indigena_consejo_comunitario',
                        css_class='s12 m6 l4'
                    )
                ),
                Row(
                    Column(
                        'municipio',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'tipo_identificacion',
                        css_class='s12 m6'
                    ),
                    Column(
                        'documento_representante',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'nombre_representante',
                        css_class='s12 m6'
                    ),
                    Column(
                        'telefono_celular',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'file',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        Div(
                            Submit(
                                'submit',
                                'Guardar',
                                css_class='button-submit'
                            ),
                            css_class="right-align"
                        ),
                        css_class="s12"
                    ),
                )
            )

        elif instrumento.nivel == 'individual':
            self.fields['hogares'] = forms.ModelChoiceField(label = "Hogar",queryset = models.Hogares.objects.filter(rutas=kwargs['initial']['pk_ruta']))

            if 'pk_instrumento_object' in kwargs['initial']:

                instrumento_object = models.InstrumentosRutaObject.objects.get(id = kwargs['initial']['pk_instrumento_object'])

                try:
                    self.fields['hogares'].initial = instrumento_object.hogares.all()[0]
                except:
                    pass

            self.helper = FormHelper(self)
            self.helper.layout = Layout(

                Row(
                    Fieldset(
                        kwargs['initial'].get('short_name'),
                    )
                ),
                Row(
                    Column(
                        'fecha_diligenciamiento',
                        css_class='s12 m6 l4'
                    ),
                    Column(
                        'nombre_comunidad',
                        css_class='s12 m6 l4'
                    ),
                    Column(
                        'resguado_indigena_consejo_comunitario',
                        css_class='s12 m6 l4'
                    )
                ),
                Row(
                    Column(
                        'municipio',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'tipo_identificacion',
                        css_class='s12 m6'
                    ),
                    Column(
                        'documento_representante',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'nombre_representante',
                        css_class='s12 m6'
                    ),
                    Column(
                        'telefono_celular',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'file',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'hogares',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        Div(
                            Submit(
                                'submit',
                                'Guardar',
                                css_class='button-submit'
                            ),
                            css_class="right-align"
                        ),
                        css_class="s12"
                    ),
                )
            )

        else:
            self.fields['hogares'] = forms.ModelMultipleChoiceField(queryset=models.Hogares.objects.filter(rutas=kwargs['initial']['pk_ruta']))

            if 'pk_instrumento_object' in kwargs['initial']:
                instrumento_object = models.InstrumentosRutaObject.objects.get(id=kwargs['initial']['pk_instrumento_object'])

                self.fields['hogares'].initial = instrumento_object.hogares.all()

            self.helper = FormHelper(self)
            self.helper.layout = Layout(

                Row(
                    Fieldset(
                        kwargs['initial'].get('short_name'),
                    )
                ),
                Row(
                    Column(
                        'fecha_diligenciamiento',
                        css_class='s12 m6 l4'
                    ),
                    Column(
                        'nombre_comunidad',
                        css_class='s12 m6 l4'
                    ),
                    Column(
                        'resguado_indigena_consejo_comunitario',
                        css_class='s12 m6 l4'
                    )
                ),
                Row(
                    Column(
                        'municipio',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'tipo_identificacion',
                        css_class='s12 m6'
                    ),
                    Column(
                        'documento_representante',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'nombre_representante',
                        css_class='s12 m6'
                    ),
                    Column(
                        'telefono_celular',
                        css_class='s12 m6'
                    )
                ),
                Row(
                    Column(
                        'file',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        'hogares',
                        css_class='s12'
                    )
                ),
                Row(
                    Column(
                        Div(
                            Submit(
                                'submit',
                                'Guardar',
                                css_class='button-submit'
                            ),
                            css_class="right-align"
                        ),
                        css_class="s12"
                    ),
                )
            )


    class Meta:
        model = models.ActaVinculacionHogar
        fields = ['file','fecha_diligenciamiento','municipio','resguado_indigena_consejo_comunitario','nombre_comunidad',
                  'tipo_identificacion','documento_representante','nombre_representante','telefono_celular']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'data-max-file-size': "10M",
                'accept': 'application/pdf,application/x-pdf'}
            ),
        }

        labels = {
            'nombre_comunidad': 'Nombre de la comunidad',
            'resguado_indigena_consejo_comunitario': 'Resguardo indigena o consejo comunitario',
        }





class DocumentoExcelForm(forms.Form):

    file = forms.FileField(widget=forms.FileInput(attrs={'accept': 'application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}))


    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")

        if file.name.split('.')[-1] == 'xlsx' or file.name.split('.')[-1] == 'xls':
            pass
        else:
            self.add_error('file', 'El archivo cargado no tiene un formato valido')


    def __init__(self, *args, **kwargs):
        super(DocumentoExcelForm, self).__init__(*args, **kwargs)
        ruta = None

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    kwargs['initial'].get('short_name'),
                )
            ),
            Row(
                Column(
                    'file',
                    css_class='s12'
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )

class Fotos4Form(forms.Form):

    foto1 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto2 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto3 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}),required=False)
    foto4 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}),required=False)


    def clean(self):
        cleaned_data = super().clean()
        foto1 = cleaned_data.get("foto1")
        foto2 = cleaned_data.get("foto2")
        foto3 = cleaned_data.get("foto3")
        foto4 = cleaned_data.get("foto4")

        if foto1.name.split('.')[-1] in ['jpg','jpeg','png']:
            pass
        else:
            self.add_error('foto1', 'El archivo cargado no tiene un formato valido')

        if foto2.name.split('.')[-1] in ['jpg','jpeg','png']:
            pass
        else:
            self.add_error('foto2', 'El archivo cargado no tiene un formato valido')


        if foto3 != None:
            if foto3.name.split('.')[-1] in ['jpg','jpeg','png']:
                pass
            else:
                self.add_error('foto3', 'El archivo cargado no tiene un formato valido')

        if foto4 != None:
            if foto4.name.split('.')[-1] in ['jpg','jpeg','png']:
                pass
            else:
                self.add_error('foto4', 'El archivo cargado no tiene un formato valido')


    def __init__(self, *args, **kwargs):
        super(Fotos4Form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    kwargs['initial'].get('short_name'),
                )
            ),
            Row(
                Column(
                    'foto1',
                    css_class='s12 m6'
                ),
                Column(
                    'foto2',
                    css_class='s12 m6'
                ),
                Column(
                    'foto3',
                    css_class='s12 m6'
                ),
                Column(
                    'foto4',
                    css_class='s12 m6'
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )

class Fotos2Form(forms.Form):

    foto1 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto2 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))


    def clean(self):
        cleaned_data = super().clean()
        foto1 = cleaned_data.get("foto1")
        foto2 = cleaned_data.get("foto2")

        if foto1.name.split('.')[-1] in ['jpg','jpeg','png']:
            pass
        else:
            self.add_error('foto1', 'El archivo cargado no tiene un formato valido')

        if foto2.name.split('.')[-1] in ['jpg','jpeg','png']:
            pass
        else:
            self.add_error('foto2', 'El archivo cargado no tiene un formato valido')



    def __init__(self, *args, **kwargs):
        super(Fotos2Form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    kwargs['initial'].get('short_name'),
                )
            ),
            Row(
                Column(
                    'foto1',
                    css_class='s12 m6'
                ),
                Column(
                    'foto2',
                    css_class='s12 m6'
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )

class Fotos5Form(forms.Form):

    foto1 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto2 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto3 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto4 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto5 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))


    def clean(self):
        cleaned_data = super().clean()
        foto1 = cleaned_data.get("foto1")
        foto2 = cleaned_data.get("foto2")
        foto3 = cleaned_data.get("foto3")
        foto4 = cleaned_data.get("foto4")
        foto5 = cleaned_data.get("foto5")

        if foto1.name.split('.')[-1] in ['jpg','jpeg','png']:
            pass
        else:
            self.add_error('foto1', 'El archivo cargado no tiene un formato valido')

        if foto2.name.split('.')[-1] in ['jpg','jpeg','png']:
            pass
        else:
            self.add_error('foto2', 'El archivo cargado no tiene un formato valido')


        if foto3 != None:
            if foto3.name.split('.')[-1] in ['jpg','jpeg','png']:
                pass
            else:
                self.add_error('foto3', 'El archivo cargado no tiene un formato valido')

        if foto4 != None:
            if foto4.name.split('.')[-1] in ['jpg','jpeg','png']:
                pass
            else:
                self.add_error('foto4', 'El archivo cargado no tiene un formato valido')

        if foto5 != None:
            if foto5.name.split('.')[-1] in ['jpg','jpeg','png']:
                pass
            else:
                self.add_error('foto5', 'El archivo cargado no tiene un formato valido')


    def __init__(self, *args, **kwargs):
        super(Fotos5Form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    kwargs['initial'].get('short_name'),
                )
            ),
            Row(
                Column(
                    'foto1',
                    css_class='s12 m6'
                ),
                Column(
                    'foto2',
                    css_class='s12 m6'
                ),
                Column(
                    'foto3',
                    css_class='s12 m6'
                ),
                Column(
                    'foto4',
                    css_class='s12 m6'
                ),
                Column(
                    'foto5',
                    css_class='s12 m6'
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )


class Fotos6Form(forms.Form):

    foto1 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto2 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto3 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto4 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto5 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))
    foto6 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))


    def clean(self):
        cleaned_data = super().clean()
        foto1 = cleaned_data.get("foto1")
        foto2 = cleaned_data.get("foto2")
        foto3 = cleaned_data.get("foto3")
        foto4 = cleaned_data.get("foto4")
        foto5 = cleaned_data.get("foto5")
        foto6 = cleaned_data.get("foto6")

        if foto1.name.split('.')[-1] in ['jpg','jpeg','png']:
            pass
        else:
            self.add_error('foto1', 'El archivo cargado no tiene un formato valido')

        if foto2.name.split('.')[-1] in ['jpg','jpeg','png']:
            pass
        else:
            self.add_error('foto2', 'El archivo cargado no tiene un formato valido')


        if foto3 != None:
            if foto3.name.split('.')[-1] in ['jpg','jpeg','png']:
                pass
            else:
                self.add_error('foto3', 'El archivo cargado no tiene un formato valido')

        if foto4 != None:
            if foto4.name.split('.')[-1] in ['jpg','jpeg','png']:
                pass
            else:
                self.add_error('foto4', 'El archivo cargado no tiene un formato valido')

        if foto5 != None:
            if foto5.name.split('.')[-1] in ['jpg','jpeg','png']:
                pass
            else:
                self.add_error('foto5', 'El archivo cargado no tiene un formato valido')

        if foto6 != None:
            if foto6.name.split('.')[-1] in ['jpg','jpeg','png']:
                pass
            else:
                self.add_error('foto6', 'El archivo cargado no tiene un formato valido')


    def __init__(self, *args, **kwargs):
        super(Fotos6Form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    kwargs['initial'].get('short_name'),
                )
            ),
            Row(
                Column(
                    'foto1',
                    css_class='s12 m6'
                ),
                Column(
                    'foto2',
                    css_class='s12 m6'
                ),
                Column(
                    'foto3',
                    css_class='s12 m6'
                ),
                Column(
                    'foto4',
                    css_class='s12 m6'
                ),
                Column(
                    'foto5',
                    css_class='s12 m6'
                ),
                Column(
                    'foto6',
                    css_class='s12 m6'
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )


class Fotos1Form(forms.Form):

    foto1 = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg,image/jpeg,image/png'}))


    def clean(self):
        cleaned_data = super().clean()
        foto1 = cleaned_data.get("foto1")

        if foto1.name.split('.')[-1] in ['jpg','jpeg','png']:
            pass
        else:
            self.add_error('foto1', 'El archivo cargado no tiene un formato valido')




    def __init__(self, *args, **kwargs):
        super(Fotos1Form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    kwargs['initial'].get('short_name'),
                )
            ),
            Row(
                Column(
                    'foto1',
                    css_class='s12 m6'
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )

class CaracterizacionInicialForm(forms.Form):
    # -------------------------------------------------------------

    # lugar de atencion
    departamento_atencion = forms.ModelChoiceField(label='Departamento de atención*',queryset=Departamentos.objects.all(),required=False)
    municipio_atencion = forms.ModelChoiceField(label='Municipio de atención*',queryset=Municipios.objects.none(),required=False)


    # residencia
    departamento_residencia = forms.ModelChoiceField(label='Departamento de residencia*',queryset=Departamentos.objects.all(),required=False)
    municipio_residencia = forms.ModelChoiceField(label='Municipio de residencia*', queryset=Municipios.objects.none(),required=False)
    zona_residencia = forms.CharField(label="Zona de residencia*",widget=forms.Select(choices=[
        ('', '----------'),
        ('Cabecera municipal','Cabecera municipal'),
        ('Centro poblado', 'Centro poblado'),
        ('Rural disperso', 'Rural disperso')
    ]),required=False)

    localidad = forms.CharField(max_length=1000,required=False)
    barrio = forms.CharField(label="Barrio*",max_length=1000,required=False)
    direccion_predio = forms.CharField(label="Dirección del predio*",max_length=1000,required=False)

    corregimiento = forms.ModelChoiceField(label='Corregimiento',queryset=Corregimientos.objects.none(),required=False)
    vereda = forms.ModelChoiceField(label='Vereda', queryset=Veredas.objects.none(),required=False)
    ubicacion_predio = forms.CharField(label="Ubicación del predio*",max_length=1000,required=False)

    telefono_fijo = forms.CharField(max_length=100,required=False)
    tipo_vivienda = forms.CharField(label="Tipo de vivienda*",widget=forms.Select(choices=[
        ('', '----------'),
        ('Casa Lote', 'Casa Lote'),
        ('Vivienda (Casa) Indigena', 'Vivienda (Casa) Indigena'),
        ('Casa', 'Casa'),
        ('Apartamento', 'Apartamento'),
        ('Cuarto(s) Inquilinato', 'Cuarto(s) Inquilinato'),
        ('Albergue', 'Albergue'),
        ('Otro tipo de Vivienda (Carpa, Tienda, Vagon, Embarcacion, Cueva, Refugio Natural, Puente, etc,) Cual?', 'Otro tipo de Vivienda (Carpa, Tienda, Vagon, Embarcacion, Cueva, Refugio Natural, Puente, etc,) Cual?'),
        ('Cuarto(s) en otro tipo de estructura', 'Cuarto(s) en otro tipo de estructura')
    ]),required=False)
    otro_tipo_vivienda = forms.CharField(label="Otro tipo de vivienda, cual?",max_length=100,required=False)

    propiedad_vivienda = forms.CharField(label="Propiedad de la vivienda*",widget=forms.Select(choices=[
        ('', '----------'),
        ('Propia Totalmente Pagada', 'Propia Totalmente Pagada'),
        ('En Arriendo o SubArriendo', 'En Arriendo o SubArriendo'),
        ('Colectiva', 'Colectiva'),
        ('Propia, la estan pagando', 'Propia, la estan pagando'),
        ('En Usufructo', 'En Usufructo'),
        ('Posesion Sin Titulo','Posesion Sin Titulo')
    ]),required=False)
    estrato_vivienda = forms.CharField(widget=forms.Select(choices=[
        ('', '----------'),
        ('Estrato 0', 'Estrato 0'),
        ('Estrato 1', 'Estrato 1'),
        ('Estrato 2', 'Estrato 2'),
        ('Estrato 3', 'Estrato 3'),
        ('Estrato 4', 'Estrato 4'),
        ('Estrato 5', 'Estrato 5'),
        ('Estrato 6', 'Estrato 6'),
    ]),required=False)

    # -------------------------------------------------------------

    # Georreferenciación

    longitud = forms.DecimalField(label="Longitud*",max_digits=15,decimal_places=10,required=False)
    latitud = forms.DecimalField(label="Latitud*",max_digits=15, decimal_places=10, required=False)
    precision = forms.DecimalField(label="Precisión*",max_digits=15, decimal_places=10, required=False)
    altitud = forms.DecimalField(label="Altitud*",max_digits=15, decimal_places=10, required=False)

    # -------------------------------------------------------------

    # información sobre la familia

    otro_telefono = forms.CharField(label="Otro telefono",max_length=100, required=False)
    descripcion_direccion = forms.CharField(label="Descripción dirección",max_length=100, required=False)
    numero_personas_familia = forms.IntegerField(label="Numero de personas*",initial=1,required=False,widget=forms.NumberInput(attrs={'min':1}))

    menores_5_anios = forms.IntegerField(label="Menores de 5 años*",initial=0,required=False,widget=forms.NumberInput(attrs={'min':0}))
    mayores_60_anios = forms.IntegerField(label="Mayores de 60 años*",initial=0,required=False,widget=forms.NumberInput(attrs={'min':0}))

    mujeres_gestantes_lactantes = forms.IntegerField(label="Mujeres gestantes o lactantes*",initial=0,required=False,widget=forms.NumberInput(attrs={'min':0}))
    discapacitados_familia = forms.IntegerField(label="Personas en condición de discapacidad*",initial=0,required=False,widget=forms.NumberInput(attrs={'min':0}))

    # -------------------------------------------------------------

    # Datos personales

    tipo_documento = forms.CharField(label="Tipo de documento*",max_length=100,widget=forms.Select(choices=[
        ('', '----------'),
        ('Cedula de ciudadania', 'Cedula de ciudadania'),
        ('Tarjeta de identidad', 'Tarjeta de identidad'),
        ('Cedula de extranjeria', 'Cedula de extranjeri'),
        ('Registro civil', 'Registro civil'),
        ('NIT', 'NIT'),
        ('SIN', 'SIN'),
        ('Registro civil de defunción', 'Registro civil de defunción'),
        ('Libreta militar', 'Libreta militar'),
        ('Matricula mercantil', 'Matricula mercantil'),
        ('Pasaporte', 'Pasaporte'),
        ('Indocumentado', 'Indocumentado'),
        ('Ninguno', 'Ninguno'),
        ('Otro', 'Otro'),
        ('PB', 'PB'),
        ('SR', 'SR'),
        ('Cedula militar', 'Cedula militar'),
    ]), required=False)

    numero_documento = forms.IntegerField(label="Número de documento*",required=False)

    primer_apellido = forms.CharField(label="Primer apellido*",max_length=100,required=False)
    segundo_apellido = forms.CharField(max_length=100, required=False)
    primer_nombre = forms.CharField(label="Primer nombre",max_length=100,required=False)
    segundo_nombre = forms.CharField(max_length=100, required=False)

    celular_1 = forms.CharField(label="Celular 1*",max_length=100,required=False)
    celular_2 = forms.CharField(max_length=100, required=False)
    correo_electronico = forms.EmailField(max_length=100, required=False)

    # Lugar y fecha de nacimiento

    departamento_nacimiento = forms.ModelChoiceField(label='Departamento de nacimiento*',queryset=Departamentos.objects.all(), required=False)
    municipio_nacimiento = forms.ModelChoiceField(label='Municipio de nacimiento*', queryset=Municipios.objects.none(),required=False)
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento*",widget=forms.TextInput(attrs={'class':'datepicker'}),required=False)

    # Lugar y fecha de expedición del documento

    departamento_expedicion = forms.ModelChoiceField(label='Departamento de expedición*',queryset=Departamentos.objects.all(), required=False)
    municipio_expedicion = forms.ModelChoiceField(label='Municipio de expedición*', queryset=Municipios.objects.none(),required=False)
    fecha_expedicion = forms.DateField(label="Fecha de expedición*",widget=forms.TextInput(attrs={'class':'datepicker'}),required=False)

    # -------------------------------------------------------------

    # Caracteristicas geenrales

    sexo = forms.CharField(label="Sexo*", max_length=100, widget=forms.Select(choices=[
        ('', '----------'),
        ('I O Intersexual', 'I O Intersexual'),
        ('Mujer', 'Mujer'),
        ('Hombre', 'Hombre')
    ]), required=False)
    tiene_libreta = forms.BooleanField(label="¿Tiene libreta militar?",initial=False,required=False,widget=forms.CheckboxInput(attrs={'class':'filled-in checkboxinput'}))
    numero_libreta = forms.CharField(label="Número de libreta militar*", required=False)
    identidad_genero = forms.CharField(label="Identidad de género", max_length=100, widget=forms.Select(choices=[
        ('', '----------'),
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Mujer transexual', 'Mujer transexual'),
        ('Hombre transexual', 'Hombre transexual')
    ]), required=False)
    condicion_sexual = forms.CharField(label="Condición sexual", max_length=100, widget=forms.Select(choices=[
        ('', '----------'),
        ('Bisexual', 'Bisexual'),
        ('Gay', 'Gay'),
        ('Lesbiana', 'Lesbiana'),
        ('Heterosexual', 'Heterosexual'),
        ('ND', 'ND')
    ]), required=False)
    estado_civil = forms.CharField(label="Estado civil*", max_length=100, widget=forms.Select(choices=[
        ('', '----------'),
        ('No reporta', 'No reporta'),
        ('Divorciado(a)', 'Divorciado(a)'),
        ('Casado(a)', 'Casado(a)'),
        ('Soltero(a)', 'Soltero(a)'),
        ('Viudo(a)', 'Viudo(a)'),
        ('Viudo(a)', 'Viudo(a)'),
        ('Union libre', 'Union libre'),
        ('Vive en pareja hace menos de 2 años', 'Vive en pareja hace menos de 2 años')
    ]), required=False)

    etnia = forms.CharField(label="Étnia*", max_length=100, widget=forms.Select(choices=[
        ('', '----------'),
        ('Rom / Gitano', 'Rom / Gitano'),
        ('Indigena', 'Indigena'),
        ('Palanquero', 'Palanquero'),
        ('Afrocolombiano / Negro', 'Afrocolombiano / Negro'),
        ('Raizal', 'Raizal'),
        ('Ninguno de los anteriores', 'Ninguno de los anteriores')
    ]), required=False)

    pueblo_indigena = forms.ModelChoiceField(label='Pueblo indigena',queryset=PueblosIndigenas.objects.all().order_by('nombre'), required=False)
    resguardo_indigena = forms.ModelChoiceField(label='Resguardo indigena', queryset=ResguardosIndigenas.objects.all().order_by('nombre'),required=False)
    comunidad_indigena = forms.ModelChoiceField(label='Comunidad indigena', queryset=ComunidadesIndigenas.objects.all().order_by('nombre'),required=False)
    lengua_nativa_indigena = forms.BooleanField(initial=False, required=False,widget=forms.CheckboxInput(attrs={'class':'filled-in checkboxinput'}))
    cual_lengua_indigena = forms.ModelChoiceField(label='Lengua nativa', queryset=LenguasNativas.objects.all().order_by('nombre'),required=False)

    consejo_afro = forms.ModelChoiceField(label='Consejo afro', queryset=ConsejosAfro.objects.all(),required=False)
    comunidad_afro = forms.ModelChoiceField(label='Comunidad afro', queryset=ComunidadesAfro.objects.all(),required=False)
    lengua_nativa_afro = forms.BooleanField(initial=False, required=False,widget=forms.CheckboxInput(attrs={'class':'filled-in checkboxinput'}))
    cual_lengua_afro = forms.ModelChoiceField(label='Lengua nativa', queryset=LenguasNativas.objects.all(),required=False)

    discapacidad = forms.BooleanField(initial=False, required=False,widget=forms.CheckboxInput(attrs={'class':'filled-in checkboxinput'}))

    registro_discapacidad = forms.CharField(label="Tiene registro de discapacidad?", max_length=100, widget=forms.Select(choices=[
        ('', '----------'),
        ('Si', 'Si'),
        ('No', 'No'),
        ('No sabe', 'No sabe')
    ]), required=False)
    categoria_discapacidad = forms.MultipleChoiceField(label='Categoria discapacidad', choices=CategoriaDiscapacidad.objects.all().values_list('id','nombre'), required=False)
    dificultades_permanentes = forms.MultipleChoiceField(label='Dificualtades permanentes para', choices=DificultadesPermanentesDiscapacidad.objects.all().values_list('id','nombre'), required=False)

    utiliza_actualmente = forms.MultipleChoiceField(label='Utiliza actualmente algun dispositivo de apoyo',choices=ElementosDiscapacidad.objects.all().values_list('id','nombre'),required=False)
    rehabilitacion = forms.MultipleChoiceField(label='Esta en rehabilitación?',choices=TiposRehabilitacionDiscapacidad.objects.all().values_list('id', 'nombre'), required=False)


    tiene_cuidador = forms.BooleanField(initial=False, required=False,widget=forms.CheckboxInput(attrs={'class':'filled-in checkboxinput'}))

    cuidador = forms.CharField(label="Quién es el cuidador?", max_length=100, widget=forms.Select(choices=[
        ('', '----------'),
        ('Algun pariente del hogar', 'Algun pariente del hogar'),
        ('Pariente en otro lugar', 'Pariente en otro lugar'),
        ('No pariente en otro lugar', 'No pariente en otro lugar')
    ]), required=False)
    parentezco = forms.CharField(label="Parentesco*", max_length=100, widget=forms.Select(choices=[
        ('', '----------'),
        ('No reporta', 'No reporta'),
        ('Hijastro(a)', 'Hijastro(a)'),
        ('Jefe(a) o Cabeza del hogar', 'Jefe(a) o Cabeza del hogar'),
        ('Pareja, Esposo(a), Conyugue o compañero(a)', 'Pareja, Esposo(a), Conyugue o compañero(a)'),
        ('Hijo(a)', 'Hijo(a)'),
        ('Yerno/Nuera', 'Yerno/Nuera'),
        ('Nieto(a)', 'Nieto(a)'),
        ('Padres(Padre/Madre)', 'Padres(Padre/Madre)'),
        ('Suegro(a)', 'Suegro(a)'),
        ('Hermanos(Hermano(a))', 'Hermanos(Hermano(a))'),
        ('Otro pariente', 'Otro pariente'),
        ('Abuelos(Abuelo(a))', 'Abuelos(Abuelo(a))'),
        ('Tios', 'Tios'),
        ('Sobrinos', 'Sobrinos'),
        ('Primos', 'Primos'),
        ('Otros no parientes', 'Otros no parientes'),
        ('Cuñados(Cuñado(a))', 'Cuñados(Cuñado(a))')
    ]), required=False)
    es_jefe = forms.BooleanField(initial=False, required=False,widget=forms.CheckboxInput(attrs={'class':'filled-in checkboxinput'}))
    es_representante_hogar = forms.BooleanField(initial=False, required=False,widget=forms.CheckboxInput(attrs={'class':'filled-in checkboxinput'}))

    bancarizacion = forms.BooleanField(initial=False, required=False,widget=forms.CheckboxInput(attrs={'class':'filled-in checkboxinput'}))
    banco = forms.ModelChoiceField(label='Banco*',queryset=Bancos.objects.all(), required=False)
    tipo_cuenta = forms.CharField(label="Tipo cuenta*", max_length=100, widget=forms.Select(choices=[
        ('', '----------'),
        ('Cuenta de ahorros', 'Cuenta de ahorros'),
        ('Cuenta corriente', 'Cuenta corriente')
    ]), required=False)
    numero_cuenta = forms.CharField(label="Número de cuenta*", max_length=100, required=False)


    nivel_escolaridad = forms.CharField(label="Nivel escolaridad*", max_length=100, widget=forms.Select(choices=[
        ('', '----------'),
        ('Técnica profesional', 'Técnica profesional'),
        ('Tecnológico', 'Tecnológico'),
        ('Profesional', 'Profesional'),
        ('Especialización', 'Especialización'),
        ('Curso largo SENA 400 HR', 'Curso largo SENA 400 HR'),
        ('Certificación habilidades SENA', 'Certificación habilidades SENA'),
        ('Curso corto SENA 40 HR', 'Curso corto SENA 40 HR'),
        ('Maestría', 'Maestría'),
        ('Preescolar', 'Preescolar'),
        ('Básica primaria(1-5)', 'Básica primaria(1-5)'),
        ('Básica secundaria(6-9)', 'Básica secundaria(6-9)'),
        ('Media(10-13)', 'Media(10-13)'),
        ('Ninguno', 'Ninguno')
    ]), required=False)
    grado_titulo = forms.CharField(label="Grado o Título alcanzado*", max_length=100, required=False)

    sabe_leer = forms.BooleanField(label="¿Sabe leer y escribir?",initial=False, required=False,widget=forms.CheckboxInput(attrs={'class':'filled-in checkboxinput'}))
    sabe_sumar_restar = forms.BooleanField(label="¿Sabe sumar y restar?",initial=False, required=False,widget=forms.CheckboxInput(attrs={'class':'filled-in checkboxinput'}))
    actualmente_estudia = forms.BooleanField(label="¿Actualmente Estudia?",initial=False, required=False,widget=forms.CheckboxInput(attrs={'class':'filled-in checkboxinput'}))
    recibe_alimentos = forms.BooleanField(initial=False, required=False,widget=forms.CheckboxInput(attrs={'class': 'filled-in checkboxinput'}))


    razon_no_estudia = forms.CharField(label="Razón por la cuál no estudia*", max_length=100, widget=forms.Select(choices=[
        ('', '----------'),
        ('No tiene interés en estudiar', 'No tiene interés en estudiar'),
        ('Considera que no está en edad escolar', 'Considera que no está en edad escolar'),
        ('Insuficiencia de recursos', 'Insuficiencia de recursos'),
        ('Prefiere trabajar', 'Prefiere trabajar'),
        ('Debe encargarse del hogar', 'Debe encargarse del hogar'),
        ('Lejanía del establecimiento educativo', 'Lejanía del establecimiento educativo'),
        ('Por inseguridad en el entorno', 'Por inseguridad en el entorno'),
        ('Tuvieron que abandonar el lugar de residencia actual', 'Tuvieron que abandonar el lugar de residencia actual'),
        ('Necesita educación especial', 'Necesita educación especial'),
        ('Por matoneo escolar', 'Por matoneo escolar'),
        ('Por embarazo', 'Por embarazo'),
        ('Por enfermedad', 'Por enfermedad'),
        ('Otro - Cual?', 'Otro - Cual?')
    ]), required=False)

    razon_no_estudia_otra = forms.CharField(label="¿Cual es la razón por la cual no estudia?*", max_length=100, required=False)  # se activa si no estudia y hay otra razon
    regimen_seguridad_social = forms.CharField(label="Régimen seguridad social*", max_length=100,widget=forms.Select(choices=[
       ('', '----------'),
       ('EPS contributivo', 'EPS contributivo'),
       ('Régimen Especial (fuerzas armadas, Ecopetrol, Universidades Públicas, Magisterio - UNIDOS)',
        'Régimen Especial (fuerzas armadas, Ecopetrol, Universidades Públicas, Magisterio - UNIDOS)'),
       ('EPS subsidiado (ARS-Administradora de Régimen Subsidiado)',
        'EPS subsidiado (ARS-Administradora de Régimen Subsidiado)'),
       ('Eps indígena', 'Eps indígena'),
       ('No tiene', 'No tiene'),
       ('No sabe, no informa', 'No sabe, no informa'),
       ('Subsidiado', 'Subsidiado'),
       ('Contributivo', 'Contributivo')
    ]), required=False)



    # -------------------------------------------------------------


    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            if name not in ['municipio_atencion','municipio_residencia','corregimiento','vereda','municipio_nacimiento','municipio_expedicion']:
                if field.disabled:
                    value = self.get_initial_for_field(field, name)
                else:
                    value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
                try:
                    if isinstance(field, FileField):
                        initial = self.get_initial_for_field(field, name)
                        value = field.clean(value, initial)
                    else:
                        value = field.clean(value)

                    self.cleaned_data[name] = value
                    if hasattr(self, 'clean_%s' % name):
                        value = getattr(self, 'clean_%s' % name)()
                        self.cleaned_data[name] = value
                except ValidationError as e:
                    self.add_error(name, e)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
                self.cleaned_data[name] = value


    def __init__(self, *args, **kwargs):
        super(CaracterizacionInicialForm, self).__init__(*args, **kwargs)

        if 'pk_hogar' in kwargs['initial']:
            hogar = models.Hogares.objects.get(pk = kwargs['initial']['pk_hogar'])

            self.fields['departamento_atencion'].initial = hogar.municipio.departamento
            self.fields['municipio_atencion'].queryset = Municipios.objects.filter(departamento = hogar.municipio.departamento)
            self.fields['municipio_atencion'].initial = hogar.municipio

            self.fields['departamento_residencia'].initial = hogar.municipio_residencia.departamento
            self.fields['municipio_residencia'].queryset = Municipios.objects.filter(departamento=hogar.municipio_residencia.departamento)
            self.fields['municipio_residencia'].initial = hogar.municipio_residencia

            self.fields['corregimiento'].queryset = Corregimientos.objects.filter(municipio=hogar.municipio_residencia).order_by('nombre')
            self.fields['vereda'].queryset = Veredas.objects.filter(municipio=hogar.municipio_residencia).order_by('nombre')

            self.fields['barrio'].initial = hogar.barrio
            self.fields['telefono_fijo'].initial = hogar.telefono

            self.fields['primer_apellido'].initial = hogar.primer_apellido
            self.fields['segundo_apellido'].initial = hogar.segundo_apellido
            self.fields['primer_nombre'].initial = hogar.primer_nombre
            self.fields['segundo_nombre'].initial = hogar.segundo_nombre
            self.fields['numero_documento'].initial = hogar.documento
            self.fields['tipo_documento'].initial = 'Cedula'

            self.fields['celular_1'].initial = hogar.celular1
            self.fields['celular_2'].initial = hogar.celular2
            self.fields['fecha_nacimiento'].initial = hogar.fecha_nacimiento.strftime('%d/%m/%Y')

class PermisosCreateForm(forms.ModelForm):

    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            if name not in ['user','rutas_ver','rutas_preaprobar','rutas_aprobar']:
                if field.disabled:
                    value = self.get_initial_for_field(field, name)
                else:
                    value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
                try:
                    if isinstance(field, FileField):
                        initial = self.get_initial_for_field(field, name)
                        value = field.clean(value, initial)
                    else:
                        value = field.clean(value)

                        if name == 'nombre':
                            try:
                                models.Rutas.objects.get(nombre = value)
                            except:
                                pass
                            else:
                                self.add_error(name, 'El nombre de la ruta ya existe')

                    self.cleaned_data[name] = value
                    if hasattr(self, 'clean_%s' % name):
                        value = getattr(self, 'clean_%s' % name)()
                        self.cleaned_data[name] = value
                except ValidationError as e:
                    self.add_error(name, e)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
                self.cleaned_data[name] = value

    def __init__(self, *args, **kwargs):
        super(PermisosCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        if 'pk' in kwargs['initial'].keys():
            permiso = models.PermisosCuentasRutas.objects.get(pk = kwargs['initial']['pk'])
            self.fields['user'].queryset = models.User.objects.filter(email = permiso.user.email)
            self.fields['user'].initial = models.PermisosCuentasRutas.objects.get(user=permiso.user)
        else:
            self.fields['user'].queryset = models.User.objects.none()
            self.fields['rutas_ver'].queryset = models.Rutas.objects.none()
            self.fields['rutas_preaprobar'].queryset = models.Rutas.objects.none()
            self.fields['rutas_aprobar'].queryset = models.Rutas.objects.none()

        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Información del permiso',
                )
            ),
            Row(
                Column(
                    Row(
                        Column(
                            'user',
                            css_class='s12'
                        )
                    ),
                    Row(
                        Column(
                            'rutas_ver',
                            css_class='s12'
                        )
                    ),
                    Row(
                        Column(
                            'rutas_preaprobar',
                            css_class='s12'
                        )
                    ),
                    Row(
                        Column(
                            'rutas_aprobar',
                            css_class='s12'
                        )
                    ),
                    css_class="s12"
                ),
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )

    class Meta:
        model = models.PermisosCuentasRutas
        fields = ['user','rutas_ver','rutas_preaprobar','rutas_aprobar']


class ArchivoRarZipForm(forms.Form):

    rar_zip = forms.FileField(widget=forms.FileInput(attrs={'accept': 'application/zip,application/x-rar-compressed,application/x-7z-compressed'}))


    def clean(self):
        cleaned_data = super().clean()
        rar_zip = cleaned_data.get("rar_zip")

        if rar_zip.name.split('.')[-1] in ['rar','zip']:
            pass
        else:
            self.add_error('foto1', 'El archivo cargado no tiene un formato valido')




    def __init__(self, *args, **kwargs):
        super(ArchivoRarZipForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    kwargs['initial'].get('short_name'),
                )
            ),
            Row(
                Column(
                    'rar_zip',
                    css_class='s12'
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )



class CambioRutaComponenteForm(forms.Form):

    ruta = forms.ModelChoiceField(label='Ruta destino',queryset=models.Rutas.objects.none(),required=False)


    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            if name not in ['ruta']:
                if field.disabled:
                    value = self.get_initial_for_field(field, name)
                else:
                    value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
                try:
                    if isinstance(field, FileField):
                        initial = self.get_initial_for_field(field, name)
                        value = field.clean(value, initial)
                    else:
                        value = field.clean(value)
                    self.cleaned_data[name] = value
                    if hasattr(self, 'clean_%s' % name):
                        value = getattr(self, 'clean_%s' % name)()
                        self.cleaned_data[name] = value
                except ValidationError as e:
                    self.add_error(name, e)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
                if value == '':
                    self.cleaned_data[name] = None
                else:
                    self.cleaned_data[name] = models.Rutas.objects.get(id = value)

    def clean(self):
        cleaned_data = super().clean()

        hogar = models.Hogares.objects.get(id = self.initial['pk'])
        componente = models.Componentes.objects.get(id=self.initial['pk_componente'])
        ruta = cleaned_data['ruta']

        if ruta != None:
            if ruta.get_cupo_componente(componente) < 1:
                self.add_error('ruta', 'La ruta no tiene cupos disponibles')

    def __init__(self, *args, **kwargs):
        super(CambioRutaComponenteForm, self).__init__(*args, **kwargs)


        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Cambio de ruta',
                )
            ),
            Row(
                Column(
                    'ruta',
                    css_class="s12 "
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )


class CambioRutaVinculacionForm(forms.Form):

    ruta = forms.ModelChoiceField(label='Ruta destino',queryset=models.Rutas.objects.none(),required=False)


    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            if name not in ['ruta']:
                if field.disabled:
                    value = self.get_initial_for_field(field, name)
                else:
                    value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
                try:
                    if isinstance(field, FileField):
                        initial = self.get_initial_for_field(field, name)
                        value = field.clean(value, initial)
                    else:
                        value = field.clean(value)
                    self.cleaned_data[name] = value
                    if hasattr(self, 'clean_%s' % name):
                        value = getattr(self, 'clean_%s' % name)()
                        self.cleaned_data[name] = value
                except ValidationError as e:
                    self.add_error(name, e)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
                if value == '':
                    self.cleaned_data[name] = None
                else:
                    self.cleaned_data[name] = models.Rutas.objects.get(id = value)

    def clean(self):
        cleaned_data = super().clean()

        hogar = models.Hogares.objects.get(id = self.initial['pk'])
        ruta = cleaned_data['ruta']

        if ruta != None:
            if ruta.get_cupo_vinculacion() < 1:
                self.add_error('ruta', 'La ruta no tiene cupos disponibles')

    def __init__(self, *args, **kwargs):
        super(CambioRutaVinculacionForm, self).__init__(*args, **kwargs)


        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Cambio de ruta',
                )
            ),
            Row(
                Column(
                    'ruta',
                    css_class="s12 "
                )
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )




class ContactoCreateForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(ContactoCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Fieldset(
                    'Información del contacto',
                )
            ),
            Row(
                Column(
                    'municipio', css_class="s12"
                )
            ),
            Row(
                Column(
                    'nombres',css_class="s12 m6 l6"
                ),
                Column(
                    'apellidos', css_class="s12 m6 l6"
                )
            ),
            Row(
                Column(
                    'cargo', css_class="s12 m6 l4"
                ),
                Column(
                    'celular', css_class="s12 m6 l4"
                ),
                Column(
                    'email', css_class="s12 m6 l4"
                )
            ),
            Row(
                Column(
                    'resguardo', css_class="s12 m6 "
                ),
                Column(
                    'comunidad', css_class="s12 m6 "
                ),
                Column(
                    'lenguas', css_class="s12 m6 "
                ),
            ),
            Row(
                Column(
                    Div(
                        Submit(
                            'submit',
                            'Guardar',
                            css_class='button-submit'
                        ),
                        css_class="right-align"
                    ),
                    css_class="s12"
                ),
            )
        )

    class Meta:
        model = models.Contactos
        fields = ['municipio','nombres','apellidos','cargo','celular','email','resguardo','comunidad','lenguas']
        widgets = {
        }