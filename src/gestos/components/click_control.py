import pyautogui
import time

ultimo_click = 0

def click_izquierdo():
    """Realiza un click izquierdo simple."""
    pyautogui.click()

def click_derecho():
    """Realiza un click derecho."""
    pyautogui.rightClick()

def doble_click():
    """Realiza un doble click."""
    global ultimo_click
    ahora = time.time()
    if ahora - ultimo_click < 0.3:
        pyautogui.doubleClick()
    ultimo_click = ahora
