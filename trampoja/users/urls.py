from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [

    path('auth/register', views.CreateUserView.create, name='register'),
    path('auth/profile', views.ProfileUserView.profile, name='profile-user'),
    path('auth/detail/<int:pk>', views.DetailUserView.detail,
         name='detail-user'),
    path('auth/set-email', views.ChangeEmailView.setEmail, name='set-email'),
    path('auth/set-password', views.ChangePasswordView.setPassword,
         name='set-password'),
    path('auth/recovery-pswd', views.RecoveryPasswordView.recovery,
         name='recovery-password'),
    url(r'^login/$', views.Login.login, name='login')
]
