# src/network/client.py

import socket
import json
import threading
import time
from src.utils.config import HOST, PORT

class EventClient:
    def __init__(self, name):
        self.name = name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.on_message_received = None

    def connect(self):
        while not self.connected:
            try:
                self.socket.connect((HOST, PORT))
                self.connected = True
                print(f"[{self.name}] Conectado al Event Bus.")
                
                # Iniciar hilo para escuchar mensajes
                listen_thread = threading.Thread(target=self.listen)
                listen_thread.daemon = True
                listen_thread.start()

            except ConnectionRefusedError:
                print(f"[{self.name}] No se pudo conectar al Event Bus. Reintentando en 3 segundos...")
                time.sleep(3)

    def listen(self):
        while self.connected:
            try:
                message = self.socket.recv(1024)
                if not message:
                    self.connected = False
                    break
                
                if self.on_message_received:
                    try:
                        event = json.loads(message.decode('utf-8'))
                        self.on_message_received(event)
                    except json.JSONDecodeError:
                        print(f"[{self.name}] Error decodificando JSON: {message.decode('utf-8')}")

            except ConnectionResetError:
                self.connected = False
                break
        
        print(f"[{self.name}] Desconectado del Event Bus.")

    def send_event(self, event_type, data):
        if self.connected:
            event = {"source": self.name, "type": event_type, "data": data}
            try:
                self.socket.sendall(json.dumps(event).encode('utf-8'))
            except socket.error:
                self.connected = False

    def close(self):
        self.connected = False
        self.socket.close()
