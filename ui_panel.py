import tkinter as tk
from tkinter import ttk

# Importar acciones desde cada módulo
from botones.carga import crear_boton_carga
from botones.nuevo_archivo import crear_boton_nuevo_archivo
from botones.analisis import crear_boton_analisis
from botones.entrenamiento import crear_boton_entrenamiento
from botones.seleccion import crear_boton_seleccion
from botones.visualizacion import crear_boton_visualizacion


class AdminPanelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧠 Sistema de Tasación de Viviendas")
        self.geometry("1000x600")
        self.configure(bg="#e9ecef")
        self.datos_procesados = None

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Sidebar.TFrame", background="#212529")
        style.configure("Sidebar.TButton", background="#343a40", foreground="#f8f9fa", font=("Segoe UI", 10), padding=(12, 8), relief="flat")
        style.map("Sidebar.TButton", background=[("active", "#495057")])
        style.configure("Content.TFrame", background="#ffffff")
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background="#ffffff")
        style.configure("Status.TLabel", font=("Segoe UI", 10), foreground="gray", background="#ffffff")

    def create_widgets(self):
        sidebar = ttk.Frame(self, width=250, style="Sidebar.TFrame")
        sidebar.pack(side="left", fill="y")

        ttk.Label(sidebar, text="   📊  Panel de control", foreground="#ffffff", background="#212529", font=("Segoe UI", 12, "bold")).pack(pady=(20, 10), anchor="w", padx=10)



#====== CARGAR BOTONES ======

        crear_boton_carga(self, sidebar)
        crear_boton_analisis(self, sidebar)
        crear_boton_entrenamiento(self, sidebar)
        crear_boton_seleccion(self, sidebar)
        crear_boton_visualizacion(self, sidebar)
        crear_boton_nuevo_archivo(self, sidebar)

# ============================

        self.content_container = ttk.Frame(self, style="Content.TFrame")
        self.content_container.pack(side="right", expand=True, fill="both", padx=20, pady=20)


        self.content = ttk.Frame(self.content_container, style="Content.TFrame")
        self.content.pack(expand=True, fill="both")
        self.show_text("Bienvenido al sistema de tasación de viviendas")

# Label de la accion que se esta realizando, se puede modificar con el uso de cada boton para que sea mas intuitiva :]
        self.status = ttk.Label(self.content_container, text="Estado: Esperando acción del usuario...", style="Status.TLabel")
        self.status.pack(side="top", anchor="w", pady=(0, 10))

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()


    def show_text(self, texto):
        self.clear_content()
        label = ttk.Label(self.content, text=texto, style="Header.TLabel", wraplength=800, justify="center")
        label.pack(expand=True, pady=40)

# ======= mostrar tabla =======

    def show_table(self, df):
        self.clear_content()
        tree_frame = ttk.Frame(self.content)
        tree_frame.pack(expand=True, fill="both")

        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")

        treeview = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        treeview.pack(expand=True, fill="both")
        tree_scroll.config(command=treeview.yview)

        treeview["columns"] = list(df.columns)
        treeview["show"] = "headings"

        for col in df.columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=100, anchor="center")

        for i, row in enumerate(df.itertuples(index=False)):
            if i >= 100:
                break
            treeview.insert("", "end", values=row)

# ============================
