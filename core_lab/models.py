# ==========================================================
#  core_lab/models.py - VERSIÓN FINAL Y CORRECTA
# ==========================================================
from django.db import models
from django.utils import timezone

class Material(models.Model):
    # Definimos las categorías como una opción fija para el menú desplegable
    class Categoria(models.TextChoices):
        METALES = 'metales', 'Metales'
        POLIMERICOS = 'polimericos', 'Poliméricos'
        CERAMICOS = 'ceramicos', 'Cerámicos'
        COMPUESTOS = 'compuestos', 'Compuestos'

    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(
        max_length=20,
        choices=Categoria.choices,
        default=Categoria.METALES # Un valor por defecto
    )

    @property
    def nombre_display(self):
        """Devuelve el nombre con guiones bajos reemplazados por espacios."""
        return self.nombre.replace('_', ' ')

    def __str__(self):
        return self.nombre

class Ensayo(models.Model):
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.tipo

class Simulacion(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    ensayo = models.ForeignKey(Ensayo, on_delete=models.CASCADE)
    resultados = models.JSONField(default=dict)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Simulación {self.id} - {self.material.nombre}"