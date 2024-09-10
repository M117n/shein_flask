function verificarSelectores() {
    // Selecciona el área de texto donde ingresas los puntos
    const puntosInput = document.getElementById('puntosInput');
    console.log('Puntos Input:', puntosInput); // Debería mostrar el elemento <textarea> en la consola

    // Selecciona el contenedor donde se muestran los resultados
    const resultado = document.getElementById('resultado');
    console.log('Resultado:', resultado); // Debería mostrar el elemento <div> para resultados

    // Selecciona el cuerpo de la tabla donde se mostrarán los resultados
    const resultadosTableBody = document.getElementById('resultados-table-body');
    console.log('Tabla de Resultados:', resultadosTableBody); // Debería mostrar el elemento <tbody> de la tabla
}

// Llama a la función para verificar selectores cuando se carga la página
