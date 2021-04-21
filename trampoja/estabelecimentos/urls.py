from django.urls import path
from . import views, views_upload

urlpatterns = [
    
    path('estabelecimento/create', views.CreateEstabelecimentoView.create, name='create-estabelecimento'),
    path('estabelecimento/liste', views.ListEstabelecimentoView.liste, name='liste-estabelecimento'),
    path('estabelecimento/profile', views.ProfileEstabelecimentoView.profile, name='profile-estabelecimento'),
    path('estabelecimento/detail/<int:pk>', views.DetailEstabelecimentoView.detail, name='detail-estabelecimento'),
    path('estabelecimento/update/<int:pk>', views.UpdateEstabelecimentoView.update, name='update-estabelecimento'),
    path('estabelecimento/delete/<int:pk>', views.DeleteEstabelecimentoView.delete, name='delete-estabelecimento'),

    path('estabelecimento/upload/<int:pk>', views_upload.UploadImageView.upload, name='upload'),
]