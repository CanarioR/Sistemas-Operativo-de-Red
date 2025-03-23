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
#-------FIFO-------------
def fifo(procesos):
    # Ordenar los procesos por tiempo de llegada
    procesosFifo = sorted(procesos, key=lambda x: x['llegada'])
    tiempoTotal = 0
    print("\nAlgoritmo FIFO:")
    for proceso in procesosFifo:
        tiempoTotal += proceso['duracion']
        print(f"Ejecutando {proceso['nombre']} (Duración: {proceso['duracion']})")
        print(f"Tiempo total transcurrido: {tiempoTotal}")

#---------SJF ----------
def sjf(procesos):
    procesos_ordenados = sorted(procesos, key=lambda x: x['llegada'])
    
    tiempo_actual = 0  # Reloj del sistema
    procesos_restantes = procesos_ordenados.copy()  # Procesos aún no ejecutados
    lista_listos = []  # Procesos que han llegado y están listos para ejecutarse

    print("\nAlgoritmo SJF:")

    while procesos_restantes or lista_listos:
        #Agregar a lista_listos los procesos que han llegado hasta este tiempo
        while procesos_restantes and procesos_restantes[0]['llegada'] <= tiempo_actual:
            lista_listos.append(procesos_restantes.pop(0))

        #adelantar el tiempo y mostrar la espera
        if not lista_listos:
            nuevo_tiempo = procesos_restantes[0]['llegada']
            print(f"Tiempo inactivo hasta {nuevo_tiempo}...")
            tiempo_actual = nuevo_tiempo
            continue

        #Elegir el proceso más corto
        lista_listos.sort(key=lambda x: x['duracion'])
        proceso = lista_listos.pop(0)

        #Ejecutar el proceso
        print(f"Ejecutando {proceso['nombre']} (Duración: {proceso['duracion']})")
        tiempo_actual += proceso['duracion']
        print(f"Tiempo total transcurrido: {tiempo_actual}")

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

def guardarProcesos(archivo, procesos):
    with open(archivo, 'w') as f:
        for p in procesos:
            f.write(f"{p['nombre']}, {p['llegada']}, {p['duracion']}, {p['prioridad']}\n")

def agregarProceso(procesos):
    nombre = input("Nombre del proceso: ")
    llegada = int(input("Tiempo de llegada: "))
    duracion = int(input("Tiempo de duración: "))
    prioridad = int(input("Prioridad (menor es mayor prioridad): "))
    nuevo_proceso = {'nombre': nombre, 'llegada': llegada, 'duracion': duracion, 'prioridad': prioridad}

    posicion = input("¿Agregar al principio o al final? (inicio/fin): ").strip().lower()
    if posicion == 'inicio':
        procesos.insert(0, nuevo_proceso)
    else:
        procesos.append(nuevo_proceso)
    print("Proceso agregado con éxito.")

def ejecutar_algoritmo(procesos, algoritmo, quantum=3):
    if algoritmo == '1':
        fifo(procesos)
    elif algoritmo == '2':
        sjf(procesos)
    elif algoritmo == '3':
        prioridades(procesos)
    elif algoritmo == '4':
        round_robin(procesos, quantum)

def menu():
    archivo = "procesos.txt"
    procesos = cargarProcesos(archivo)

    while True:
        print("\n1. Agregar proceso")
        print("2. Ejecutar algoritmo")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregarProceso(procesos)
            guardarProcesos(archivo, procesos)
        elif opcion == '2':
            print("\nSeleccione el algoritmo:")
            print("1. FIFO")
            print("2. SJF")
            print("3. Prioridades")
            print("4. Round Robin")
            algoritmo = input("Ingrese el número del algoritmo: ")

            if algoritmo == '4':
                quantum = int(input("Ingrese el quantum para Round Robin: "))
                ejecutar_algoritmo(procesos, algoritmo, quantum)
            else:
                ejecutar_algoritmo(procesos, algoritmo)
        elif opcion == '3':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

menu()


