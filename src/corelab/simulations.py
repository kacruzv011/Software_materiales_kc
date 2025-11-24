# ====================================================================
#  src/corelab/simulations.py - Módulo de Lógica de Simulación
# ====================================================================
#  Contiene todas las funciones para extraer propiedades de PDFs,
#  detectar tipos de material y generar curvas sintéticas de
#  esfuerzo-deformación para diferentes ensayos mecánicos.
# ====================================================================

import numpy as np
import pandas as pd
import os
import re

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

# --- Módulos de Simulación Principales ---

def simular_metal(E, Sy, Su, εf, G, **kwargs):
    """Orquesta la simulación completa para un material metálico dúctil.

    Llama a las funciones específicas para generar las curvas de tensión,
    compresión y torsión basadas en modelos de comportamiento dúctil.

    Args:
        E (float): Módulo de Young (Pa).
        Sy (float): Límite de fluencia (Pa).
        Su (float): Resistencia máxima a la tracción (Pa).
        εf (float): Deformación en el punto de fractura.
        G (float): Módulo de cizalladura (Pa).
        **kwargs: Argumentos adicionales para compatibilidad con el Unpacker.

    Returns:
        dict: Un diccionario con las curvas de 'tension', 'compresion' y 'torsion'.
              Cada valor es una tupla de (tiempo, deformación, esfuerzo).
    """
    εu = εf * 0.9
    t_t, ε_t, σ_t = curva_tension_metal(E, Sy, Su, εu, εf)
    t_c, ε_c, σ_c = curva_compresion_metal(E, Sy, Su, εu)
    t_tor, γ_tor, τ_tor = curva_torsion_ductil(G, Sy, Su, εf)
    return {"tension": (t_t, ε_t, σ_t), "compresion": (t_c, ε_c, σ_c), "torsion": (t_tor, γ_tor, τ_tor)}

def simular_polimero(E, Sy, Su, εf, G, **kwargs):
    """Orquesta la simulación completa para un material polimérico.

    Utiliza modelos que simulan el comportamiento característico de los polímeros,
    incluyendo el fenómeno de "cold drawing".

    Args:
        E (float): Módulo de Young (Pa).
        Sy (float): Límite de fluencia (Pa).
        Su (float): Resistencia máxima a la tracción (Pa).
        εf (float): Deformación en el punto de fractura.
        G (float): Módulo de cizalladura (Pa).
        **kwargs: Argumentos adicionales.

    Returns:
        dict: Diccionario con las curvas de simulación generadas.
    """
    t_t, ε_t, σ_t = curva_tension_polimero(E, Sy, Su, εf)
    t_c, ε_c, σ_c = curva_compresion_polimero(E, Sy)
    t_tor, γ_tor, τ_tor = curva_torsion_ductil(G, Sy, Su, εf)
    return {"tension": (t_t, ε_t, σ_t), "compresion": (t_c, ε_c, σ_c), "torsion": (t_tor, γ_tor, τ_tor)}

def simular_ceramico(E, Su_tension, Su_compresion, G, **kwargs):
    """Orquesta la simulación para un material cerámico frágil.

    Utiliza modelos de comportamiento elástico lineal hasta la fractura,
    que es característico de los materiales cerámicos.

    Args:
        E (float): Módulo de Young (Pa).
        Su_tension (float): Resistencia a la fractura por tensión (Pa).
        Su_compresion (float): Resistencia a la fractura por compresión (Pa).
        G (float): Módulo de cizalladura (Pa).
        **kwargs: Argumentos adicionales.

    Returns:
        dict: Diccionario con las curvas de simulación generadas.
    """
    t_t, ε_t, σ_t = curva_lineal(E, Su_tension)
    t_c, ε_c, σ_c = curva_lineal(E, -Su_compresion)  # Esfuerzo negativo para compresión
    t_tor, γ_tor, τ_tor = curva_torsion_fragil(G, Su_tension)
    return {"tension": (t_t, ε_t, σ_t), "compresion": (t_c, ε_c, σ_c), "torsion": (t_tor, γ_tor, τ_tor)}

def curva_lineal(E, Su, p=100):
    """Genera una curva elástica simple hasta la fractura para materiales frágiles.

    Args:
        E (float): Módulo de Young (Pa).
        Su (float): Resistencia a la fractura (Pa).
        p (int): Número de puntos a generar.

    Returns:
        tuple: (tiempo, deformacion, esfuerzo)
    """
    deformacion = np.linspace(0, Su / E, p)
    esfuerzo = E * deformacion
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

# --- Funciones de Generación de Curvas ---

def curva_tension_metal(E, Sy, Su, εu, εf, p=300):
    """Genera una curva de tensión sintética para metales dúctiles.

    Modela el comportamiento elástico, la fluencia, el endurecimiento por
    deformación (strain hardening) y la estricción (necking) hasta la fractura.
    
    Returns:
        tuple: (tiempo, deformacion, esfuerzo)
    """
    εy=Sy/E; σf=Su*0.9; p1=int(p*0.1); ε1=np.linspace(0,εy,p1); σ1=E*ε1; p2=int(p*0.5); ε2=np.linspace(εy,εu,p2); σ2=Sy+(Su-Sy)*(((ε2-εy)/(εu-εy))**0.5) if (εu-εy)>0 else Sy; p3=p-p1-p2; ε3=np.linspace(εu,εf,p3); σ3=Su-(Su-σf)*(((ε3-εu)/(εf-εu))**2) if (εf-εu)>0 else [Su]; 
    deformacion = np.concatenate((ε1,ε2,ε3)); esfuerzo = np.concatenate((σ1,σ2,σ3))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_compresion_metal(E, Sy, Su, εu, p=200):
    """Genera una curva de compresión sintética para metales dúctiles."""
    εy=Sy/E; p1=int(p*0.2); ε1=np.linspace(0,-εy,p1); σ1=E*ε1; p2=p-p1; ε2=np.linspace(-εy,-εu*1.1,p2); σ_pos=Sy+(Su-Sy)*(((abs(ε2)-εy)/(εu-εy))**0.5) if (εu-εy)>0 else Sy; σ2=-σ_pos; 
    deformacion = np.concatenate((ε1,ε2)); esfuerzo = np.concatenate((σ1,σ2))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_torsion_ductil(G, Sy, Su, εf, p=300):
    """Genera una curva de torsión sintética para materiales dúctiles."""
    τy=Sy/np.sqrt(3); τu=Su/np.sqrt(3); γy=τy/G; γf=εf*1.7; p1=int(p*0.1); γ1=np.linspace(0,γy,p1,endpoint=False); τ1=G*γ1; p2=p-p1; γ2=np.linspace(γy,γf,p2); τ2=τy+(τu-τy)*(((γ2-γy)/(γf-γy))**0.2) if (γf-γy)>0 else τy; 
    deformacion = np.concatenate((γ1,γ2)); esfuerzo = np.concatenate((τ1,τ2))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_torsion_fragil(G, Su_tension, p=100):
    """Genera una curva de torsión sintética para materiales frágiles."""
    τ_max=Su_tension*0.9; γ_fractura=τ_max/G; deformacion=np.linspace(0,γ_fractura,p); esfuerzo=G*deformacion
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_tension_polimero(E, Sy, Su, εf, p=400):
    """Genera una curva de tensión sintética para polímeros."""
    εy=Sy/E; Su_draw=Sy*0.8; ε_cold_draw_end=εf*0.8; p1=int(p*0.05); ε1=np.linspace(0,εy,p1); σ1=E*ε1; p2=int(p*0.1); ε2=np.linspace(εy,εy*2,p2); σ2=Sy-(Sy-Su_draw)*((ε2-εy)/εy)**0.5; p3=int(p*0.75); ε3=np.linspace(εy*2,ε_cold_draw_end,p3); σ3=np.full_like(ε3,Su_draw); p4=p-p1-p2-p3; ε4=np.linspace(ε_cold_draw_end,εf,p4); σ4=Su_draw+(Su-Su_draw)*((ε4-ε_cold_draw_end)/(εf-ε_cold_draw_end)); 
    deformacion = np.concatenate((ε1,ε2,ε3,ε4)); esfuerzo = np.concatenate((σ1,σ2,σ3,σ4))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

def curva_compresion_polimero(E, Sy, p=200):
    """Genera una curva de compresión sintética para polímeros."""
    εy=Sy/E; p1=int(p*0.2); ε1=np.linspace(0,-εy,p1); σ1=E*ε1; p2=p-p1; ε2=np.linspace(-εy,-εy*10,p2); σ2=-Sy-(E*0.05)*(abs(ε2)-εy)**0.8; 
    deformacion = np.concatenate((ε1,ε2)); esfuerzo = np.concatenate((σ1,σ2))
    tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
    return tiempo, deformacion, esfuerzo

# --- Funciones de Extracción y Detección ---

def identify_material_type(text):
    """Identifica el tipo de material a partir de un texto.

    Busca palabras clave en el texto extraído del PDF para clasificar
    el material en 'metal', 'polimero' o 'ceramico'.

    Args:
        text (str): El texto completo extraído de un PDF.

    Returns:
        str: El tipo de material detectado. Devuelve 'metal' como valor por defecto.
    """
    text=text.lower();
    if any(k in text for k in['steel','iron','aluminum','alloy']): return "metal"
    if any(k in text for k in['polymer','polyethylene','nylon','abs','pvc']): return "polimero"
    if any(k in text for k in['ceramic','alumina','zirconia','glass','concrete','cement']): return "ceramico"
    return "metal"

def get_properties_from_pdf(file_path):
    """Extrae propiedades mecánicas clave de un archivo PDF y detecta el tipo de material.

    Esta función está optimizada para leer PDFs con formatos de ficha técnica
    similares a los de MatWeb.com. Utiliza una biblioteca de sinónimos y
    expresiones regulares para encontrar los valores.

    Args:
        file_path (str): La ruta completa al archivo PDF a procesar.

    Returns:
        tuple: Una tupla `(nombre, propiedades, tipo_material)` en caso de éxito.
        
            - **nombre** (*str*): El nombre del material extraído y sanitizado.
            - **propiedades** (*dict*): Un diccionario con las propiedades mecánicas.
            - **tipo_material** (*str*): El tipo de material detectado.
        
        Si el procesamiento falla, devuelve `(None, None, None)`.
    """
    if not fitz: 
        print("Error: PyMuPDF no está instalado.")
        return None, None, None
    try:
        doc = fitz.open(file_path)
        text = "".join(page.get_text() for page in doc)
        doc.close()
        
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