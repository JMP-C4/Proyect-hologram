import sys
from PySide6.QtWidgets import QApplication
from src.gestos.gesture_app import GestureApp


def main():
    app = QApplication(sys.argv)
    window = GestureApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
