# ==============================================================================
#  src/project_config/asgi.py - Interfaz de Servidor Asíncrono
# ==============================================================================
#  Este archivo configura la interfaz de la aplicación web de Django para
#  servidores compatibles con el estándar ASGI (el sucesor de WSGI). Es el
#  punto de entrada para servidores asíncronos como Uvicorn o Daphne y es
#  necesario para funcionalidades en tiempo real (ej. WebSockets).
#
#  CORRECCIONES PARA LA MODULARIZACIÓN:
#  - Al igual que en manage.py/wsgi.py, se añade el directorio 'src/' al
#    path de Python y se actualiza 'DJANGO_SETTINGS_MODULE'.
# ==============================================================================

"""
ASGI config for CoreLab project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

# --- ¡INICIO DE LA CORRECCIÓN PARA MODULARIZACIÓN! ---
#  Añadimos 'src/' al path para que el servidor pueda encontrar los módulos.
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
# --- FIN DE LA CORRECCIÓN ---


# --- ¡SEGUNDA CORRECCIÓN PARA MODULARIZACIÓN! ---
# Apuntamos a la nueva ubicación del archivo de settings.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_config.settings")

# La variable 'application' es la que el servidor asíncrono utilizará.
application = get_asgi_application()