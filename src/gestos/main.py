"""
Punto de entrada principal de la aplicación de Control por Gestos.

Uso:
    python -m src.gestos.main
"""
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

def main():
    """Inicializa y ejecuta la aplicación."""
    print("=" * 60)
    print("🚀 Iniciando Sistema de Control por Gestos v0.3")
    print("=" * 60)
    
    try:
        # Crear aplicación Qt
        app = QApplication(sys.argv)
        app.setApplicationName("Control por Gestos")
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        
        # Importar después de crear QApplication
        from src.gestos.gesture_app import GestureApp
        
        # Crear ventana principal
        window = GestureApp()
        window.show()
        
        print("✅ Aplicación iniciada correctamente")
        print("💡 Presiona Ctrl+C en la terminal o cierra la ventana para salir")
        print("-" * 60)
        
        # Ejecutar loop de eventos
        exit_code = app.exec()
        
        print("=" * 60)
        print(f"👋 Aplicación cerrada (código: {exit_code})")
        print("=" * 60)
        
        return exit_code
        
    except ImportError as e:
        print(f"❌ ERROR: Falta una dependencia: {e}")
        print("💡 Solución: pip install -r requirements.txt")
        
        QMessageBox.critical(
            None,
            "Error de Dependencias",
            f"Falta una dependencia requerida:\n{e}\n\n"
            f"Ejecuta: pip install -r requirements.txt"
        )
        return 1
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        
        QMessageBox.critical(
            None,
            "Error Crítico",
            f"La aplicación no pudo iniciarse:\n{e}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())