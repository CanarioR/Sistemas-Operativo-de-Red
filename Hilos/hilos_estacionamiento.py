import tkinter as tk
import threading
import time
import random

# --- Variables globales ---
tam_max = 12
estacionamiento = []
frecuencia_entrada = random.choice([0.5, 1, 2])
frecuencia_salida = random.choice([0.5, 1, 2])
ejecutando = True
lock = threading.Lock()

# --- Clase Auto ---
class Auto:
    contador = 1
    def __init__(self):
        self.id = Auto.contador
        Auto.contador += 1
    def __str__(self):
        return f"A{self.id}"

# --- Lógica de Entrada/Salida ---
def entrada_autos():
    global frecuencia_entrada
    while ejecutando:
        time.sleep(frecuencia_entrada)
        with lock:
            if len(estacionamiento) < tam_max:
                auto = Auto()
                estacionamiento.append(auto)
        actualizar_gui()

def salida_autos():
    global frecuencia_salida
    while ejecutando:
        time.sleep(frecuencia_salida)
        with lock:
            if estacionamiento:
                estacionamiento.pop(0)
        actualizar_gui()

# --- Actualizar interfaz ---
def actualizar_gui():
    for i in range(tam_max):
        if i < len(estacionamiento):
            celdas[i].config(text=str(estacionamiento[i]), bg="lightgreen")
        else:
            celdas[i].config(text="", bg="white")
    estado_label.config(text=f"Ocupados: {len(estacionamiento)}/{tam_max}")
    entrada_label.config(text=f"Frecuencia Entrada: {frecuencia_entrada}s")
    salida_label.config(text=f"Frecuencia Salida: {frecuencia_salida}s")

# --- Cambiar frecuencias ---
def cambiar_frecuencia(tipo):
    global frecuencia_entrada, frecuencia_salida
    try:
        valor = float(frecuencia_entry.get())
        if tipo == 'e':
            frecuencia_entrada = valor
        elif tipo == 's':
            frecuencia_salida = valor
        actualizar_gui()
    except ValueError:
        pass  # Silencio si el usuario escribe mal

# --- Interfaz gráfica ---
ventana = tk.Tk()
ventana.title("Estacionamiento - Control de Autos")

frame = tk.Frame(ventana)
frame.pack(pady=10)

# Celdas del estacionamiento
celdas = []
for i in range(tam_max):
    lbl = tk.Label(frame, text="", width=6, height=2, relief="ridge", borderwidth=2, bg="white")
    lbl.grid(row=0, column=i, padx=2, pady=2)
    celdas.append(lbl)

# Información
estado_label = tk.Label(ventana, text="Ocupados: 0/12", font=("Arial", 12))
estado_label.pack()

entrada_label = tk.Label(ventana, text=f"Frecuencia Entrada: {frecuencia_entrada}s")
entrada_label.pack()

salida_label = tk.Label(ventana, text=f"Frecuencia Salida: {frecuencia_salida}s")
salida_label.pack()

# Cambiar frecuencia
frecuencia_entry = tk.Entry(ventana)
frecuencia_entry.pack(pady=5)

boton_entrada = tk.Button(ventana, text="Cambiar Frecuencia Entrada", command=lambda: cambiar_frecuencia('e'))
boton_entrada.pack()

boton_salida = tk.Button(ventana, text="Cambiar Frecuencia Salida", command=lambda: cambiar_frecuencia('s'))
boton_salida.pack()

# --- Iniciar hilos ---
threading.Thread(target=entrada_autos, daemon=True).start()
threading.Thread(target=salida_autos, daemon=True).start()

# --- Ejecutar GUI ---
actualizar_gui()
ventana.mainloop()

# --- Cuando se cierra ---
ejecutando = False
