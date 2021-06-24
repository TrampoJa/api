from django.urls import path
from . import views

urlpatterns = [

     path('confirmado', views.CreateConfirmadoView.create, name='confirmado'),
     path('f_confirmados/', views.ListToFreelancerConfirmadoView.listToFreelancer,
          name='f_confirmados'),
     path('e_confirmados/', views.ListToEstabelecimentoConfirmadoView.listToEstabelecimento,
          name='e_confirmados'),
]
