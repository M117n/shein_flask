from flask import Flask, request, jsonify, render_template, redirect, url_for
import pandas as pd
import os
import datetime
from flask_cors import CORS


app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

RESULTS_DIRECTORY = 'data\\resultados.csv'
LOG_DIRECTORY = 'data\logs.csv'

@app.route('/')
def home():
    return render_template('index.html')

def load_df(directory):
    try:
        if os.path.exists(directory):
            df = pd.read_csv(directory)
        else:
            df = pd.DataFrame(columns=['Jugador', 'Puntos'])
        return df
    except Exception as e:
        print(f"Error loading DataFrame from {directory}: {e}")
        return pd.DataFrame(columns=['Jugador', 'Puntos'])

def save_df(df, ruta):
    try:
        df.to_csv(ruta, index=False)
    except Exception as e:
        print(f"Error saving DataFrame to {ruta}: {e}")

def delete_points(jugador):
    try:
        if os.path.exists(RESULTS_DIRECTORY):
            df = pd.read_csv(RESULTS_DIRECTORY)
            # Selecciona el jugador y pone los puntos en 0
            df.loc[df['Jugador'] == jugador, 'Puntos'] = 0
            # Guarda los cambios
            df.to_csv(RESULTS_DIRECTORY, index=False)
        else:
            print("El archivo de resultados no existe.")
    except Exception as e:
        print(f"Error: {e}")

def calcular_puntos(jugadas, jugador):
    puntos = []
    tipos = []
    for jugada in jugadas:
        jugada = jugada.lower()

        if 'jugador' in jugada.lower() or 'jugadora' in jugada.lower():
            # Si la jugada contiene 'jugador', no se suman puntos y se ignora.
            tipos.append('Jugador')
            puntos.append(0)  # Puntos para jugada ignorada
            delete_points(jugador)
            continue
        elif 'nuevo' in jugada.lower():
            puntos.append(5)
            tipos.append('Nuevo')
        elif 'intercambio' in jugada.lower():
            puntos.append(3)
            tipos.append('Intercambio')
        else:
            puntos.append(1)
            tipos.append('Regular')

    return puntos, tipos

def create_log(types):
    try:
        # Verificar si el archivo existe
        if os.path.exists(LOG_DIRECTORY):
            try:
                # Intentar leer el archivo
                log_df = pd.read_csv(LOG_DIRECTORY)
                # Si el archivo está vacío, crear un DataFrame con las columnas correctas
                if log_df.empty:
                    log_df = pd.DataFrame(columns=['Jugador', 'Fecha', 'Hora', 'Puntos', 'Tipo'])
            except pd.errors.EmptyDataError:
                # Si hay un error de datos vacíos, crear el DataFrame con las columnas correctas
                log_df = pd.DataFrame(columns=['Jugador', 'Fecha', 'Hora', 'Puntos', 'Tipo'])
        else:
            # Si el archivo no existe, crear un DataFrame nuevo con las columnas correctas
            log_df = pd.DataFrame(columns=['Jugador', 'Fecha', 'Hora', 'Puntos', 'Tipo'])

        fecha_hora = datetime.datetime.now()
        fecha = fecha_hora.date()
        hora = fecha_hora.time()

        log_entries = []

        for player, tipos in types.items():
            for tipo, puntos in tipos.items():
                log_entry = {
                    'Jugador': player,
                    'Fecha': fecha,
                    'Hora': hora,
                    'Puntos': puntos,
                    'Tipo': tipo
                }
                log_entries.append(log_entry)

        new_entries_df = pd.DataFrame(log_entries)
        log_df = pd.concat([log_df, new_entries_df], ignore_index=True)

        save_df(log_df, LOG_DIRECTORY)
    except Exception as e:
        print(f"Error creando log: {e}")

