from django.db.models import Manager
from rest_framework.exceptions import NotFound, ValidationError


class MotivoManager(Manager):
    def get_motivo(self, key):
        try:
            return self.get(motivo=key)
        except Exception:
            raise NotFound(detail=["Motivo não encontrado."])


class ReporteManager(Manager):
    def get_reporte(self, pk):
        try:
            return self.get(pk=pk)
        except Exception:
            raise NotFound(detail=["Reporte não encontrado."])

    def trampoJaReportado(self, data):
        if self.filter(freelancer=data['freelancer'], trampo=data['oferta']):
            return True
        
        return False

    def create_reporte(self, reporte):
        try:
            return self.create(
                freelancer_id=reporte['freelancer'],
                trampo_id=reporte['oferta'],
                descricao=reporte['descricao']
            )
        except Exception:
            raise ValidationError("Não foi possível reportar")
