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

from django.db import models
from django.utils import timezone

class Material(models.Model):
    """Representa un material único y sus propiedades intrínsecas en la base de datos.

    Este modelo es la entidad central del proyecto. Almacena la información
    identificativa clave de cada material que puede ser seleccionado y utilizado
    en las simulaciones de ensayos mecánicos.
    
    Cada instancia de este modelo corresponde a una entrada única en el catálogo de
    materiales del simulador.
    """

    class Categoria(models.TextChoices):
        """
        Define las categorías de materiales permitidas como una enumeración fija.
        
        El uso de `models.TextChoices` es una buena práctica de Django que
        garantiza la integridad de los datos, ya que el campo 'categoria'
        solo puede aceptar uno de estos valores.

        Cada miembro de la enumeración es una tupla:
        (valor_almacenado_en_db, etiqueta_legible_para_humanos)
        """
        METALES = 'metales', 'Metales'
        POLIMERICOS = 'polimericos', 'Poliméricos'
        CERAMICOS = 'ceramicos', 'Cerámicos'
        COMPUESTOS = 'compuestos', 'Compuestos'

    nombre = models.CharField(
        max_length=100, 
        unique=True,
        help_text=(
            "El identificador único del material, usado internamente para "
            "enlazar con los archivos de datos CSV. Por convención, debe "
            "usar guiones bajos en lugar de espacios (ej. 'AISI_1020_Steel')."
        )
    )
    
    categoria = models.CharField(
        max_length=20,
        choices=Categoria.choices,
        default=Categoria.METALES,
        help_text=(
            "Clasificación o familia a la que pertenece el material. Este campo "
            "determina qué modelo de simulación se utilizará y cómo se "
            "agrupará el material en la interfaz de usuario."
        )
    )

    @property
    def nombre_display(self):
        """
        Propiedad calculada que devuelve el nombre del material en un formato
        limpio y legible para ser mostrado en la interfaz de usuario (UI).
        
        Este método no se almacena en la base de datos, sino que se calcula
        en tiempo real cada vez que se accede a él.
        
        Example:
            Si `self.nombre` es "AISI_1020_Steel", `self.nombre_display`
            devolverá "AISI 1020 Steel".

        Returns:
            str: El nombre del material con los guiones bajos reemplazados por espacios.
        """
        return self.nombre.replace('_', ' ')

    def __str__(self):
        """
        Devuelve la representación en cadena de texto del objeto.

        Este método es utilizado por Django en muchas partes, especialmente
        en el panel de administración, para mostrar una representación
        legible de cada instancia del modelo.
        
        Returns:
            str: El nombre legible del material (utiliza `nombre_display`).
        """
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