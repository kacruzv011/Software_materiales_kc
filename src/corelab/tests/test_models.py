# ==========================================================
#  Archivo: src/corelab/tests/test_models.py (CORREGIDO)
# ==========================================================
import pytest
# --- ¡CAMBIO CRÍTICO! ---
# Apuntamos a la nueva ubicación del módulo de modelos dentro
# del paquete 'corelab' (sin guion bajo).
from corelab.models import Material

@pytest.mark.django_db
def test_material_nombre_display():
    """
    Verifica que la propiedad `nombre_display` del modelo Material
    reemplaza correctamente los guiones bajos por espacios.
    """
    material = Material.objects.create(
        nombre="Acero_De_Prueba_Super_Largo",
        categoria=Material.Categoria.METALES
    )
    assert material.nombre_display == "Acero De Prueba Super Largo"

@pytest.mark.django_db
def test_material_creation_count():
    """
    Verifica que después de crear un material, el conteo en la BD es correcto.
    """
    assert Material.objects.count() == 0
    Material.objects.create(nombre="Otro_Acero", categoria=Material.Categoria.METALES)
    assert Material.objects.count() == 1