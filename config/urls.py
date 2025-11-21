# En config/urls.py - LA CONFIGURACIÓN FINAL

from django.contrib import admin
from django.urls import path
from core_lab import views as core_lab_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Página Principal (/) -> Muestra la vista de bienvenida 'home'.
    path('', core_lab_views.home, name='home'),
    
    # 2. Página de Simulación (/simulacion/) -> Muestra la vista 'simulacion'.
    path('simulacion/', core_lab_views.simulacion, name='simulacion'),
    
    # 3. Página de Materiales (/materiales/) -> Muestra la vista 'materiales'.
    path('materiales/', core_lab_views.materiales, name='materiales'),
    
    # 4. URLs de la API y de Descargas
    path('api/obtener_datos/', core_lab_views.obtener_datos, name='obtener_datos'),
    path('download/material/<str:material_name>/', core_lab_views.download_material_data, name='download_material_data'),
]