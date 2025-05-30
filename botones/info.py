import tkinter as tk
from tkinter import ttk
import pandas as pd

def crear_boton_info(app, sidebar):
    boton = ttk.Button(
        sidebar,
        text="ℹ️ Información DataFrame",
        style="Sidebar.TButton",
        command=lambda: mostrar_info_dataframe(app)
    )
    boton.pack(fill="x", padx=15, pady=5)

def mostrar_info_dataframe(app):
    if app.datos_procesados is None:
        app.status.config(text="No hay datos cargados.")
        app.show_text("Primero cargá un archivo con datos.")
        return

    app.clear_content()

    notebook = ttk.Notebook(app.content)
    notebook.pack(expand=True, fill='both')

    df = app.datos_procesados


    frame_info = ttk.Frame(notebook)
    notebook.add(frame_info, text="Info")

    info_df = pd.DataFrame({
        "Columna": df.columns,
        "Tipo": df.dtypes.astype(str),
        "No. Nulos": df.isnull().sum(),
        "No. Únicos": df.nunique()
    })

    tree_info = ttk.Treeview(frame_info, columns=list(info_df.columns), show="headings")
    tree_info.pack(expand=True, fill='both')

    for col in info_df.columns:
        tree_info.heading(col, text=col)
        tree_info.column(col, anchor='center', width=120)

    for _, row in info_df.iterrows():
        tree_info.insert("", "end", values=list(row))

    scroll_info = ttk.Scrollbar(frame_info, orient="vertical", command=tree_info.yview)
    scroll_info.pack(side="right", fill="y")
    tree_info.configure(yscrollcommand=scroll_info.set)

    #detalle variable categorica
    def on_info_select(event):
        selected_item = tree_info.selection()
        if selected_item:
            col_name = tree_info.item(selected_item[0])['values'][0]
            tipo_col = tree_info.item(selected_item[0])['values'][1]
            if 'object' in tipo_col or 'category' in tipo_col:
                mostrar_detalle_categorica(df, col_name)

    tree_info.bind("<<TreeviewSelect>>", on_info_select)



    frame_desc = ttk.Frame(notebook)
    notebook.add(frame_desc, text="Describe")

    desc_df = df.describe(include='all').fillna("")

    columnas = ["Estadística"] + list(desc_df.columns)
    tree_desc = ttk.Treeview(frame_desc, columns=columnas, show="headings")
    tree_desc.pack(expand=True, fill='both')

    for col in columnas:
        tree_desc.heading(col, text=col)
        tree_desc.column(col, anchor='center', width=100)

    for idx, row in desc_df.iterrows():
        tree_desc.insert("", "end", values=[idx] + list(row))

    scroll_desc = ttk.Scrollbar(frame_desc, orient="vertical", command=tree_desc.yview)
    scroll_desc.pack(side="right", fill="y")
    tree_desc.configure(yscrollcommand=scroll_desc.set)

    app.status.config(text="Mostrando información y estadísticas del DataFrame")

def mostrar_detalle_categorica(df, columna):
    top = tk.Toplevel()
    top.title(f"Detalle variable categórica: {columna}")
    top.geometry("400x300")

    series = df[columna].astype(str)

    conteo = series.value_counts()
    porcentaje = series.value_counts(normalize=True).mul(100).round(2)


    detalle_df = pd.DataFrame({
        'Categoría': conteo.index,
        'Frecuencia': conteo.values,
        'Porcentaje (%)': porcentaje.values
    })

    tree = ttk.Treeview(top, columns=list(detalle_df.columns), show="headings")
    tree.pack(expand=True, fill='both')

    for col in detalle_df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=120)

    for _, row in detalle_df.iterrows():
        tree.insert("", "end", values=list(row))

    scroll = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
    scroll.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scroll.set)
