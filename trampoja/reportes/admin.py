from django.contrib import admin
from .models import Reportes, Motivos


@admin.register(Reportes)
class ReportesAdmin(admin.ModelAdmin):
    list_display = ['id', 'freelancer', 'descricao']
    search_fields = [ 'id', 'freelancer', 'descricao']

@admin.register(Motivos)
class MotivosAdmin(admin.ModelAdmin):
    list_display = ['id', 'motivo', 'nome']
    search_fields = ['id', 'motivo', 'nome']
