from django.contrib import admin
from .models import Confirmados


@admin.register(Confirmados)
class ConfirmadosAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'oferta', 'create']
    search_fields = ['id', 'owner', 'oferta', 'create']
