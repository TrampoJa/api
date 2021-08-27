from django.urls import path
from . import views

urlpatterns = [
    path('reportar', views.CreateReporteView.create, name='create-reporte'),
    path('reportes/<int:pk>', views.GetReportesFreelancerView.get, name='reportes')
]
