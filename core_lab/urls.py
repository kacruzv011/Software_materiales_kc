# core_lab/urls.py - VERSIÓN CORREGIDA Y LIMPIA
from django.urls import path
from . import views

app_name = "core_lab"

urlpatterns = [
    # No definimos la ruta '' aquí. Eso se hace en el urls.py principal.
    
    # Páginas del sistema
    path('simulacion/', views.simulacion, name='simulacion'),
    path('materiales/', views.materiales, name='materiales'),

    # API y descargas
    path('obtener_datos/', views.obtener_datos, name='obtener_datos'),
    path('plot.png', views.plot_png, name='plot_png'),
    path('download/data.csv', views.download_csv, name='download_csv'),
]