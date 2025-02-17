import os
import time

def eliminarArchivos(ruta):
    for carpetaRaiz, _, archivos in os.walk(ruta):
        for archivo in archivos:
            if archivo.endswith(".png"):
                archivoPath = os.path.join(carpetaRaiz, archivo)
                print(f"Eliminando: {archivoPath}")
                os.remove(archivoPath)

def monitorearEliminar():
    rutaScript = os.getcwd()
    while True:
        eliminarArchivos(rutaScript)
        time.sleep(5)  # Espera 5 segundos antes de volver a escanear

if __name__ == "__main__":
    print("Inicio")
    monitorearEliminar()
