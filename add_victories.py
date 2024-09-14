import pandas as pd
import os


RESULTS_DIRECTORY = os.path.join('data', 'resultados.csv')
data = pd.read_csv(RESULTS_DIRECTORY)

victorias = {
    'Andrea Talamante': 3,
    'Nuri Lizbeth': 1,
    'Vakita': 1,
    'Ximena Camacho': 1,
    'Doris': 5,
    'Mary Torres': 5,
    'Denisse Valenzuela': 5,
    'Maritza': 2,
    'Brenda': 3,
    'Glendy': 3,
    'Marisol': 5,
    'Natasha': 3,
    'Yiseth': 3,
    'Bueno': 3,
    'Edixia Maradiaga': 5,
    'Karla Pinto': 3,
    'Yane': 4,
    'Alec': 2,
    'Brigitte': 3,
    'Ross': 1,
    'Keyla Perez': 4,
    'Luisana Romero': 3,
    'Anaileth': 1,
    'Bere': 3,
    'Yennifer': 3,
    'Heysy': 1,
    'Kim': 3,
    'Sammy': 2,
    'Osmany': 5,
    'Mile': 2,
    'Marie Kreations': 1,
    'Maura Ochoa': 4,
    'Liz Bravo': 4,
    'Blanky Ruiz': 4,
    'Bautista': 2,
    'Dayana': 1,
    'Wendy Hernandez': 1,
    'Arlin': 1,
    'Jade Aragon': 3,
    'Inez': 1,
    'Yadi': 2,
    'Aury Beato': 1,
    'Christian Bustamante': 2,
    'Chayo': 2,
    'Ale': 1,
    'Georgina Rizzo': 1,
    'Leidimar': 1
}

victorias = {k.upper(): v for k, v in victorias.items()}

# Añadir la columna 'Victorias' y asignar valores de la lista, con valores predeterminados de 0
data['Victorias'] = data['Jugador'].apply(lambda x: victorias.get(x.upper(), 0))

# Guardar el CSV actualizado
data.to_csv(RESULTS_DIRECTORY, index=False)

print(f"Archivo CSV actualizado guardado en {RESULTS_DIRECTORY}")