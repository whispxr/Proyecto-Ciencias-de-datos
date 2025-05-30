import tkinter as tk
from tkinter import ttk

# Importar acciones desde cada módulo
from botones.carga import crear_boton_carga
from botones.nuevo_archivo import crear_boton_nuevo_archivo
from botones.analisis import crear_boton_analisis
from botones.entrenamiento import crear_boton_entrenamiento
from botones.seleccion import crear_boton_seleccion
from botones.visualizacion import crear_boton_visualizacion
from botones.info import crear_boton_info


class AdminPanelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧠 Sistema de Tasación de Viviendas")
        self.geometry("1000x600")
        self.configure(bg="#e9ecef")
        self.datos_originales = None
        self.datos_procesados = None
        self.datos_normalizados = None  

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
        crear_boton_info(self, sidebar)
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

    def show_data_tabs(self):
        self.clear_content()
        notebook = ttk.Notebook(self.content)
        notebook.pack(expand=True, fill="both")

        # Pestaña datos originales
        frame_original = ttk.Frame(notebook)
        notebook.add(frame_original, text="Datos Originales")

        # Pestaña datos limpios
        frame_limpios = ttk.Frame(notebook)
        notebook.add(frame_limpios, text="Datos Limpios")

        # Mostrar tabla en cada pestaña
        self.show_table(self.datos_originales, frame_original)
        self.show_table(self.datos_procesados, frame_limpios)


    def show_table(self, df, parent=None, max_rows=None):
        """
        Muestra el DataFrame en un Treeview.
        Si parent es None usa self.content.
        max_rows limita filas mostradas (None = sin límite).
        """

        if parent is None:
            parent = self.content

        # Limpiar contenido previo en ese frame (por si se reutiliza)
        for widget in parent.winfo_children():
            widget.destroy()

        tree_frame = ttk.Frame(parent)
        tree_frame.pack(expand=True, fill="both")

        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y")

        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        treeview = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        treeview.pack(expand=True, fill="both")

        tree_scroll_y.config(command=treeview.yview)
        tree_scroll_x.config(command=treeview.xview)

        treeview["columns"] = list(df.columns)
        treeview["show"] = "headings"

        for col in df.columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=120, anchor="center")

        filas = df.itertuples(index=False)
        count = 0
        for row in filas:
            if max_rows is not None and count >= max_rows:
                break
            treeview.insert("", "end", values=row)
            count += 1

        # Agregar botón para mostrar todas filas si hay límite
        if max_rows is not None and len(df) > max_rows:
            def mostrar_todas():
                self.show_table(df, parent, max_rows=None)

            btn_mostrar_todo = ttk.Button(parent, text=f"Mostrar todas las filas ({len(df)})", command=mostrar_todas)
            btn_mostrar_todo.pack(pady=5)
# ============================
