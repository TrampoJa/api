from rest_framework import serializers
from enderecos.models import Enderecos


class EnderecosSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Enderecos
        fields = [
            'id',
            'pais',
            'estado',
            'cidade',
            'bairro',
            'rua',
            'numero',
            'complemento',
            'logradouro',
            'owner',
        ]
