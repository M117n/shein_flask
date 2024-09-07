async function ejecutarProcesamiento() {
    let puntos = document.getElementById('puntosInput').value;

    // Limpieza de los datos: eliminar líneas vacías y espacios innecesarios
    puntos = puntos.split('\n').map(line => line.trim()).filter(line => line !== '').join('\n');

    console.log("Datos enviados después de limpieza:", puntos); // Log para verificar datos

    try {
        const response = await fetch('/update_results', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ results: puntos }),
        });

        const data = await response.json();
        if (response.ok && data.status === 'success') {
            document.getElementById('resultado').innerText = 'Resultados procesados correctamente.';
            
            // Llama a mostrarResultado una vez que la actualización sea exitosa
            // await mostrarResultado();
        } else {
            document.getElementById('resultado').innerText = data.message || 'Error al procesar los resultados.';
        }
    } catch (error) {
        console.error('Error al procesar los resultados:', error);
        document.getElementById('resultado').innerText = 'Error al procesar los resultados.';
    }
}

async function mostrarResultado() {
    try {
        const response = await fetch(`/get_latest_results?timestamp=${new Date().getTime()}`);
        console.log("Respuesta del servidor:", response);

        const data = await response.json();
        console.log("Datos recibidos:", data); // Verifica el contenido exacto de la respuesta

        if (response.ok && data.status === 'success') {
            const tableBody = document.getElementById('resultados-table-body');
            tableBody.innerHTML = ''; // Limpiar la tabla antes de agregar nuevos resultados
            
            data.data.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${row.Jugador}</td><td>${row.Puntos}</td>`;
                tableBody.appendChild(tr);
            });
            
            // Añade un log para confirmar la actualización del DOM
            console.log("Tabla actualizada con los datos más recientes:", tableBody.innerHTML);
        } else {
            console.error("Error en la respuesta del servidor:", data); // Log para errores específicos
            document.getElementById('resultado').innerText = data.message || 'Error al obtener los resultados.';
        }
    } catch (error) {
        console.error('Error fetching latest results:', error);
        document.getElementById('resultado').innerText = 'Error al obtener los resultados_1';
    }
}

function descargarResultados() {
    window.location.href = '/download_latest_results';
}