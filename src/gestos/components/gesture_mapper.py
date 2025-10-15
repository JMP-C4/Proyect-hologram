import numpy as np

class GestureMapper:
    def __init__(self):
        # Índices de los landmarks de las puntas de los dedos
        self.tip_ids = [4, 8, 12, 16, 20]

    def detect_gesture(self, hand_landmarks):
        if not hand_landmarks:
            return None

        landmarks = hand_landmarks.landmark

        # --- Contar dedos levantados ---
        fingers_up = []
        # Pulgar (eje X)
        if landmarks[self.tip_ids[0]].x < landmarks[self.tip_ids[0] - 1].x:
            fingers_up.append(1)
        else:
            fingers_up.append(0)
        
        # Otros 4 dedos (eje Y)
        for i in range(1, 5):
            if landmarks[self.tip_ids[i]].y < landmarks[self.tip_ids[i] - 2].y:
                fingers_up.append(1)
            else:
                fingers_up.append(0)

        total_fingers = fingers_up.count(1)

        # --- Detección de gesto de clic ---
        # Calcular distancia entre la punta del pulgar y el índice
        thumb_tip = np.array([landmarks[4].x, landmarks[4].y])
        index_tip = np.array([landmarks[8].x, landmarks[8].y])
        distance = np.linalg.norm(thumb_tip - index_tip)

        if distance < 0.05: # Umbral de distancia para el clic
            return "CLICK"

        # --- Mapeo de gestos basado en dedos levantados ---
        if total_fingers == 1 and fingers_up[1]:
            return "POINTING"
        if total_fingers == 5:
            return "OPEN_HAND"
        if total_fingers == 0:
            return "FIST"
        
        return None # Ningún gesto reconocido
