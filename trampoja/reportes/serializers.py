from rest_framework import serializers
from .models import Reportes, Motivos

class MotivosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Motivos
        fields = ['nome']


class ReportesSerializer(serializers.ModelSerializer):
    estabelecimento = serializers.ReadOnlyField(source="trampo.owner.estabelecimento.nome")
    freelancer_email = serializers.ReadOnlyField(source="freelancer.owner.email")

    class Meta:
        model = Reportes
        fields = [
            'id',
            'freelancer',
            'freelancer_email',
            'trampo',
            'estabelecimento',
            'descricao',
            'motivos',
            'created'
        ]
        depth = 1
