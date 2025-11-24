# ==========================================================
#  Archivo: src/corelab/management/commands/fix_categories.py
#  Propósito: Script de mantenimiento para corregir los datos
#             de la categoría en la base de datos.
# ==========================================================

from django.core.management.base import BaseCommand
from corelab.models import Material

class Command(BaseCommand):
    """
    Este comando recorre todos los materiales en la base de datos
    y convierte el valor de su campo 'categoria' a minúsculas.
    """
    help = 'Normaliza el campo "categoria" de todos los materiales a minúsculas.'

    def handle(self, *args, **options):
        self.stdout.write("================================================")
        self.stdout.write("⚙️  Iniciando script de corrección de categorías...")
        self.stdout.write("================================================")
        
        # Obtenemos todos los materiales de la base de datos.
        materiales = Material.objects.all()
        
        if not materiales.exists():
            self.stdout.write(self.style.WARNING("No se encontraron materiales en la base de datos."))
            return

        update_count = 0
        for material in materiales:
            # Guardamos el valor original para poder compararlo.
            categoria_original = material.categoria
            categoria_corregida = categoria_original.lower()

            # Solo actualizamos si es necesario, para ser más eficientes.
            if categoria_original != categoria_corregida:
                material.categoria = categoria_corregida
                material.save()
                self.stdout.write(f"  -> Corregido '{material.nombre}': '{categoria_original}' -> '{categoria_corregida}'")
                update_count += 1
        
        self.stdout.write("-" * 48)
        if update_count == 0:
            self.stdout.write(self.style.SUCCESS("✅ ¡Todo correcto! No se necesitaron actualizaciones."))
        else:
            self.stdout.write(self.style.SUCCESS(f"🎉 ¡Éxito! Se actualizaron {update_count} materiales."))