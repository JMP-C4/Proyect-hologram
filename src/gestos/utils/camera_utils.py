import cv2

def inicializar_camara(width=640, height=480):
    """Inicializa la cámara con la resolución deseada."""
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    if not cap.isOpened():
        raise IOError("No se pudo acceder a la cámara.")
    return cap
