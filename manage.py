#!/usr/bin/env python
# ==========================================================
#  manage.py - Punto de Entrada de Django
# ==========================================================
#  Este archivo es la utilidad principal para interactuar
#  con un proyecto Django desde la línea de comandos.
#
#  CORRECCIONES PARA LA MODULARIZACIÓN:
#  - Se añade el directorio 'src/' al path de Python para
#    que Django pueda encontrar las aplicaciones y la configuración.
#  - Se actualiza 'DJANGO_SETTINGS_MODULE' para apuntar a la
#    nueva ubicación del archivo de configuración.
# ==========================================================

"""Django's command-line utility for administrative tasks."""
import os
import sys

# --- ¡INICIO DE LA CORRECCIÓN PARA MODULARIZACIÓN! ---
#  El siguiente bloque es esencial para que la estructura 'src/' funcione.
#  Le dice a Python: "Oye, antes de buscar módulos en cualquier otro lado,
#  busca dentro de la carpeta 'src/' que está en el mismo directorio que este archivo."
try:
    # Añadimos el directorio 'src' al path de búsqueda de Python
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
except Exception as e:
    # Capturamos un posible error en caso de que algo salga mal
    print(f"Error al modificar el sys.path: {e}")
# --- FIN DE LA CORRECCIÓN ---


def main():
    """Ejecuta las tareas administrativas."""
    
    # --- ¡SEGUNDA CORRECCIÓN PARA MODULARIZACIÓN! ---
    # Actualizamos la variable de entorno para que apunte a la nueva
    # ubicación del archivo de configuración del proyecto: 'src/project_config/settings.py'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_config.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()