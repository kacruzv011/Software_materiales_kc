# ==============================================================================
#  src/project_config/urls.py - Directorio de URLs Principal
# ==============================================================================
#  Este archivo es el punto de entrada principal para el enrutamiento de URLs
#  en el proyecto. Mapea las rutas URL a las funciones de vista correspondientes.
#
#  CORRECCIONES PARA LA MODULARIZACIÓN:
#  - El import 'from core_lab ...' ha sido actualizado a 'from corelab ...'
#    para reflejar el nuevo nombre del paquete (sin guion bajo).
# ==============================================================================
"""
URL configuration for the CoreLab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings  # Importamos settings
from django.conf.urls.static import static  # Importamos la utilidad para archivos estáticos/media

# --- ¡CAMBIO CRÍTICO PARA LA MODULARIZACIÓN! ---
# Importamos las vistas desde el paquete 'corelab' (sin guion bajo)
from corelab import views as corelab_views

# --- Lista de patrones de URL ---
# Django revisa cada patrón en orden hasta que encuentra una coincidencia.
urlpatterns = [
    # Ruta para el panel de administración de Django
    path('admin/', admin.site.urls),

    # --- PÁGINAS PRINCIPALES DEL SITIO ---
    # La raíz del sitio ('') se mapea a la vista 'home'.
    path('', corelab_views.home, name='home'),
    
    # URL para la página del simulador
    path('simulacion/', corelab_views.simulacion, name='simulacion'),
    
    # URL para el catálogo de materiales
    path('materiales/', corelab_views.materiales, name='materiales'),
    
    # --- ENDPOINTS DE API Y DESCARGAS ---
    # Endpoint que el JavaScript del simulador utiliza para obtener datos
    path('api/obtener_datos/', corelab_views.obtener_datos, name='obtener_datos'),
    
    # Endpoint dinámico para descargar el CSV de un material específico
    path('download/material/<str:material_name>/', corelab_views.download_material_data, name='download_material_data'),
]

# --- ¡CONFIGURACIÓN ADICIONAL E IMPORTANTE! ---
# Esto le dice a Django que, DURANTE EL DESARROLLO (cuando DEBUG=True),
# debe servir los archivos que los usuarios suben (ej. los PDFs).
# Esto es necesario para que tu management command pueda encontrar los PDFs que coloques en 'media/'.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)