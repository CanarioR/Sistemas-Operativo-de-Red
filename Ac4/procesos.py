def cargarProcesos(archivo):
    procesos = []
    with open(archivo, 'r') as f:
        for linea in f:
            nombre, llegada, duracion, prioridad = linea.strip().split(', ')
            procesos.append({
                'nombre': nombre,
                'llegada': int(llegada),
                'duracion': int(duracion),
                'prioridad': int(prioridad)
            })
    return procesos

def prioridades(procesos):
    procesos_ordenados = sorted(procesos, key=lambda x: x['llegada'])
    tiempo_actual = 0
    procesos_restantes = procesos_ordenados.copy()
    lista_listos = []

    print("\nAlgoritmo de Prioridades:")

    while procesos_restantes or lista_listos:
        while procesos_restantes and procesos_restantes[0]['llegada'] <= tiempo_actual:
            lista_listos.append(procesos_restantes.pop(0))

        if not lista_listos:
            tiempo_actual = procesos_restantes[0]['llegada']
            continue

        lista_listos.sort(key=lambda x: x['prioridad'])
        proceso = lista_listos.pop(0)
        print(f"Ejecutando {proceso['nombre']} (Duración: {proceso['duracion']}, Prioridad: {proceso['prioridad']})")
        tiempo_actual += proceso['duracion']
        print(f"Tiempo total transcurrido: {tiempo_actual}")


def round_robin(procesos, quantum=3):
    procesos_ordenados = sorted(procesos, key=lambda x: x['llegada'])
    tiempo_actual = 0
    cola = []
    procesos_restantes = procesos_ordenados.copy()

    print("\nAlgoritmo Round Robin:")

    while procesos_restantes or cola:
        while procesos_restantes and procesos_restantes[0]['llegada'] <= tiempo_actual:
            cola.append(procesos_restantes.pop(0))

        if not cola:
            tiempo_actual = procesos_restantes[0]['llegada']
            continue

        proceso = cola.pop(0)
        if proceso['duracion'] > quantum:
            print(f"Ejecutando {proceso['nombre']} (Ejecutando {quantum} unidades de tiempo)")
            tiempo_actual += quantum
            proceso['duracion'] -= quantum
            cola.append(proceso)  # Se vuelve a poner al final de la cola
        else:
            print(f"Ejecutando {proceso['nombre']} (Duración: {proceso['duracion']})")
            tiempo_actual += proceso['duracion']

        print(f"Tiempo total transcurrido: {tiempo_actual}")


# Cargar los procesos desde un archivo
archivo = "procesos.txt"  # Nombre del archivo de entrada
procesos = cargarProcesos(archivo)

prioridades(procesos)
round_robin(procesos)
