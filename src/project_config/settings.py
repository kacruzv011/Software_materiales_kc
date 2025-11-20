# ==============================================================================
#  ARCHIVO DE CONFIGURACIÓN DE DJANGO (settings.py)
# ==============================================================================
#  Este archivo actúa como el "panel de control" central para toda la aplicación
#  Django. Define la configuración de la base de datos, las aplicaciones instaladas,
#  las rutas a plantillas y archivos estáticos, y mucho más.
#
#  Este archivo ha sido adaptado para una ESTRUCTURA MODULAR con un directorio 'src/'.
# ==============================================================================

import os
from pathlib import Path

# ==============================================================================
#  1. CONFIGURACIÓN BÁSICA DE RUTAS
# ==============================================================================

# BASE_DIR define la ruta absoluta a la raíz del proyecto. Es la carpeta que
# contiene 'manage.py' y 'src/'.
# ¡CORRECCIÓN CLAVE! Como este archivo está en 'src/project_config/', debemos
# subir tres niveles (.parent.parent.parent) para llegar a la raíz.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ==============================================================================
#  2. CONFIGURACIÓN DE SEGURIDAD Y DESARROLLO
# ==============================================================================

# SECRET_KEY es una clave única para tu instalación de Django.
# ¡NUNCA la compartas ni la subas a un repositorio público con su valor real!
# En producción, esta clave debe leerse desde una variable de entorno.
SECRET_KEY = "django-insecure-55zs@2+evxrtp3kt3vu+2n4!5$p!(unqlvq^en2g=-*=pjub7$"

# DEBUG = True muestra páginas de error detalladas. Es muy útil para el desarrollo.
# ¡ADVERTENCIA! En producción, esto DEBE ser False para no exponer información sensible.
DEBUG = True

# ALLOWED_HOSTS es una lista de los nombres de dominio que tu sitio puede servir.
# En producción, aquí irían tus dominios, ej: ['www.corelab.com', 'corelab.com']
ALLOWED_HOSTS = []


# ==============================================================================
#  3. APLICACIONES
# ==============================================================================
# INSTALLED_APPS es la lista de todas las "apps" que componen tu proyecto.
# Django las usa para encontrar modelos, plantillas, comandos, etc.
INSTALLED_APPS = [
    # Aplicaciones estándar de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Aplicaciones de terceros
    'rest_framework',  # Incluida para compatibilidad con tus APIs, si las tienes
    
    # ¡NUESTRAS APLICACIONES!
    # ¡CORRECCIÓN CLAVE! Apuntamos a la clase de configuración de nuestra app 'corelab'
    # y usamos el nombre correcto con mayúsculas: CoreLabConfig.
    'corelab.apps.CoreLabConfig',
]


# ==============================================================================
#  4. MIDDLEWARE
# ==============================================================================
# El middleware son "plugins" que procesan las peticiones y respuestas de Django.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==============================================================================
#  5. CONFIGURACIÓN DE URLS Y PLANTILLAS
# ==============================================================================

# ¡CORRECCIÓN! Le dice a Django dónde encontrar el archivo de URLs principal.
ROOT_URLCONF = 'project_config.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # ¡CORRECCIÓN! Le decimos a Django que busque plantillas globales en la
        # carpeta 'src/templates/'. Aquí vive nuestro 'base.html'.
        "DIRS": [BASE_DIR / 'src' / 'templates'],
        # Django también buscará en las carpetas 'templates' de cada app.
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ¡CORRECCIÓN! Apunta al punto de entrada para servidores WSGI.
WSGI_APPLICATION = 'project_config.wsgi.application'


# ==============================================================================
#  6. BASE DE DATOS
# ==============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ==============================================================================
#  7. VALIDACIÓN DE CONTRASEÑAS Y OTROS
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-es"  # Español como idioma principal
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
#  8. GESTIÓN DE ARCHIVOS ESTÁTICOS Y MEDIA
# ==============================================================================

# La URL que se usará en las plantillas para referirse a los archivos estáticos.
STATIC_URL = "/static/"

# Lista de directorios donde el 'FileSystemFinder' de Django buscará archivos.
# Lo dejamos vacío por ahora, ya que el 'AppDirectoriesFinder' encontrará
# los archivos de 'corelab' por nosotros. Podemos añadir 'src/static/'
# en el futuro si queremos una carpeta global.
STATICFILES_DIRS = [
    # BASE_DIR / 'src' / 'static', <--- Opcional, lo mantenemos simple por ahora
]

# Carpeta donde `collectstatic` reunirá TODOS los archivos para producción.
# Esto no afecta al servidor de desarrollo.
STATIC_ROOT = BASE_DIR / "staticfiles_collected"

# (El resto de la configuración de MEDIA no cambia)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'