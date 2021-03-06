from rest_framework import serializers
from estabelecimentos.models import Estabelecimentos


class EstabelecimentosSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    cidade = serializers.ReadOnlyField(source='owner.endereco.cidade')
    rua = serializers.ReadOnlyField(source='owner.endereco.rua')
    numero = serializers.ReadOnlyField(source='owner.endereco.numero')
    bairro = serializers.ReadOnlyField(source='owner.endereco.bairro')

    class Meta:
        model = Estabelecimentos
        fields = [
            'id',
            'nome',
            'cnpj',
            'razao_social',
            'tipo',
            'telefone',
            'logo',
            'create',
            'owner',
            'cidade',
            'rua',
            'numero',
            'bairro',
            'ofertas_para_publicar'
        ]
