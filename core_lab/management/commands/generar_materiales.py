# ====================================================================
#  Archivo: core_lab/management/commands/generar_materiales.py
#  Propósito: Comando de Django para procesar PDFs y actualizar
#             la base de datos con nuevos materiales.
# ====================================================================

import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings

# --- ¡Aquí importamos nuestras herramientas! ---
from core_lab.utils import (
    get_properties_from_pdf,
    curva_tension_mejorada,
    curva_compresion_corregida,
    curva_torsion_corregida
)
from core_lab.models import Material


class Command(BaseCommand):
    help = 'Procesa archivos PDF para extraer propiedades de materiales y generar los archivos CSV para la simulación.'

    def handle(self, *args, **options):
        self.stdout.write("======================================================")
        self.stdout.write("🚀 INICIANDO PROCESO DE GENERACIÓN DE MATERIALES 🚀")
        self.stdout.write("======================================================")

        # --- Definimos las carpetas ---
        # 1. De dónde leer los PDFs
        pdf_input_folder = os.path.join(settings.BASE_DIR, 'media', 'uploads', 'pdfs')
        # 2. Dónde guardar los CSVs (donde el simulador los lee)
        csv_output_folder = os.path.join(settings.BASE_DIR, 'materials', 'data')
        
        # Crear carpetas si no existen, para evitar errores
        os.makedirs(pdf_input_folder, exist_ok=True)
        os.makedirs(csv_output_folder, exist_ok=True)
        
        pdf_files = [f for f in os.listdir(pdf_input_folder) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            self.stdout.write(self.style.WARNING(f"📂 No se encontraron archivos PDF en la carpeta: {pdf_input_folder}"))
            return

        self.stdout.write(f"🔍 Encontrados {len(pdf_files)} archivo(s) PDF para procesar.")
        
        processed_count = 0
        for pdf_file in pdf_files:
            self.stdout.write("-" * 50)
            file_path = os.path.join(pdf_input_folder, pdf_file)
            
            self.stdout.write(f"📄 Procesando: {pdf_file}")
            nombre_material_raw, props = get_properties_from_pdf(file_path)
            
            if nombre_material_raw and props:
                nombre_material = nombre_material_raw.replace(' ', '_')
                
                # --- AQUÍ ACTUALIZAMOS LA BASE DE DATOS ---
                # `get_or_create` es una forma segura de crear un objeto si no existe,
                # o simplemente obtenerlo si ya fue creado.
                material_obj, created = Material.objects.get_or_create(
                    nombre=nombre_material,
                    defaults={'categoria': Material.Categoria.METALES} # Asume que es un metal por ahora
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"   ✨ Nuevo material '{nombre_material}' añadido a la base de datos."))
                else:
                    self.stdout.write(self.style.NOTICE(f"   🔄 Material '{nombre_material}' ya existe, se actualizarán los datos."))

                # --- Lógica de generación de curvas y guardado de CSVs ---
                E, Su, Sy, G, εf, εu = props.values()

                try:
                    # Tensión
                    t_t, d_t, e_t = curva_tension_mejorada(E, Sy, Su, εu, εf)
                    df_tension = pd.DataFrame({"tiempo": t_t, "deformacion": d_t, "esfuerzo": e_t})
                    df_tension.to_csv(os.path.join(csv_output_folder, f"{nombre_material}_tension.csv"), index=False, header=False)
                    
                    # Compresión
                    t_c, d_c, e_c = curva_compresion_corregida(E, Sy, Su, εu)
                    df_compresion = pd.DataFrame({"tiempo": t_c, "deformacion": d_c, "esfuerzo": e_c})
                    df_compresion.to_csv(os.path.join(csv_output_folder, f"{nombre_material}_compresion.csv"), index=False, header=False)

                    # Torsión (usaremos deformacion/esfuerzo para consistencia)
                    t_tor, d_tor, e_tor = curva_torsion_corregida(G, Sy, Su, εf)
                    df_torsion = pd.DataFrame({"tiempo": t_tor, "deformacion": d_tor, "esfuerzo": e_tor})
                    df_torsion.to_csv(os.path.join(csv_output_folder, f"{nombre_material}_torsion.csv"), index=False, header=False)
                    
                    self.stdout.write(self.style.SUCCESS(f"   ✅ Archivos CSV para '{nombre_material}' generados correctamente."))
                    processed_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"   ❌ Error al generar o guardar los CSVs para '{nombre_material}': {e}"))
                    
    
        self.stdout.write("-" * 50)
        self.stdout.write(self.style.SUCCESS(f"🎉 Proceso completado. Se procesaron {processed_count} de {len(pdf_files)} archivos con éxito."))