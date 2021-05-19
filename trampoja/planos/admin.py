from django.contrib import admin
from .models import Planos

@admin.register(Planos)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'valor', 'quantidade', 'descricao', 'especial']
