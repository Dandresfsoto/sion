from rest_framework import serializers
from .models import ProyectosApi


class ProyectosApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProyectosApi
        fields = ['json']

    def create(self, validated_data):

        try:
            documento_gestor = validated_data['json']['documento']
            tipo_proyecto = validated_data['json']['data']['project_type']

            documentos_hogares = []

            for manager in validated_data['json']['data']['managers']:
                documentos_hogares.append(manager['document'])

            documentos_hogares = set(documentos_hogares)

        except:
            instance = ProyectosApi.objects.create(**validated_data)
        else:
            query = ProyectosApi.objects.filter(json__documento=documento_gestor, json__data__project_type=tipo_proyecto)
            if query.count() > 0:

                copiado = False

                for proyecto in query:
                    documentos = set(proyecto.get_documentos_managers())

                    interseccion = documentos_hogares.intersection(documentos)

                    if len(interseccion) > 0:
                        instance = proyecto
                        instance.json = validated_data['json']
                        instance.save()
                        copiado = True
                        break

                if copiado == False:
                    instance = ProyectosApi.objects.create(**validated_data)

            else:
                instance = ProyectosApi.objects.create(**validated_data)
        return instance
