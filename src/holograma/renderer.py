from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename, TransparencyAttrib, WindowProperties
from direct.task.Task import Task
import os
import socket
import json
import threading

from .rotations import aplicar_rotaciones


class GestureNetworkReceiver:
    """
    Receptor de red para eventos de gestos.
    Ejecuta en un thread separado para no bloquear el renderer.
    """
    
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.running = False
        self.thread = None
        self.callbacks = {}
    
    def register_callback(self, event_name, callback):
        """Registra un callback para un tipo de evento."""
        self.callbacks[event_name] = callback
        print(f"📢 Callback registrado para: {event_name}")
    
    def start(self):
        """Inicia el servidor de red en un thread."""
        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        print(f"🌐 Servidor de gestos iniciado en {self.host}:{self.port}")
    
    def _run_server(self):
        """Bucle principal del servidor."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            
            print(f"⏳ Esperando conexión de detector de gestos...")
            
            self.client_socket, addr = self.server_socket.accept()
            print(f"✅ Cliente conectado desde {addr}")
            
            buffer = ""
            while self.running:
                try:
                    data = self.client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    
                    buffer += data
                    
                    # Procesar mensajes completos (separados por \n)
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        self._process_message(line)
                        
                except Exception as e:
                    print(f"❌ Error recibiendo datos: