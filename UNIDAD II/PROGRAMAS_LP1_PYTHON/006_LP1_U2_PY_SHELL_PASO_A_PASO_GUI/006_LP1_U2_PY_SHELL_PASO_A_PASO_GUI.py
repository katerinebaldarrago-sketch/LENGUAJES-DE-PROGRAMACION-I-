import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Colores ----------
COLOR_NORMAL = "#B0BEC5"     # gris: fuera del subgrupo actual
COLOR_GRUPO = "#64B5F6"      # azul: elementos del subgrupo (separados por gap)
COLOR_TOMAR = "#FFD54F"      # amarillo: elemento i que se toma (temp)
COLOR_COMPARA = "#EF5350"    # rojo: elemento arr[j-gap] que se compara
COLOR_HUECO = "#FFA726"      # naranja: posición j (hueco)
COLOR_DESPLAZA = "#AB47BC"   # morado: elemento desplazado
COLOR_INSERTA = "#66BB6A"    # verde: temp insertado / ordenado


# ---------- Lógica: genera todos los pasos del algoritmo ----------
def generar_pasos(datos):
    arr = datos[:]
    n = len(arr)
    pasos = []

    def agregar(msg, kind="info", gap=None, i=None, j=None, temp=None, comp=()):
        pasos.append({
            "arr": arr[:], "msg": msg, "kind": kind,
            "gap": gap, "i": i, "j": j, "temp": temp, "comp": comp,
        })

    agregar("Arreglo original: " + " ".join(map(str, arr)))

    gap = n // 2
    while gap > 0:
        agregar(f"=== Nuevo incremento: gap = {gap} ===", gap=gap)

        for i in range(gap, n):
            temp = arr[i]
            j = i
            agregar(f"i = {i}: se guarda temp = arr[{i}] = {temp}",
                    "tomar", gap, i, j, temp)

            while j >= gap:
                agregar(f"Comparar arr[{j - gap}] = {arr[j - gap]} con temp = {temp}",
                        "comparar", gap, i, j, temp, (j - gap, j))
                if arr[j - gap] > temp:
                    valor = arr[j - gap]
                    arr[j] = valor
                    agregar(f"{valor} > {temp}: se desplaza {valor} de la posición "
                            f"{j - gap} a la {j}",
                            "desplazar", gap, i, j, temp, (j - gap, j))
                    j -= gap
                else:
                    agregar(f"{arr[j - gap]} no es mayor que {temp}: se detiene",
                            "detener", gap, i, j, temp, (j - gap, j))
                    break

            arr[j] = temp
            agregar(f"Se inserta temp = {temp} en la posición {j}",
                    "insertar", gap, i, j, temp, (j,))

        gap //= 2

    agregar("¡Arreglo ordenado! " + " ".join(map(str, arr)), "fin")
    return pasos


