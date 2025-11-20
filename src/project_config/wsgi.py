# ==============================================================================
#  src/project_config/wsgi.py - Interfaz del Servidor Web
# ==============================================================================
#  Este archivo configura la interfaz de la aplicación web de Django para
#  servidores compatibles con el estándar WSGI. Es el punto de entrada
#  para servidores de producción como Gunicorn o uWSGI.
#
#  CORRECCIONES PARA LA MODULARIZACIÓN:
#  - Al igual que en manage.py, se añade el directorio 'src/' al path de Python.
#  - Se actualiza 'DJANGO_SETTINGS_MODULE' para apuntar a la nueva
#    ubicación del archivo de configuración ('project_config.settings').
# ==============================================================================

"""
WSGI config for CoreLab project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# --- ¡INICIO DE LA CORRECCIÓN PARA MODULARIZACIÓN! ---
#  Este bloque asegura que el servidor web pueda encontrar tus aplicaciones
#  dentro del directorio 'src/'.
#
#  1. Obtenemos la ruta raíz del proyecto (la carpeta que contiene 'src/').
#     'Path(__file__).resolve().parent' nos da 'src/project_config/'.
#     '.parent.parent' sube dos niveles hasta 'Software_materiales_kc/'.
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / 'src'
#  2. Insertamos la carpeta 'src/' al principio del path de búsqueda de Python.
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
# --- FIN DE LA CORRECCIÓN ---


# --- ¡SEGUNDA CORRECCIÓN PARA MODULARIZACIÓN! ---
# Apuntamos a la nueva ubicación del archivo de settings.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_config.settings')


# La variable 'application' es la que el servidor web utilizará.
application = get_wsgi_application()