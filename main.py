import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from modulo1 import cargar_limpiar_datos


class AdminPanelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧠 Sistema de Tasación de Viviendas")
        self.geometry("1000x600")
        self.minsize(900, 500)
        self.configure(bg="#e9ecef")

        self.datos_procesados = None  # Variable para guardar los datos procesados

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Sidebar.TFrame", background="#212529")

        style.configure(
            "Sidebar.TButton",
            background="#343a40",
            foreground="#f8f9fa",
            font=("Segoe UI", 10),
            padding=(12, 8),
            relief="flat",
            borderwidth=1,
            focusthickness=3,
            focuscolor="#adb5bd",
        )

        style.map(
            "Sidebar.TButton",
            background=[("active", "#495057")],
            relief=[("pressed", "sunken")],
        )

        style.configure("Content.TFrame", background="#ffffff")
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background="#ffffff")
        style.configure("Status.TLabel", font=("Segoe UI", 10), foreground="gray", background="#ffffff")

    def create_widgets(self):
        sidebar = ttk.Frame(self, width=250, style="Sidebar.TFrame")
        sidebar.pack(side="left", fill="y")



# ======= BOTONES ======
        ttk.Label(
            sidebar,
            text="   📊  Panel de control",
            foreground="#ffffff",
            background="#212529",
            font=("Segoe UI", 12, "bold"),
        ).pack(pady=(20, 10), anchor="w", padx=10)


 # ======= Carga y limpieza ======
        self.load_button = ttk.Button(
            sidebar,
            text="📂 Carga y limpieza de datos",
            style="Sidebar.TButton",
            command=self.load_file
        )
        self.load_button.pack(fill="x", padx=15, pady=5, anchor="w")


# ======= Análisis y visualización ======
        self.analisis_button = ttk.Button(
            sidebar,
            text="📈 Análisis exploratorio",
            style="Sidebar.TButton",
            command=self.show_dummy_text
        )
        self.analisis_button.pack(fill="x", padx=15, pady=5, anchor="w")


# ======= Entrenamiento ======
        self.entrenar_button = ttk.Button(
            sidebar,
            text="🤖 Entrenar modelo",
            style="Sidebar.TButton",
            command=self.show_dummy_text
        )
        self.entrenar_button.pack(fill="x", padx=15, pady=5, anchor="w")

# ======= Seleccion ======

        self.seleccion_button = ttk.Button(
            sidebar,
            text="🎯 Selección de características",
            style="Sidebar.TButton",
            command=self.show_dummy_text
        )
        self.seleccion_button.pack(fill="x", padx=15, pady=5, anchor="w")



# ======= Visualizacion ======

        self.visualizacion_button = ttk.Button(
            sidebar,
            text="📊 Visualización de resultados",
            style="Sidebar.TButton",
            command=self.show_dummy_text
        )
        self.visualizacion_button.pack(fill="x", padx=15, pady=5, anchor="w")

# ======= Cargar Nuevo archivo ======

        self.cargar_nuevo_button = ttk.Button(
            sidebar,
            text="🗂️ Cargar nuevo archivo",
            style="Sidebar.TButton",
            command=self.load_file
        )
        self.cargar_nuevo_button.pack(fill="x", padx=15, pady=5, anchor="w")


# ====================================================


        self.content_container = ttk.Frame(self, style="Content.TFrame")
        self.content_container.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        self.status = ttk.Label(
            self.content_container,
            text="Estado: Esperando acción del usuario...",
            style="Status.TLabel",
        )
        self.status.pack(side="top", anchor="w", pady=(0, 10))

        self.content = ttk.Frame(self.content_container, style="Content.TFrame")
        self.content.pack(expand=True, fill="both")
        self.show_text("Bienvenido al sistema de tasación de viviendas")

        

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_text(self, texto):
        self.clear_content()
        label = ttk.Label(self.content, text=texto, style="Header.TLabel", wraplength=800, justify="center")
        label.pack(expand=True, pady=40)

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

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xls *.xlsx")])
        if filepath:
            try:
                self.datos_procesados = cargar_limpiar_datos(filepath)
                self.status.config(text=f"Archivo cargado y procesado: {filepath.split('/')[-1]} mostrando 100 filas.")
                self.show_table(self.datos_procesados.head(100))

                self.load_button.config(text="👁️ Ver archivo", command=self.show_loaded_file)

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar el archivo:\n{e}")
                self.status.config(text="Error al procesar archivo.")

    def show_loaded_file(self):
        if self.datos_procesados is not None:
            self.show_table(self.datos_procesados.head(100))
            self.status.config(text="Mostrando datos cargados.")
        else:
            self.status.config(text="No hay datos cargados para mostrar.")

    def show_dummy_text(self):
        self.show_text("Este módulo aún está en desarrollo.")
        self.status.config(text="Estado: módulo en desarrollo.")


if __name__ == "__main__":
    app = AdminPanelApp()
    app.mainloop()
