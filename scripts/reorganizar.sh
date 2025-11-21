#!/bin/bash

# --- Script para Reorganizar un Proyecto Django a una Estructura Profesional ---

echo "ADVERTENCIA: Este script reorganizará la estructura de tu proyecto."
echo "Asegúrate de tener una copia de seguridad o de haber hecho 'git commit'."
read -p "Presiona Enter para continuar..."

# 1. Crear carpetas estándar
echo "--> Creando carpetas: 'scripts', 'templates', 'static'..."
mkdir -p scripts
mkdir -p templates
mkdir -p static/css static/js static/images

# 2. Mover los scripts .sh a su nueva carpeta
echo "--> Moviendo los scripts (.sh) a la carpeta 'scripts/'..."
# Mueve todos los archivos que terminen en .sh a la nueva carpeta
mv *.sh scripts/

# 3. Renombrar la carpeta principal de configuración
# El nombre 'SimuMaterial' es ambiguo. 'config' es una convención común.
echo "--> Renombrando la carpeta del proyecto 'SimuMaterial/' a 'config/'..."
if [ -d "SimuMaterial" ]; then
    mv SimuMaterial config
else
    echo "    Advertencia: La carpeta 'SimuMaterial' no fue encontrada. Omitiendo."
fi

# 4. Mover la plantilla base a la carpeta de templates global
# Buscamos la plantilla base que casi seguro está en core_lab
echo "--> Moviendo 'base.html' a la carpeta global 'templates/'..."
if [ -f "core_lab/templates/core_lab/base.html" ]; then
    mv core_lab/templates/core_lab/base.html templates/
else
    echo "    Advertencia: No se encontró 'base.html' en core_lab. Deberás moverla manualmente."
fi

echo ""
echo "--------------------------------------------------------"
echo "✅ ¡Reorganización completada!"
echo "--------------------------------------------------------"
echo ""
echo "⚠️ ACCIÓN MANUAL REQUERIDA ⚠️"
echo "Debes actualizar tus archivos de configuración. Abre los siguientes archivos y haz estos cambios:"
echo ""
echo "1. En 'manage.py':"
echo "   Cambia: os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SimuMaterial.settings')"
echo "   A:      os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')"
echo ""
echo "2. En 'config/settings.py':"
echo "   - Cambia: ROOT_URLCONF = 'SimuMaterial.urls'"
echo "     A:      ROOT_URLCONF = 'config.urls'"
echo "   - Cambia: WSGI_APPLICATION = 'SimuMaterial.wsgi.application'"
echo "     A:      WSGI_APPLICATION = 'config.wsgi.application'"
echo "   - Busca la sección TEMPLATES y añade 'BASE_DIR / \"templates\"' a DIRS:"
echo "     'DIRS': [BASE_DIR / 'templates'],"
echo ""
echo "3. En 'config/wsgi.py' y 'config/asgi.py':"
echo "   Cambia: os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SimuMaterial.settings')"
echo "   A:      os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')"
echo ""
echo "Después de hacer estos cambios, ya puedes borrar las carpetas conflictivas."