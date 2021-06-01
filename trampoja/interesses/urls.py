from django.urls import path
from . import views

urlpatterns = [

    path('interesse', views.CreateInteresseView.create, name='interesse'),
    path('f_interesses/', views.ListToFreelancerInteresseView.listToFreelancer,
         name='f_interesses'),
    path('e_interesses/', views.ListToEstabelecimentoInteresseView.listToEstabelecimento,
         name='e_interesses')
]
