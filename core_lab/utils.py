# ====================================================================
#  utils.py - VERSIÓN FINAL Y DEFINITIVA (ESTANDARIZADA)
# ====================================================================

import numpy as np
import pandas as pd
import os
import re

try:
    import fitz  # PyMuPDF
except ImportError:
    print("❌ ERROR CRÍTICO: 'PyMuPDF' no está instalado. Ejecute 'pip install PyMuPDF'.")
    fitz = None

# --- Módulos de Simulación ---

def simular_metal(E, Sy, Su, εf, G, **kwargs):
    t_t, ε_t, σ_t = curva_tension_metal(E, Sy, Su, εf * 0.9, εf)
    t_c, ε_c, σ_c = curva_compresion_metal(E, Sy, Su, εf * 0.9)
    t_tor, γ_tor, τ_tor = curva_torsion_ductil(G, Sy, Su, εf)
    return {"tension": (t_t, ε_t, σ_t), "compresion": (t_c, ε_c, σ_c), "torsion": (t_tor, γ_tor, τ_tor)}

def simular_polimero(E, Sy, Su, εf, G, **kwargs):
    t_t, ε_t, σ_t = curva_tension_polimero(E, Sy, Su, εf)
    t_c, ε_c, σ_c = curva_compresion_polimero(E, Sy)
    t_tor, γ_tor, τ_tor = curva_torsion_ductil(G, Sy, Su, εf)
    return {"tension": (t_t, ε_t, σ_t), "compresion": (t_c, ε_c, σ_c), "torsion": (t_tor, γ_tor, τ_tor)}

def simular_ceramico(E, Su_tension, Su_compresion, G, **kwargs):
    t_t, ε_t, σ_t = curva_lineal(E, Su_tension)
    t_c, ε_c, σ_c = curva_lineal(E, -Su_compresion) # Esfuerzo negativo para compresión
    t_tor, γ_tor, τ_tor = curva_torsion_fragil(G, Su_tension)
    return {"tension": (t_t, ε_t, σ_t), "compresion": (t_c, ε_c, σ_c), "torsion": (t_tor, γ_tor, τ_tor)}
    
def curva_lineal(E, Su, p=100):
    """Genera una curva elástica simple hasta la fractura."""
    deformacion = np.linspace(0, Su / E, p)
    esfuerzo = E * deformacion
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

# --- Funciones de Generación de Curvas (Todas devuelven: tiempo, deformacion, esfuerzo) ---

def curva_tension_metal(E, Sy, Su, εu, εf, p=300):
    εy=Sy/E; σf=Su*0.9; p1=int(p*0.1); ε1=np.linspace(0,εy,p1); σ1=E*ε1
    p2=int(p*0.5); ε2=np.linspace(εy,εu,p2); σ2=Sy+(Su-Sy)*(((ε2-εy)/(εu-εy))**0.5) if (εu-εy)>0 else Sy
    p3=p-p1-p2; ε3=np.linspace(εu,εf,p3); σ3=Su-(Su-σf)*(((ε3-εu)/(εf-εu))**2) if (εf-εu)>0 else [Su]
    deformacion = np.concatenate((ε1,ε2,ε3)); esfuerzo = np.concatenate((σ1,σ2,σ3))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_compresion_metal(E, Sy, Su, εu, p=200):
    εy=Sy/E; p1=int(p*0.2); ε1=np.linspace(0,-εy,p1); σ1=E*ε1
    p2=p-p1; ε2=np.linspace(-εy,-εu*1.1,p2); σ_pos=Sy+(Su-Sy)*(((abs(ε2)-εy)/(εu-εy))**0.5) if (εu-εy)>0 else Sy; σ2=-σ_pos
    deformacion = np.concatenate((ε1,ε2)); esfuerzo = np.concatenate((σ1,σ2))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_torsion_ductil(G, Sy, Su, εf, p=300):
    τy=Sy/np.sqrt(3); τu=Su/np.sqrt(3); γy=τy/G; γf=εf*1.7; p1=int(p*0.1)
    γ1=np.linspace(0,γy,p1,endpoint=False); τ1=G*γ1; p2=p-p1; γ2=np.linspace(γy,γf,p2)
    τ2=τy+(τu-τy)*(((γ2-γy)/(γf-γy))**0.2) if (γf-γy)>0 else τy
    deformacion = np.concatenate((γ1,γ2)); esfuerzo = np.concatenate((τ1,τ2))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_torsion_fragil(G, Su_tension, p=100):
    τ_max=Su_tension*0.9; γ_fractura=τ_max/G; deformacion=np.linspace(0,γ_fractura,p); esfuerzo=G*deformacion
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_tension_polimero(E, Sy, Su, εf, p=400):
    εy=Sy/E; Su_draw=Sy*0.8; ε_cold_draw_end=εf*0.8; p1=int(p*0.05); ε1=np.linspace(0,εy,p1); σ1=E*ε1
    p2=int(p*0.1); ε2=np.linspace(εy,εy*2,p2); σ2=Sy-(Sy-Su_draw)*((ε2-εy)/εy)**0.5
    p3=int(p*0.75); ε3=np.linspace(εy*2,ε_cold_draw_end,p3); σ3=np.full_like(ε3,Su_draw)
    p4=p-p1-p2-p3; ε4=np.linspace(ε_cold_draw_end,εf,p4); σ4=Su_draw+(Su-Su_draw)*((ε4-ε_cold_draw_end)/(εf-ε_cold_draw_end))
    deformacion = np.concatenate((ε1,ε2,ε3,ε4)); esfuerzo = np.concatenate((σ1,σ2,σ3,σ4))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_compresion_polimero(E, Sy, p=200):
    εy=Sy/E; p1=int(p*0.2); ε1=np.linspace(0,-εy,p1); σ1=E*ε1
    p2=p-p1; ε2=np.linspace(-εy,-εy*10,p2); σ2=-Sy-(E*0.05)*(abs(ε2)-εy)**0.8
    deformacion = np.concatenate((ε1,ε2)); esfuerzo = np.concatenate((σ1,σ2))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

