import tkinter as tk
from tkinter import messagebox

# ---------- Colores ----------
COLOR_NORMAL = "#4A90D9"
COLOR_COMPARA = "#F5C518"
COLOR_INTERCAMBIO = "#E74C3C"
COLOR_ORDENADO = "#2ECC71"

# ---------- Estado global de la simulación ----------
estado = {
    "pasos": [],
    "indice": -1,
    "auto": False,
    "after_id": None,
}

widgets = {}


# =====================================================
#  LÓGICA: genera todos los pasos de la prueba de escritorio
# =====================================================
def arreglo_a_texto(arr):
    return " ".join(str(x) for x in arr)


def generar_pasos(datos):
    """Ejecuta burbuja y guarda cada paso para poder simularlo."""
    arr = list(datos)
    n = len(arr)
    pasos = []
    ordenados = set()
    total_intercambios = 0

    pasos.append({
        "arr": arr[:], "comp": (), "ordenados": set(), "color": COLOR_NORMAL,
        "texto": f"Arreglo original: {arreglo_a_texto(arr)}\n",
    })

    for i in range(n - 1):
        pasos.append({
            "arr": arr[:], "comp": (), "ordenados": set(ordenados),
            "color": COLOR_NORMAL,
            "texto": f"PASADA {i + 1}: i = {i}",
        })
        hubo_intercambio = False
        paso = 1

        for j in range(n - 1 - i):
            a, b = arr[j], arr[j + 1]
            if a > b:
                pasos.append({
                    "arr": arr[:], "comp": (j, j + 1), "ordenados": set(ordenados),
                    "color": COLOR_COMPARA,
                    "texto": f"  Paso {paso}: j = {j} -> {a} > {b} (verdadero) -> intercambiar",
                })
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                total_intercambios += 1
                hubo_intercambio = True
                pasos.append({
                    "arr": arr[:], "comp": (j, j + 1), "ordenados": set(ordenados),
                    "color": COLOR_INTERCAMBIO,
                    "texto": f"          arr[{j}] <-> arr[{j + 1}] -> {arreglo_a_texto(arr)}",
                })
            else:
                pasos.append({
                    "arr": arr[:], "comp": (j, j + 1), "ordenados": set(ordenados),
                    "color": COLOR_COMPARA,
                    "texto": f"  Paso {paso}: j = {j} -> {a} > {b} (falso) -> no intercambia",
                })
            paso += 1

        ordenados.add(n - 1 - i)
        if not hubo_intercambio:
            ordenados = set(range(n))
        pasos.append({
            "arr": arr[:], "comp": (), "ordenados": set(ordenados),
            "color": COLOR_NORMAL,
            "texto": f"  Resultado: {arreglo_a_texto(arr)}\n",
        })
        if not hubo_intercambio:
            pasos.append({
                "arr": arr[:], "comp": (), "ordenados": set(ordenados),
                "color": COLOR_NORMAL,
                "texto": "  No hubo intercambios -> el arreglo ya está ordenado\n",
            })
            break

    pasos.append({
        "arr": arr[:], "comp": (), "ordenados": set(range(n)), "color": COLOR_NORMAL,
        "texto": f"Total de intercambios: {total_intercambios}\n\n"
                 f"Arreglo ordenado: {arreglo_a_texto(arr)}",
    })
    return pasos


# =====================================================
#  DIBUJO: columnas verticales
# =====================================================
def dibujar_columnas(arr, comp, ordenados, color_comp):
    canvas = widgets["canvas"]
    canvas.delete("all")
    n = len(arr)
    if n == 0:
        return

    ancho = int(canvas["width"])
    alto = int(canvas["height"])
    margen = 30
    base = alto - 40
    max_alto = alto - 100
    maximo = max(arr)
    espacio = (ancho - 2 * margen) / n
    ancho_col = espacio * 0.7

    for k, valor in enumerate(arr):
        x0 = margen + k * espacio + (espacio - ancho_col) / 2
        x1 = x0 + ancho_col
        altura = (valor / maximo) * max_alto if maximo > 0 else 0
        y0 = base - altura

        if k in comp:
            color = color_comp
        elif k in ordenados:
            color = COLOR_ORDENADO
        else:
            color = COLOR_NORMAL

        canvas.create_rectangle(x0, y0, x1, base, fill=color, outline="black", width=2)
        canvas.create_text((x0 + x1) / 2, y0 - 12, text=str(valor),
                           font=("Arial", 14, "bold"))
        canvas.create_text((x0 + x1) / 2, base + 15, text=f"arr[{k}]",
                           font=("Arial", 10))
    canvas.create_line(margen - 10, base, ancho - margen + 10, base, width=2)


def mostrar_paso(i):
    paso = estado["pasos"][i]
    dibujar_columnas(paso["arr"], paso["comp"], paso["ordenados"], paso["color"])

    log = widgets["log"]
    log.config(state="normal")
    log.insert("end", paso["texto"] + "\n")
    log.see("end")
    log.config(state="disabled")

    widgets["estado"].config(text=f"Paso {i} de {len(estado['pasos']) - 1}")


