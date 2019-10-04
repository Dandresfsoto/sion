#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fest_2019 import models, forms

modelos = {
    'documento_1':{
        'model':models.Documento,
        'form':forms.DocumentoForm,
        'template':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/documento.html',
        'template_ver':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/documento_ver.html'

    },
    'documento_excel':{
        'model':models.DocumentoExcel,
        'form':forms.DocumentoExcelForm,
        'template':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/documento_excel.html',
        'template_ver':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/documento_excel_ver.html'

    },
    'fotos_4':{
        'model':models.Fotos4,
        'form':forms.Fotos4Form,
        'template':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/fotos4.html',
        'template_ver':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/fotos4_ver.html'

    },
    'fotos_5':{
        'model':models.Fotos5,
        'form':forms.Fotos5Form,
        'template':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/fotos5.html',
        'template_ver':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/fotos5_ver.html'

    },
    'fotos_6':{
        'model':models.Fotos6,
        'form':forms.Fotos6Form,
        'template':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/fotos6.html',
        'template_ver':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/fotos6_ver.html'

    },
    'fotos_2':{
        'model':models.Fotos2,
        'form':forms.Fotos2Form,
        'template':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/fotos2.html',
        'template_ver':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/fotos2_ver.html'

    },
    'fotos_1':{
        'model':models.Fotos1,
        'form':forms.Fotos1Form,
        'template':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/fotos1.html',
        'template_ver':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/fotos1_ver.html'

    },
    'caracterizacion_inicial':{
        'model':models.CaracterizacionInicial,
        'form':forms.CaracterizacionInicialForm,
        'template':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/caracterizacion_inicial.html',
        'template_ver':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/caracterizacion_inicial_ver.html'

    },
    'archivo_rar_zip':{
        'model':models.ArchivoRarZip,
        'form':forms.ArchivoRarZipForm,
        'template':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/archivo_rar_zip.html',
        'template_ver':'fest_2019/misrutas/actividades/hogares/instrumentos/templates/archivo_rar_zip_ver.html'

    },
}


def get_modelo(key):
    return modelos[key]