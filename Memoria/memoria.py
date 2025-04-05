import tkinter as tk
from tkinter import ttk, filedialog, messagebox

MEMORIA_BASE = [1000, 400, 1800, 700, 900, 1200, 1500]

def peor_ajuste(archivos, memoria):
    asignaciones = []
    for archivo, tam in archivos:
        peor_idx = -1
        peor_bloque = -1
        for i, bloque in enumerate(memoria):
            if bloque >= tam and bloque > peor_bloque:
                peor_bloque = bloque
                peor_idx = i
        if peor_idx != -1:
            asignaciones.append((archivo, tam, peor_idx, MEMORIA_BASE[peor_idx]))
            memoria[peor_idx] -= tam
        else:
            asignaciones.append((archivo, tam, -1, None))
    return asignaciones

def siguiente_ajuste(archivos, memoria):
    asignaciones = []
    inicio = 0
    n = len(memoria)
    for archivo, tam in archivos:
        encontrado = False
        for i in range(n):
            idx = (inicio + i) % n
            if memoria[idx] >= tam:
                asignaciones.append((archivo, tam, idx, MEMORIA_BASE[idx]))
                memoria[idx] -= tam
                inicio = idx  # Actualizamos el punto de inicio para el siguiente archivo
                encontrado = True
                break
        if not encontrado:
            asignaciones.append((archivo, tam, -1, None))
    return asignaciones


class MemoriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Administración de Memoria")
        self.archivos = []
        self.memoria_actual = MEMORIA_BASE.copy()
        self.asignaciones = []

        self.setup_widgets()

    def setup_widgets(self):
        frame_top = ttk.Frame(self.root)
        frame_top.pack(pady=10)

        ttk.Button(frame_top, text="Cargar archivo .txt", command=self.cargar_archivos).grid(row=0, column=0, padx=5)

        self.algoritmo_var = tk.StringVar(value="peor")
        ttk.Radiobutton(frame_top, text="Peor Ajuste", variable=self.algoritmo_var, value="peor").grid(row=0, column=1)
        ttk.Radiobutton(frame_top, text="Siguiente Ajuste", variable=self.algoritmo_var, value="siguiente").grid(row=0, column=2)

        ttk.Button(frame_top, text="Asignar Memoria", command=self.asignar).grid(row=0, column=3, padx=5)
        ttk.Button(frame_top, text="Reiniciar", command=self.reiniciar).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("archivo", "tamano", "bloque", "bloque_tam"), show="headings", height=8)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=600, height=250, bg="white")
        self.canvas.pack(pady=10)

    def cargar_archivos(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if not ruta:
            return
        try:
            self.archivos = []
            with open(ruta, "r") as f:
                for linea in f:
                    partes = linea.strip().split(",")
                    if len(partes) == 2:
                        nombre = partes[0].strip()
                        tamano = int(partes[1].replace("kb", "").strip())
                        self.archivos.append((nombre, tamano))
            messagebox.showinfo("Carga exitosa", f"{len(self.archivos)} archivos cargados.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def asignar(self):
        if not self.archivos:
            messagebox.showwarning("Advertencia", "Primero carga un archivo.")
            return

        self.tree.delete(*self.tree.get_children())
        self.memoria_actual = MEMORIA_BASE.copy()

        if self.algoritmo_var.get() == "peor":
            self.asignaciones = peor_ajuste(self.archivos, self.memoria_actual)
        else:
            self.asignaciones = siguiente_ajuste(self.archivos, self.memoria_actual)

        for archivo, tam, idx, bloque_tam in self.asignaciones:
            bloque_str = str(idx + 1) if idx != -1 else "No asignado"
            bloque_tam_str = f"{bloque_tam} KB" if bloque_tam else "-"
            self.tree.insert("", "end", values=(archivo, f"{tam} KB", bloque_str, bloque_tam_str))

        self.dibujar_bloques()


    def dibujar_bloques(self):
        self.canvas.delete("all")
        ancho_canvas = 600
        alto_bloque = 25
        separacion = 10

        max_bloque = max(MEMORIA_BASE)
        escalar = ancho_canvas / max_bloque

        for i, bloque_total in enumerate(MEMORIA_BASE):
            x = 150  # desplazamos el bloque a la derecha para dejar espacio al texto
            y = i * (alto_bloque + separacion) + 10
            bloque_usado = bloque_total - self.memoria_actual[i]

            # Etiqueta de bloque a la izquierda
            self.canvas.create_text(x - 10, y + alto_bloque / 2, anchor="e",
                                    text=f"Bloque {i + 1}: {bloque_total} KB", font=("Arial", 10, "bold"))

            # Bloque completo (verde)
            self.canvas.create_rectangle(x, y, x + bloque_total * escalar, y + alto_bloque, fill="lightgreen", outline="black")

            # Bloque usado (rojo)
            if bloque_usado > 0:
                self.canvas.create_rectangle(x, y, x + bloque_usado * escalar, y + alto_bloque, fill="tomato", outline="black")

            # Mostrar archivos dentro del bloque
            offset = 0
            for archivo, tam, idx, _ in self.asignaciones:
                if idx == i:
                    self.canvas.create_text(x + offset * escalar + 5, y + alto_bloque / 2,
                                            anchor="w", text=archivo, font=("Arial", 8, "italic"))
                    offset += tam

    def reiniciar(self):
        self.tree.delete(*self.tree.get_children())
        self.canvas.delete("all")
        self.archivos = []
        self.memoria_actual = MEMORIA_BASE.copy()
        self.asignaciones = []

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoriaApp(root)
    root.mainloop()
