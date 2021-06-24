from django.contrib import admin
from .models import FreeLancers, Documentos


@admin.register(FreeLancers)
class FreelancerAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'sobrenome', 'rg', 'nascimento', 'telefone', 'create', 'verificado']
    search_fields = ['nome', 'rg', 'telefone', 'verificado']

@admin.register(Documentos)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['freelancer', 'frente', 'verso', 'selfie', 'create']
    search_fields = ['freelancer__id']
