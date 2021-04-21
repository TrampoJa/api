from rest_framework import serializers
from interesses.models import Interesses
from avaliacoes.models import Avaliacoes
from confirmados.models import Confirmados
from django.db.models import Avg


class InteressesSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    oferta = serializers.ReadOnlyField(source='oferta.id')
    freelancer = serializers.ReadOnlyField(source='owner.freelancer.id')
    oferta_nome = serializers.ReadOnlyField(source='oferta.nome')
    oferta_valor = serializers.ReadOnlyField(source='oferta.valor')
    oferta_hora = serializers.ReadOnlyField(source='oferta.time')
    oferta_hora_final = serializers.ReadOnlyField(source='oferta.time_final')
    oferta_data = serializers.ReadOnlyField(source='oferta.date_inicial')
    oferta_status = serializers.ReadOnlyField(source='oferta.status')
    oferta_canceled = serializers.ReadOnlyField(source='oferta.canceled')
    freelancer_nome = serializers.ReadOnlyField(source='owner.freelancer.nome')
    freelancer_owner = serializers.ReadOnlyField(source='owner.freelancer.owner.id')
    freelancer_sobrenome = serializers.ReadOnlyField(source='owner.freelancer.sobrenome')
    freelancer_telefone = serializers.ReadOnlyField(source='owner.freelancer.telefone')
    freelancer_bio = serializers.ReadOnlyField(source='owner.freelancer.bio')
    estabelecimento = serializers.ReadOnlyField(source='oferta.owner.estabelecimento.nome')
    estabelecimento_telefone = serializers.ReadOnlyField(source='oferta.owner.estabelecimento.telefone')
    estabelecimento_id = serializers.ReadOnlyField(source='oferta.owner.estabelecimento.id')
    estabelecimento_owner = serializers.ReadOnlyField(source='oferta.owner.id')
    estabelecimento_email = serializers.ReadOnlyField(source='oferta.owner.email')
    avaliacao = serializers.SerializerMethodField()
    trampos = serializers.SerializerMethodField()

    def get_avaliacao(self, interesse):
        avaliacao = Avaliacoes.objects.filter(owner_id=interesse.owner.id).aggregate(Avg('nota'))
        return avaliacao['nota__avg']
    
    def get_trampos(self, interesse):
        trampos = Confirmados.objects.filter(owner=interesse.owner, oferta_id__closed=True).count()
        return trampos

    class Meta:
        model = Interesses
        fields = [
            'id',
            'oferta',
            'freelancer',
            'freelancer_owner',
            'owner',
            'oferta_nome',
            'oferta_valor',
            'oferta_hora',
            'oferta_hora_final',
            'oferta_data',
            'oferta_status',
            'oferta_canceled',
            'freelancer_nome',
            'freelancer_sobrenome',
            'freelancer_telefone',
            'freelancer_bio',
            'estabelecimento',
            'estabelecimento_telefone',
            'estabelecimento_owner',
            'estabelecimento_id',
            'estabelecimento_email',
            'avaliacao',
            'trampos',
            'create'
        ]