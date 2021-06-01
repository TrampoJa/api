from rest_framework import serializers
from avaliacoes.models import Avaliacoes


class AvaliacoesSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Avaliacoes
        fields = [
            'id',
            'nota',
            'owner',
            'oferta',
            'create'
        ]
