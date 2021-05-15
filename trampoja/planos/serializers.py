from rest_framework import serializers
from .models import Planos


class PlanosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planos
        fields = '__all__'