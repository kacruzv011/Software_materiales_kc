======================
Guía de Inicio Rápido
======================

Sigue estos pasos para instalar, configurar y ejecutar el proyecto CoreLab en tu máquina local.

1. Instalación
---------------

Primero, clona el repositorio desde GitHub y navega hasta el directorio del proyecto. Luego, se recomienda crear un entorno virtual e instalar las dependencias.

.. code-block:: bash

   pip install -r requirements.txt

2. Configuración de la Base de Datos
---------------------------------------

Una vez instaladas las dependencias, necesitas crear la base de datos y una cuenta de administrador para acceder al panel de Django.

.. code-block:: bash

   python manage.py migrate
   python manage.py createsuperuser

3. Generar los Materiales Iniciales
---------------------------------------

El simulador necesita archivos de datos para funcionar. Coloca tus fichas técnicas en formato PDF en la carpeta ``media/uploads/pdfs/`` y ejecuta el siguiente comando para procesarlos.

.. code-block:: bash

   python manage.py generar_materiales

4. Ejecutar el Simulador
---------------------------

¡Ya está todo listo! Inicia el servidor de desarrollo de Django:

.. code-block:: bash

   python manage.py runserver

Abre tu navegador y visita `http://127.0.0.1:8000/` para acceder a la aplicación.