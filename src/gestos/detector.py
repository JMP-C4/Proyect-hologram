# src/gestos/detector.py

import cv2
import mediapipe as mp
import time
from src.network.client import EventClient

# --- Clases para detección de gestos ---

class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_con=0.8, track_con=0.8):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0):
        self.lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
        return self.lm_list

    def fingers_up(self):
        fingers = []
        # Pulgar (eje x)
        if self.lm_list[self.tip_ids[0]][1] > self.lm_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # Otros 4 dedos (eje y)
        for id in range(1, 5):
            if self.lm_list[self.tip_ids[id]][2] < self.lm_list[self.tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

# --- Aplicación principal de gestos ---

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    event_client = EventClient("Gestos")
    event_client.connect()

    last_gesture = None
    last_gesture_time = 0
    cooldown = 1.0  # 1 segundo de cooldown

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.find_hands(img)
        lm_list = detector.find_position(img)

        current_gesture = None

        if len(lm_list) != 0:
            fingers = detector.fingers_up()
            
            # Gesto: Puño cerrado (ningún dedo levantado)
            if fingers == [0, 0, 0, 0, 0]:
                current_gesture = "fist"
            # Gesto: Mano abierta (todos los dedos levantados)
            elif fingers == [1, 1, 1, 1, 1]:
                current_gesture = "open_hand"
            # Gesto: Apuntar (índice levantado)
            elif fingers == [0, 1, 0, 0, 0]:
                current_gesture = "point"

        # Enviar evento solo si el gesto cambia y ha pasado el cooldown
        if current_gesture and (current_gesture != last_gesture or time.time() - last_gesture_time > cooldown):
            event_client.send_event("gesture_detected", {"gesture": current_gesture})
            print(f"Gesto enviado: {current_gesture}")
            last_gesture = current_gesture
            last_gesture_time = time.time()

        cv2.imshow("Detector de Gestos", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    event_client.close()

if __name__ == "__main__":
    main()
