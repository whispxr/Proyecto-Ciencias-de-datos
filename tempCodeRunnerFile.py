        # Panel lateral
        sidebar = ttk.Frame(self, width=250, style="Sidebar.TFrame")
        sidebar.pack(side="left", fill="y")

        ttk.Label(
            sidebar,
            text="   📊  Panel de control",
            foreground="#ffffff",
            background="#212529",
            font=("Segoe UI", 12, "bold"),
        ).pack(pady=(20, 10), anchor="w", padx=10)

        buttons_info = [
            ("📂 Carga y limpieza de datos", self.load_file),
            ("📈 Análisis exploratorio", self.show_dummy_text),
            ("🤖 Entrenar modelo", self.show_dummy_text),
            ("🎯 Selección de características", self.show_dummy_text),
            ("📊 Visualización de resultados", self.show_dummy_text),
            ("🗂️ Cargar nuevo archivo", self.load_file),
        ]

        for text, command in buttons_info:
            ttk.Button(sidebar, text=text, style="Sidebar.TButton", command=command).pack(
                fill="x", padx=15, pady=5, anchor="w"
            )

        # Contenedor para estado + contenido
        self.content_container = ttk.Frame(self, style="Content.TFrame")
        self.content_container.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        # Etiqueta de estado arriba
        self.status = ttk.Label(
            self.content_container,
            text="Estado: Esperando acción del usuario...",
            style="Status.TLabel",
        )
        self.status.pack(side="top", anchor="w", pady=(0, 10))

        # Área de contenido central debajo del estado
        self.content = ttk.Frame(self.content_container, style="Content.TFrame")
        self.content.pack(expand=True, fill="both")

        # Mostrar texto de bienvenida inicialmente
        self.show_text("Bienvenido al sistema de tasación de viviendas")