# = "========================================================
#  Archivo: src/corelab/tests/test_utils.py (CORREGIDO)
# =========================================================
import pytest
# --- ¡CAMBIO CRÍTICO! ---
# Apuntamos a la nueva ubicación del módulo de simulaciones
from corelab.simulations import identify_material_type

def test_identify_material_type_metal():
    """Verifica que la función identifica correctamente un texto como 'metal'."""
    sample_text = "Data sheet for AISI 1020 Steel, a plain carbon steel."
    result = identify_material_type(sample_text)
    assert result == "metal"

def test_identify_material_type_polimero():
    """Verifica que la función identifica correctamente un texto como 'polimero'."""
    sample_text = "This describes Polyethylene (HDPE), a common polymer."
    result = identify_material_type(sample_text)
    assert result == "polimero"

def test_identify_material_type_ceramico():
    """Verifica que la función identifica correctamente un texto como 'ceramico'."""
    sample_text = "Properties of Alumina, an oxide ceramic material."
    result = identify_material_type(sample_text)
    assert result == "ceramico"