# ---------- Interfaz ----------
class AppShell:
    ANCHO, ALTO = 800, 380

    def __init__(self, root):
        self.root = root
        root.title("Ordenación Shell - paso a paso")
        root.resizable(False, False)

        self.pasos = []
        self.indice = 0
        self.auto = False
        self.after_id = None

        # Entrada de datos
        top = ttk.Frame(root, padding=8)
        top.pack(fill="x")
        ttk.Label(top, text="Datos (separados por espacio):").pack(side="left")
        self.entrada = ttk.Entry(top, width=30)
        self.entrada.insert(0, "64 25 12 22 11")
        self.entrada.pack(side="left", padx=6)
        ttk.Button(top, text="Cargar", command=self.cargar).pack(side="left")

        # Canvas
        self.canvas = tk.Canvas(root, width=self.ANCHO, height=self.ALTO,
                                bg="white", highlightthickness=1,
                                highlightbackground="#999")
        self.canvas.pack(padx=8)

        # Información del paso
        self.lbl_info = ttk.Label(root, text="", font=("Segoe UI", 11, "bold"),
                                  wraplength=780)
        self.lbl_info.pack(pady=(6, 0))
        self.lbl_vars = ttk.Label(root, text="", font=("Consolas", 10))
        self.lbl_vars.pack()
        self.lbl_paso = ttk.Label(root, text="")
        self.lbl_paso.pack()

        # Botones
        bar = ttk.Frame(root, padding=6)
        bar.pack()
        ttk.Button(bar, text="⏮ Reiniciar", command=self.reiniciar).grid(row=0, column=0, padx=3)
        ttk.Button(bar, text="◀ Anterior", command=self.anterior).grid(row=0, column=1, padx=3)
        ttk.Button(bar, text="Siguiente ▶", command=self.siguiente).grid(row=0, column=2, padx=3)
        self.btn_auto = ttk.Button(bar, text="▶ Reproducir", command=self.alternar_auto)
        self.btn_auto.grid(row=0, column=3, padx=3)
        ttk.Label(bar, text="Velocidad:").grid(row=0, column=4, padx=(12, 2))
        self.velocidad = tk.Scale(bar, from_=200, to=2000, orient="horizontal",
                                  length=120, showvalue=False)
        self.velocidad.set(900)
        self.velocidad.grid(row=0, column=5)
        ttk.Label(bar, text="(ms)").grid(row=0, column=6)

        # Registro de pasos
        frame_log = ttk.Frame(root, padding=(8, 0, 8, 8))
        frame_log.pack(fill="both")
        self.log = tk.Listbox(frame_log, height=6, font=("Consolas", 9))
        sb = ttk.Scrollbar(frame_log, command=self.log.yview)
        self.log.config(yscrollcommand=sb.set)
        self.log.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Leyenda
        leyenda = ttk.Frame(root, padding=(8, 0, 8, 8))
        leyenda.pack()
        for color, txt in [(COLOR_GRUPO, "Subgrupo"), (COLOR_TOMAR, "temp (i)"),
                           (COLOR_COMPARA, "Comparado"), (COLOR_HUECO, "Posición j"),
                           (COLOR_DESPLAZA, "Desplazado"), (COLOR_INSERTA, "Insertado")]:
            tk.Label(leyenda, bg=color, width=2).pack(side="left", padx=(6, 2))
            ttk.Label(leyenda, text=txt).pack(side="left")

        self.cargar()

    # ----- Control -----
    def cargar(self):
        try:
            datos = [int(x) for x in self.entrada.get().split()]
            if len(datos) < 2:
                raise ValueError
            if any(d < 0 for d in datos):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingresa al menos 2 números enteros "
                                          "positivos separados por espacios.")
            return
        self.detener_auto()
        self.pasos = generar_pasos(datos)
        self.indice = 0
        self.log.delete(0, "end")
        self.mostrar()

    def reiniciar(self):
        self.detener_auto()
        self.indice = 0
        self.mostrar()

    def siguiente(self):
        if self.indice < len(self.pasos) - 1:
            self.indice += 1
            self.mostrar()
        else:
            self.detener_auto()

    def anterior(self):
        if self.indice > 0:
            self.indice -= 1
            self.mostrar()

    def alternar_auto(self):
        if self.auto:
            self.detener_auto()
        else:
            if self.indice >= len(self.pasos) - 1:
                self.indice = 0
            self.auto = True
            self.btn_auto.config(text="⏸ Pausar")
            self.ciclo_auto()

    def ciclo_auto(self):
        if not self.auto:
            return
        if self.indice < len(self.pasos) - 1:
            self.indice += 1
            self.mostrar()
            self.after_id = self.root.after(self.velocidad.get(), self.ciclo_auto)
        else:
            self.detener_auto()

    def detener_auto(self):
        self.auto = False
        self.btn_auto.config(text="▶ Reproducir")
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    # ----- Dibujo -----
    def mostrar(self):
        p = self.pasos[self.indice]
        self.dibujar(p)

        self.lbl_info.config(text=p["msg"])
        gap = p["gap"] if p["gap"] is not None else "-"
        i = p["i"] if p["i"] is not None else "-"
        j = p["j"] if p["j"] is not None else "-"
        temp = p["temp"] if p["temp"] is not None else "-"
        self.lbl_vars.config(text=f"gap = {gap}   i = {i}   j = {j}   temp = {temp}")
        self.lbl_paso.config(text=f"Paso {self.indice} de {len(self.pasos) - 1}")

        # Registro acumulado hasta el paso actual
        self.log.delete(0, "end")
        for k in range(self.indice + 1):
            self.log.insert("end", f"{k:>3}. {self.pasos[k]['msg']}")
        self.log.see("end")

    def color_barra(self, idx, p):
        kind, gap, i, j, comp = p["kind"], p["gap"], p["i"], p["j"], p["comp"]

        if kind == "fin":
            return COLOR_INSERTA
        if gap is None:
            return COLOR_NORMAL

        color = COLOR_NORMAL
        # Subgrupo del incremento actual (mismo residuo que i)
        if i is not None and idx % gap == i % gap:
            color = COLOR_GRUPO

        if kind == "tomar" and idx == i:
            color = COLOR_TOMAR
        elif kind == "comparar":
            if idx == comp[0]:
                color = COLOR_COMPARA
            elif idx == comp[1]:
                color = COLOR_HUECO
        elif kind == "desplazar":
            if idx == comp[1]:
                color = COLOR_DESPLAZA
            elif idx == comp[0]:
                color = COLOR_HUECO
        elif kind == "detener":
            if idx == comp[0]:
                color = COLOR_COMPARA
            elif idx == comp[1]:
                color = COLOR_HUECO
        elif kind == "insertar" and idx == comp[0]:
            color = COLOR_INSERTA
        return color

    def dibujar(self, p):
        c = self.canvas
        c.delete("all")
        arr = p["arr"]
        n = len(arr)
        maximo = max(max(arr), 1)

        margen_izq, margen_der = 30, 150       # espacio a la derecha para temp
        base_y = self.ALTO - 40
        alto_max = self.ALTO - 110
        area = self.ANCHO - margen_izq - margen_der
        ancho_slot = area / n
        ancho_barra = min(ancho_slot * 0.7, 90)

        # Línea base
        c.create_line(margen_izq - 10, base_y, margen_izq + area, base_y, fill="#555")

        for idx, val in enumerate(arr):
            x_centro = margen_izq + ancho_slot * idx + ancho_slot / 2
            x1, x2 = x_centro - ancho_barra / 2, x_centro + ancho_barra / 2
            h = max(10, (val / maximo) * alto_max)
            y1 = base_y - h
            c.create_rectangle(x1, y1, x2, base_y,
                               fill=self.color_barra(idx, p), outline="#37474F", width=2)
            c.create_text(x_centro, y1 - 12, text=str(val), font=("Segoe UI", 12, "bold"))
            c.create_text(x_centro, base_y + 16, text=f"[{idx}]", font=("Consolas", 10))

        # Flechas / marcas de i y j
        if p["i"] is not None and p["kind"] != "fin":
            self.marca(p["i"], "i", "#F9A825", margen_izq, ancho_slot, base_y + 32)
        if p["j"] is not None and p["kind"] in ("comparar", "desplazar", "detener", "insertar"):
            pos = p["comp"][0] if p["kind"] == "insertar" else p["j"]
            self.marca(pos, "j", "#EF6C00", margen_izq, ancho_slot, base_y + 32, desplazar=14)

        # Recuadro de temp
        if p["temp"] is not None and p["kind"] != "fin":
            tx = margen_izq + area + 40
            ht = max(10, (p["temp"] / maximo) * alto_max)
            c.create_text(tx + 35, 25, text="temp", font=("Segoe UI", 11, "bold"))
            c.create_rectangle(tx, base_y - ht, tx + 70, base_y,
                               fill=COLOR_TOMAR, outline="#37474F", width=2, dash=(4, 2))
            c.create_text(tx + 35, base_y - ht - 12, text=str(p["temp"]),
                          font=("Segoe UI", 12, "bold"))

        # Título del gap
        if p["gap"] is not None:
            c.create_text(10, 12, anchor="w", text=f"Incremento (gap) = {p['gap']}",
                          font=("Segoe UI", 12, "bold"), fill="#1565C0")

    def marca(self, idx, texto, color, margen_izq, ancho_slot, y, desplazar=0):
        x = margen_izq + ancho_slot * idx + ancho_slot / 2 + desplazar
        self.canvas.create_text(x, y, text=f"▲{texto}", fill=color,
                                font=("Segoe UI", 10, "bold"))


if __name__ == "__main__":
    root = tk.Tk()
    AppShell(root)
    root.mainloop()
