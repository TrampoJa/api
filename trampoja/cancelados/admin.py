from django.contrib import admin
from .models import Cancelados


@admin.register(Cancelados)
class CanceladosAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'justificativa', 'owner', 'oferta', 'autor', 'create']
    search_fields = [
        'id', 'justificativa', 'owner', 'oferta', 'autor', 'create']
