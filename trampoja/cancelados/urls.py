from django.urls import path
from . import views

urlpatterns = [
    
    path('cancelar', views.CreateCanceladoView.create, name='cancelar'),
    path('f_cancelados/', views.ListToFreelancerCanceladosView.listToFreelancer, name='f_cancelados'),
    path('e_cancelados/', views.ListToEstabelecimentoCanceladosView.listToEstabelecimento, name='e_cancelados'),
]