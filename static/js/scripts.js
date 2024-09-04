async function ejecutarProcesamiento() {
    const puntos = document.getElementById('puntosInput').value;
    const response = await fetch('/update_results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ results: puntos }),
    });

    const data = await response.json();
    if (data.status === 'success') {
        document.getElementById('resultado').innerText = 'Resultados procesados correctamente.';
    } else {
        document.getElementById('resultado').innerText = 'Error al procesar los resultados.';
    }
}

async function mostrarResultado() {
    try {
        const response = await fetch('/get_latest_results');  // Asegúrate de que esta ruta coincide con la definida en app.py
        const data = await response.json();

        if (response.ok && data.status === 'success') {
            document.getElementById('resultado').innerText = JSON.stringify(data.data);
        } else {
            document.getElementById('resultado').innerText = data.message || 'Error al obtener los resultados.';
        }
    } catch (error) {
        console.error('Error fetching latest results:', error);
        document.getElementById('resultado').innerText = 'Error al obtener los resultados.';
    }
}

