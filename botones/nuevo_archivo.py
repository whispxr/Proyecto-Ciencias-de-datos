from tkinter import ttk
from botones.carga import load_file


def crear_boton_nuevo_archivo(app, sidebar):
    boton = ttk.Button(
        sidebar,
        text="🗂️ Cargar nuevo archivo",
        style="Sidebar.TButton",
        command=lambda: load_file(app)
    )
    boton.pack(fill="x", padx=15, pady=5)
    app.cargar_nuevo_button = boton


#Si se carga un nuevo archivo se vuelve a ocupar la funcion de load que esta en carga.py
