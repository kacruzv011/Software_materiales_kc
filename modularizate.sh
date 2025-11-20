#!/bin/bash

# ==========================================================
#  🚀 Script para Modularizar un Proyecto Django 🚀
# ==========================================================
#  Este script reorganiza una estructura de Django estándar
#  a una estructura modular con un directorio 'src/'.
# ==========================================================

echo "⚠️  ADVERTENCIA: Este script reorganizará drásticamente la estructura de tu proyecto."
echo "    Se recomienda encarecidamente que hagas un 'git commit' de todos tus cambios"
echo "    antes de continuar, para tener un punto de restauración seguro."
echo ""
read -p "    Presiona Enter para comenzar la modularización..."

# --- PASO 1: Crear la nueva estructura de directorios ---

echo ""
echo "--> Creando el directorio 'src/'..."
mkdir -p src

# --- PASO 2: Mover y renombrar las aplicaciones principales ---

echo "--> Moviendo 'core_lab/' a 'src/corelab/'..."
if [ -d "core_lab" ]; then
    mv core_lab src/corelab
else
    echo "    AVISO: No se encontró la carpeta 'core_lab'. Se omite."
fi

echo "--> Moviendo 'config/' a 'src/project_config/'..."
if [ -d "config" ]; then
    mv config src/project_config
else
    echo "    AVISO: No se encontró la carpeta 'config'. Se omite."
fi

echo "--> Moviendo 'templates/' (si existe en la raíz) a 'src/templates/'..."
if [ -d "templates" ]; then
    mv templates src/templates
else
    echo "    AVISO: No hay una carpeta 'templates' en la raíz. Se omite."
fi

echo "--> Moviendo 'static/' (si existe en la raíz) a 'src/static/'..."
if [ -d "static" ]; then
    mv static src/static
else
    echo "    AVISO: No hay una carpeta 'static' en la raíz. Se omite."
fi

echo "--> Renombrando 'core_lab/utils.py' a 'src/corelab/simulations.py'..."
if [ -f "src/corelab/utils.py" ]; then
    mv src/corelab/utils.py src/corelab/simulations.py
else
    echo "    AVISO: No se encontró 'utils.py'. Se omite el renombrado."
fi


# --- PASO 3: Imprimir instrucciones para los cambios manuales ---

echo ""
echo "--------------------------------------------------------"
echo "✅ Reorganización de archivos completada con éxito."
echo "--------------------------------------------------------"
echo ""
echo "🔴 ACCIÓN MANUAL REQUERIDA: Ahora debes actualizar tu código."
echo "   Sigue estas instrucciones cuidadosamente:"
echo ""
echo "1. En 'manage.py':"
echo "   - Añade estas 3 LÍNEAS al PRINCIPIO del archivo (después de los imports):"
echo '     import sys'
echo "     sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))"
echo "   - Busca la línea 'os.environ.setdefault' y cámbiala a:"
echo "     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_config.settings')"
echo ""
echo "2. En 'src/project_config/settings.py':"
echo "   - Busca 'ROOT_URLCONF' y cámbialo a: ROOT_URLCONF = 'project_config.urls'"
echo "   - Busca 'WSGI_APPLICATION' y cámbialo a: WSGI_APPLICATION = 'project_config.wsgi.application'"
echo "   - En 'INSTALLED_APPS', cambia 'core_lab' por 'corelab' (sin el guion bajo)."
echo "   - En 'TEMPLATES', actualiza 'DIRS' a: 'DIRS': [BASE_DIR / 'src/templates']"
echo ""
echo "3. En 'src/project_config/wsgi.py' y 'src/project_config/asgi.py':"
echo "   - Añade estas 3 LÍNEAS al PRINCIPIO (igual que en manage.py)."
echo "   - Cambia la línea 'os.environ.setdefault' a:"
echo "     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_config.settings')"
echo ""
echo "4. En 'src/corelab/management/commands/generar_materiales.py':"
echo "   - Cambia la línea 'from core_lab.utils import ...' por:"
echo "     from corelab.simulations import ..."
echo "   - Cambia la línea 'from core_lab.models import Material' por:"
echo "     from corelab.models import Material"
echo ""
echo "¡Una vez que hayas hecho estos cambios, tu proyecto estará completamente modularizado!"
echo "No olvides crear el archivo 'pyproject.toml' si planeas distribuirlo."