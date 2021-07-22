from django.contrib import admin
from .models import Avaliacoes


@admin.register(Avaliacoes)
class AvaliacoesAdmin(admin.ModelAdmin):
    list_display = ['id', 'nota', 'owner', 'oferta', 'create']
    search_fields = ['id', 'nota', 'owner', 'oferta', 'create']
