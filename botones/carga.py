from tkinter import ttk, filedialog, messagebox
from botones.limpieza_carga import cargar_limpiar_datos
from normalizacion import normalizar_datos

def crear_boton_carga(app, sidebar):
    boton = ttk.Button(
        sidebar,
        text="📂 Carga y limpieza de datos",
        style="Sidebar.TButton",
        command=lambda: load_file(app)
    )
    boton.pack(fill="x", padx=15, pady=5)
    app.sidebar_button = boton


def load_file(app):
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xls *.xlsx")])
    if filepath:
        try:
            import pandas as pd

            # Leer datos originales sin limpiar
            if filepath.endswith('.csv'):
                app.datos_originales = pd.read_csv(filepath)
            else:
                app.datos_originales = pd.read_excel(filepath)

            # Cargar datos procesados limpios y mensaje de limpieza
            df_limpio, mensaje = cargar_limpiar_datos(filepath)
            app.datos_procesados = df_limpio
            app.log_limpieza = mensaje  # Guardar mensaje para mostrar luego

            # Normalizar datos
            app.datos_normalizados = normalizar_datos(app.datos_procesados)

            app.status.config(text=f"Archivo cargado: {filepath.split('/')[-1]}")
            show_loaded_file(app)

            app.sidebar_button.config(text="👁️ Ver archivos", command=lambda: show_loaded_file(app))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo:\n{e}")
            app.status.config(text="Error al procesar archivo.")


def show_loaded_file(app):
    if app.datos_originales is not None and app.datos_procesados is not None:
        app.show_data_tabs()
        app.status.config(text=app.log_limpieza)  # Mostrar mensaje de limpieza
    else:
        app.status.config(text="No hay datos cargados para mostrar.")
