def aplicar_rotaciones(
    modelo_maestro,
    frontal, frontal_base_hpr,
    later, later_base_hpr,
    topSide, topSide_base_hpr,
    bottomSide, bottomSide_base_hpr
):
    """
    Aplica las rotaciones sincronizadas para el efecto Pepper's Ghost.
    - El heading (H) del maestro controla la rotación.
    - Frontal y superior giran normal.
    - Posterior e inferior giran en espejo.
    """

    # Heading del modelo maestro
    maestro_h = modelo_maestro.getH()

    # Frontal
    frontal.setHpr(
        frontal_base_hpr[0] + maestro_h,
        frontal_base_hpr[1],
        frontal_base_hpr[2]
    )

    # Posterior (espejo del frontal)
    later.setHpr(
        later_base_hpr[0] - maestro_h,
        later_base_hpr[1],
        later_base_hpr[2]
    )

    # Superior
    topSide.setHpr(
        topSide_base_hpr[0] + maestro_h,
        topSide_base_hpr[1],
        topSide_base_hpr[2]
    )

    # Inferior (espejo del superior)
    bottomSide.setHpr(
        bottomSide_base_hpr[0] - maestro_h,
        bottomSide_base_hpr[1],
        bottomSide_base_hpr[2]
    )
