from django.db import models
from rest_framework.exceptions import NotFound

class PlanosManager(models.Manager):
    def get_plano(self, pk):
        try:
            return self.get(pk=pk)
        except Exception:
            raise NotFound(detail="Plano não encontrado.")

    def set_plano(self, estabelecimento, plano):
        estabelecimento.plano_contratado = plano
        estabelecimento.ofertas_para_publicar = plano.quantidade
        estabelecimento.save()
        return estabelecimento.data