# ⚙️ Pedagogical Simulator of a Universal Testing Machine (PSUTM)

[![PyPI Version](https://badge.fury.io/py/psutm-simulator-kacruzv011.svg)](https://pypi.org/project/psutm-simulator-kacruzv011/)
[![Documentation](https://img.shields.io/badge/docs-leerm%C3%A1s-brightgreen)](https://kacruzv011.github.io/Software_materiales_kc/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Un simulador web educativo, desarrollado en Django, para la caracterización mecánica de materiales mediante ensayos virtuales de tensión, compresión y torsión.

**Autores:** Kevin Cruz, Alexei.
Un proyecto de la **Universidad Distrital Francisco José de Caldas**.

![Screenshot de la Simulación](url_a_tu_screenshot.png) <!-- Reemplaza esto con una URL a una imagen de tu simulador. Puedes subirla a la pestaña "Issues" de GitHub y copiar el enlace. -->

---


## 🧰 Tecnologías utilizadas

| Herramienta | Descripción |
|--------------|-------------|
| **Python 3.10+** | Lenguaje base del proyecto. |
| **Django 5.x** | Framework principal para el backend y gestión web. |
| **SQLite3** | Base de datos por defecto (puede migrarse a PostgreSQL o MySQL). |
| **Matplotlib** | Generación de gráficas de resultados de simulación. |
| **Pandas / NumPy** | Procesamiento y análisis de datos de los materiales. |
| **HTML / CSS (Django templates)** | Renderizado de interfaz web básica. |
| **JupyterLab (opcional)** | Entorno auxiliar para pruebas de simulación. |


Este proyecto tiene dos formas de uso: como una **aplicación web completa** que puedes ejecutar localmente, o como una **librería de Python** que puedes usar en tus propios proyectos.

## 1. Para Usuarios Finales: Ejecutar la Interfaz Web Completa 🚀

Esta es la opción si quieres usar el simulador interactivo tal y como fue diseñado.

### Requisitos Previos

- Python 3.8 o superior
- Git

### Guía de Instalación y Ejecución

Sigue estos pasos en tu terminal para tener el simulador funcionando en tu máquina en menos de 5 minutos.

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/kacruzv011/Software_materiales_kc.git
    cd Software_materiales_kc
    ```

2.  **(Recomendado) Crea y activa un entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # venv\Scripts\activate    # En Windows
    ```

3.  **Instala todas las dependencias necesarias:**
    Este proyecto utiliza dos archivos de requisitos. `requirements-dev.txt` incluye todo lo necesario para correr la aplicación y también las herramientas de desarrollo como `matplotlib` para generar nuevos materiales.
    ```bash
    pip install -r requirements-dev.txt
    ```

4.  **Configura la base de datos:**
    Este comando creará el archivo de base de datos local y todas las tablas necesarias.
    ```bash
    python manage.py migrate
    ```

5.  **Genera los materiales iniciales:**
    El simulador necesita los archivos de datos CSV para funcionar. Este comando los creará automáticamente a partir de los PDFs de ejemplo incluidos.
    ```bash
    python manage.py generar_materiales
    ```

6.  **¡Inicia el servidor!**
    ```bash
    python manage.py runserver
    ```

¡Listo! Abre tu navegador web y visita **http://127.0.0.1:8000/** para acceder al simulador.

---

## 2. Para Desarrolladores: Usar la Librería (`corelab`) en un Proyecto Externo 📦

Si solo te interesa el "motor" de simulación (la lógica para leer PDFs, generar curvas, y los modelos de Django) para integrarlo en tu propio código, puedes instalar la librería directamente desde PyPI.

### Instalación desde PyPI

```bash
pip install psutm-simulator-kacruzv011
```
Ejemplo de Uso como Librería

Una vez instalado, puedes importar las funciones principales en tu propio código Python.

from corelab.simulations import get_properties_from_pdf, simular_metal
from corelab.models import Material

# Extraer propiedades de un PDF local
nombre, props, mtype = get_properties_from_pdf("ruta/a/mi_ficha.pdf")

if props:
    # Generar curvas de simulación
    curvas_sinteticas = simular_metal(**props)
    
    # También puedes interactuar con los modelos de Django en tu propio proyecto,
    # siempre que tengas 'corelab' en tus INSTALLED_APPS.
    nuevo_material = Material.objects.create(nombre=nombre, categoria=mtype)


Para más detalles sobre la API y las funciones disponibles, consulta la Documentación Oficial Completa.

## ⚖️ Licencia y Descargo de Responsabilidad

Este proyecto se distribuye bajo los términos de la **Licencia Pública General de GNU v3 (GPLv3)**. Para más detalles, consulta el archivo `LICENSE`.

### Disclaimer

1.  **Naturaleza de los Datos:** Este es un simulador con fines **estrictamente educativos**. Los datos de las curvas de ensayo son **sintéticos** y generados por modelos matemáticos. **NO deben ser utilizados para diseño de ingeniería en el mundo real.**

2.  **Fuente de las Propiedades:** Las propiedades de entrada para los modelos han sido extraídas de las fichas técnicas públicas de [MatWeb.com](https://www.matweb.com). Agradecemos a MatWeb por este invaluable recurso. Este proyecto no está afiliado ni respaldado por MatWeb 


