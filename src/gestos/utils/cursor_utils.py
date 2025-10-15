import pyautogui
import numpy as np

# Desactivar el fail-safe de pyautogui para evitar interrupciones
pyautogui.FAILSAFE = False

class CursorControl:
    def __init__(self, screen_width, screen_height, frame_width, frame_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.smoothening = 7 # Factor de suavizado
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = 0, 0

    def move_cursor(self, hand_landmarks):
        if not hand_landmarks:
            return

        # Coordenadas del dedo índice
        index_tip = hand_landmarks.landmark[8]
        x = int(index_tip.x * self.frame_width)
        y = int(index_tip.y * self.frame_height)

        # Mapear a la pantalla
        screen_x = np.interp(x, (0, self.frame_width), (0, self.screen_width))
        screen_y = np.interp(y, (0, self.frame_height), (0, self.screen_height))

        # Suavizar el movimiento
        self.curr_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        self.curr_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening

        # Mover el cursor
        pyautogui.moveTo(self.curr_x, self.curr_y)

        self.prev_x, self.prev_y = self.curr_x, self.curr_y

def perform_click():
    pyautogui.click()
