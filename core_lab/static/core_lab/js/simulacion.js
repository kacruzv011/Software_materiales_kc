document.addEventListener('DOMContentLoaded', () => {
    console.log("Simulación JS Final (sin saltos) cargado.");

    // ==================================================================
    //  ZONA DE CONFIGURACIÓN
    // ==================================================================
    const DRAG_LIMITS_Y = {
        compresion_start: '20%',
        tension_start:    '29%'
    };
    const PIXELS_POR_PUNTO = 2; // Ajusta este valor según la sensibilidad deseada
    // ==================================================================

    const materialSelect = document.getElementById('material-select');
    const tipoEnsayoSelect = document.getElementById('tipo-ensayo-select');
    const mordaza = document.getElementById('mordaza-superior-movil');
    const handleTorsion = document.getElementById('handle-torsion');
    const canvas = document.getElementById('grafica');
    const tablaDatosBody = document.getElementById('tabla-datos').querySelector('tbody');
    const placeholderText = document.getElementById('placeholder-text');

    let chartInstance, datosEnsayoCompletos = [], isDragging = false, lastMousePos = 0, currentIndex = -1;

    async function cargarDatos() {
        const material = materialSelect.value, ensayo = tipoEnsayoSelect.value;
        if (!material || !ensayo) return;
        reiniciarEstado(ensayo);
        placeholderText.textContent = "Cargando datos...";
        try {
            const response = await fetch(`${OBTENER_DATOS_URL}?material=${material}&tipo_ensayo=${ensayo}`);
            const data = await response.json();
            if (!data.success) throw new Error(data.error);
            datosEnsayoCompletos = data.datos_tabla;
            placeholderText.textContent = `¡Listo! Inicia el ensayo de ${ensayo}.`;
            if (ensayo === 'torsion') handleTorsion.style.cursor = 'ew-resize';
            else mordaza.style.cursor = 'grab';
        } catch (err) { placeholderText.textContent = `Error: ${err.message}`; }
    }
    materialSelect.addEventListener('change', cargarDatos);
    tipoEnsayoSelect.addEventListener('change', cargarDatos);

    function onMouseDown(e) {
        if (datosEnsayoCompletos.length === 0) return;
        isDragging = true;
        const ensayo = tipoEnsayoSelect.value;
        if (ensayo === 'torsion') { lastMousePos = e.clientX; } 
        else { lastMousePos = e.clientY; mordaza.style.cursor = 'grabbing'; }
        e.preventDefault();
    }
    mordaza.addEventListener('mousedown', onMouseDown);
    handleTorsion.addEventListener('mousedown', onMouseDown);

    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const ensayo = tipoEnsayoSelect.value;
        let delta = 0, cambioEnIndice = 0, currentMousePos = 0;
        if (ensayo === 'torsion') { /* Lógica de Torsión aquí */ }
        else {
            currentMousePos = e.clientY;
            delta = currentMousePos - lastMousePos;
            cambioEnIndice = (ensayo === 'tension') ? -delta / PIXELS_POR_PUNTO : delta / PIXELS_POR_PUNTO;
        }
        lastMousePos = currentMousePos;
        currentIndex += cambioEnIndice;
        currentIndex = Math.max(0, Math.min(datosEnsayoCompletos.length - 1, currentIndex));
        actualizarUI(Math.floor(currentIndex));
    });

    window.addEventListener('mouseup', () => { if (isDragging) { isDragging = false; mordaza.style.cursor = 'grab'; } });

    function actualizarUI(index) {
        if (!chartInstance) return;
        if (datosEnsayoCompletos.length === 0 || index < 0) {
            chartInstance.data.labels = []; chartInstance.data.datasets[0].data = [];
            chartInstance.update('none');
            tablaDatosBody.innerHTML = `<tr><td colspan="3">Selecciona un material y ensayo</td></tr>`;
            return;
        }
        const puntosHastaAhora = datosEnsayoCompletos.slice(0, index + 1);
        const puntoActual = datosEnsayoCompletos[index];
        tablaDatosBody.innerHTML = `<tr><td>${parseFloat(puntoActual.tiempo).toFixed(2)}</td><td>${parseFloat(puntoActual.deformacion).toFixed(4)}</td><td>${parseFloat(puntoActual.esfuerzo).toExponential(2)}</td></tr>`;
        chartInstance.data.labels = puntosHastaAhora.map(d => d.deformacion);
        chartInstance.data.datasets[0].data = puntosHastaAhora.map(d => d.esfuerzo);
        chartInstance.update('none');
        
        const porcentajeDeAvance = index / (datosEnsayoCompletos.length - 1);
        const limiteSuperiorPx = mordaza.parentElement.offsetHeight * (parseFloat(DRAG_LIMITS_Y.compresion_start) / 100);
        const limiteInferiorPx = mordaza.parentElement.offsetHeight * (parseFloat(DRAG_LIMITS_Y.tension_start) / 100);
        const rangoDeArrastrePx = limiteInferiorPx - limiteSuperiorPx;
        
        const newTop = (tipoEnsayoSelect.value === 'compresion') 
                        ? limiteSuperiorPx + (rangoDeArrastrePx * porcentajeDeAvance) 
                        : limiteInferiorPx - (rangoDeArrastrePx * porcentajeDeAvance);
        mordaza.style.top = `${newTop}px`;
    }
    
    function crearGrafico() {
        if (chartInstance) chartInstance.destroy();
        const ctx = canvas.getContext('2d');
        chartInstance = new Chart(ctx, { type: "line", data: { labels: [], datasets: [{ label: "Esfuerzo vs Deformación", data: [], borderColor: "#007bff", borderWidth: 2, pointRadius: 0, tension: 0.1 }] }, options: { responsive: true, maintainAspectRatio: false, scales: { x: { title: { display: true, text: "Deformación (%)" } }, y: { title: { display: true, text: "Esfuerzo (Pa)" }, ticks: { callback: (value) => (typeof value === 'number') ? value.toExponential(1) : value } } }, plugins: { legend: { display: true, position: 'top' } } } });
    }

    function reiniciarEstado(ensayoSeleccionado = null) {
        const ensayo = ensayoSeleccionado || tipoEnsayoSelect.value;
        datosEnsayoCompletos = [], currentIndex = -1, isDragging = false;
        
        actualizarUI(-1);
        placeholderText.textContent = "Selecciona un material y ensayo para comenzar.";
        handleTorsion.style.display = 'none';
        mordaza.style.cursor = 'not-allowed';

        if (ensayo === 'torsion') { handleTorsion.style.display = 'block'; mordaza.style.top = '25%'; } 
        else if (ensayo === 'compresion') { mordaza.style.top = DRAG_LIMITS_Y.compresion_start; } 
        else { mordaza.style.top = DRAG_LIMITS_Y.tension_start; }
    }
    
    materialSelect.selectedIndex = 0, tipoEnsayoSelect.selectedIndex = 0;
    crearGrafico();
    reiniciarEstado();
});