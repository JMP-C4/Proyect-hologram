import cv2

def draw_pointer(frame, hand_landmarks):
    """Dibuja un círculo en la punta del dedo índice para actuar como puntero."""
    if hand_landmarks:
        # Landmark 8 es la punta del dedo índice
        index_tip = hand_landmarks.landmark[8]
        h, w, c = frame.shape
        x, y = int(index_tip.x * w), int(index_tip.y * h)
        # Dibuja un círculo magenta como puntero
        cv2.circle(frame, (x, y), 10, (255, 0, 255), cv2.FILLED)
