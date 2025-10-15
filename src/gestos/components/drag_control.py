import pyautogui

en_arrastre = False

def iniciar_arrastre():
    """Mantiene el click izquierdo presionado."""
    global en_arrastre
    if not en_arrastre:
        pyautogui.mouseDown()
        en_arrastre = True

def soltar_arrastre():
    """Suelta el click izquierdo."""
    global en_arrastre
    if en_arrastre:
        pyautogui.mouseUp()
        en_arrastre = False
