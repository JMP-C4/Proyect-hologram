# src/holograma/holograma.py

from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, WindowProperties, FrameBufferProperties, VBase3
from src.network.client import EventClient
import json

class HologramApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Cargar un modelo simple (un panda)
        self.model = self.loader.loadModel("panda")
        self.model.reparentTo(self.render)
        self.model.setScale(0.25, 0.25, 0.25)
        self.model.setPos(0, 5, 0)

        # Configurar cliente de eventos
        self.event_client = EventClient("Holograma")
        self.event_client.on_message_received = self.handle_event
        self.event_client.connect()

        # Añadir tarea para procesar eventos de la red
        self.taskMgr.add(self.update, "update")

    def handle_event(self, event):
        if event.get('type') == 'gesture_detected':
            gesture = event.get('data', {}).get('gesture')
            print(f"[Holograma] Gesto recibido: {gesture}")
            
            # Realizar acciones basadas en el gesto
            if gesture == 'fist':
                self.model.hprInterval(1.0, self.model.getHpr() + VBase3(90, 0, 0)).start()
            elif gesture == 'open_hand':
                self.model.setScale(0.25, 0.25, 0.25)
            elif gesture == 'point':
                self.model.setScale(self.model.getScale() * 1.2)

    def update(self, task):
        # Este método se asegura de que la app siga corriendo
        # y procesando tareas de Panda3D.
        return task.cont

def main():
    app = HologramApp()
    app.run()

if __name__ == "__main__":
    main()
