from django.urls import path
from . import views

urlpatterns = [

     path('ofertas/create', views.CreateOfertaView.create, name='create-ofertas'),
     path('ofertas/liste', views.ListOfertaView.liste, name='liste-ofertas'),
     path('ofertas/profile', views.ProfileOfertaView.profile, name='profile-ofertas'),
     path('ofertas/detail/<int:pk>',
          views.DetailOfertaView.detail, name='detail-ofertas'),
     path('ofertas/update/<int:pk>',
          views.UpdateOfertaView.update, name='update-ofertas'),
     path('ofertas/delete/<int:pk>',
          views.DeleteOfertaView.delete, name='delete-ofertas'),
]
