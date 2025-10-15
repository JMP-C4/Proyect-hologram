import cv2
import mouse  # mucho más rápido que pyautogui
import pyautogui  # solo para obtener el tamaño de pantalla
from utils.hand_tracking import suavizar_landmark

screen_width, screen_height = pyautogui.size()

def mover_cursor_por_gesto(frame, hand_landmarks):
    """Mueve el cursor rápidamente según la posición del dedo índice."""
    mean_x, mean_y = suavizar_landmark(hand_landmarks)
    height, width, _ = frame.shape

    x = int(mean_x * width)
    y = int(mean_y * height)

    screen_x = int((x / width) * screen_width)
    screen_y = int((y / height) * screen_height)

    # movimiento directo, sin suavizado de pyautogui
    mouse.move(screen_x, screen_y, absolute=True, duration=0)

    # punto de referencia visual
    cv2.circle(frame, (x, y), 10, (255, 0, 255), cv2.FILLED)
