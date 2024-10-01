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
                const tdVictorias = document.createElement('td'); // Crear una celda para 'Ganados'
                const tdActions = document.createElement('td'); // Crear una celda para acciones
                const deleteBtn = document.createElement('button'); // Crear botón 'Eliminar'

                // Hacer celdas editables o no editables
                tdJugador.contentEditable = true;
                tdPuntos.contentEditable = true;
                tdVictorias.contentEditable = false; 
                
                // Configurar botón 'Eliminar'
                deleteBtn.textContent = 'Eliminar';
                deleteBtn.onclick = () => {
                    if (!confirmarEjecucion()) {
                        console.log('Acción cancelada por el usuario.');
                        return;
                    }
                    tr.remove();
                };
                tdActions.appendChild(deleteBtn);

                // Asignar texto a las celdas
                tdJugador.textContent = row.Jugador; // Asignar texto a la celda 'Jugador'
                tdPuntos.textContent = row.Puntos;   // Asignar texto a la celda 'Puntos'
                tdVictorias.textContent = row.Victorias || 0; // Asignar texto a la celda 'Ganados'

                // Agregar las celdas a la fila en el orden correcto
                tr.appendChild(tdJugador);   // Agregar la celda 'Jugador' a la fila
                tr.appendChild(tdPuntos);    // Agregar la celda 'Puntos' a la fila
                tr.appendChild(tdVictorias);   // Agregar la celda 'Ganados' a la fila
                tr.appendChild(tdActions);

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


async function deshacerCambios() {
    fetch('/undo_last_update', {
        method: 'POST',        
    }).then(response => response.json()).then(data => {
        if (data.status == 'success') {
            alert('El último cambio ha sido deshecho exitosamente.');
        } else {
            alert('No se pudo deshacer el cambio: ' + data.message);
        }
    }).catch(error => {
        console.error('Error al intentar deshacer los cambios.', error);
    });
}

function guardarCambios() {
    const tableBody = document.getElementById('resultados-table-body');
    const rows = tableBody.querySelectorAll('tr');
    const data = [];

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        const jugador = cells[0].textContent.trim();
        const puntos = parseInt(cells[1].textContent.trim());
        const victorias = parseInt(cells[2].textContent.trim());
        data.push({ Jugador: jugador, Puntos: puntos, Victorias: victorias });
    });

    fetch('/update_table', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: data })
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            alert('Cambios guardados correctamente.');
        } else {
            alert('Error al guardar los cambios: ' + result.message);
        }
    })
    .catch(error => {
        console.error('Error al guardar los cambios:', error);
    });
}

function confirmarEjecucion() {
    return window.confirm("¿Estás seguro de que deseas ejecutar esta acción? Los cambios serán permanentes.");
}

function descargarResultados() {
    window.location.href = '/download_latest_results';
}
