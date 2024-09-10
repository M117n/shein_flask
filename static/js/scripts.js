if (document.readyState !== 'loading') {
    console.log('document is already ready, just execute code here');
    inicializarEventos(); // Llama a la función que inicializa los eventos
} else {
    document.addEventListener('DOMContentLoaded', function () {
        console.log('document was not ready, place code here');
        inicializarEventos(); // Llama a la función que inicializa los eventos
    });
}

function inicializarEventos() {
    const ejecutarBtn = document.querySelector('button[onclick="ejecutarProcesamiento()"]');
    if (ejecutarBtn) {
        ejecutarBtn.addEventListener('click', ejecutarProcesamiento);
    }

    const resultadoBtn = document.querySelector('button[onclick="mostrarResultado()"]');
    if (resultadoBtn) {
        resultadoBtn.addEventListener('click', mostrarResultado);
    }

    const descargarBtn = document.querySelector('button[onclick="descargarResultados()"]');
    if (descargarBtn) {
        descargarBtn.addEventListener('click', descargarResultados);
    }
}

async function mostrarResultado() {
    const tableBody = document.getElementById('resultados-table-body');
    if (!tableBody) {
        console.error('El elemento "resultados-table-body" no se encuentra en el DOM.');
        return;
    }

    try {
        const response = await fetch(`/get_latest_results?timestamp=${new Date().getTime()}`);
        console.log("Respuesta del servidor:", response);

        if (!response.ok) {
            throw new Error('Error al obtener los resultados.');
        }

        const data = await response.json();
        console.log("Datos recibidos:", data);

        if (data.status === 'success') {
            // Limpiar las filas anteriores
            tableBody.innerHTML = '';

            // Crear nuevas filas para cada dato recibido
            data.data.forEach(row => {
                const tr = document.createElement('tr'); // Crear una fila
                const tdJugador = document.createElement('td'); // Crear una celda para 'Jugador'
                const tdPuntos = document.createElement('td'); // Crear una celda para 'Puntos'
                
                tdJugador.textContent = row.Jugador; // Asignar texto a la celda 'Jugador'
                tdPuntos.textContent = row.Puntos; // Asignar texto a la celda 'Puntos'

                tr.appendChild(tdJugador); // Agregar la celda 'Jugador' a la fila
                tr.appendChild(tdPuntos); // Agregar la celda 'Puntos' a la fila

                tableBody.appendChild(tr); // Agregar la fila al cuerpo de la tabla
            });

            console.log("Tabla actualizada con los datos más recientes:", tableBody.innerHTML);
        } else {
            throw new Error(data.message || 'Error al obtener los resultados.');
        }
    } catch (error) {
        console.error('Error fetching latest results:', error);
        // Mostrar mensajes de error en un lugar separado, como un div debajo de la tabla
        document.getElementById('resultado').innerText = 'Error al obtener los resultados.';
    }
}


async function ejecutarProcesamiento() {
    if (!confirmarEjecucion()) {
        console.log('Acción cancelada por el usuario.');
        return;
    }
    
    let puntos = document.getElementById('puntosInput').value;

    puntos = puntos.split('\n').map(line => line.trim()).filter(line => line !== '').join('\n');

    if (puntos === '') {
        console.warn('No se han proporcionado puntos para procesar.');
        document.getElementById('resultado').innerText = 'No se han proporcionado puntos para procesar.';
        return;
    }

    console.log("Datos enviados después de limpieza:", puntos);

    try {
        const response = await fetch('/update_results', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ results: puntos }),
        });

        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor.');
        }

        const data = await response.json();
        if (data.status === 'success') {
            document.getElementById('resultado').innerText = 'Resultados procesados correctamente.';
        } else {
            document.getElementById('resultado').innerText = data.message || 'Error al procesar los resultados.';
        }
    } catch (error) {
        console.error('Error al procesar los resultados:', error);
        document.getElementById('resultado').innerText = 'Error al procesar los resultados.';
    }
}

function confirmarEjecucion() {
    return window.confirm("¿Estás seguro de que deseas ejecutar esta acción? Los cambios serán permanentes.");
}

function descargarResultados() {
    window.location.href = '/download_latest_results';
}
