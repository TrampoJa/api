from django.urls import path
from . import views, views_upload

urlpatterns = [
     path('freelancer/create', views.CreateFreeLancerView.create,
          name='create-freelancer'),
     path('freelancer/liste', views.ListFreeLancerView.liste,
          name='liste-freelancer'),
     path('freelancer/profile', views.ProfileFreeLancerView.profile,
          name='profile-freelancer'),
     path('freelancer/detail/<int:pk>',
          views.DetailFreeLancerView.detail, name='detail-freelancer'),
     path('freelancer/update/<int:pk>',
          views.UpdateFreeLancerView.update, name='update-freelancer'),
     path('freelancer/delete/<int:pk>',
          views.DeleteFreeLancerView.delete, name='delete-freelancer'),
     path('freelancer/count-ofertas',
          views.CountOfertasConfirmadasFreelancerView.count, name='count-ofertas'),
     path('freelancer/historico/<int:pk>',
          views.HistoricoFreelancerView.historico, name='historico'),

     path('freelancer/upload/<int:pk>',
          views_upload.UploadImageView.upload, name='upload'),  
     path('freelancer/upload-docs/<int:step>',
          views_upload.UploadImageDocsView.upload, name='upload-docs')
]
