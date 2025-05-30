import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import seaborn as sns

def crear_boton_analisis(app, sidebar):
    boton = ttk.Button(
        sidebar,
        text="📈 Análisis exploratorio",
        style="Sidebar.TButton",
        command=lambda: mostrar_analisis_exploratorio(app)
    )
    boton.pack(fill="x", padx=15, pady=5)

def mostrar_analisis_exploratorio(app):
    if app.datos_procesados is None or app.datos_procesados.empty:
        app.status.config(text="No hay datos procesados para analizar.")
        app.show_text("Primero cargá y limpá un archivo con datos.")
        return

    df = app.datos_normalizacod.copy()

    # Quitar ID si existe
    if "ID" in df.columns:
        df = df.drop(columns=["ID"])

    app.clear_content()

    notebook = ttk.Notebook(app.content)
    notebook.pack(expand=True, fill='both')

    ####### PESTAÑA 1: Métricas para variable seleccionada #########
    frame_metricas = ttk.Frame(notebook)
    notebook.add(frame_metricas, text="Métricas")

    label_var_metricas = ttk.Label(frame_metricas, text="Seleccioná variable para métricas:")
    label_var_metricas.pack(pady=5)

    vars_numericas = df.select_dtypes(include=np.number).columns.tolist()

    combo_metricas = ttk.Combobox(frame_metricas, values=vars_numericas, state="readonly")
    combo_metricas.pack(pady=5)
    combo_metricas.current(0)

    tree_metricas = ttk.Treeview(frame_metricas, columns=("Métrica", "Valor"), show="headings", height=8)
    tree_metricas.heading("Métrica", text="Métrica")
    tree_metricas.heading("Valor", text="Valor")
    tree_metricas.column("Métrica", anchor="center", width=150)
    tree_metricas.column("Valor", anchor="center", width=150)
    tree_metricas.pack(expand=True, fill="both", padx=10, pady=10)

    def actualizar_metricas(event=None):
        var = combo_metricas.get()
        serie = df[var]

        metricas = {
            "Media": serie.mean(),
            "Mediana": serie.median(),
            "Desviación estándar": serie.std(),
            "Percentil 25": serie.quantile(0.25),
            "Percentil 50": serie.quantile(0.5),
            "Percentil 75": serie.quantile(0.75),
            "Máximo": serie.max(),
            "Mínimo": serie.min(),
        }

        for i in tree_metricas.get_children():
            tree_metricas.delete(i)
        for metrica, valor in metricas.items():
            tree_metricas.insert("", "end", values=(metrica, f"{valor:,.2f}"))

    combo_metricas.bind("<<ComboboxSelected>>", actualizar_metricas)
    actualizar_metricas()

    ####### PESTAÑA 2: Visualización múltiple con selección de gráfico #########
    frame_graficos = ttk.Frame(notebook)
    notebook.add(frame_graficos, text="Visualización múltiple")

    label_sel_vars = ttk.Label(frame_graficos, text="Seleccioná variables para graficar (Ctrl+click para seleccionar varias):")
    label_sel_vars.pack(pady=(10,5))

    # Para visualizar variables numéricas no discretas (ej: descartar variables con pocos valores únicos)
    vars_continuas = [v for v in vars_numericas if df[v].nunique() > 10]

    listbox_vars = tk.Listbox(frame_graficos, selectmode="extended", height=8)
    for v in vars_continuas:
        listbox_vars.insert("end", v)
    listbox_vars.pack(padx=10, pady=(0,10), fill="x")

    label_sel_tipo = ttk.Label(frame_graficos, text="Seleccioná tipo de gráfico para todas las variables:")
    label_sel_tipo.pack(pady=(5,5))

    tipos_grafico = ["Boxplot", "Histograma", "Dispersión"]
    combo_grafico = ttk.Combobox(frame_graficos, values=tipos_grafico, state="readonly")
    combo_grafico.pack(pady=(0,10))
    combo_grafico.current(0)

    var_todas = tk.IntVar()
    check_todas = ttk.Checkbutton(frame_graficos, text="Graficar todas las variables continuas juntas", variable=var_todas)
    check_todas.pack()

    btn_graficar = ttk.Button(frame_graficos, text="Graficar")
    btn_graficar.pack(pady=5)

    canvas_frame = ttk.Frame(frame_graficos)
    canvas_frame.pack(expand=True, fill="both")

    def graficar_variables():
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        if var_todas.get() == 1:
            # Graficar todas las variables juntas (sólo continuas)
            fig, ax = plt.subplots(figsize=(7, 5))
            tipo = combo_grafico.get()

            if tipo == "Boxplot":
                datos = [df[v].dropna() for v in vars_continuas]
                ax.boxplot(datos, labels=vars_continuas)
                ax.set_title("Boxplot de todas las variables continuas")
                ax.tick_params(axis='x', rotation=45)
            elif tipo == "Histograma":
                # Histogramas superpuestos con transparencia
                for v in vars_continuas:
                    ax.hist(df[v].dropna(), bins=30, alpha=0.5, label=v)
                ax.set_title("Histogramas de todas las variables continuas")
                ax.legend()
            elif tipo == "Dispersión":
                app.status.config(text="Gráfico de dispersión no soporta múltiples variables juntas.")
                return
            else:
                app.status.config(text="Tipo de gráfico no soportado.")
                return

            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(expand=True, fill="both")

            app.status.config(text=f"Gráfico de todas las variables juntas ({tipo})")
        else:
            # Graficar variables seleccionadas individualmente
            vars_sel = [listbox_vars.get(i) for i in listbox_vars.curselection()]
            if not vars_sel:
                app.status.config(text="Seleccioná al menos una variable o marcá 'Todas las variables juntas'.")
                return

            n = len(vars_sel)
            fig, axs = plt.subplots(n, 1, figsize=(6, 4*n), squeeze=False)
            tipo = combo_grafico.get()

            for i, var in enumerate(vars_sel):
                ax = axs[i, 0]
                data = df[var].dropna()

                if tipo == "Boxplot":
                    ax.boxplot(data, vert=False)
                    ax.set_title(f"Boxplot de {var}")
                elif tipo == "Histograma":
                    ax.hist(data, bins=30, color='skyblue', edgecolor='black')
                    ax.set_title(f"Histograma de {var}")
                elif tipo == "Dispersión":
                    # Para dispersión, graficamos var vs índice
                    ax.scatter(data.index, data, alpha=0.6)
                    ax.set_title(f"Dispersión de {var} vs índice")
                    ax.set_xlabel("Índice")
                    ax.set_ylabel(var)
                else:
                    ax.text(0.5, 0.5, "Tipo de gráfico no soportado", ha='center')

                ax.grid(True)

            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(expand=True, fill="both")

            app.status.config(text=f"Graficando {n} variable(s) con {tipo}")

    btn_graficar.config(command=graficar_variables)

    ####### PESTAÑA 3: Relación entre dos variables #########
    frame_relacion = ttk.Frame(notebook)
    notebook.add(frame_relacion, text="Relación entre variables")

    label_var_x = ttk.Label(frame_relacion, text="Seleccioná variable X:")
    label_var_x.pack(pady=(10,5))

    combo_var_x = ttk.Combobox(frame_relacion, values=vars_numericas, state="readonly")
    combo_var_x.pack(pady=5)
    combo_var_x.current(0)

    label_var_y = ttk.Label(frame_relacion, text="Seleccioná variable Y:")
    label_var_y.pack(pady=(10,5))

    combo_var_y = ttk.Combobox(frame_relacion, values=vars_numericas, state="readonly")
    combo_var_y.pack(pady=5)
    combo_var_y.current(1 if len(vars_numericas)>1 else 0)

    label_tipo_rel = ttk.Label(frame_relacion, text="Seleccioná tipo de gráfico:")
    label_tipo_rel.pack(pady=5)

    combo_tipo_rel = ttk.Combobox(frame_relacion, values=["Dispersión", "Boxplot (Y vs X discreta)", "Histograma (X)"], state="readonly")
    combo_tipo_rel.pack(pady=5)
    combo_tipo_rel.current(0)

    btn_graf_rel = ttk.Button(frame_relacion, text="Graficar")
    btn_graf_rel.pack(pady=10)

    canvas_rel = ttk.Frame(frame_relacion)
    canvas_rel.pack(expand=True, fill="both")

    def graficar_relacion():
        for widget in canvas_rel.winfo_children():
            widget.destroy()

        x = combo_var_x.get()
        y = combo_var_y.get()
        tipo = combo_tipo_rel.get()

        fig, ax = plt.subplots(figsize=(7,5))

        if tipo == "Dispersión":
            ax.scatter(df[x], df[y], alpha=0.6)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(f"Dispersión: {y} vs {x}")
            ax.grid(True)
        elif tipo == "Boxplot (Y vs X discreta)":
            # Solo tiene sentido si X es discreta
            if df[x].dtype not in [np.object_, 'category'] and df[x].nunique() > 20:
                app.status.config(text="Variable X no es discreta. Elegí otra opción.")
                return
            sns.boxplot(x=df[x], y=df[y], ax=ax)
            ax.set_title(f"Boxplot de {y} según {x}")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        elif tipo == "Histograma (X)":
            ax.hist(df[x], bins=30, color='orange', edgecolor='black')
            ax.set_title(f"Histograma de {x}")
            ax.set_xlabel(x)
            ax.set_ylabel("Frecuencia")
        else:
            ax.text(0.5, 0.5, "Tipo de gráfico no soportado", ha="center")

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=canvas_rel)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

        app.status.config(text=f"Gráfico de relación: {tipo}")

    btn_graf_rel.config(command=graficar_relacion)
