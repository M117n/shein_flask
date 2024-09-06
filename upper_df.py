import pandas as pd


RESULTS_DIRECTORY = 'data\\resultados.csv'
data_frame = pd.read_csv(RESULTS_DIRECTORY)

data_frame['Jugador'] = data_frame['Jugador'].str.upper()

data_frame.to_csv(RESULTS_DIRECTORY, index=False)