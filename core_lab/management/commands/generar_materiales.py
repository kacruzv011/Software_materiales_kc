# ==============================================================================
#  Archivo: core_lab/management/commands/generar_materiales.py (v2.0)
#  Propósito: Comando de Django que utiliza la lógica avanzada de utils.py
#             para procesar PDFs, detectar tipos de material y actualizar la BD.
# ==============================================================================
import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings

# --- ¡Importamos TODAS nuestras nuevas herramientas! ---
from core_lab.utils import (
    fitz, get_properties_from_pdf,
    simular_metal, simular_polimero, simular_ceramico
)
from core_lab.models import Material

# Diccionario que mapea el tipo de material a su función de simulación
SIMULATION_FUNCTIONS = {
    'metal': simular_metal,
    'polimero': simular_polimero,
    'ceramico': simular_ceramico,
}

# Diccionario que mapea el tipo de material a sus propiedades requeridas
REQUIRED_PROPERTIES = {
    'metal': ['E', 'Sy', 'Su', 'G', 'εf'],
    'polimero': ['E', 'Sy', 'Su', 'εf', 'G'],
    'ceramico': ['E', 'Su_tension', 'Su_compresion', 'G'],
}


class Command(BaseCommand):
    help = 'Procesa archivos PDF para generar datos de simulación y actualizar la base de datos.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("="*60))
        self.stdout.write(self.style.SUCCESS("🚀 INICIANDO PROCESO DE GENERACIÓN DE MATERIALES (v2.0) 🚀"))
        self.stdout.write(self.style.SUCCESS("="*60))

        if not fitz:
            self.stderr.write(self.style.ERROR("❌ ERROR CRÍTICO: 'PyMuPDF' no está instalado. El comando no puede continuar."))
            return

        pdf_input_folder = os.path.join(settings.BASE_DIR, 'media', 'uploads', 'pdfs')
        csv_output_folder = os.path.join(settings.BASE_DIR, 'materials', 'data')
        os.makedirs(pdf_input_folder, exist_ok=True); os.makedirs(csv_output_folder, exist_ok=True)
        
        pdf_files = [f for f in os.listdir(pdf_input_folder) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            self.stdout.write(self.style.WARNING(f"📂 No se encontraron PDFs en: {pdf_input_folder}"))
            return

        self.stdout.write(f"🔍 Encontrados {len(pdf_files)} PDF(s) para procesar.")
        
        processed_count = 0
        failed_files = []

        for pdf_file in pdf_files:
            self.stdout.write("-" * 60)
            file_path = os.path.join(pdf_input_folder, pdf_file)
            self.stdout.write(f"📄 Procesando: {pdf_file}")
            
            name, props, mtype = get_properties_from_pdf(file_path)

            if not all([name, props, mtype]):
                self.stderr.write(self.style.ERROR("  -> ❌ No se pudieron extraer datos básicos del PDF."))
                failed_files.append(pdf_file)
                continue

            self.stdout.write(f"  -> Tipo detectado: {mtype.upper()}")

            # Estimar 'G' si no se encuentra
            if 'G' not in props and 'E' in props:
                nu = 0.35 if mtype == "polimero" else 0.22 if mtype == "ceramico" else 0.3
                props['G'] = props['E'] / (2 * (1 + nu))
                self.stdout.write(self.style.NOTICE(f"  -> AVISO: 'G' no encontrado. Se estimó usando ν={nu}."))
            
            # Verificar si tenemos todas las propiedades para el tipo de material
            required_keys = REQUIRED_PROPERTIES.get(mtype, [])
            if not all(key in props for key in required_keys):
                missing = [key for key in required_keys if key not in props]
                self.stderr.write(self.style.ERROR(f"  -> ❌ Datos insuficientes. Faltan: {missing}."))
                failed_files.append(pdf_file)
                continue
            
            self.stdout.write(f"  -> Propiedades encontradas: {', '.join(props.keys())}")
            
            # --- Actualización de la Base de Datos ---
            material_obj, created = Material.objects.get_or_create(
                nombre=name,
                defaults={'categoria': mtype}
            )
            # Si el material ya existía, actualizamos su categoría
            if not created and material_obj.categoria != mtype:
                material_obj.categoria = mtype
                material_obj.save()
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"  -> ✨ Nuevo material '{name}' añadido a la base de datos."))
            else:
                self.stdout.write(self.style.NOTICE(f"  -> 🔄 Material '{name}' ya existe. Se actualizarán sus datos."))

            # --- Generación de Curvas y Guardado de CSVs ---
            sim_func = SIMULATION_FUNCTIONS.get(mtype)
            try:
                curvas = sim_func(**props)
                for ensayo_tipo, datos in curvas.items():
                    # El return de simular_ceramico puede tener 3 valores, lo manejamos
                    if len(datos) == 3:
                        tiempo, deformacion, esfuerzo = datos
                    else:
                        deformacion, esfuerzo = datos
                        tiempo = np.linspace(0, len(deformacion) * 0.1, len(deformacion))
                        
                    df = pd.DataFrame({"tiempo": tiempo, "deformacion": deformacion, "esfuerzo": esfuerzo})
                    df.to_csv(os.path.join(csv_output_folder, f"{name}_{ensayo_tipo}.csv"), index=False, header=False)
                
                self.stdout.write(self.style.SUCCESS(f"  -> ✅ Archivos CSV para '{name}' generados."))
                processed_count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"  -> ❌ Error durante la simulación o guardado de CSV: {e}"))
                failed_files.append(pdf_file)
                
    
        self.stdout.write("="*60)
        self.stdout.write(self.style.SUCCESS(f"🎉 Proceso completado. {processed_count} de {len(pdf_files)} archivos procesados con éxito."))
        
        if failed_files:
            self.stdout.write(self.style.WARNING("\n--- ⚠️ RESUMEN DE ARCHIVOS QUE FALLARON ---"))
            for filename in set(failed_files):
                self.stdout.write(f"  - {filename}")