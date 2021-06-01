from rest_framework import serializers
from cancelados.models import Cancelados


class CanceladosSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    oferta = serializers.ReadOnlyField(source='oferta.id')
    freelancer = serializers.ReadOnlyField(source='owner.freelancer.id')
    oferta_nome = serializers.ReadOnlyField(source='oferta.nome')
    oferta_valor = serializers.ReadOnlyField(source='oferta.valor')
    oferta_hora = serializers.ReadOnlyField(source='oferta.time')
    oferta_hora_final = serializers.ReadOnlyField(source='oferta.time_final')
    oferta_data = serializers.ReadOnlyField(source='oferta.date_inicial')
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
    estabelecimento_telefone = serializers.ReadOnlyField(
        source='oferta.owner.estabelecimento.telefone')
    estabelecimento_owner = serializers.ReadOnlyField(source='oferta.owner.id')
    estabelecimento_email = serializers.ReadOnlyField(
        source='oferta.owner.email')

    class Meta:
        model = Cancelados
        fields = [
            'id',
            'justificativa',
            'oferta',
            'freelancer',
            'owner',
            'autor',
            'oferta_nome',
            'oferta_valor',
            'oferta_hora',
            'oferta_hora_final',
            'oferta_data',
            'freelancer_nome',
            'freelancer_sobrenome',
            'freelancer_telefone',
            'freelancer_bio',
            'freelancer_owner',
            'freelancer_email',
            'estabelecimento',
            'estabelecimento_owner',
            'estabelecimento_id',
            'estabelecimento_telefone',
            'estabelecimento_email',
            'create'
        ]
