"""
Controlador principal que conecta la detección de gestos con las acciones del sistema.
"""
import logging
import time
from typing import Optional, Dict, Any

from src.gestos.components.click_control import ClickController
from src.gestos.components.drag_control import DragController
from src.gestos.components.scroll_control import ScrollController
from src.gestos.utils.cursor_utils import CursorControl

logger = logging.getLogger(__name__)


class GestureController:
    """Controlador que mapea gestos detectados a acciones del sistema."""
    
    # Configuración de cooldown para evitar eventos repetidos
    COOLDOWN_SECONDS = 0.5
    
    def __init__(self):
        """Inicializa el controlador con todos los sistemas de control."""
        logger.info("Inicializando GestureController")
        
        # Controladores de acciones
        self.click_controller = ClickController()
        self.drag_controller = DragController()
        self.scroll_controller = ScrollController()
        
        # Control del cursor (se inicializa cuando se necesite)
        self.cursor_control: Optional[CursorControl] = None
        
        # Estado de gestos
        self.last_gesture: Optional[str] = None
        self.last_gesture_time: float = 0.0
        self.gesture_history: list = []
        
        # Mapeo de gestos a acciones
        self.gesture_actions = {
            'CLICK': self._handle_click,
            'POINTING': self._handle_pointing,
            'OPEN_HAND': self._handle_open_hand,
            'FIST': self._handle_fist,
        }
        
        logger.info(f"Gestos registrados: {list(self.gesture_actions.keys())}")
    
    def process_gesture(
        self,
        gesture: str,
        hand_landmarks: Any,
        frame_shape: Optional[tuple] = None
    ) -> None:
        """
        Procesa un gesto detectado y ejecuta la acción correspondiente.
        
        Args:
            gesture: Nombre del gesto detectado
            hand_landmarks: Landmarks de la mano detectada
            frame_shape: Dimensiones del frame (height, width, channels)
        """
        current_time = time.time()
        
        # Verificar cooldown para evitar acciones repetidas
        if self._is_in_cooldown(gesture, current_time):
            return
        
        # Ejecutar acción del gesto
        if gesture in self.gesture_actions:
            try:
                logger.info(f"Ejecutando acción para gesto: {gesture}")
                self.gesture_actions[gesture](hand_landmarks, frame_shape)
                
                # Actualizar historial
                self._update_gesture_history(gesture, current_time)
                
            except Exception as e:
                logger.error(f"Error al ejecutar acción de {gesture}: {e}")
        else:
            logger.warning(f"Gesto no reconocido: {gesture}")
    
    def _is_in_cooldown(self, gesture: str, current_time: float) -> bool:
        """Verifica si el gesto está en período de cooldown."""
        if gesture == self.last_gesture:
            time_since_last = current_time - self.last_gesture_time
            if time_since_last < self.COOLDOWN_SECONDS:
                return True
        return False
    
    def _update_gesture_history(self, gesture: str, timestamp: float) -> None:
        """Actualiza el historial de gestos."""
        self.last_gesture = gesture
        self.last_gesture_time = timestamp
        
        # Mantener solo los últimos 10 gestos
        self.gesture_history.append({
            'gesture': gesture,
            'timestamp': timestamp
        })
        if len(self.gesture_history) > 10:
            self.gesture_history.pop(0)
    
    # ===== Handlers de Gestos =====
    
    def _handle_click(self, hand_landmarks: Any, frame_shape: Optional[tuple]) -> None:
        """Maneja el gesto de click (pulgar e índice juntos)."""
        logger.info("🖱️ Click detectado")
        self.click_controller.left_click()
    
    def _handle_pointing(self, hand_landmarks: Any, frame_shape: Optional[tuple]) -> None:
        """Maneja el gesto de apuntar (mover cursor)."""
        if frame_shape is None:
            return
        
        # Inicializar cursor control si es necesario
        if self.cursor_control is None:
            import pyautogui
            screen_width, screen_height = pyautogui.size()
            h, w = frame_shape[0], frame_shape[1]
            self.cursor_control = CursorControl(
                screen_width, screen_height, w, h
            )
        
        # Mover cursor según posición del índice
        self.cursor_control.move_cursor(hand_landmarks)
        logger.debug("👆 Moviendo cursor")
    
    def _handle_open_hand(self, hand_landmarks: Any, frame_shape: Optional[tuple]) -> None:
        """Maneja el gesto de mano abierta (scroll up o detener drag)."""
        # Si estaba arrastrando, soltar
        if self.drag_controller.is_dragging():
            logger.info("🖐️ Soltando arrastre")
            self.drag_controller.release_drag()
        else:
            logger.info("⬆️ Scroll arriba")
            self.scroll_controller.scroll_up()
    
    def _handle_fist(self, hand_landmarks: Any, frame_shape: Optional[tuple]) -> None:
        """Maneja el gesto de puño (scroll down o iniciar drag)."""
        # Alternar entre scroll y drag según contexto
        if self.drag_controller.is_dragging():
            logger.info("⬇️ Scroll abajo (en drag)")
            self.scroll_controller.scroll_down()
        else:
            # Iniciar drag si el puño se mantiene
            logger.info("✊ Iniciando arrastre")
            self.drag_controller.start_drag()
    
    # ===== Utilidades =====
    
    def get_gesture_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas sobre los gestos detectados."""
        gesture_counts = {}
        for entry in self.gesture_history:
            gesture = entry['gesture']
            gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
        
        return {
            'total_gestures': len(self.gesture_history),
            'unique_gestures': len(gesture_counts),
            'gesture_counts': gesture_counts,
            'last_gesture': self.last_gesture,
            'history': self.gesture_history[-5:]  # Últimos 5
        }
    
    def reset(self) -> None:
        """Reinicia el estado del controlador."""
        logger.info("Reiniciando GestureController")
        self.last_gesture = None
        self.last_gesture_time = 0.0
        self.gesture_history.clear()
        
        # Asegurar que no quede drag activo
        if self.drag_controller.is_dragging():
            self.drag_controller.release_drag()