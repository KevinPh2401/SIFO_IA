from django.urls import path
from . import views

from django.conf import settings
from django.contrib.staticfiles.urls import static
from libreria.views import deditos_view

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('usuarios/crear', views.crear, name='crear'),
    path('usuarios/editar', views.editar, name='editar'),
    path('eliminar/<int:id>', views.eliminar, name='eliminar'),
    path('usuarios/editar/<int:id>', views.editar, name='editar'),
    path('calculadora-deditos/', deditos_view, name='calculadora_deditos'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
