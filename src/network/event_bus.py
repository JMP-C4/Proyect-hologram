# src/network/event_bus.py

import socket
import threading
import json
from src.utils.config import HOST, PORT

class EventBus:
    def __init__(self):
        self.clients = []
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))

    def handle_client(self, client_socket):
        with self.lock:
            self.clients.append(client_socket)
        
        print(f"[EventBus] Nuevo cliente conectado. Total: {len(self.clients)}")

        try:
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break
                self.broadcast(message, client_socket)
        finally:
            with self.lock:
                self.clients.remove(client_socket)
            client_socket.close()
            print(f"[EventBus] Cliente desconectado. Total: {len(self.clients)}")

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client in self.clients:
                if client is not sender_socket:
                    try:
                        client.sendall(message)
                    except socket.error:
                        # Cliente podría haberse desconectado
                        pass

    def start(self):
        print(f"[EventBus] Iniciando en {HOST}:{PORT}")
        self.server_socket.listen()
        while True:
            client_socket, _ = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.daemon = True
            thread.start()

def main():
    bus = EventBus()
    bus.start()

if __name__ == "__main__":
    main()
