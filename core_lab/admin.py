# ==========================================================
#  core_lab/admin.py - VERSIÓN FINAL Y CORRECTA
# ==========================================================
from django.contrib import admin
from .models import Material, Ensayo, Simulacion

class MaterialAdmin(admin.ModelAdmin):
    # Le decimos que muestre el 'nombre' y la nueva 'categoria' en la lista
    list_display = ('nombre', 'categoria')
    # Añadimos un filtro útil por categoría
    list_filter = ('categoria',)
    # Añadimos una barra de búsqueda por nombre
    search_fields = ('nombre',)

# Registramos todos los modelos para que aparezcan en el Admin
admin.site.register(Material, MaterialAdmin)
admin.site.register(Ensayo)
admin.site.register(Simulacion)