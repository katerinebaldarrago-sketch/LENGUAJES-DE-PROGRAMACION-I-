import tkinter as tk
from tkinter import messagebox

NUMEROS_INICIALES = "64 25 12 22 11"

# ---------------------------------------------------------------
# PALETA DE COLORES (rosa / celeste / morado)
# ---------------------------------------------------------------
FONDO        = "#f7f0fb"   # lila muy claro
TITULO       = "#6a1b9a"   # morado
BARRA_NORMAL = "#8e44ad"   # morado medio
BARRA_COMP   = "#4fc3f7"   # celeste
BARRA_INTER  = "#ec407a"   # rosa
BOTON        = "#8e44ad"   # morado
BOTON_TXT    = "white"
RESULTADO    = "#c2185b"   # rosa oscuro
FINAL        = "#7b1fa2"   # morado
TEXTO_NORMAL = "#6a1b9a"
TEXTO_ROJO   = "#ec407a"   # rosa (antes rojo)

# ---------------------------------------------------------------
# FUNCIONES DEL ALGORITMO
# ---------------------------------------------------------------
def formato(arreglo):
    return "[" + ", ".join(str(x) for x in arreglo) + "]"


def intercambiar(arreglo, a, b):
    aux = arreglo[a]
    arreglo[a] = arreglo[b]
    arreglo[b] = aux


def ordenar_burbuja_con_eventos(numeros):
    arreglo = numeros[:]
    n = len(arreglo)
    pasos = []
    eventos = []

    pasos.append(("titulo", "Metodo de Ordenacion Burbuja"))
    pasos.append(("normal", "Ejemplo: Numeros = " + formato(arreglo)))
    pasos.append(("normal", ""))
    pasos.append(("rojo", "Prueba de escritorio:"))
    for k in range(n):
        pasos.append(("normal", f"   Numeros[{k}] = {arreglo[k]}"))

    for i in range(n - 1):
        pasos.append(("normal", ""))
        pasos.append(("rojo", f"Pasada {i + 1}: (Cuando i={i})  j varia 0 a {n - 2 - i}"))
        eventos.append({"tipo": "pasada", "arreglo": arreglo[:]})

        for j in range(n - 1 - i):
            comparacion = f"   j={j}: {arreglo[j]}>{arreglo[j + 1]}?"
            eventos.append({"tipo": "comparar", "i": j, "j": j + 1, "arreglo": arreglo[:]})
            if arreglo[j] > arreglo[j + 1]:
                intercambiar(arreglo, j, j + 1)
                pasos.append(("normal", f"{comparacion} Si, intercambio  <->  {formato(arreglo)}"))
                eventos.append({"tipo": "intercambio", "i": j, "j": j + 1, "arreglo": arreglo[:]})
            else:
                pasos.append(("normal", f"{comparacion} No"))

        pasos.append(("resultado", f"   Resultado: {formato(arreglo)}"))

    pasos.append(("normal", ""))
    pasos.append(("final", f"Resultado final: {formato(arreglo)}"))
    eventos.append({"tipo": "fin", "arreglo": arreglo[:]})
    return arreglo, pasos, eventos


def leer_numeros(texto):
    partes = texto.replace(",", " ").split()
    if len(partes) < 2:
        raise ValueError("Ingresa al menos 2 numeros.")
    return [int(p) for p in partes]


# ---------------------------------------------------------------
# INTERFAZ
# ---------------------------------------------------------------
def mostrar_pasos(salida, pasos):
    salida.config(state="normal")
    salida.delete("1.0", tk.END)
    for etiqueta, texto in pasos:
        salida.insert(tk.END, texto + "\n", etiqueta)
    salida.config(state="disabled")


class AnimadorBarras:
    def __init__(self, canvas):
        self.canvas = canvas
        self.arreglo = []
        self.barras = []
        self.animando = False

    def dibujar(self, arreglo, resaltar=None, intercambio=None):
        self.canvas.delete("all")
        self.arreglo = arreglo[:]
        self.barras = []
        ancho_total = int(self.canvas.winfo_width()) or 640
        alto_total = int(self.canvas.winfo_height()) or 260
        margen = 20
        if not arreglo:
            return
        max_val = max(arreglo) or 1
        n = len(arreglo)
        espacio = (ancho_total - 2 * margen) / n
        ancho_barra = min(espacio * 0.7, 70)

        for idx, valor in enumerate(arreglo):
            alto = (valor / max_val) * (alto_total - 60)
            x0 = margen + idx * espacio + (espacio - ancho_barra) / 2
            x1 = x0 + ancho_barra
            y1 = alto_total - 30
            y0 = y1 - alto

            color = BARRA_NORMAL
            if resaltar and idx in resaltar:
                color = BARRA_COMP
            if intercambio and idx in intercambio:
                color = BARRA_INTER

            rect = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
            texto = self.canvas.create_text((x0 + x1) / 2, y0 - 12,
                                            text=str(valor),
                                            font=("Segoe UI", 10, "bold"),
                                            fill=TEXTO_NORMAL)
            self.barras.append((rect, texto))

    def animar_eventos(self, eventos, al_terminar=None):
        self.animando = True
        indice = [0]

        def paso():
            if indice[0] >= len(eventos):
                self.animando = False
                if al_terminar:
                    al_terminar()
                return
            ev = eventos[indice[0]]
            indice[0] += 1

            if ev["tipo"] == "comparar":
                self.dibujar(ev["arreglo"], resaltar=(ev["i"], ev["j"]))
                delay = 300
            elif ev["tipo"] == "intercambio":
                self.dibujar(ev["arreglo"], intercambio=(ev["i"], ev["j"]))
                delay = 500
            elif ev["tipo"] == "pasada":
                self.dibujar(ev["arreglo"])
                delay = 250
            else:
                self.dibujar(ev["arreglo"])
                delay = 300

            self.canvas.after(delay, paso)

        paso()


