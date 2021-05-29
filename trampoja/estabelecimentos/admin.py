from django.contrib import admin
from .models import Estabelecimentos

@admin.register(Estabelecimentos)
class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf_cnpj', 'telefone', 'plano_contratado',
                    'ofertas_para_publicar', 'create', 'tipo']
    search_fields = ['nome', 'cpf_cnpj', 'telefone',]
