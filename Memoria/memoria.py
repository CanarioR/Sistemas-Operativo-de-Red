import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Bloques de memoria iniciales
MEMORIA_BASE = [1000, 400, 1800, 700, 900, 1200, 1500]

class AdministradorMemoria:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrador de Memoria - Práctica 7")

        self.bloques = [{"tam": tam, "disponible": True} for tam in MEMORIA_BASE]
        self.archivos = []
        self.asignaciones = []

        self.setup_widgets()

    def setup_widgets(self):
        frame_top = ttk.Frame(self.root)
        frame_top.pack(pady=5)

        ttk.Button(frame_top, text="Agregar Bloque", command=self.agregar_bloque).grid(row=0, column=0, padx=5)
        ttk.Button(frame_top, text="Agregar Archivo Virtual", command=self.agregar_archivo_virtual).grid(row=0, column=1, padx=5)
        ttk.Button(frame_top, text="Cargar Archivo TXT", command=self.cargar_archivos_txt).grid(row=0, column=2, padx=5)

        self.algoritmo_var = tk.StringVar(value="primer")
        for i, (nombre, val) in enumerate([("Primer Ajuste", "primer"), ("Mejor Ajuste", "mejor"),
                                           ("Peor Ajuste", "peor"), ("Siguiente Ajuste", "siguiente")]):
            ttk.Radiobutton(frame_top, text=nombre, variable=self.algoritmo_var, value=val).grid(row=1, column=i)

        ttk.Button(frame_top, text="Asignar Archivos", command=self.asignar).grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(frame_top, text="Limpiar", command=self.limpiar).grid(row=2, column=2, columnspan=2, pady=5)

        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Archivo", "Tamaño", "Bloque", "Tamaño Bloque"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack()

    def agregar_bloque(self):
        top = tk.Toplevel(self.root)
        top.title("Agregar Bloque de Memoria")

        tk.Label(top, text="Tamaño (KB):").grid(row=0, column=0)
        entry_tam = tk.Entry(top)
        entry_tam.grid(row=0, column=1)

        disponible_var = tk.BooleanVar(value=True)
        tk.Checkbutton(top, text="Disponible", variable=disponible_var).grid(row=1, column=0, columnspan=2)

        posicion_var = tk.StringVar(value="final")
        ttk.Radiobutton(top, text="Al inicio", variable=posicion_var, value="inicio").grid(row=2, column=0)
        ttk.Radiobutton(top, text="Al final", variable=posicion_var, value="final").grid(row=2, column=1)

        def agregar():
            try:
                tam = int(entry_tam.get())
                bloque = {"tam": tam, "disponible": disponible_var.get()}
                if posicion_var.get() == "inicio":
                    self.bloques.insert(0, bloque)
                else:
                    self.bloques.append(bloque)
                top.destroy()
                self.dibujar_bloques()
            except ValueError:
                messagebox.showerror("Error", "Tamaño inválido")

        ttk.Button(top, text="Agregar", command=agregar).grid(row=3, column=0, columnspan=2)

    def agregar_archivo_virtual(self):
        top = tk.Toplevel(self.root)
        top.title("Agregar Archivo Virtual")

        tk.Label(top, text="Nombre:").grid(row=0, column=0)
        entry_nombre = tk.Entry(top)
        entry_nombre.grid(row=0, column=1)

        tk.Label(top, text="Tamaño (KB):").grid(row=1, column=0)
        entry_tam = tk.Entry(top)
        entry_tam.grid(row=1, column=1)

        posicion_var = tk.StringVar(value="final")
        ttk.Radiobutton(top, text="Al inicio", variable=posicion_var, value="inicio").grid(row=2, column=0)
        ttk.Radiobutton(top, text="Al final", variable=posicion_var, value="final").grid(row=2, column=1)

        def agregar():
            try:
                nombre = entry_nombre.get()
                tam = int(entry_tam.get())
                if posicion_var.get() == "inicio":
                    self.archivos.insert(0, (nombre, tam))
                else:
                    self.archivos.append((nombre, tam))
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Tamaño inválido")

        ttk.Button(top, text="Agregar", command=agregar).grid(row=3, column=0, columnspan=2)

    def cargar_archivos_txt(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            with open(archivo, "r") as f:
                for linea in f:
                    nombre, tam = linea.strip().split(",")
                    self.archivos.append((nombre.strip(), int(tam.strip().replace("kb", ""))))

    def asignar(self):
        self.tree.delete(*self.tree.get_children())
        bloques_estado = [b["tam"] if b["disponible"] else 0 for b in self.bloques]

        algoritmo = self.algoritmo_var.get()
        if algoritmo == "primer":
            self.asignaciones = self.primer_ajuste(bloques_estado)
        elif algoritmo == "mejor":
            self.asignaciones = self.mejor_ajuste(bloques_estado)
        elif algoritmo == "peor":
            self.asignaciones = self.peor_ajuste(bloques_estado)
        else:
            self.asignaciones = self.siguiente_ajuste(bloques_estado)

        for archivo, tam, idx, bloque_tam in self.asignaciones:
            bloque_str = str(idx + 1) if idx != -1 else "No asignado"
            bloque_tam_str = f"{bloque_tam} KB" if bloque_tam else "-"
            self.tree.insert("", "end", values=(archivo, f"{tam} KB", bloque_str, bloque_tam_str))

        self.dibujar_bloques()

    def limpiar(self):
        self.archivos = []
        self.asignaciones = []
        self.bloques = [{"tam": tam, "disponible": True} for tam in MEMORIA_BASE]
        self.tree.delete(*self.tree.get_children())
        self.dibujar_bloques()

    def primer_ajuste(self, memoria):
        asignaciones = []
        for archivo, tam in self.archivos:
            asignado = False
            for i, bloque in enumerate(memoria):
                if bloque >= tam:
                    asignaciones.append((archivo, tam, i, self.bloques[i]["tam"]))
                    memoria[i] -= tam
                    asignado = True
                    break
            if not asignado:
                asignaciones.append((archivo, tam, -1, None))
        return asignaciones

    def mejor_ajuste(self, memoria):
        asignaciones = []
        for archivo, tam in self.archivos:
            mejor_idx = -1
            mejor_bloque = float("inf")
            for i, bloque in enumerate(memoria):
                if bloque >= tam and bloque < mejor_bloque:
                    mejor_bloque = bloque
                    mejor_idx = i
            if mejor_idx != -1:
                asignaciones.append((archivo, tam, mejor_idx, self.bloques[mejor_idx]["tam"]))
                memoria[mejor_idx] -= tam
            else:
                asignaciones.append((archivo, tam, -1, None))
        return asignaciones

    def peor_ajuste(self, memoria):
        asignaciones = []
        for archivo, tam in self.archivos:
            peor_idx = -1
            peor_bloque = -1
            for i, bloque in enumerate(memoria):
                if bloque >= tam and bloque > peor_bloque:
                    peor_bloque = bloque
                    peor_idx = i
            if peor_idx != -1:
                asignaciones.append((archivo, tam, peor_idx, self.bloques[peor_idx]["tam"]))
                memoria[peor_idx] -= tam
            else:
                asignaciones.append((archivo, tam, -1, None))
        return asignaciones

    def siguiente_ajuste(self, memoria):
        asignaciones = []
        n = len(memoria)
        inicio = 0
        for archivo, tam in self.archivos:
            asignado = False
            for i in range(n):
                idx = (inicio + i) % n
                if memoria[idx] >= tam:
                    asignaciones.append((archivo, tam, idx, self.bloques[idx]["tam"]))
                    memoria[idx] -= tam
                    inicio = idx
                    asignado = True
                    break
            if not asignado:
                asignaciones.append((archivo, tam, -1, None))
        return asignaciones

    def dibujar_bloques(self):
        self.canvas.delete("all")
        ancho_canvas = 700
        alto_bloque = 25
        separacion = 10
        escalar = ancho_canvas / max(b["tam"] for b in self.bloques) if self.bloques else 1

        for i, bloque in enumerate(self.bloques):
            x = 180
            y = i * (alto_bloque + separacion) + 10
            usado = bloque["tam"] if not bloque["disponible"] else 0

            # Etiqueta de bloque
            self.canvas.create_text(x - 20, y + alto_bloque / 2, anchor="e",
                                    text=f"Bloque {i + 1}: {bloque['tam']} KB", font=("Arial", 10, "bold"))

            # Fondo verde
            self.canvas.create_rectangle(x, y, x + bloque["tam"] * escalar, y + alto_bloque,
                                         fill="lightgreen", outline="black")

            # Espacio ocupado (rojo)
            if usado > 0:
                self.canvas.create_rectangle(x, y, x + usado * escalar, y + alto_bloque,
                                             fill="tomato", outline="black")

            # Archivos asignados
            offset = 0
            for archivo, tam, idx, _ in self.asignaciones:
                if idx == i:
                    self.canvas.create_text(x + offset * escalar + 5, y + alto_bloque / 2,
                                            anchor="w", text=archivo, font=("Arial", 8, "italic"))
                    offset += tam

# Ejecutar
root = tk.Tk()
app = AdministradorMemoria(root)
root.mainloop()
