# ==============================================================================
#  src/corelab/models.py - Definición de los Modelos de la Base de Datos
# ==============================================================================
#  Este archivo define la estructura de la base de datos para la aplicación 'corelab'.
#  Cada clase representa una tabla en la base de datos, y cada atributo de la
#  clase representa una columna en esa tabla. Django utiliza estos modelos para
#  interactuar con los datos de forma abstracta y segura (ORM).
# ==============================================================================

from django.db import models
from django.utils import timezone

class Material(models.Model):
    """Representa un material único en la base de datos.

    Este modelo almacena las propiedades identificativas de cada material que puede ser
    utilizado en las simulaciones.

    Attributes:
        nombre (CharField): El identificador único del material. Por convención, debe
                            usar guiones bajos en lugar de espacios para mantener la
                            consistencia con los nombres de archivo.
        categoria (CharField): La clasificación del material (ej. 'metales', 'polimericos'),
                               definida por las opciones en la clase interna Categoria.
    """
    class Categoria(models.TextChoices):
        """Define las categorías de materiales permitidas en la base de datos."""
        METALES = 'metales', 'Metales'
        POLIMERICOS = 'polimericos', 'Poliméricos'
        CERAMICOS = 'ceramicos', 'Cerámicos'
        COMPUESTOS = 'compuestos', 'Compuestos'

    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(
        max_length=20,
        choices=Categoria.choices,
        default=Categoria.METALES
    )

    @property
    def nombre_display(self):
        """Devuelve el nombre del material en un formato legible para el usuario.

        Returns:
            str: El nombre del material con guiones bajos reemplazados por espacios.
        """
        return self.nombre.replace('_', ' ')

    def __str__(self):
        """Representación en cadena del modelo, utilizada en el admin de Django."""
        return self.nombre_display

class Ensayo(models.Model):
    """Representa un tipo de ensayo mecánico (ej. Tensión, Compresión).

    Este modelo es actualmente un placeholder y podría expandirse en el futuro para
    almacenar parámetros específicos de cada tipo de ensayo.

    Attributes:
        tipo (CharField): El nombre del ensayo.
        descripcion (TextField): Una descripción opcional más detallada.
    """
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        """Representación en cadena del modelo."""
        return self.tipo.capitalize()

class Simulacion(models.Model):
    """Registra la ejecución de un ensayo específico sobre un material.

    Este modelo actúa como un registro histórico, vinculando un Material y un Ensayo
    y almacenando los resultados generados.

    Attributes:
        material (ForeignKey): Una relación con el material que fue ensayado.
        ensayo (ForeignKey): Una relación con el tipo de ensayo que se realizó.
        resultados (JSONField): Un campo para almacenar los datos crudos de la simulación
                                en formato JSON.
        fecha_creacion (DateTimeField): La fecha y hora en que se creó el registro.
    """
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    ensayo = models.ForeignKey(Ensayo, on_delete=models.CASCADE)
    resultados = models.JSONField(default=dict)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Representación en cadena para el admin, ej. 'Simulación 15 - Acero 1020'."""
        return f"Simulación {self.id} - {self.material.nombre}"