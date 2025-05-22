from tkinter import ttk, filedialog, messagebox
from botones.limpieza_carga import cargar_limpiar_datos


def crear_boton_carga(app, sidebar):
    boton = ttk.Button(
        sidebar,
        text="📂 Carga y limpieza de datos",
        style="Sidebar.TButton",
        command=lambda: load_file(app)
    )
    boton.pack(fill="x", padx=15, pady=5)
    app.sidebar_button = boton



#Principal Funcion de carga, cambia el boton de Cargar a visualizar como tabla para evitar cargar el mismo archivo
def load_file(app):
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xls *.xlsx")])
    if filepath:
        try:
            app.datos_procesados = cargar_limpiar_datos(filepath)
            app.status.config(text=f"Archivo cargado y procesado: {filepath.split('/')[-1]} mostrando 100 filas.")
            show_loaded_file(app)
            
            app.sidebar_button.config(text="👁️ Ver archivo", command=lambda: show_loaded_file(app))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo:\n{e}")
            app.status.config(text="Error al procesar archivo.")




def show_loaded_file(app):
    if app.datos_procesados is not None:
        app.show_table(app.datos_procesados.head(100))
        app.status.config(text="Mostrando datos cargados.")
    else:
        app.status.config(text="No hay datos cargados para mostrar.")
