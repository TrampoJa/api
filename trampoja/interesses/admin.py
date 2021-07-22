from django.contrib import admin
from .models import Interesses


@admin.register(Interesses)
class InteressesAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'oferta', 'create']
    search_fields = ['id', 'owner', 'oferta', 'create']