# ---------------------------------------------------------------
# ACCIONES
# ---------------------------------------------------------------
def accion_ordenar(entrada, salida, lbl_resultado, animador):
    try:
        numeros = leer_numeros(entrada.get())
    except ValueError as error:
        messagebox.showerror("Dato invalido", f"Revisa los numeros ingresados.\n{error}")
        return
    if animador.animando:
        return
    ordenado, pasos, eventos = ordenar_burbuja_con_eventos(numeros)
    mostrar_pasos(salida, pasos)
    lbl_resultado.config(text="Ordenado: " + formato(ordenado))
    animador.dibujar(numeros)
    animador.animar_eventos(eventos)


def accion_limpiar(entrada, salida, lbl_resultado, animador):
    entrada.delete(0, tk.END)
    entrada.insert(0, NUMEROS_INICIALES)
    salida.config(state="normal")
    salida.delete("1.0", tk.END)
    salida.config(state="disabled")
    lbl_resultado.config(text="")
    try:
        animador.dibujar(leer_numeros(NUMEROS_INICIALES))
    except Exception:
        animador.canvas.delete("all")


def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Metodo de Ordenacion Burbuja")
    ventana.geometry("720x820")
    ventana.configure(bg=FONDO)

    tk.Label(ventana, text="Metodo de Ordenacion Burbuja",
             font=("Segoe UI", 18, "bold"), fg=TITULO, bg=FONDO).pack(pady=(15, 5))

    marco = tk.Frame(ventana, bg=FONDO)
    marco.pack(pady=5)
    tk.Label(marco, text="Numeros (separados por espacio):",
             font=("Segoe UI", 11), fg=TITULO, bg=FONDO).grid(row=0, column=0, padx=5)
    entrada = tk.Entry(marco, font=("Segoe UI", 12), width=28, justify="center",
                       fg=TITULO, highlightbackground="#ce93d8", highlightcolor=BARRA_INTER)
    entrada.insert(0, NUMEROS_INICIALES)
    entrada.grid(row=0, column=1, padx=5)

    marco_botones = tk.Frame(ventana, bg=FONDO)
    marco_botones.pack(pady=8)

    lbl_resultado = tk.Label(ventana, text="", font=("Segoe UI", 13, "bold"),
                             fg=RESULTADO, bg=FONDO)

    # Canvas de barras
    marco_barras = tk.Frame(ventana, bg="white", bd=1, relief="solid")
    marco_barras.pack(fill="x", padx=15, pady=(5, 10))
    canvas = tk.Canvas(marco_barras, bg="white", height=260, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    animador = AnimadorBarras(canvas)

    # Cuadro de texto
    marco_texto = tk.Frame(ventana)
    marco_texto.pack(fill="both", expand=True, padx=15, pady=5)
    barra = tk.Scrollbar(marco_texto)
    barra.pack(side="right", fill="y")
    salida = tk.Text(marco_texto, font=("Consolas", 11), bg="white",
                     yscrollcommand=barra.set, state="disabled", wrap="none")
    salida.pack(side="left", fill="both", expand=True)
    barra.config(command=salida.yview)

    salida.tag_config("titulo", foreground=TITULO,      font=("Consolas", 13, "bold"))
    salida.tag_config("rojo",   foreground=TEXTO_ROJO,  font=("Consolas", 11, "bold"))
    salida.tag_config("normal", foreground=TEXTO_NORMAL)
    salida.tag_config("resultado", foreground="#4a148c", font=("Consolas", 11, "bold"))
    salida.tag_config("final",  foreground=FINAL,       font=("Consolas", 12, "bold"))

    tk.Button(marco_botones, text="Ordenar", font=("Segoe UI", 11, "bold"),
              bg=BOTON, fg=BOTON_TXT, activebackground=BARRA_INTER,
              activeforeground="white", width=12, relief="flat",
              command=lambda: accion_ordenar(entrada, salida, lbl_resultado, animador)).pack(side="left", padx=6)
    tk.Button(marco_botones, text="Limpiar", font=("Segoe UI", 11),
              bg="#ce93d8", fg=TITULO, activebackground=BARRA_COMP,
              activeforeground="white", width=12, relief="flat",
              command=lambda: accion_limpiar(entrada, salida, lbl_resultado, animador)).pack(side="left", padx=6)

    lbl_resultado.pack(pady=8)

    ventana.update_idletasks()
    try:
        animador.dibujar(leer_numeros(NUMEROS_INICIALES))
    except Exception:
        pass

    return ventana


def main():
    ventana = crear_interfaz()
    ventana.mainloop()


if __name__ == "__main__":
    main()
