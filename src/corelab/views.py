# ==========================================================
#  core_lab/views.py - VERSIÓN FINALÍSIMA Y COMPLETA
# ==========================================================

import os, io, csv, json, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Material, Ensayo, Simulacion

# ============================================================
#  VISTAS PRINCIPALES (TODAS LAS FUNCIONES RESTAURADAS)
# ============================================================

def simulacion(request):
    materiales = Material.objects.all().order_by('nombre')
    ensayos = Ensayo.objects.all().order_by('tipo')
    return render(request, 'core_lab/simulacion.html', {'materiales': materiales, 'ensayos': ensayos})

# ==========================================================
#  core_lab/views.py - FUNCIÓN MATERIALES ACTUALIZADA
# ==========================================================


def materiales(request):
    """
    Crea una lista estructurada con información técnica detallada para cada categoría
    de material y la pasa a la plantilla para su visualización interactiva.
    """
    # Diccionario enriquecido con información técnica y propiedades físicas clave
    descripciones = {
        'metales': {
            'tagline': "Materiales caracterizados por su enlace metálico, que resulta en una alta conductividad eléctrica y térmica, ductilidad y brillo.",
            'properties': [
                "<strong>Estructura Cristalina y Ductilidad:</strong> Los átomos se ordenan en redes cristalinas (BCC, FCC, HCP) que permiten el deslizamiento de planos atómicos a través del movimiento de dislocaciones. Este mecanismo es la base de su capacidad para deformarse plásticamente (ductilidad) sin fracturarse.",
                "<strong>Conductividad Térmica y Eléctrica:</strong> La 'nube' o 'mar' de electrones deslocalizados del enlace metálico tiene una alta movilidad, permitiendo la transferencia eficiente tanto de carga eléctrica (corriente) como de energía térmica (vibraciones de la red o fonones).",
                "<strong>Rigidez (Módulo de Young):</strong> La fuerte atracción electrostática entre los núcleos iónicos y la nube de electrones confiere a los metales una alta resistencia a la deformación elástica, resultando en un Módulo de Young elevado.",
            ]
        },
        'polimericos': {
            'tagline': "Macromoléculas formadas por la repetición de monómeros. Sus propiedades dependen de la longitud de las cadenas, su entrelazamiento y las fuerzas intermoleculares.",
            'properties': [
                "<strong>Baja Conductividad:</strong> Los electrones están confinados en enlaces covalentes, impidiendo su libre movimiento. Esto los convierte en excelentes aislantes eléctricos y térmicos.",
                "<strong>Viscoelasticidad:</strong> Exhiben un comportamiento mecánico intermedio entre un sólido elástico y un fluido viscoso. Bajo carga, las cadenas poliméricas se desenredan y alinean, un proceso dependiente del tiempo y la temperatura que da lugar a fenómenos como la fluencia (creep) y la relajación de tensiones.",
                "<strong>Estructura Molecular (Termoplásticos vs. Termoestables):</strong> Los termoplásticos consisten en cadenas lineales o ramificadas unidas por débiles fuerzas de Van der Waals, permitiendo su reblandecimiento y moldeo con calor. Los termoestables poseen una red tridimensional de enlaces cruzados (cross-linking) que les confiere mayor rigidez y estabilidad térmica, pero no pueden ser reprocesados.",
            ]
        },
        'ceramicos': {
            'tagline': "Compuestos inorgánicos, no metálicos, con enlaces iónicos y/o covalentes fuertes que les confieren alta dureza y resistencia a la compresión y a altas temperaturas.",
            'properties': [
                "<strong>Fragilidad (Baja Tenacidad a la Fractura):</strong> La rigidez de los enlaces iónicos/covalentes y la compleja estructura cristalina impiden el movimiento de dislocaciones. La concentración de esfuerzos en la punta de una grieta no puede ser disipada por deformación plástica, lo que lleva a una propagación catastrófica de la fractura con mínima absorción de energía.",
                "<strong>Alta Dureza y Resistencia a la Compresión:</strong> La enorme energía requerida para romper los fuertes enlaces primarios hace que los cerámicos sean extremadamente resistentes a la indentación (dureza) y a las fuerzas de compresión.",
                "<strong>Estabilidad Química y Térmica (Refractarios):</strong> Al ser a menudo óxidos, nitruros o carburos, ya se encuentran en un estado de baja energía, lo que les confiere una excelente resistencia a la corrosión química y a la degradación a temperaturas elevadas (comportamiento refractario).",
            ]
        },
        'compuestos': {
            'tagline': "Materiales multifásicos diseñados para combinar las mejores características de sus constituyentes, logrando propiedades que no son alcanzables por ninguno de los componentes por sí solo.",
            'properties': [
                "<strong>Anisotropía:</strong> Sus propiedades mecánicas son altamente direccionales y dependen de la orientación de la fase de refuerzo (e.g., fibras). Son significativamente más resistentes y rígidos en la dirección de las fibras que en la dirección transversal.",
                "<strong>Principio de Acción Combinada:</strong> Se basan en una fase matriz (generalmente polimérica o metálica) que cohesiona y protege a una fase de refuerzo (fibras de carbono, vidrio, etc.) que aporta la rigidez y resistencia. La 'Ley de las Mezclas' es un modelo de primer orden para predecir propiedades como el módulo elástico.",
                "<strong>Alta Relación Resistencia-Peso:</strong> Al combinar fibras ligeras y extremadamente resistentes (como el carbono) con una matriz de baja densidad, se obtienen materiales con una rigidez y resistencia comparables o superiores a las de los metales, pero con una fracción de su peso. Esto es crucial en la industria aeroespacial y automotriz.",
            ]
        }
    }
    
    # El resto de la lógica no necesita cambios
    datos_categorias = []
    for valor, nombre in Material.Categoria.choices:
        datos_categorias.append({
            'valor': valor,
            'nombre': nombre,
            'descripcion': descripciones.get(valor),
            'materiales': Material.objects.filter(categoria=valor).order_by('nombre')
        })

    context = {
        'datos_categorias': datos_categorias
    }
    
    return render(request, 'core_lab/materiales.html', context)
