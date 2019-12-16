#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fest_2019 import models, forms

modelos = {
    'documento_1':{
        'model':models.Documento,
        'form':forms.DocumentoForm,
        'template':'fest_2019/misrutas/actividades/instrumentos/templates/documento.html',
        'template_ver':'fest_2019/misrutas/actividades/instrumentos/templates/documento_ver.html'
    },
    'acta_socializacion_comunidades':{
        'model':models.ActaSocializacionComunidades,
        'form':forms.ActaSocializacionComunidadesForm,
        'template':'fest_2019/misrutas/actividades/instrumentos/templates/acta_socializacion_comunidades.html',
        'template_ver':'fest_2019/misrutas/actividades/instrumentos/templates/acta_socializacion_comunidades_ver.html'
    },
    'acta_vinculacion_hogar':{
        'model':models.ActaVinculacionHogar,
        'form':forms.ActaVinculacionHogarForm,
        'template':'fest_2019/misrutas/actividades/instrumentos/templates/acta_vinculacion_hogar.html',
        'template_ver':'fest_2019/misrutas/actividades/instrumentos/templates/acta_vinculacion_hogar_ver.html'
    },
}


def get_modelo(key):
    return modelos[key]