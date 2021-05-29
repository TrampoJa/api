from django.contrib import admin
from .models import Historico

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ['estabelecimento', 'plano', 'create']
