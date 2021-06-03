from django.urls import path
from . import views

urlpatterns = [
    path('planos/set', views.setPlanoEstabelecimento.set_plano,
         name='set-plano'),
    path('planos/liste', views.ListPlanosView.liste, name='liste-planos'),
]
