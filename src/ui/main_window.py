# src/ui/main_window.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control del Holograma")

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta de estado
        self.status_label = QLabel("Estado: Desconectado")
        layout.addWidget(self.status_label)

        # Botón de ejemplo
        self.test_button = QPushButton("Enviar Evento de Prueba")
        layout.addWidget(self.test_button)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
