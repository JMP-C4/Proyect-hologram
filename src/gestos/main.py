import tkinter as tk
from .gesture_app import GestureApp

def main():
    """Punto de entrada principal para la aplicación."""
    root = tk.Tk()
    app = GestureApp(root, "Control de Gestos Holográficos")

if __name__ == "__main__":
    main()