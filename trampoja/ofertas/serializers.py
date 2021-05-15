from rest_framework import serializers
from .models import Ofertas
from avaliacoes.models import Avaliacoes
from django.db.models import Avg


class OfertasSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    estabelecimento = serializers.ReadOnlyField(source='owner.estabelecimento.nome')
    estabelecimento_id = serializers.ReadOnlyField(source='owner.estabelecimento.id')
    logo = serializers.ImageField(source='owner.estabelecimento.logo', allow_null=True, read_only=True)
    telefone = serializers.ReadOnlyField(source='owner.estabelecimento.telefone')
    cidade = serializers.ReadOnlyField(source='owner.endereco.cidade')
    rua = serializers.ReadOnlyField(source='owner.endereco.rua')
    numero = serializers.ReadOnlyField(source='owner.endereco.numero')
    bairro = serializers.ReadOnlyField(source='owner.endereco.bairro')
    avaliacao = serializers.SerializerMethodField()

    def get_avaliacao(self, oferta):
        avaliacao = Avaliacoes.objects.filter(owner_id=oferta.owner.id).aggregate(Avg('nota'))
        return avaliacao['nota__avg']

    class Meta:
        model = Ofertas
        fields = [
            'id',
            'nome',
            'valor',
            'time',
            'time_final',
            'date_inicial',
            'obs',
            'create',
            'owner',
            'estabelecimento',
            'estabelecimento_id',
            'telefone',
            'cidade',
            'rua',
            'numero',
            'bairro',
            'status',
            'edit',
            'canceled',
            'closed',
            'logo',
            'avaliacao'
        ]