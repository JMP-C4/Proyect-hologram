"""
Aplicación principal de control por gestos con interfaz PySide6.
"""
import cv2
from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, Qt

# IMPORTS ABSOLUTOS CORREGIDOS
from src.gestos.components.ui_components import ControlPanel, LegendPanel
from src.gestos.components.hand_tracking import HandTracker
from src.gestos.components.gesture_mapper import GestureMapper
from src.gestos.utils.camera_utils import inicializar_camara


class GestureApp(QWidget):
    """Ventana principal de la aplicación de control por gestos."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Gestos Holográficos v0.3")
        self.resize(1200, 700)
        
        # --- Estado ---
        self.detection_active = False
        self.last_gesture = None
        
        # --- Inicializar componentes ---
        try:
            self._init_camera()
            self._init_detection_components()
            self._init_ui()
            self._load_stylesheet()
            self._setup_timer()
            print("✅ GestureApp inicializada correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar GestureApp: {e}")
            raise
    
    def _init_camera(self):
        """Inicializa la cámara."""
        try:
            self.cap = inicializar_camara(width=640, height=480)
            print("✅ Cámara inicializada")
        except IOError as e:
            print(f"❌ Error de cámara: {e}")
            raise
    
    def _init_detection_components(self):
        """Inicializa los componentes de detección de gestos."""
        try:
            self.hand_tracker = HandTracker(
                mode=False,
                max_hands=1,
                detection_con=0.7,
                track_con=0.7
            )
            self.gesture_mapper = GestureMapper()
            print("✅ Componentes de detección inicializados")
        except Exception as e:
            print(f"⚠️ Advertencia al inicializar detección: {e}")
            self.hand_tracker = None
            self.gesture_mapper = None
    
    def _init_ui(self):
        """Inicializa la interfaz de usuario."""
        # Label para video
        self.video_label = QLabel("Iniciando cámara...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setFixedSize(640, 480)
        self.video_label.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                border: 2px solid #3498db;
                border-radius: 10px;
            }
        """)
        
        # Label de estado
        self.status_label = QLabel("Estado: Listo")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #95a5a6;
                color: #ecf0f1;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        
        # Paneles
        self.control_panel = ControlPanel(self)
        self.legend_panel = LegendPanel()
        
        # Layout principal
        main_layout = QHBoxLayout(self)
        
        # Layout izquierdo (video)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.video_label, 1)
        left_layout.addWidget(self.status_label)
        
        # Layout derecho (controles)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.control_panel)
        right_layout.addWidget(self.legend_panel)
        right_layout.addStretch()
        
        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 1)
        
        self.setLayout(main_layout)
    
    def _load_stylesheet(self):
        """Carga la hoja de estilos CSS."""
        try:
            # Usar pathlib para rutas relativas seguras
            css_path = Path(__file__).parent / "css" / "main.qss"
            
            if css_path.exists():
                with open(css_path, 'r', encoding='utf-8') as f:
                    self.setStyleSheet(f.read())
                print(f"✅ Estilos cargados desde: {css_path}")
            else:
                print(f"⚠️ No se encontró archivo CSS: {css_path}")
        except Exception as e:
            print(f"⚠️ Error al cargar estilos: {e}")
    
    def _setup_timer(self):
        """Configura el temporizador para actualizar frames."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # ~30 FPS
    
    def toggle_detection(self):
        """Activa o desactiva la detección de gestos."""
        self.detection_active = not self.detection_active
        self.control_panel.update_detection_button(self.detection_active)
        
        status = "Activa ✅" if self.detection_active else "Inactiva"
        self.status_label.setText(f"Detección: {status}")
        
        # Cambiar color del indicador
        color = "#27ae60" if self.detection_active else "#95a5a6"
        self.status_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: #ecf0f1;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }}
        """)
        
        print(f"🎮 Detección: {status}")
    
    def update_frame(self):
        """Actualiza el frame de la cámara y procesa gestos."""
        if not self.cap or not self.cap.isOpened():
            self.video_label.setText("❌ Cámara no disponible")
            return
        
        ret, frame = self.cap.read()
        if not ret:
            self.video_label.setText("❌ Error al leer frame")
            return
        
        # Voltear para efecto espejo
        frame = cv2.flip(frame, 1)
        
        # Procesar detección si está activa
        if self.detection_active and self.hand_tracker and self.gesture_mapper:
            try:
                # Procesar con HandTracker
                frame, results = self.hand_tracker.process_frame(frame)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Detectar gesto
                        gesture = self.gesture_mapper.detect_gesture(hand_landmarks)
                        
                        if gesture and gesture != self.last_gesture:
                            # Mostrar gesto detectado
                            print(f"✋ Gesto detectado: {gesture}")
                            self.last_gesture = gesture
                            
                            # Mostrar en pantalla
                            cv2.putText(
                                frame,
                                f"Gesto: {gesture}",
                                (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.2,
                                (0, 255, 0),
                                3
                            )
                            
                            # Aquí podrías agregar acciones:
                            # if gesture == "CLICK":
                            #     from src.gestos.components.click_control import click_izquierdo
                            #     click_izquierdo()
                
            except Exception as e:
                print(f"⚠️ Error en detección: {e}")
        
        # Indicador visual de estado
        status_color = (0, 255, 0) if self.detection_active else (128, 128, 128)
        cv2.circle(frame, (frame.shape[1] - 30, 30), 15, status_color, -1)
        
        # Convertir a QImage y mostrar
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        self.video_label.setPixmap(
            QPixmap.fromImage(q_img).scaled(
                self.video_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
    
    def on_closing(self):
        """Maneja el cierre de la aplicación."""
        print("🔴 Cerrando aplicación...")
        
        # Detener temporizador
        if hasattr(self, 'timer'):
            self.timer.stop()
        
        # Liberar cámara
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
            print("✅ Cámara liberada")
        
        # Limpiar OpenCV
        cv2.destroyAllWindows()
        
        # Cerrar ventana
        self.close()
    
    def closeEvent(self, event):
        """Maneja el evento de cierre de ventana."""
        self.on_closing()
        event.accept()