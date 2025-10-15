import tkinter as tk
from PIL import Image, ImageTk
import cv2
import pyautogui
from .components.hand_tracking import HandTracker
from .components.ui_components import ControlPanel, LegendPanel
from .components.gesture_mapper import GestureMapper
from .utils.cursor_utils import CursorControl, perform_click

class GestureApp:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.cap = cv2.VideoCapture(self.video_source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.hand_tracker = HandTracker()
        self.gesture_mapper = GestureMapper()
        screen_w, screen_h = pyautogui.size()
        self.cursor_control = CursorControl(screen_w, screen_h, 640, 480)

        self.detection_active = False

        # Main frame
        main_frame = tk.Frame(window)
        main_frame.pack(fill='both', expand=True)

        # Video Canvas
        self.canvas = tk.Canvas(main_frame, width=640, height=480)
        self.canvas.pack(side='left', fill='both', expand=True)

        # Right Panel (Controls + Legend)
        right_panel = tk.Frame(main_frame)
        right_panel.pack(side='right', fill='y', padx=10, pady=10)

        self.control_panel = ControlPanel(right_panel, app_controller=self)
        self.control_panel.pack(side='top', fill='x')

        self.legend_panel = LegendPanel(right_panel)
        self.legend_panel.pack(side='bottom', fill='both', expand=True)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update()
        self.window.mainloop()

    def toggle_detection(self):
        self.detection_active = not self.detection_active
        state_text = "Detener Detección" if self.detection_active else "Iniciar Detección"
        self.control_panel.btn_toggle_detection.config(text=state_text)

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            if self.detection_active:
                frame, results = self.hand_tracker.process_frame(frame)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        gesture = self.gesture_mapper.detect_gesture(hand_landmarks)

                        # Conectar gestos a acciones
                        if gesture == "POINTING":
                            self.cursor_control.move_cursor(hand_landmarks)
                            draw_pointer(frame, hand_landmarks)
                        elif gesture == "CLICK":
                            perform_click()
                            # Podríamos añadir un feedback visual para el clic aquí
                        elif gesture:
                            # Imprime otros gestos para futura implementación
                            print(f"Gesto reconocido: {gesture}")

            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        self.window.after(10, self.update)

    def on_closing(self):
        self.cap.release()
        self.window.destroy()

if __name__ == "__main__":
    GestureApp(tk.Tk(), "Control de Gestos Holográficos")
