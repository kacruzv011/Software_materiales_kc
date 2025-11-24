# ==============================================================================
#  docs/source/conf.py - Archivo de Configuración de Sphinx
# ==============================================================================
#  Este archivo controla cómo Sphinx construye la documentación de tu proyecto.
#  Aquí se configuran las extensiones, el tema visual, y lo más importante,
#  se le enseña a Sphinx a encontrar y entender el código fuente de tu
#  proyecto Django.
# ==============================================================================

import os
import sys
import django

# --- PASO 1: AÑADIR LA RUTA AL CÓDIGO FUENTE (MODULARIZADO) ---
# Le decimos a Sphinx que busque código Python en nuestro directorio 'src/'.
# 'os.path.abspath('../../src')' sube dos niveles desde este archivo
# (docs/source -> raíz) y luego entra a 'src/'.
sys.path.insert(0, os.path.abspath('../../src'))


# --- PASO 2: CONFIGURAR Y CARGAR EL ENTORNO DE DJANGO ---
# Es esencial para que Sphinx pueda importar tus modelos y vistas sin errores.
# Sphinx ejecutará 'django.setup()' y tendrá acceso a todo tu proyecto.
os.environ['DJANGO_SETTINGS_MODULE'] = 'project_config.settings'
django.setup()


# ==============================================================================
#  Información del Proyecto (Valores de sphinx-quickstart)
# ==============================================================================
project = 'CoreLab'
copyright = '2025, Kevin Cruz'
author = 'Kevin Cruz'
release = '4.0.0'


# ==============================================================================
#  Configuración General de Sphinx
# ==============================================================================

# --- PASO 3: AÑADIR LAS EXTENSIONES NECESARIAS ---
# 'extensions' es la lista de "plugins" que le dan superpoderes a Sphinx.
extensions = [
    # Esencial: Habilita la capacidad de importar módulos y extraer
    #           documentación automáticamente de los docstrings.
    'sphinx.ext.autodoc',

    # Útil: Añade enlaces '[source]' al lado de la documentación, permitiendo
    #       ver el código fuente directamente.
    'sphinx.ext.viewcode',
    
    # ¡La Magia!: Permite a Sphinx entender docstrings escritos en el
    #               formato legible de Google, que es más intuitivo que el
    #               formato por defecto (reST).
    'sphinx.ext.napoleon',
]

# Directorios que contienen plantillas personalizadas (no lo necesitamos