def home(request):
    materiales = Material.objects.all().order_by('nombre')
    ensayos = Ensayo.objects.all().order_by('tipo')
    return render(request, 'core_lab/index.html', {
        'materiales': materiales,
        'ensayos': ensayos
    })

def plot_png(request):
    # ¡ESTA ERA LA FUNCIÓN QUE FALTABA!
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.set_title("Esfuerzo - Deformación (placeholder)")
    ax.set_xlabel("Deformación")
    ax.set_ylabel("Esfuerzo (Pa)")
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.text(0.5, 0.5, "Sin datos aún", ha='center', va='center',
            transform=ax.transAxes, fontsize=14, color='gray')
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    resp = HttpResponse(buf.getvalue(), content_type='image/png')
    if request.GET.get('download') == '1':
        resp['Content-Disposition'] = 'attachment; filename="corelab_plot_placeholder.png"'
    return resp

def download_material_data(request, material_name):
    """
    Busca el archivo de datos para un material específico (asumiendo ensayo de 'tensión'
    por defecto) y lo devuelve como una descarga CSV.
    """
    # Asumimos que queremos los datos del ensayo más común: "tensión"
    tipo_ensayo = 'tension'
    nombre_archivo = f"{material_name}_{tipo_ensayo}.csv"
    ruta_archivo = os.path.join(settings.BASE_DIR, 'materials', 'data', nombre_archivo)

    try:
        # Abrimos el archivo en modo binario ('rb') para leer su contenido crudo
        with open(ruta_archivo, 'rb') as f:
            csv_data = f.read()

        # Creamos una respuesta HTTP con el contenido del archivo
        response = HttpResponse(csv_data, content_type='text/csv')
        
        # Le decimos al navegador que es un archivo adjunto para descargar
        response['Content-Disposition'] = f'attachment; filename="datos_{nombre_archivo}"'
        
        return response

    except FileNotFoundError:
        # Si el archivo no existe, devolvemos un error 404 claro
        return HttpResponseNotFound(f"No se encontró el archivo de datos para '{material_name}' con ensayo de 'tensión'.")
# ============================================================
#  API PARA OBTENER DATOS (VERSIÓN ROBUSTA)
# ============================================================
@csrf_exempt
def obtener_datos(request):
    material_nombre = request.GET.get('material')
    tipo_ensayo = request.GET.get('tipo_ensayo')

    if not material_nombre or not tipo_ensayo:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    nombre_archivo = f"{material_nombre}_{tipo_ensayo.lower()}.csv"
    ruta_archivo = os.path.join(settings.BASE_DIR, 'materials', 'data', nombre_archivo)

    try:
        df = pd.read_csv(ruta_archivo, header=None)
        num_columnas = len(df.columns)
        
        if num_columnas == 3:
            df.columns = ['tiempo', 'deformacion', 'esfuerzo']
        elif num_columnas == 2:
            df.columns = ['deformacion', 'esfuerzo']
            df.insert(0, 'tiempo', [i * 0.1 for i in range(len(df))])
        else:
            raise ValueError(f"Formato de archivo inesperado con {num_columnas} columnas.")

        datos_grafica = [{'x': row['deformacion'], 'y': row['esfuerzo']} for _, row in df.iterrows()]
        datos_tabla = df.to_dict(orient='records')
        
        return JsonResponse({
            'success': True,
            'datos_grafica': datos_grafica,
            'datos_tabla': datos_tabla,
            'eje_x_label': 'Deformación (%)',
            'eje_y_label': 'Esfuerzo (Pa)',
        })
    except FileNotFoundError:
        mensaje_error = f'No se encontró el archivo: {nombre_archivo}'
        return JsonResponse({'error': mensaje_error, 'success': False}, status=404)
    except Exception as e:
        mensaje_error = f'Error al procesar el archivo: {str(e)}'
        return JsonResponse({'error': mensaje_error, 'success': False}, status=500)