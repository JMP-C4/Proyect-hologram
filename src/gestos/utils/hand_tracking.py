import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# Configuración de MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Cola para suavizar movimientos (almacena últimas posiciones del índice)
posiciones = deque(maxlen=5)

def obtener_manos():
    """Inicializa el detector de manos de MediaPipe."""
    return mp_hands.Hands(
        model_complexity=1,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

def procesar_mano(frame, hands):
    """Procesa el frame con MediaPipe y devuelve los resultados."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return hands.process(rgb_frame)

def dibujar_manos(frame, hand_landmarks):
    """Dibuja las conexiones y puntos de la mano en la imagen."""
    mp_drawing.draw_landmarks(
        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

def suavizar_landmark(hand_landmarks):
    """Devuelve coordenadas del índice (landmark 8) suavizadas."""
    x = hand_landmarks.landmark[8].x
    y = hand_landmarks.landmark[8].y

    posiciones.append((x, y))
    arr = np.array(posiciones)
    mean_x, mean_y = np.mean(arr, axis=0)
    return mean_x, mean_y

