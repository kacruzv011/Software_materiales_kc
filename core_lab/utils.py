# ==========================================================
#  Archivo: core_lab/utils.py
#  Propósito: Contiene las funciones reutilizables para
#             procesar PDFs y generar datos sintéticos.
# ==========================================================

import numpy as np
import pandas as pd
import os
import re
import matplotlib.pyplot as plt

# --- Se intenta importar la librería para leer PDF ---
try:
    import fitz  # PyMuPDF
except ImportError:
    # Si la librería no está, creamos un objeto 'None' para poder comprobarlo
    fitz = None

# -----------------------------------------------------------
# ⚙️ Función para extraer propiedades desde PDF
# -----------------------------------------------------------
def get_properties_from_pdf(file_path):
    if not fitz:
        print("❌ ERROR CRÍTICO: La librería 'PyMuPDF' no está instalada.")
        print("   Por favor, ejecute 'pip install PyMuPDF' para continuar.")
        return None, None
        
    try:
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        
        properties = {}
        
        # --- Patrones de búsqueda robustos ---
        prop_patterns = {
            "E": r"Modulus of\s*Elasticity[\s\S]*?(\d+\.?\d*)\s*(GPa)",
            "Su": r"Tensile Strength,\s*Ultimate[\s\S]*?(\d+\.?\d*)\s*(MPa)",
            "Sy": r"Tensile Strength,\s*Yield[\s\S]*?(\d+\.?\d*)\s*(MPa)",
            "G": r"Shear Modulus[\s\S]*?(\d+\.?\d*)\s*(GPa)",
            "εf": r"Elongation at\s*Break[\s\S]*?(\d+\.?\d*)\s*(%)"
        }

        # Extraer nombre del material del PDF
        material_name = os.path.basename(file_path).replace('.pdf', '') # Nombre por defecto
        title_match = re.search(r'^(.*?)\s+as rolled', full_text, re.IGNORECASE)
        if title_match:
            material_name = title_match.group(1).strip().replace(' ','_') + "_as_rolled"

        for key, pattern in prop_patterns.items():
            match = re.search(pattern, full_text)
            if match:
                value_str, unit_str = match.group(1), match.group(2)
                value = float(value_str)
                # Conversión de unidades
                if "GPa" in unit_str: value *= 1e9
                elif "MPa" in unit_str: value *= 1e6
                elif "%" in unit_str: value /= 100
                properties[key] = value
        
        if len(properties) < 5: 
            print(f"⚠️  No se encontraron todas las propiedades en '{os.path.basename(file_path)}'. Se omite.")
            return None, None
            
        properties['εu'] = properties.get('εf', 0) * 0.9
        return material_name, properties

    except Exception as e:
        print(f"❌ Ocurrió un error al procesar el PDF '{os.path.basename(file_path)}': {e}")
        return None, None

# -----------------------------------------------------------
# ⚙️ Funciones de Generación de Curvas
# -----------------------------------------------------------
def curva_tension_mejorada(E, Sy, Su, εu, εf, puntos=300):
    εy=Sy/E; σf=Su*0.9; pts1=int(puntos*0.1); ε1=np.linspace(0,εy,pts1); σ1=E*ε1
    pts2=int(puntos*0.5); ε2=np.linspace(εy,εu,pts2)
    σ2=Sy+(Su-Sy)*(((ε2-εy)/(εu-εy))**0.5) if (εu-εy)>0 else Sy
    pts3=puntos-len(ε1)-len(ε2); ε3=np.linspace(εu,εf,pts3)
    σ3=Su-(Su-σf)*(((ε3-εu)/(εf-εu))**2) if (εf-εu)>0 else [Su]
    # Se añade 'tiempo' a los datos generados para consistencia con el frontend
    deformacion = np.concatenate((ε1,ε2,ε3))
    esfuerzo = np.concatenate((σ1,σ2,σ3))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_compresion_corregida(E, Sy, Su, εu, puntos=200):
    εy=Sy/E; pts1=int(puntos*0.2); ε1=np.linspace(0,-εy,pts1); σ1=E*ε1
    pts2=puntos-pts1; ε2=np.linspace(-εy,-εu*1.1,pts2)
    σ_pos=Sy+(Su-Sy)*(((abs(ε2)-εy)/(εu-εy))**0.5) if (εu-εy)>0 else Sy
    σ2=-σ_pos
    deformacion = np.concatenate((ε1,ε2))
    esfuerzo = np.concatenate((σ1,σ2))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_torsion_corregida(G, Sy, Su, εf, puntos=300):
    τy=Sy/np.sqrt(3); τu=Su/np.sqrt(3); γy=τy/G; γf=εf*1.7
    pts1=int(puntos*0.1); γ1=np.linspace(0,γy,pts1,endpoint=False); τ1=G*γ1
    pts2=puntos-pts1; γ2=np.linspace(γy,γf,pts2)
    τ2=τy+(τu-τy)*(((γ2-γy)/(γf-γy))**0.2) if (γf-γy)>0 else τy
    deformacion = np.concatenate((γ1,γ2))
    esfuerzo = np.concatenate((τ1,τ2))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo