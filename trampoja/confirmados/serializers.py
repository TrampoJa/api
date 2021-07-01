from rest_framework import serializers
from confirmados.models import Confirmados
from avaliacoes.models import Avaliacoes
from django.db.models import Avg


class ConfirmadosSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    oferta = serializers.ReadOnlyField(source='oferta.id')
    freelancer = serializers.ReadOnlyField(source='owner.freelancer.id')
    oferta_nome = serializers.ReadOnlyField(source='oferta.nome')
    oferta_valor = serializers.ReadOnlyField(source='oferta.valor')
    oferta_hora = serializers.ReadOnlyField(source='oferta.time')
    oferta_hora_final = serializers.ReadOnlyField(source='oferta.time_final')
    oferta_data = serializers.ReadOnlyField(source='oferta.date_inicial')
    oferta_closed = serializers.ReadOnlyField(source='oferta.closed')
    freelancer_nome = serializers.ReadOnlyField(source='owner.freelancer.nome')
    freelancer_sobrenome = serializers.ReadOnlyField(
        source='owner.freelancer.sobrenome')
    freelancer_telefone = serializers.ReadOnlyField(
        source='owner.freelancer.telefone')
    freelancer_bio = serializers.ReadOnlyField(source='owner.freelancer.bio')
    freelancer_owner = serializers.ReadOnlyField(
        source='owner.freelancer.owner.id')
    freelancer_email = serializers.ReadOnlyField(
        source='owner.freelancer.owner.email')
    estabelecimento = serializers.ReadOnlyField(
        source='oferta.owner.estabelecimento.nome')
    estabelecimento_id = serializers.ReadOnlyField(
        source='oferta.owner.estabelecimento.id')
    estabelecimento_owner = serializers.ReadOnlyField(source='oferta.owner.id')
    avaliacao = serializers.SerializerMethodField()
    freelancer_avaliacao = serializers.SerializerMethodField()
    estabelecimento_avaliacao = serializers.SerializerMethodField()
    trampos = serializers.SerializerMethodField()

    def get_avaliacao(self, confirmado):
        avaliacao = Avaliacoes.objects.filter(
            owner_id=confirmado.owner.id).aggregate(Avg('nota'))
        return avaliacao['nota__avg']

    def get_freelancer_avaliacao(self, confirmado):
        try:
            avaliacao = Avaliacoes.objects.get(
                owner_id=confirmado.oferta.owner_id, oferta=confirmado.oferta)
            return avaliacao.nota
        except Avaliacoes.DoesNotExist:
            ...

    def get_estabelecimento_avaliacao(self, confirmado):
        try:
            avaliacao = Avaliacoes.objects.get(
                owner_id=confirmado.owner.id, oferta=confirmado.oferta)
            return avaliacao.nota
        except Avaliacoes.DoesNotExist:
            ...

    def get_trampos(self, confirmado):
        trampos = Confirmados.objects.filter(
            owner=confirmado.owner, oferta_id__closed=True).count()
        return trampos

    class Meta:
        model = Confirmados
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
            'oferta_closed',
            'freelancer_nome',
            'freelancer_sobrenome',
            'freelancer_telefone',
            'freelancer_bio',
            'freelancer_owner',
            'freelancer_email',
            'estabelecimento',
            'estabelecimento_owner',
            'estabelecimento_id',
            'avaliacao',
            'trampos',
            'freelancer_avaliacao',
            'estabelecimento_avaliacao',
            'create'
        ]