def log_statistic():
    try:
        if os.path.exists(LOG_DIRECTORY):
            log_df = pd.read_csv(LOG_DIRECTORY)
        else:
            log_df = pd.DataFrame(columns=['Jugador', 'Fecha', 'Hora', 'Puntos', 'Tipo'])

        group_log_df = log_df.groupby('Jugador')

    except Exception as e:
        print("Error creando estadistica")

def to_excel(df):
    try:
        df.to_excel(f'Resultados_{datetime.date.today()}.xlsx', index=False)
    except Exception as e:
        print(f"Error exporting to Excel: {e}")

def procesar_resultados(texto):
    try:
        data = {}
        jugador_actual = None
        lineas = texto.splitlines()

        for linea in lineas:
            linea = linea.strip()
            # Identificar un nuevo jugador si la línea no empieza con guion y no está vacía
            if linea and not linea.startswith('-'):
                jugador_actual = linea
                data[jugador_actual] = []
            # Si hay un jugador actual, asociar jugadas correctamente
            elif linea.startswith('-') and jugador_actual:
                jugada = linea.replace('-', '').strip()  # Limpiar guion y espacios
                if jugada:  # Asegurarse de que no es una línea vacía después de limpiar
                    data[jugador_actual].append(jugada)
            else:
                # Mensaje de depuración para formato inesperado
                print(f"Formato inesperado o jugador actual no definido: '{linea}'")

        # Si no se encontraron jugadores, retorna un DataFrame vacío
        if not data:
            print("No se encontraron jugadores válidos en los datos.")
            return pd.DataFrame(columns=['Jugador', 'Puntos']), [], [], []

        jugadores = list(data.keys())
        puntos = []
        tipos = {}

        for jugador in jugadores:
            p, t = calcular_puntos(data[jugador], jugador)
            puntos.append(sum(p))
            tipos[jugador] = dict(zip(t, p))

        df = pd.DataFrame({
            'Jugador': jugadores,
            'Puntos': puntos
        })

        return df, tipos

    except Exception as e:
        print(f"Error processing results: {e}")
        return pd.DataFrame(columns=['Jugador', 'Puntos']), [], [], []


    
@app.route('/get_latest_results', methods=['GET'])
def get_latest_results():
    try:
        data = load_df(RESULTS_DIRECTORY)
        if data.empty:
            return jsonify({'status': 'error', 'message': 'No hay resultados disponibles.'}), 404
        
        final_data = data.groupby('Jugador', as_index=False)['Puntos'].sum()
        final_data = final_data.sort_values(by='Puntos', ascending=False)
        return jsonify({'status': 'success', 'data': final_data.to_dict(orient='records')}), 200
    except Exception as e:
        print(f"Error in get_latest_results: {e}")
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred.'}), 500

@app.route('/update_results', methods=['POST'])
def update_results():
    try:
        content = request.json.get('results', '')
        if not content:
            return jsonify({'status': 'error', 'message': 'No results provided.'}), 400
        
        # Log para verificar los datos recibidos
        print(f"Contenido recibido: {content}")

        new_data, types = procesar_resultados(content)
        print(f"Datos procesados: {new_data}")  # Log para ver los datos procesados

        new_data['Puntos'] = new_data['Puntos'].astype(int)
        data = load_df(RESULTS_DIRECTORY)
        print(f"Datos cargados de CSV: {data}")  # Log para ver datos cargados del CSV

        merged_data = pd.concat([data, new_data], ignore_index=True)
        final_data = merged_data.groupby('Jugador', as_index=False)['Puntos'].sum()
        final_data = final_data.sort_values(by='Puntos', ascending=False)

        save_df(final_data, RESULTS_DIRECTORY)
        print(f"Datos guardados en CSV: {final_data}")  # Log para ver los datos finales guardados

        create_log(types)

        return jsonify({'status': 'success', 'message': 'Se actualizó correctamente', 'data': final_data.to_dict(orient='records')}), 200
    except Exception as e:
        print(f"Error in update_results: {e}")
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred.'}), 500


if __name__ == '__main__':
    app.run(debug=True)