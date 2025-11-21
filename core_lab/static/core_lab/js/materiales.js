// ==========================================================
//  materiales.js - VERSIÓN CORREGIDA Y MÁS ROBUSTA
// ==========================================================
document.addEventListener('DOMContentLoaded', () => {
    // 1. Obtenemos el menú desplegable de categorías.
    const categoriaSelect = document.getElementById('categoria-select');
    
    // Si no encontramos el elemento, salimos para evitar errores.
    if (!categoriaSelect) {
        console.error("Error: No se encontró el elemento <select> con id 'categoria-select'.");
        return;
    }
    
    // 2. Obtenemos TODAS las secciones que contienen la información de las categorías.
    //    Esto nos da una colección de elementos para mostrar u ocultar.
    const secciones = document.querySelectorAll('.seccion-categoria');

    // 3. Añadimos el "listener" para el evento 'change'.
    //    Esta función se ejecutará CADA VEZ que el usuario cambie la opción del menú.
    categoriaSelect.addEventListener('change', (event) => {
        // Obtenemos el valor de la opción seleccionada (ej: "metales", "polimericos", etc.)
        const categoriaSeleccionada = event.target.value;

        // DEBUG: Mostramos en la consola qué categoría se seleccionó.
        // Abre la consola (F12) en tu navegador para ver este mensaje.
        console.log(`Categoría seleccionada: ${categoriaSeleccionada}`);

        // Ocultamos todas las secciones para empezar de cero.
        secciones.forEach(seccion => {
            seccion.style.display = 'none';
        });

        // Si se seleccionó una categoría válida (no la opción "Elige una categoría")...
        if (categoriaSeleccionada) {
            // Construimos el ID de la sección que queremos mostrar.
            // Ejemplo: si el valor es "metales", el ID será "seccion-metales".
            const idSeccionAMostrar = `seccion-${categoriaSeleccionada}`;
            
            // Buscamos esa sección específica en el documento.
            const seccionAMostrar = document.getElementById(idSeccionAMostrar);
            
            if (seccionAMostrar) {
                // Si la encontramos, la hacemos visible.
                seccionAMostrar.style.display = 'block';
                console.log(`Mostrando sección con ID: #${idSeccionAMostrar}`);
            } else {
                console.error(`Error: No se encontró una sección con el ID #${idSeccionAMostrar}`);
            }
        }
    });

});