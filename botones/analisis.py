from tkinter import ttk


def crear_boton_analisis(app, sidebar):
    boton = ttk.Button(
        sidebar,
        text="📈 Análisis exploratorio",
        style="Sidebar.TButton",
        command=lambda: app.show_text("Este módulo aún está en desarrollo.")
    )
    boton.pack(fill="x", padx=15, pady=5)
