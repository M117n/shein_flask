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

def calcular_puntos(jugadas):
    puntos = []
    tipos = []
    for jugada in jugadas:
        if 'jugador' in jugada.lower():
            # Si la jugada contiene 'jugador', no se suman puntos y se ignora.
            tipos.append('Jugador')
            puntos.append(0)  # Puntos para jugada ignorada
            continue
        if 'nuevo' in jugada.lower():
            puntos.append(5)
            tipos.append('Nuevo')
        elif 'intercambio' in jugada.lower():
            puntos.append(3)
            tipos.append('Intercambio')
        else:
            puntos.append(1)
            tipos.append('Regular')
    return puntos, tipos

def create_log(player, points, types):
    try:
        if os.path.exists(LOG_DIRECTORY):
            log_df = pd.read_csv(LOG_DIRECTORY)
        else:
            log_df = pd.DataFrame(columns=['Jugador', 'Fecha', 'Hora', 'Puntos', 'Tipo'])

        fecha_hora = datetime.datetime.now()
        fecha = fecha_hora.date()
        hora = fecha_hora.time()

        for point, point_type in zip(points, types):
            log_entry = {
                'Jugador': player,
                'Fecha': fecha,
                'Hora': hora,
                'Puntos': point,
                'Tipo': point_type
            }
            log_df = pd.concat([log_df, pd.DataFrame([log_entry])], ignore_index=True)

        save_df(log_df, LOG_DIRECTORY)
    except Exception as e:
        print(f"Error creating log for {player}: {e}")

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
            if not linea.startswith('⁃') and linea:
                jugador_actual = linea
                data[jugador_actual] = []
            elif linea.startswith('⁃') and jugador_actual:
                jugada = linea.replace('⁃', '').strip()
                data[jugador_actual].append(jugada)

        jugadores = list(data.keys())
        puntos = []
        tipos = []

        for jugador in jugadores:
            p, t = calcular_puntos(data[jugador])
            puntos.append(p)
            tipos.append(t)

        df = pd.DataFrame({
            'Jugador': jugadores,
            'Puntos': puntos
        })

        return df, jugadores, puntos, tipos
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

        new_data, players, points, types = procesar_resultados(content)

        # Explode para poder separar listas de puntos dentro del DF
        try:
            new_data = new_data.explode('Puntos')
            new_data['Puntos'] = new_data['Puntos'].astype(int)
        except Exception as e:
            print(f"Error during explode and conversion: {e}")
            return jsonify({'status': 'error', 'message': 'Error processing points.'}), 500

        data = load_df(RESULTS_DIRECTORY)
        merged_data = pd.concat([data, new_data], ignore_index=True)
        final_data = merged_data.groupby('Jugador', as_index=False)['Puntos'].sum()
        final_data = final_data.sort_values(by='Puntos', ascending=False)

        save_df(final_data, RESULTS_DIRECTORY)

        for player, points_player, type_player in zip(players, points, types):
            create_log(player, points_player, type_player)

        return jsonify({'status': 'success', 'message': 'Results updated successfully', 'data': final_data.to_dict(orient='records')}), 200
    except Exception as e:
        print(f"Error in update_results: {e}")
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred.'}), 500

if __name__ == '__main__':
    app.run(debug=True)