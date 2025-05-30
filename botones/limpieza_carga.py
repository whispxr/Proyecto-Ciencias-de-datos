import pandas as pd

def cargar_limpiar_datos(filepath, umbral_nulos=0.1, eliminar_outliers=False):
    # 1. Cargar archivo
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    mensaje = ""
    # 2. Eliminar columnas con demasiados nulos (más del umbral)
    cols_a_dropear = df.columns[df.isnull().mean() > umbral_nulos]
    if len(cols_a_dropear) > 0:
        mensaje += (f"Columnas eliminadas por tener más del {umbral_nulos*100:.0f}% de nulos: {list(cols_a_dropear)}\n")
        df = df.drop(columns=cols_a_dropear)

    # 3. Eliminar filas con más de 4 valores nulos
    n_antes = len(df)
    df = df[df.isnull().sum(axis=1) <= 4]
    n_despues = len(df)
    mensaje += f"Se eliminaron {n_antes - n_despues} filas con más de 4 valores nulos.\n"

    # 4. Identificación o eliminación de outliers en columnas numéricas continuas
    cols_outliers = ['Precio', 'Metros Totales', 'Metros Útiles']
    for col in cols_outliers:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower) | (df[col] > upper)]
            mensaje += f"{col}: {len(outliers)} outliers detectados.\n"

            if eliminar_outliers:
                df = df[(df[col] >= lower) & (df[col] <= upper)]
                mensaje += f"Outliers eliminados en '{col}'.\n"

    return df, mensaje
