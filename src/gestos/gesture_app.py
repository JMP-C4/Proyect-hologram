import cv2
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, Qt, QFile, QTextStream
from .components.ui_components import ControlPanel, LegendPanel
from .utils.camera_utils import inicializar_camara


class GestureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Gestos Holográficos")
        self.resize(1000, 600)

        # --- Cargar estilos QSS ---
        self.load_stylesheet("src/gestos/css/main.qss")
        # --- Estado ---
        self.detection_active = False

        # --- Cámara ---
        self.cap = inicializar_camara()

        # --- Elementos UI ---
        self.video_label = QLabel("Iniciando cámara...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setFixedSize(640, 480)

        self.control_panel = ControlPanel(self)
        self.legend_panel = LegendPanel()

        # --- Layouts ---
        main_layout = QHBoxLayout(self)
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.control_panel)
        right_panel.addWidget(self.legend_panel)

        main_layout.addWidget(self.video_label, 3)
        main_layout.addLayout(right_panel, 1)
        self.setLayout(main_layout)

        # --- Temporizador de actualización ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    # -------------------
    #  Métodos principales
    # -------------------

    def load_stylesheet(self, path: str):
        """Carga un archivo QSS para aplicar estilo global a la interfaz."""
        file = QFile(path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()
        else:
            print(f"[ADVERTENCIA] No se pudo cargar la hoja de estilos: {path}")

    def toggle_detection(self):
        """Activa o desactiva la detección."""
        self.detection_active = not self.detection_active
        self.control_panel.update_detection_button(self.detection_active)

    def update_frame(self):
        """Actualiza el frame de la cámara."""
        ret, frame = self.cap.read()
        if not ret:
            self.video_label.setText("Error al leer la cámara.")
            return

        frame = cv2.flip(frame, 1)

        if self.detection_active:
            # Aquí se integraría el HandTracker y el GestureMapper
            pass

        # Mostrar el frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def on_closing(self):
        """Cierra la aplicación correctamente."""
        self.cap.release()
        self.close()
