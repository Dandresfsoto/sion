from rest_framework import serializers
from .models import ProyectosApi
from usuarios.models import User


class ProyectosApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProyectosApi
        fields = ['id','json']
        read_only_fields = ['id']

    def validate_json(self, validated_data):
        try:
            documento_gestor = validated_data['documento']
            tipo_proyecto = validated_data['data']['project_type']

            documentos_hogares = []

            for manager in validated_data['data']['managers']:
                documentos_hogares.append(manager['document'])

            documentos_hogares = set(documentos_hogares)

        except:
            pass
        else:

            query = ProyectosApi.objects.filter(json__documento=documento_gestor,json__data__project_type=tipo_proyecto)
            if query.count() > 0:

                for proyecto in query:
                    documentos = set(proyecto.get_documentos_managers())

                    interseccion = documentos_hogares.intersection(documentos)

                    if len(interseccion) > 0:
                        if not proyecto.actualizar_app:
                            raise serializers.ValidationError("El proyecto no permite ser actualizado")



        return validated_data



    def create(self, validated_data):

        try:
            documento_gestor = validated_data['json']['documento']
            tipo_proyecto = validated_data['json']['data']['project_type']

            documentos_hogares = []

            for manager in validated_data['json']['data']['managers']:
                documentos_hogares.append(manager['document'])

            documentos_hogares = set(documentos_hogares)

        except:
            try:
                user = User.objects.get(cedula=documento_gestor)
            except:
                user = None

            instance = ProyectosApi.objects.create(**validated_data)
            instance.agregar_observacion(user=user, estado = "Cargado", descripcion="Proyecto creado")
        else:

            try:
                user = User.objects.get(cedula=documento_gestor)
            except:
                user = None

            query = ProyectosApi.objects.filter(json__documento=documento_gestor, json__data__project_type=tipo_proyecto)
            if query.count() > 0:

                copiado = False

                for proyecto in query:
                    proyecto.agregar_observacion(user=user, estado="Actualización", descripcion="Proyecto actualizado")
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
                    instance.agregar_observacion(user=user, estado="Cargado",descripcion="Proyecto creado")

            else:
                instance = ProyectosApi.objects.create(**validated_data)
                instance.agregar_observacion(user=self.user, estado="Cargado", descripcion="Proyecto creado")
        return instance
