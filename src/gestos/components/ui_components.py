import tkinter as tk

class ControlPanel(tk.Frame):
    def __init__(self, parent, app_controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app_controller = app_controller
        self.configure(padx=10, pady=10)

        self.btn_toggle_detection = tk.Button(self, text="Iniciar Detección", command=self.app_controller.toggle_detection)
        self.btn_toggle_detection.pack(fill='x', pady=5)

        self.btn_calibrate = tk.Button(self, text="Calibrar")
        self.btn_calibrate.pack(fill='x', pady=5)

        self.btn_action1 = tk.Button(self, text="Acción 1")
        self.btn_action1.pack(fill='x', pady=5)

        self.btn_action2 = tk.Button(self, text="Acción 2")
        self.btn_action2.pack(fill='x', pady=5)

        self.btn_additional1 = tk.Button(self, text="Adicional 1")
        self.btn_additional1.pack(fill='x', pady=5)

        self.btn_additional2 = tk.Button(self, text="Adicional 2")
        self.btn_additional2.pack(fill='x', pady=5)

        self.btn_exit = tk.Button(self, text="Salir", command=self.app_controller.on_closing)
        self.btn_exit.pack(fill='x', pady=10)

class LegendPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(padx=10, pady=10)

        legend_text = (
            "--- Leyenda de Gestos ---" 
            "- Gesto 1: [Acción]\n"
            "- Gesto 2: [Acción]\n"
            "- Gesto 3: [Acción]\n"
            "- Gesto 4: [Acción]\n"
            "- Gesto 5: [Acción]\n"
        )

        self.lbl_legend = tk.Label(self, text=legend_text, justify='left', anchor='w')
        self.lbl_legend.pack(fill='both', expand=True)
