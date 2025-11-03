"""
Controlador de eventos de click del mouse.
"""
import time
import pyautogui


class ClickController:
    """Gestiona los diferentes tipos de clicks del mouse."""
    
    DOUBLE_CLICK_THRESHOLD = 0.3  # Segundos para detectar doble click
    
    def __init__(self):
        """Inicializa el controlador de clicks."""
        self.last_click_time = 0.0
        self.click_count = 0
        
        # Configuración de pyautogui
        pyautogui.PAUSE = 0.01
        pyautogui.FAILSAFE = True
    
    def left_click(self):
        """Realiza un click izquierdo simple."""
        try:
            pyautogui.click()
            self.click_count += 1
        except Exception as e:
            print(f"❌ Error en left_click: {e}")
    
    def right_click(self):
        """Realiza un click derecho."""
        try:
            pyautogui.rightClick()
        except Exception as e:
            print(f"❌ Error en right_click: {e}")
    
    def double_click(self):
        """Realiza un doble click si se detecta rapidez."""
        current_time = time.time()
        time_since_last = current_time - self.last_click_time
        
        if time_since_last < self.DOUBLE_CLICK_THRESHOLD:
            try:
                pyautogui.doubleClick()
                print("🖱️ Doble click")
            except Exception as e:
                print(f"❌ Error en double_click: {e}")
        
        self.last_click_time = current_time


# Mantener funciones legacy para compatibilidad
_controller = ClickController()

def click_izquierdo():
    """Realiza un click izquierdo simple (función legacy)."""
    _controller.left_click()

def click_derecho():
    """Realiza un click derecho (función legacy)."""
    _controller.right_click()

def doble_click():
    """Realiza un doble click (función legacy)."""
    _controller.double_click()