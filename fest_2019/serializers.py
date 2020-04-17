from rest_framework import serializers
from .models import ProyectosApi


class ProyectosApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProyectosApi
        fields = ['json']
