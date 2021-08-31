from rest_framework import serializers
from .models import Reportes, Motivos

class MotivosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Motivos
        fields = ['nome']


class ReportesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reportes
        fields = [
            'id',
            'freelancer',
            'trampo',
            'descricao',
            'motivos',
            'created'
        ]
        depth = 1
