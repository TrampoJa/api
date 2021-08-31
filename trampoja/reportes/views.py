from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from .serializers import ReportesSerializer
from .models import Reportes, Motivos
from .permissions import IsOwnerOrReadOnly
from .tasks import task_send_reportes_message

from ofertas.views import get_oferta


class CreateReporteView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    @login_required()
    def create(request, format=None):
        if Reportes.manager.trampoJaReportado(request.data):
            raise ValidationError(detail="Ops, você já reportou este trampo!")

        oferta = get_oferta(request.data['oferta'])

        if not oferta.closed:
            raise ValidationError(detail="O trampo precisa estar finalizado para poder ser reportado.")

        try:
            if IsOwnerOrReadOnly.has_object_permission(request, oferta):
                reporte = Reportes.manager.create_reporte(request.data)
                motivos = request.data['motivos']

                for key in motivos:
                    if motivos[key] == True:
                        motivo = Motivos.manager.get_motivo(key)
                        
                        reporte.motivos.add(motivo)
                
                reporteSerializer = ReportesSerializer(reporte)

                task_send_reportes_message.delay()
                
                return Response(reporteSerializer.data, status=status.HTTP_201_CREATED)

            raise PermissionDenied(detail=["Você não tem permissão para isso."])

        except Exception:
            raise ValidationError("Não foi possível reportar")


class GetReportesFreelancerView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def get(request, pk):
        try:
            reportes = Reportes.manager.filter(freelancer=pk)
            reportesSerializer = ReportesSerializer(reportes, many=True)

            return Response(reportesSerializer.data)
        
        except Exception:
            raise ValidationError("Não foi possível listar os reportes")
