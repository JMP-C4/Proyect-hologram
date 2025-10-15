# src/holograma/floors.py
from panda3d.core import CardMaker, TransparencyAttrib

def crear_suelos(render):
    """
    Crea todos los pisos (centro, frontal, posterior, superior, inferior).
    Retorna un diccionario con las referencias de cada uno.
    """
    cm = CardMaker("suelo")
    cm.setFrame(-10, 10, -10, 10)

    suelos = {}

    # Centro
    suelos["centro"] = render.attachNewNode(cm.generate())
    suelos["centro"].setPos(0, 0, -1)
    suelos["centro"].setHpr(0, -90, 0)
    suelos["centro"].setColor(0.3, 0.3, 0.3, 0.5)
    suelos["centro"].setTransparency(TransparencyAttrib.M_alpha)

    # Frontal
    suelos["frontal"] = render.attachNewNode(cm.generate())
    suelos["frontal"].setPos(3, 0, -1)
    suelos["frontal"].setHpr(0, -90, 0)
    suelos["frontal"].setColor(0.2, 0.4, 0.2, 0.3)
    suelos["frontal"].setTransparency(TransparencyAttrib.M_alpha)

    # Posterior
    suelos["posterior"] = render.attachNewNode(cm.generate())
    suelos["posterior"].setPos(-3, 0, -1)
    suelos["posterior"].setHpr(0, -90, 0)
    suelos["posterior"].setColor(0.4, 0.2, 0.2, 0.3)
    suelos["posterior"].setTransparency(TransparencyAttrib.M_alpha)

    # Superior
    suelos["superior"] = render.attachNewNode(cm.generate())
    suelos["superior"].setPos(0, 0, 2)
    suelos["superior"].setHpr(0, -90, 0)
    suelos["superior"].setColor(0.2, 0.2, 0.4, 0.3)
    suelos["superior"].setTransparency(TransparencyAttrib.M_alpha)

    # Inferior
    suelos["inferior"] = render.attachNewNode(cm.generate())
    suelos["inferior"].setPos(0, 0, -4)
    suelos["inferior"].setHpr(0, -90, 0)
    suelos["inferior"].setColor(0.4, 0.4, 0.2, 0.3)
    suelos["inferior"].setTransparency(TransparencyAttrib.M_alpha)

    return suelos
