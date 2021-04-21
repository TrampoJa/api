from django.urls import path
from . import views

urlpatterns = [
    
    path('avaliacao', views.CreateAvaliacaoView.create, name='avaliacao'),
    path('avaliacao/get', views.GetSelfAvaliacaoView.getSelf, name='get-avaliacao'),
]