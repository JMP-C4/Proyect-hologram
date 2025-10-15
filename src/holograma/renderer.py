from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename, TransparencyAttrib, CardMaker
from direct.task.Task import Task
import os

#importaciones
from rotations import aplicar_rotaciones
#from holograma.floors import crear_suelos


class HologramaApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Ruta del modelo base
        base_path = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_path, "..", "assets", "models", "tu_modelo.glb")

        # Crear suelos desde floors.py
        #self.suelos = crear_suelos(self.render)

        # Cargar modelo original
        self.modelo_base = self.loader.loadModel(Filename.fromOsSpecific(model_path))
        self.modelo_base.setTransparency(TransparencyAttrib.M_alpha)
        self.modelo_base.setScale(3)

        self.modelo_maestro = self.modelo_base.copyTo(self.render)
        self.modelo_maestro.hide()
        self.modelo_maestro.setPos(0, 0, 0)

        # Nodo raíz
        self.root = self.render.attachNewNode("holograma_root")

        # ==============================
        # Copias para efecto holograma
        # ==============================

        # Frontal
        self.later = self.modelo_base.copyTo(self.root)
        self.later.setHpr(90, 90, 0)
        self.later.setPos(2.8, 0, 0)
        self.later_base_hpr = (90, 90, 0)

        # Posterior
        self.frontal = self.modelo_base.copyTo(self.root)
        self.frontal.setHpr(-90, 90, 0)
        self.frontal.setPos(-3, 0, 0)
        self.frontal_base_hpr = (-90, 90, 0)

        # Superior
        self.topSide = self.modelo_base.copyTo(self.root)
        self.topSide.setHpr(0, 0, 0)
        self.topSide.setPos(0, 0, 2.8)
        self.topSide_base_hpr = (0, 0, 0)

        # Inferior
        self.bottomSide = self.modelo_base.copyTo(self.root)
        self.bottomSide.setHpr(0, -180, 0)
        self.bottomSide.setPos(0, 0, -2.8)
        self.bottomSide_base_hpr = (0, -180, 0)

        # ==============================
        # Cámara
        # ==============================
        self.disableMouse()
        self.camera.setPos(0, -15, 5)
        self.camera.lookAt(self.root)

        # ==============================
        # Control de mouse
        # ==============================
        self.last_mouse = None
        self.accept("mouse1", self.start_drag)
        self.accept("mouse1-up", self.stop_drag)
        self.taskMgr.add(self.drag_task, "DragTask")

    def start_drag(self):
        if self.mouseWatcherNode.hasMouse():
            self.last_mouse = (
                self.mouseWatcherNode.getMouseX(),
                self.mouseWatcherNode.getMouseY()
            )

    def stop_drag(self):
        self.last_mouse = None

    def drag_task(self, task):
        if self.last_mouse and self.mouseWatcherNode.hasMouse():
            x, y = self.mouseWatcherNode.getMouseX(), self.mouseWatcherNode.getMouseY()
            last_x, last_y = self.last_mouse
            dx, _ = x - last_x, y - last_y

            sens = 100  # sensibilidad
            self.modelo_maestro.setH(self.modelo_maestro.getH() + dx * sens)

            # Usar función de rotations.py
            aplicar_rotaciones(
                self.modelo_maestro,
                self.later, self.later_base_hpr,
                self.frontal, self.frontal_base_hpr,
                self.topSide, self.topSide_base_hpr,
                self.bottomSide, self.bottomSide_base_hpr
            )

            self.last_mouse = (x, y)

        return task.cont


if __name__ == "__main__":
    app = HologramaApp()
    app.run()
