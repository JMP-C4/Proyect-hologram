import cv2

def mostrar_frame(frame, ventana="Control de Cursor - Gestos"):
    """Muestra la ventana con el frame actual."""
    cv2.imshow(ventana, frame)

def tecla_presionada():
    """Retorna la tecla presionada, o None si no hay."""
    key = cv2.waitKey(1) & 0xFF
    return key
