# ==========================================================
#  src/corelab/apps.py - Configuración de la App
# ==========================================================
#  Este archivo le dice a Django cómo debe tratar a la
#  aplicación 'corelab'.
#
#  CORRECCIONES PARA LA MODULARIZACIÓN:
#  - El atributo 'name' ha sido actualizado de 'core_lab' a
#    'corelab' para coincidir con el nuevo nombre del paquete.
# ==========================================================
from django.apps import AppConfig

class CoreLabConfig(AppConfig):
    """
    Clase de configuración para la aplicación 'corelab'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    
    # --- ¡ESTA ES LA LÍNEA CRÍTICA Y CORREGIDA! ---
    # El nombre debe coincidir EXACTAMENTE con el nombre del directorio
    # del paquete/aplicación.
    name = 'corelab'