from django.urls import path
from . import views

urlpatterns = [
    path('endereco/create', views.CreateEnderecoView.create, name='create-endereco'),
    path('endereco/profile', views.ProfileEnderecoView.profile,
         name='profile-endereco'),
    path('endereco/update/<int:pk>',
         views.UpdateEnderecoView.update, name='update-endereco'),
]
