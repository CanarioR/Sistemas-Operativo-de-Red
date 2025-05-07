import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

# Crear ventana
ventana = tk.Tk()
ventana.title("Movimiento con hilos")
ventana.geometry("600x400")

# Canvas
canvas = tk.Canvas(ventana, width=600, height=400, bg="white")
canvas.pack()

# Cargar imágenes
img1 = Image.open("1.png").resize((50, 50))
img2 = Image.open("2.png").resize((50, 50))

tk_img1 = ImageTk.PhotoImage(img1)
tk_img2 = ImageTk.PhotoImage(img2)

# Crear imágenes en el canvas
img1_id = canvas.create_image(0, 150, anchor="nw", image=tk_img1)
img2_id = canvas.create_image(300, 0, anchor="nw", image=tk_img2)

# Posiciones
pos_x = 0
pos_y = 0

# Función para mover horizontalmente (imagen 1)
def mover_horizontal():
    global pos_x
    while pos_x < 550:
        pos_x += 2
        canvas.after(0, canvas.move, img1_id, 2, 0)
        time.sleep(0.01)

# Función para mover verticalmente (imagen 2)
def mover_vertical():
    global pos_y
    while pos_y < 350:
        pos_y += 2
        canvas.after(0, canvas.move, img2_id, 0, 2)
        time.sleep(0.01)

# Iniciar hilos
hilo1 = threading.Thread(target=mover_horizontal)
hilo2 = threading.Thread(target=mover_vertical)

hilo1.start()
hilo2.start()

# Iniciar interfaz
ventana.mainloop()
