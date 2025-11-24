// ==============================================================================
//  materiales.js - Lógica de Interactividad para el Catálogo de Materiales
// ==============================================================================
//  Este script controla el menú desplegable de la página de materiales.
//  Funciona como un "interruptor" que muestra la sección de la categoría
//  seleccionada y oculta las demás. No realiza nuevas peticiones al servidor.
// ==============================================================================
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. CONFIGURACIÓN INICIAL ---
    const categoriaSelect = document.getElementById('categoria-select');
    
    // Si no encontramos el menú, detenemos el script para evitar errores.
    if (!categoriaSelect) {
        console.error("Error: No se encontró el elemento <select> con id 'categoria-select'.");
        return;
    }
    
    // Obtenemos una lista de TODAS las secciones de contenido de las categorías.
    const secciones = document.querySelectorAll('.seccion-categoria');
    console.log(`Encontradas ${secciones.length} secciones de categoría.`);

    // --- 2. EVENT LISTENER ---
    // Esta función se ejecuta CADA VEZ que el usuario cambia la opción del menú.
    categoriaSelect.addEventListener('change', (event) => {
        // Obtenemos el valor de la opción seleccionada (ej: "metales")
        const categoriaSeleccionada = event.target.value;

        // Primero, ocultamos todas las secciones para empezar de cero.
        secciones.forEach(seccion => {
            seccion.style.display = 'none';
        });

        // Si se seleccionó una categoría válida...
        if (categoriaSeleccionada) {
            // Construimos el ID de la sección que queremos mostrar (ej: "seccion-metales")
            const idSeccionAMostrar = `seccion-${categoriaSeleccionada}`;
            
            // Buscamos esa sección específica en el documento.
            const seccionAMostrar = document.getElementById(idSeccionAMostrar);
            
            if (seccionAMostrar) {
                // Si la encontramos, la hacemos visible con un efecto suave.
                seccionAMostrar.style.display = 'block';
                console.log(`Mostrando sección: #${idSeccionAMostrar}`);
            } else {
                console.error(`Error: No se encontró una sección con el ID #${idSeccionAMostrar}`);
            }
        }
    });

});