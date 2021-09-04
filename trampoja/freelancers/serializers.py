from rest_framework import serializers
from .models import FreeLancers, Documentos

from reportes.models import Reportes


class FreeLancersSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    cidade = serializers.ReadOnlyField(source='owner.endereco.cidade')
    rua = serializers.ReadOnlyField(source='owner.endereco.rua')
    numero = serializers.ReadOnlyField(source='owner.endereco.numero')
    bairro = serializers.ReadOnlyField(source='owner.endereco.bairro')
    reportes = serializers.SerializerMethodField()

    def get_reportes(self, freelancer):
        return Reportes.manager.filter(freelancer=freelancer.id).count()

    class Meta:
        model = FreeLancers
        fields = [
            'id',
            'nome',
            'sobrenome',
            'telefone',
            'nascimento',
            'foto',
            'rg',
            'bio',
            'create',
            'owner',
            'cidade',
            'rua',
            'numero',
            'bairro',
            'reportes'
        ]


class DocumentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documentos
        fields = '__all__'
