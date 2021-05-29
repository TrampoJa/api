from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('website.urls')),
    url(r'^', include('users.urls')),
    url(r'^', include('ofertas.urls')),
    url(r'^', include('interesses.urls')),
    url(r'^', include('confirmados.urls')),
    url(r'^', include('cancelados.urls')),
    url(r'^', include('freelancers.urls')),
    url(r'^', include('estabelecimentos.urls')),
    url(r'^', include('avaliacoes.urls')),
    url(r'^', include('enderecos.urls')),
    url(r'^', include('planos.urls')),
    url(r'^token/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
