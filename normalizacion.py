import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalizar_datos(df_limpio):
    df = df_limpio.copy()

    # Columnas numéricas a normalizar (según reglas dadas)
    columnas_a_normalizar = [
        'Precio', 
        'Metros Totales', 
        'Metros Útiles', 
        'Año Construcción'
    ]

    # Verificamos que existan en el DataFrame
    columnas_a_normalizar = [col for col in columnas_a_normalizar if col in df.columns]

    # Aplicar MinMaxScaler
    scaler = MinMaxScaler()
    df_normalizado = df.copy()
    df_normalizado[columnas_a_normalizar] = scaler.fit_transform(df[columnas_a_normalizar])

    return df_normalizado
