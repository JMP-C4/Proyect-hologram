# src/main.py

import multiprocessing
import time

# Importar las funciones principales de cada módulo
from src.network.event_bus import main as event_bus_main
from src.gestos.detector import main as gestos_main
from src.holograma.holograma import main as holograma_main
from src.ui.main_window import main as ui_main

def run_process(target):
    p = multiprocessing.Process(target=target)
    p.start()
    return p

if __name__ == "__main__":
    multiprocessing.freeze_support() # Necesario para Windows

    print("Iniciando la aplicación holográfica...")

    # 1. Iniciar el Bus de Eventos
    print("Iniciando el Bus de Eventos...")
    event_bus_process = run_process(event_bus_main)
    time.sleep(1) # Dar tiempo al bus para que se inicie

    # 2. Iniciar el renderizador de Holograma
    print("Iniciando el Holograma 3D...")
    hologram_process = run_process(holograma_main)

    # 3. Iniciar el detector de Gestos
    print("Iniciando el detector de Gestos...")
    gestos_process = run_process(gestos_main)

    # 4. Iniciar la Interfaz de Usuario
    print("Iniciando la Interfaz de Usuario...")
    ui_process = run_process(ui_main)

    # Mantener el proceso principal vivo y manejar la salida
    try:
        # Esperar a que los procesos terminen (lo cual no sucederá hasta que se cierren)
        event_bus_process.join()
        hologram_process.join()
        gestos_process.join()
        ui_process.join()
    except KeyboardInterrupt:
        print("\nCerrando todos los procesos...")
        event_bus_process.terminate()
        hologram_process.terminate()
        gestos_process.terminate()
        ui_process.terminate()
