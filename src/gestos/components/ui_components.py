from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt


class ControlPanel(QWidget):
    def __init__(self, app_controller):
        super().__init__()
        self.app_controller = app_controller

        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.btn_toggle_detection = QPushButton("Iniciar Detección")
        self.btn_toggle_detection.clicked.connect(self.app_controller.toggle_detection)
        layout.addWidget(self.btn_toggle_detection)

        self.btn_calibrate = QPushButton("Calibrar")
        layout.addWidget(self.btn_calibrate)

        self.btn_action1 = QPushButton("Acción 1")
        layout.addWidget(self.btn_action1)

        self.btn_action2 = QPushButton("Acción 2")
        layout.addWidget(self.btn_action2)

        self.btn_additional1 = QPushButton("Adicional 1")
        layout.addWidget(self.btn_additional1)

        self.btn_additional2 = QPushButton("Adicional 2")
        layout.addWidget(self.btn_additional2)

        layout.addStretch()

        self.btn_exit = QPushButton("Salir")
        self.btn_exit.clicked.connect(self.app_controller.on_closing)
        layout.addWidget(self.btn_exit)

        self.setLayout(layout)

    def update_detection_button(self, is_active: bool):
        self.btn_toggle_detection.setText("Detener Detección" if is_active else "Iniciar Detección")


class LegendPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        layout = QVBoxLayout()

        legend_text = (
            "--- Leyenda de Gestos ---\n"
            "- Gesto 1: [Acción]\n"
            "- Gesto 2: [Acción]\n"
            "- Gesto 3: [Acción]\n"
            "- Gesto 4: [Acción]\n"
            "- Gesto 5: [Acción]\n"
        )

        self.lbl_legend = QLabel(legend_text)
        self.lbl_legend.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.lbl_legend)

        self.setLayout(layout)
