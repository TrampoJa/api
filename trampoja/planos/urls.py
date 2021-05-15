from django.urls import path
from . import views

urlpatterns = [
    path('planos/set', views.setPlanoEstabelecimento.create, name='set-plano'),
    path('planos/liste', views.ListPlanosView.liste, name='liste-planos'),
    path('planos/profile', views.ProfilePlanosView.profile, name='profile-planos'),
]