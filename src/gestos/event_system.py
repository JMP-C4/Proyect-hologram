"""
Sistema de eventos para conectar detección de gestos con el renderer 3D.
Permite comunicación desacoplada entre módulos mediante un patrón Observer.
"""

import socket
import json
import threading
import time
from typing import Callable, Dict, List, Any
from enum import Enum


class GestureEvent(Enum):
    """Tipos de eventos de gestos disponibles."""
    POINTING = "pointing"
    CLICK = "click"
    PINCH = "pinch"
    OPEN_HAND = "open_hand"
    FIST = "fist"
    PEACE = "peace"
    THUMBS_UP = "thumbs_up"
    THREE_FINGERS = "three_fingers"
    SWIPE_LEFT = "swipe_left"
    SWIPE_RIGHT = "swipe_right"
    SWIPE_UP = "swipe_up"
    SWIPE_DOWN = "swipe_down"
    ROTATION = "rotation"  # Evento especial para rotación continua


class GestureEventBus:
    """
    Bus de eventos para gestos.
    Permite suscribirse a eventos y emitirlos.
    """
    
    def __init__(self):
        self._subscribers: Dict[GestureEvent, List[Callable]] = {}
        self._lock = threading.Lock()
    
    def subscribe(self, event: GestureEvent, callback: Callable):
        """
        Suscribe un callback a un tipo de evento.
        
        Args:
            event: Tipo de evento GestureEvent
            callback: Función que será llamada cuando ocurra el evento
        """
        with self._lock:
            if event not in self._subscribers:
                self._subscribers[event] = []
            self._subscribers[event].append(callback)
            print(f"📢 Suscrito a evento: {event.value}")
    
    def unsubscribe(self, event: GestureEvent, callback: Callable):
        """Desuscribe un callback de un evento."""
        with self._lock:
            if event in self._subscribers:
                self._subscribers[event].remove(callback)
    
    def emit(self, event: GestureEvent, data: Dict[str, Any] = None):
        """
        Emite un evento a todos los suscriptores.
        
        Args:
            event: Tipo de evento
            data: Datos adicionales del evento
        """
        with self._lock:
            if event in self._subscribers:
                for callback in self._subscribers[event]:
                    try:
                        if data:
                            callback(data)
                        else:
                            callback()
                    except Exception as e:
                        print(f"❌ Error en callback de {event.value}: {e}")


class NetworkEventBridge:
    """
    Puente de red para enviar eventos de gestos al renderer 3D mediante sockets.
    Útil cuando el renderer está en un proceso separado.
    """
    
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self._lock = threading.Lock()
    
    def connect(self):
        """Establece conexión con el servidor del renderer."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"🌐 Conectado al renderer en {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ Error al conectar: {e}")
            self.connected = False
            return False
    
    def send_gesture_event(self, event: GestureEvent, data: Dict[str, Any] = None):
        """
        Envía un evento de gesto al renderer.
        
        Args:
            event: Tipo de evento
            data: Datos adicionales (posición, velocidad, etc.)
        """
        if not self.connected:
            return
        
        try:
            message = {
                'event': event.value,
                'data': data or {},
                'timestamp': time.time()
            }
            
            json_data = json.dumps(message) + '\n'
            
            with self._lock:
                self.socket.sendall(json_data.encode('utf-8'))
                
        except Exception as e:
            print(f"❌ Error al enviar evento: {e}")
            self.connected = False
    
    def disconnect(self):
        """Cierra la conexión."""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.connected = False
            print("🔴 Desconectado del renderer")


class GestureController:
    """
    Controlador principal que une detección de gestos con acciones.
    """
    
    def __init__(self, use_network=False):
        self.event_bus = GestureEventBus()
        self.network_bridge = NetworkEventBridge() if use_network else None
        
        if self.network_bridge:
            self.network_bridge.connect()
        
        # Registrar handlers por defecto
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Registra los handlers básicos de eventos."""
        # Rotación
        self.event_bus.subscribe(
            GestureEvent.ROTATION,
            lambda data: self._handle_rotation(data)
        )
        
        # Click
        self.event_bus.subscribe(
            GestureEvent.CLICK,
            lambda: print("🖱️ Click detectado")
        )
        
        # Swipes
        self.event_bus.subscribe(
            GestureEvent.SWIPE_LEFT,
            lambda: print("👈 Swipe izquierda")
        )
        
        self.event_bus.subscribe(
            GestureEvent.SWIPE_RIGHT,
            lambda: print("👉 Swipe derecha")
        )
    
    def _handle_rotation(self, data):
        """Handler para eventos de rotación."""
        rotation_angle = data.get('angle', 0)
        print(f"🔄 Rotación: {rotation_angle}°")
        
        # Enviar al renderer si está conectado
        if self.network_bridge and self.network_bridge.connected:
            self.network_bridge.send_gesture_event(
                GestureEvent.ROTATION,
                data
            )
    
    def process_gesture(self, gesture_name: str, gesture_data: Dict = None):
        """
        Procesa un gesto detectado y emite el evento correspondiente.
        
        Args:
            gesture_name: Nombre del gesto (debe coincidir con GestureEvent)
            gesture_data: Datos adicionales del gesto
        """
        try:
            # Convertir nombre a enum
            event = GestureEvent(gesture_name.lower())
            
            # Emitir evento local
            self.event_bus.emit(event, gesture_data)
            
            # Enviar por red si está habilitado
            if self.network_bridge and self.network_bridge.connected:
                self.network_bridge.send_gesture_event(event, gesture_data)
                
        except ValueError:
            print(f"⚠️ Gesto no reconocido: {gesture_name}")
    
    def shutdown(self):
        """Cierra todas las conexiones."""
        if self.network_bridge:
            self.network_bridge.disconnect()


# ===== Ejemplo de uso =====

if __name__ == "__main__":
    # Crear controlador
    controller = GestureController(use_network=False)
    
    # Suscribir a un evento personalizado
    def on_fist_detected():
        print("✊ ¡Puño detectado!")
    
    controller.event_bus.subscribe(GestureEvent.FIST, on_fist_detected)
    
    # Simular detección de gestos
    controller.process_gesture("FIST")
    controller.process_gesture("CLICK")
    controller.process_gesture("ROTATION", {"angle": 45, "speed": 2.5})
    
    # Limpiar
    controller.shutdown()