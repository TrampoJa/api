from rest_framework import serializers
from users.models import User
from freelancers.models import FreeLancers


class FreeLancersSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    cidade = serializers.ReadOnlyField(source='owner.endereco.cidade')
    rua = serializers.ReadOnlyField(source='owner.endereco.rua')
    numero = serializers.ReadOnlyField(source='owner.endereco.numero')
    bairro = serializers.ReadOnlyField(source='owner.endereco.bairro')

    class Meta:
        model = FreeLancers
        fields = [
            'id',
            'nome' ,
            'sobrenome',
            'telefone',
            'nascimento',
            'foto',
            'rg',
            'foto_doc',
            'bio',
            'create',
            'owner',
            'cidade',
            'rua',
            'numero',
            'bairro'
        ]