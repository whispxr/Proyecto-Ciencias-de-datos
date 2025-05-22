import pandas as pd

def cargar_limpiar_datos(archivo, umbral_nulos=0.5):

    if archivo.endswith('.csv'):
        df = pd.read_csv(archivo)
    elif archivo.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(archivo)
    else:
        raise ValueError("El archivo debe ser .csv, .xls o .xlsx")
    
    # 1. Eliminar columnas con más del umbral de nulos
    limite_nulos = umbral_nulos * len(df)
    df = df.loc[:, df.isnull().sum() <= limite_nulos]

    # 2. Eliminar filas duplicadas
    df = df.drop_duplicates()

    # 3. Reemplazar valores nulos numéricos por la media
    num_cols = df.select_dtypes(include='number').columns
    for col in num_cols:
        media = df[col].mean()
        df[col] = df[col].fillna(media)  # CORRECCIÓN: asignar la columna completa

    # 4. Reemplazar valores nulos categóricos por la moda
    cat_cols = df.select_dtypes(include='object').columns
    for col in cat_cols:
        moda = df[col].mode()
        if not moda.empty:
            df[col] = df[col].fillna(moda[0])  # CORRECCIÓN: asignar la columna completa
        else:
            df[col] = df[col].fillna('')  # CORRECCIÓN: asignar la columna completa

    # 5. Eliminar filas que todavía tengan nulos (por si quedó alguno)
    df = df.dropna()

    return df
