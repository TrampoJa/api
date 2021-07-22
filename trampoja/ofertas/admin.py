from django.contrib import admin
from .models import Ofertas


@admin.register(Ofertas)
class OfertasAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'nome', 'valor', 'time', 'time_final', 'date_inicial', 'obs',
        'owner', 'create', 'status', 'edit', 'canceled', 'closed'
    ]
    search_fields = [
        'id', 'nome', 'valor', 'time', 'time_final', 'obs', 
        'owner' 'create', 'status', 'edit', 'canceled', 'closed'
    ]