# --- Funciones de Extracción de PDF y Detección de Tipo ---
def identify_material_type(text):
    text=text.lower()
    if any(k in text for k in['steel','iron','aluminum','alloy']): return "metal"
    if any(k in text for k in['polymer','polyethylene','nylon','abs','pvc']): return "polimero"
    if any(k in text for k in['ceramic','alumina','zirconia','glass','concrete','cement']): return "ceramico"
    return "metal" # Valor por defecto

def get_properties_from_pdf(file_path):
    if not fitz: return None, None, None
    try:
        doc = fitz.open(file_path)
        text = "".join(page.get_text() for page in doc)
        doc.close()
        
        # Sanitizar nombre del archivo para usarlo como ID
        name_raw = os.path.basename(file_path).replace('.pdf', '').replace(',', '')
        name = name_raw.replace(' ', '_')
        mtype = identify_material_type(text)
        
        props = {}
        synonym_library = {"E":["Modulus of Elasticity","Tensile Modulus","Young's Modulus","Flexural Modulus"],"Su":["Tensile Strength, Ultimate","Ultimate Tensile Strength"],"Sy":["Tensile Strength, Yield","Yield Strength","Flexural Yield Strength"],"G":["Shear Modulus"],"εf":["Elongation at Break"],"Su_tension":["Tensile Strength, Ultimate","Flexural Strength","Tensile Strength"],"Su_compresion":["Compressive Strength","Ultimate Compressive Strength","Crushing Strength"]}
        
        required_keys = []
        if mtype == "metal": required_keys=['E','Sy','Su','G','εf']
        elif mtype == "polimero": required_keys=['E','Sy','Su','εf']
        elif mtype == "ceramico": required_keys=['E','Su_tension','Su_compresion']
        search_keys = list(set(required_keys + ['G']))

        for key in search_keys:
            name_patterns_regex = "|".join([s.replace(" ", r"\s*") for s in synonym_library.get(key, [])])
            if not name_patterns_regex: continue
            avg_pattern = re.compile(rf"(?:{name_patterns_regex})[\s\S]*?Average value:\s*([\d\.]+)\s*(GPa|MPa|%)", re.IGNORECASE)
            match = avg_pattern.search(text)
            if not match:
                fallback_pattern = re.compile(rf"(?:{name_patterns_regex})[\s\S]*?([\d\.]+)\s*(GPa|MPa|%)", re.IGNORECASE)
                match = fallback_pattern.search(text)
            
            if match:
                val, unit = float(match.group(1)), match.group(2)
                if "GPa" in unit: val *= 1e9
                elif "MPa" in unit: val *= 1e6
                elif "%" in unit: val /= 100
                props[key] = val
                
        return name, props, mtype
    except Exception as e:
        print(f"❌ Error al procesar '{os.path.basename(file_path)}': {e}")
        return None, None, None