# =====================================================
#  CONTROLES
# =====================================================
def leer_datos():
    texto = widgets["entrada"].get().replace(",", " ").split()
    try:
        datos = [int(x) for x in texto]
    except ValueError:
        messagebox.showerror("Error", "Escribe solo números enteros separados por espacios.")
        return None
    if len(datos) < 2:
        messagebox.showerror("Error", "Escribe al menos 2 números.")
        return None
    if min(datos) < 0:
        messagebox.showerror("Error", "Usa números enteros positivos.")
        return None
    if len(datos) > 15:
        messagebox.showerror("Error", "Máximo 15 números.")
        return None
    return datos


def pausar_auto():
    if estado["after_id"] is not None:
        widgets["ventana"].after_cancel(estado["after_id"])
        estado["after_id"] = None
    estado["auto"] = False
    widgets["btn_auto"].config(text="Automático")


def limpiar_log():
    widgets["log"].config(state="normal")
    widgets["log"].delete("1.0", "end")
    widgets["log"].config(state="disabled")


def iniciar():
    """Lee los datos, genera los pasos y muestra el estado inicial."""
    pausar_auto()
    datos = leer_datos()
    if datos is None:
        return
    estado["pasos"] = generar_pasos(datos)
    estado["indice"] = 0
    limpiar_log()
    mostrar_paso(0)


def siguiente():
    if not estado["pasos"]:
        iniciar()
        return
    if estado["indice"] < len(estado["pasos"]) - 1:
        estado["indice"] += 1
        mostrar_paso(estado["indice"])
    else:
        pausar_auto()


def ciclo_auto():
    if not estado["auto"]:
        return
    if estado["indice"] >= len(estado["pasos"]) - 1:
        pausar_auto()
        return
    siguiente()
    retraso = widgets["velocidad"].get()
    estado["after_id"] = widgets["ventana"].after(retraso, ciclo_auto)


def alternar_auto():
    if estado["auto"]:
        pausar_auto()
        return
    if not estado["pasos"]:
        iniciar()
        if not estado["pasos"]:
            return
    estado["auto"] = True
    widgets["btn_auto"].config(text="Pausar")
    ciclo_auto()


# =====================================================
#  INTERFAZ
# =====================================================
def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Ordenación Burbuja - Prueba de escritorio")
    widgets["ventana"] = ventana

    # Barra superior
    barra = tk.Frame(ventana)
    barra.pack(pady=8)

    tk.Label(barra, text="Datos:").pack(side="left")
    entrada = tk.Entry(barra, width=30)
    entrada.insert(0, "64 25 12 22 11")
    entrada.pack(side="left", padx=5)
    widgets["entrada"] = entrada

    tk.Button(barra, text="Iniciar / Reiniciar", command=iniciar).pack(side="left", padx=3)
    tk.Button(barra, text="Siguiente paso", command=siguiente).pack(side="left", padx=3)
    btn_auto = tk.Button(barra, text="Automático", command=alternar_auto)
    btn_auto.pack(side="left", padx=3)
    widgets["btn_auto"] = btn_auto

    # Velocidad
    vel = tk.Frame(ventana)
    vel.pack()
    tk.Label(vel, text="Pausa entre pasos (ms):").pack(side="left")
    velocidad = tk.Scale(vel, from_=100, to=2000, orient="horizontal", length=200)
    velocidad.set(800)
    velocidad.pack(side="left")
    widgets["velocidad"] = velocidad

    # Leyenda
    leyenda = tk.Frame(ventana)
    leyenda.pack(pady=4)
    for texto, color in [("Normal", COLOR_NORMAL), ("Comparando", COLOR_COMPARA),
                         ("Intercambio", COLOR_INTERCAMBIO), ("Ordenado", COLOR_ORDENADO)]:
        tk.Label(leyenda, width=2, bg=color).pack(side="left", padx=(10, 2))
        tk.Label(leyenda, text=texto).pack(side="left")

    # Canvas con columnas verticales
    canvas = tk.Canvas(ventana, width=700, height=360, bg="white",
                       highlightthickness=1, highlightbackground="gray")
    canvas.pack(padx=10, pady=5)
    widgets["canvas"] = canvas

    widgets["estado"] = tk.Label(ventana, text="Pulsa 'Iniciar / Reiniciar'",
                                 font=("Arial", 11, "bold"))
    widgets["estado"].pack()

    # Registro de la prueba de escritorio
    marco_log = tk.Frame(ventana)
    marco_log.pack(padx=10, pady=8, fill="both", expand=True)
    scroll = tk.Scrollbar(marco_log)
    scroll.pack(side="right", fill="y")
    log = tk.Text(marco_log, height=12, font=("Courier New", 10),
                  yscrollcommand=scroll.set, state="disabled")
    log.pack(side="left", fill="both", expand=True)
    scroll.config(command=log.yview)
    widgets["log"] = log

    return ventana


def main():
    ventana = crear_interfaz()
    iniciar()
    ventana.mainloop()


if __name__ == "__main__":
    main()
