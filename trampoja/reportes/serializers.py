from rest_framework import serializers
from .models import Reportes


class ReportesSerializer(serializers.ModelSerializer):
    motivos = serializers.MethodField()

    def get_motivos(self, reporte):
        return reporte.motivos.all()

    class Meta:
        model = Reportes
        fields = [
            'id',
            'freelancer',
            'motivos',
            'nome',
            'created'
        ]
