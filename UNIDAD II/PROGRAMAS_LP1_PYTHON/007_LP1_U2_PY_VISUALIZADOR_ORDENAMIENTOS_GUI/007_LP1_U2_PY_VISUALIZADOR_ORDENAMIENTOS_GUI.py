"""
Visualizador de algoritmos de ordenamiento (tkinter)
- Seleccion, Burbuja, Insercion, Insercion con incremento (Shell) y Quick Sort
- Barras animadas + prueba de escritorio en tabla
- Panel con el codigo C++ del metodo: la linea que se ejecuta se ilumina
- Tonos morados y azules
"""
import random
import re
import tkinter as tk
from tkinter import ttk, messagebox

# ----------------------------------------------------------------------
# Paleta (morados y azules)
# ----------------------------------------------------------------------
BG = "#120e2b"          # fondo general
PANEL = "#1d1744"       # paneles
PANEL2 = "#2a2060"      # paneles claros
TXT = "#e8e0ff"         # texto
MUTED = "#a99ee0"       # texto secundario
BTN_PURPLE = "#7b2cbf"
BTN_PURPLE_H = "#9d4edd"
BTN_BLUE = "#3a5ce5"
BTN_BLUE_H = "#5b7bff"

COLORES = {
    "normal": "#4361ee",   # azul
    "cmp": "#a06cd5",      # morado (se compara)
    "swap": "#d8b4fe",     # lila (se mueve / intercambia)
    "pivot": "#5a189a",    # morado oscuro (pivote / menor actual)
    "key": "#90e0ef",      # celeste (clave / posicion actual)
    "sorted": "#48bfe3",   # azul claro (ya ordenado)
}
LEYENDA = [
    ("normal", "Sin procesar"),
    ("cmp", "Comparando"),
    ("swap", "Intercambio / desplazo"),
    ("pivot", "Pivote / menor"),
    ("key", "Clave / posicion"),
    ("sorted", "Ordenado"),
]


# ----------------------------------------------------------------------
# Codigo C++ que se muestra en el panel (la linea resaltada sigue la ejecucion)
# ----------------------------------------------------------------------
CODIGO = {
    "Seleccion": """void seleccion(int d[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int menor = i;
        for (int j = i + 1; j < n; j++) {
            if (d[j] < d[menor])
                menor = j;
        }
        if (menor != i)
            swap(d[i], d[menor]);
    }
}""",
    "Burbuja": """void burbuja(int d[], int n) {
    for (int p = 1; p < n; p++) {
        bool hubo = false;
        for (int j = 0; j < n - p; j++) {
            if (d[j] > d[j + 1]) {
                swap(d[j], d[j + 1]);
                hubo = true;
            }
        }
        if (!hubo) break;
    }
}""",
    "Insercion": """void insercion(int d[], int n) {
    for (int i = 1; i < n; i++) {
        int clave = d[i];
        int j = i - 1;
        while (j >= 0 && d[j] > clave) {
            d[j + 1] = d[j];
            j--;
        }
        d[j + 1] = clave;
    }
}""",
    "Insercion con incremento": """void shell(int d[], int n) {
    for (int inc = n / 2; inc > 0; inc /= 2) {
        for (int i = inc; i < n; i++) {
            int clave = d[i];
            int j = i;
            while (j >= inc && d[j - inc] > clave) {
                d[j] = d[j - inc];
                j -= inc;
            }
            d[j] = clave;
        }
    }
}""",
    "Quick Sort": """void quickSort(int d[], int ini, int fin) {
    if (ini < fin) {
        int p = particion(d, ini, fin);
        quickSort(d, ini, p - 1);
        quickSort(d, p + 1, fin);
    }
}

int particion(int d[], int ini, int fin) {
    int pivote = d[fin];
    int i = ini - 1;
    for (int j = ini; j < fin; j++) {
        if (d[j] <= pivote) {
            i++;
            swap(d[i], d[j]);
        }
    }
    swap(d[i + 1], d[fin]);
    return i + 1;
}""",
}
CODIGO = {k: v.split("\n") for k, v in CODIGO.items()}


# ----------------------------------------------------------------------
# Algoritmos como generadores.
# Cada paso hace: yield (copia_del_arreglo, marcas, fila_de_tabla, linea_cpp)
#   marcas: {indice: rol}   fila: (referencia, comparacion, accion) o None
#   linea_cpp: indice (desde 0) de la linea de CODIGO que se esta ejecutando
# ----------------------------------------------------------------------
def mk(done, *pares):
    m = {k: "sorted" for k in done}
    for idx, rol in pares:
        m[idx] = rol
    return m


def seleccion(a):
    n = len(a)
    yield list(a), {}, None, 0
    done = set()
    for i in range(n - 1):
        ref = f"Pasada {i + 1}"
        m = i
        yield list(a), mk(done, (i, "key")), None, 1
        yield list(a), mk(done, (i, "key")), None, 2
        yield list(a), mk(done, (i, "key")), None, 3
        for j in range(i + 1, n):
            si = a[j] < a[m]
            yield (list(a), mk(done, (i, "key"), (m, "pivot"), (j, "cmp")),
                   (ref, f"{a[j]} < {a[m]}", f"Si: menor en pos {j}" if si else "No"), 4)
            if si:
                m = j
                yield list(a), mk(done, (i, "key"), (m, "pivot")), None, 5
        if m != i:
            yield list(a), mk(done, (i, "key"), (m, "pivot")), None, 7
            a[i], a[m] = a[m], a[i]
            yield (list(a), mk(done, (i, "swap"), (m, "swap")),
                   (ref, "-", f"Intercambio [{i}] <-> [{m}]"), 8)
        else:
            yield list(a), mk(done, (i, "key")), (ref, "-", "Sin intercambio"), 7
        done.add(i)


def burbuja(a):
    n = len(a)
    yield list(a), {}, None, 0
    done = set()
    for p in range(1, n):
        ref = f"Pasada {p}"
        hubo = False
        yield list(a), mk(done), None, 1
        yield list(a), mk(done), None, 2
        yield list(a), mk(done), None, 3
        for j in range(n - p):
            c = f"{a[j]} > {a[j + 1]}"
            if a[j] > a[j + 1]:
                yield list(a), mk(done, (j, "cmp"), (j + 1, "cmp")), None, 4
                a[j], a[j + 1] = a[j + 1], a[j]
                yield (list(a), mk(done, (j, "swap"), (j + 1, "swap")),
                       (ref, c, f"Si: intercambio [{j}] <-> [{j + 1}]"), 5)
                hubo = True
                yield list(a), mk(done, (j, "swap"), (j + 1, "swap")), None, 6
            else:
                yield (list(a), mk(done, (j, "cmp"), (j + 1, "cmp")),
                       (ref, c, "No cambia"), 4)
        done.add(n - p)
        yield list(a), mk(done), None, 9
        if not hubo:
            break


def insercion(a):
    n = len(a)
    yield list(a), {}, None, 0
    done = {0}
    for i in range(1, n):
        ref = f"Pasada {i}"
        clave = a[i]
        j = i - 1
        yield list(a), mk(done, (i, "key")), None, 1
        yield (list(a), mk(done, (i, "key")),
               (ref, f"clave = {clave}", "Tomo la clave"), 2)
        yield list(a), mk(done, (i, "key")), None, 3
        cortado = False
        while j >= 0:
            c = f"{a[j]} > {clave}"
            if a[j] > clave:
                yield list(a), mk(done, (j, "cmp"), (j + 1, "key")), None, 4
                a[j + 1] = a[j]
                yield (list(a), mk(done, (j + 1, "swap"), (j, "cmp")),
                       (ref, c, f"Si: desplazo a pos {j + 1}"), 5)
                yield list(a), mk(done, (j + 1, "swap"), (j, "cmp")), None, 6
                j -= 1
            else:
                yield (list(a), mk(done, (j, "cmp"), (j + 1, "key")),
                       (ref, c, "No: se detiene"), 4)
                cortado = True
                break
        if not cortado:
            yield list(a), mk(done, (j + 1, "key")), None, 4
        a[j + 1] = clave
        yield (list(a), mk(done, (j + 1, "key")),
               (ref, "-", f"Inserta {clave} en pos {j + 1}"), 8)
        done = set(range(i + 1))


def shell(a):
    n = len(a)
    yield list(a), {}, None, 0
    inc = n // 2
    ronda = 0
    while inc > 0:
        ronda += 1
        ref = f"Ronda {ronda} (inc={inc})"
        yield list(a), mk(set()), None, 1
        for i in range(inc, n):
            clave = a[i]
            j = i
            yield list(a), mk(set(), (i, "key")), None, 2
            yield (list(a), mk(set(), (i, "key")),
                   (ref, f"clave = {clave}", f"Tomo la clave de pos {i}"), 3)
            yield list(a), mk(set(), (i, "key")), None, 4
            cortado = False
            while j >= inc:
                c = f"{a[j - inc]} > {clave}"
                if a[j - inc] > clave:
                    yield list(a), mk(set(), (j - inc, "cmp"), (j, "key")), None, 5
                    a[j] = a[j - inc]
                    yield (list(a), mk(set(), (j, "swap"), (j - inc, "cmp")),
                           (ref, c, f"Si: desplazo a pos {j}"), 6)
                    yield list(a), mk(set(), (j, "swap"), (j - inc, "cmp")), None, 7
                    j -= inc
                else:
                    yield (list(a), mk(set(), (j - inc, "cmp"), (j, "key")),
                           (ref, c, "No: se detiene"), 5)
                    cortado = True
                    break
            if not cortado:
                yield list(a), mk(set(), (j, "key")), None, 5
            a[j] = clave
            yield (list(a), mk(set(), (j, "key")),
                   (ref, "-", f"Inserta {clave} en pos {j}"), 9)
        inc //= 2


def _particion(a, lo, hi, done, st):
    st["n"] += 1
    ref = f"Particion {st['n']} [{lo}..{hi}]"
    pivote = a[hi]
    i = lo - 1
    yield list(a), mk(done, (hi, "pivot")), None, 8
    yield (list(a), mk(done, (hi, "pivot")),
           (ref, f"pivote = {pivote}", f"i = {i}"), 9)
    yield list(a), mk(done, (hi, "pivot")), None, 10
    yield list(a), mk(done, (hi, "pivot")), None, 11
    for j in range(lo, hi):
        c = f"{a[j]} <= {pivote}"
        if a[j] <= pivote:
            yield list(a), mk(done, (hi, "pivot"), (j, "cmp")), None, 12
            i += 1
            yield list(a), mk(done, (hi, "pivot"), (i, "key"), (j, "cmp")), None, 13
            a[i], a[j] = a[j], a[i]
            yield (list(a), mk(done, (hi, "pivot"), (i, "swap"), (j, "swap")),
                   (ref, c, f"Si: i={i}, intercambio [{i}] <-> [{j}]"), 14)
        else:
            yield (list(a), mk(done, (hi, "pivot"), (j, "cmp")), (ref, c, "No"), 12)
    p = i + 1
    a[p], a[hi] = a[hi], a[p]
    done.add(p)
    yield (list(a), mk(done, (p, "pivot")),
           (ref, f"P = i+1 = {i}+1 = {p}", f"Intercambio [{p}] <-> [{hi}]"), 17)
    yield list(a), mk(done, (p, "pivot")), None, 18
    return p


def _qs(a, lo, hi, done, st):
    if lo < hi:
        yield list(a), mk(done), None, 1
        yield list(a), mk(done), None, 2
        p = yield from _particion(a, lo, hi, done, st)
        yield list(a), mk(done), None, 3
        yield from _qs(a, lo, p - 1, done, st)
        yield list(a), mk(done), None, 4
        yield from _qs(a, p + 1, hi, done, st)
    elif lo == hi:
        done.add(lo)


def quick(a):
    yield list(a), mk(set()), None, 0
    yield from _qs(a, 0, len(a) - 1, set(), {"n": 0})


ALGORITMOS = {
    "Seleccion": seleccion,
    "Burbuja": burbuja,
    "Insercion": insercion,
    "Insercion con incremento": shell,
    "Quick Sort": quick,
}


# ----------------------------------------------------------------------
# Interfaz grafica
# ----------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de ordenamientos")
        self.geometry("1420x800")
        self.minsize(1100, 680)
        self.configure(bg=BG)

        self.original = [64, 25, 12, 22, 11]
        self.estado = (list(self.original), {})
        self.gen = None
        self.algo = None
        self.corriendo = False
        self.after_id = None
        self.pasos = 0
        self.botones_algo = {}

        self._estilos()
        self._construir()
        self.mostrar_codigo(None)
        self.dibujar(*self.estado)

    # ---------- construccion ----------
    def _estilos(self):
        st = ttk.Style(self)
        st.theme_use("clam")
        st.configure("Treeview", background=PANEL, fieldbackground=PANEL,
                     foreground=TXT, rowheight=24, borderwidth=0,
                     font=("Consolas", 10))
        st.configure("Treeview.Heading", background=BTN_PURPLE, foreground="white",
                     font=("Segoe UI", 10, "bold"), relief="flat")
        st.map("Treeview", background=[("selected", BTN_BLUE)])
        st.map("Treeview.Heading", background=[("active", BTN_PURPLE_H)])
        st.configure("Vertical.TScrollbar", background=PANEL2, troughcolor=PANEL,
                     bordercolor=PANEL, arrowcolor=TXT)

    def _boton(self, padre, texto, comando, color, hover, ancho=None):
        b = tk.Button(padre, text=texto, command=comando, bg=color, fg="white",
                      activebackground=hover, activeforeground="white",
                      relief="flat", bd=0, cursor="hand2", padx=12, pady=7,
                      font=("Segoe UI", 10, "bold"), width=ancho)
        b.bind("<Enter>", lambda e: b.config(bg=hover) if b["state"] != "disabled" else None)
        b.bind("<Leave>", lambda e: b.config(bg=b._color))
        b._color = color
        b._hover = hover
        return b

    def _construir(self):
        # Titulo
        tk.Label(self, text="Visualizador de algoritmos de ordenamiento",
                 bg=BG, fg=TXT, font=("Segoe UI", 18, "bold")).pack(pady=(12, 2))
        tk.Label(self, text="Elige un metodo y mira como se ordenan las barras y que linea de C++ se ejecuta",
                 bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack()

        # Entrada de valores
        f1 = tk.Frame(self, bg=PANEL)
        f1.pack(fill="x", padx=14, pady=(10, 4))
        tk.Label(f1, text="Valores (separados por coma o espacio):", bg=PANEL,
                 fg=TXT, font=("Segoe UI", 10)).pack(side="left", padx=(10, 6), pady=10)
        self.entrada = tk.Entry(f1, width=34, bg=PANEL2, fg="white",
                                insertbackground="white", relief="flat",
                                font=("Consolas", 11))
        self.entrada.insert(0, ", ".join(map(str, self.original)))
        self.entrada.pack(side="left", padx=4, ipady=4)
        self.entrada.bind("<Return>", lambda e: self.cargar())
        self._boton(f1, "Cargar valores", self.cargar, BTN_BLUE, BTN_BLUE_H).pack(side="left", padx=6)
        self._boton(f1, "Aleatorio", self.aleatorio, BTN_PURPLE, BTN_PURPLE_H).pack(side="left", padx=2)

        # Botones de algoritmos
        f2 = tk.Frame(self, bg=BG)
        f2.pack(fill="x", padx=14, pady=4)
        for k, nombre in enumerate(ALGORITMOS):
            color, hover = (BTN_PURPLE, BTN_PURPLE_H) if k % 2 == 0 else (BTN_BLUE, BTN_BLUE_H)
            b = self._boton(f2, nombre, lambda n=nombre: self.iniciar(n), color, hover)
            b.pack(side="left", expand=True, fill="x", padx=3)
            self.botones_algo[nombre] = b

        # Controles
        f3 = tk.Frame(self, bg=BG)
        f3.pack(fill="x", padx=14, pady=4)
        self.b_pausa = self._boton(f3, "Pausar", self.pausar, PANEL2, BTN_PURPLE)
        self.b_pausa.pack(side="left", padx=3)
        self.b_paso = self._boton(f3, "Paso a paso", self.un_paso, PANEL2, BTN_BLUE)
        self.b_paso.pack(side="left", padx=3)
        self._boton(f3, "Reiniciar", self.reiniciar, PANEL2, BTN_PURPLE).pack(side="left", padx=3)
        tk.Label(f3, text="Velocidad:", bg=BG, fg=TXT,
                 font=("Segoe UI", 10)).pack(side="left", padx=(24, 4))
        self.vel = tk.Scale(f3, from_=1, to=100, orient="horizontal", length=200,
                            bg=BG, fg=TXT, troughcolor=PANEL2, highlightthickness=0,
                            activebackground=BTN_PURPLE_H, bd=0)
        self.vel.set(60)
        self.vel.pack(side="left")
        self.lbl_estado = tk.Label(f3, text="Listo", bg=BG, fg=MUTED,
                                   font=("Segoe UI", 10, "italic"))
        self.lbl_estado.pack(side="right", padx=8)

        # Cuerpo: izquierda (barras + tabla) y derecha (codigo C++)
        cuerpo = tk.Frame(self, bg=BG)
        cuerpo.pack(fill="both", expand=True, padx=14, pady=(2, 12))

        der = tk.Frame(cuerpo, bg=PANEL)
        der.pack(side="right", fill="y", padx=(10, 0))
        izq = tk.Frame(cuerpo, bg=BG)
        izq.pack(side="left", fill="both", expand=True)

        # --- izquierda: canvas, leyenda, tabla
        self.canvas = tk.Canvas(izq, bg=PANEL, height=300, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, pady=(4, 2))
        self.canvas.bind("<Configure>", lambda e: self.dibujar(*self.estado))

        f4 = tk.Frame(izq, bg=BG)
        f4.pack(fill="x")
        for clave, texto in LEYENDA:
            tk.Label(f4, bg=COLORES[clave], width=2).pack(side="left", padx=(8, 3), pady=4)
            tk.Label(f4, text=texto, bg=BG, fg=MUTED,
                     font=("Segoe UI", 9)).pack(side="left")

        f5 = tk.Frame(izq, bg=BG)
        f5.pack(fill="both", expand=True, pady=(4, 0))
        tk.Label(f5, text="Prueba de escritorio", bg=BG, fg=TXT,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        cols = ("paso", "ref", "comp", "accion", "arreglo")
        self.tabla = ttk.Treeview(f5, columns=cols, show="headings", height=7)
        for c, t, w in zip(cols, ("Paso", "Referencia", "Comparacion", "Accion", "Arreglo"),
                           (45, 170, 120, 220, 300)):
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=w, anchor="w")
        self.tabla.tag_configure("par", background=PANEL)
        self.tabla.tag_configure("impar", background="#241c52")
        self.tabla.tag_configure("mov", foreground="#d8b4fe")
        sb = ttk.Scrollbar(f5, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tabla.pack(side="left", fill="both", expand=True)

        # --- derecha: codigo C++
        cab = tk.Frame(der, bg=PANEL)
        cab.pack(fill="x", padx=8, pady=(8, 4))
        self.lbl_codigo = tk.Label(cab, text="Codigo C++", bg=PANEL, fg=TXT,
                                   font=("Segoe UI", 11, "bold"))
        self.lbl_codigo.pack(side="left")
        self._boton(cab, "Copiar", self.copiar_codigo, BTN_BLUE, BTN_BLUE_H).pack(side="right")

        marco = tk.Frame(der, bg=PANEL)
        marco.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.codigo = tk.Text(marco, width=54, bg="#17123a", fg=TXT, relief="flat",
                              font=("Consolas", 11), wrap="none", cursor="arrow",
                              padx=6, pady=6, spacing1=2, spacing3=2,
                              selectbackground=BTN_BLUE, highlightthickness=0)
        sy = ttk.Scrollbar(marco, orient="vertical", command=self.codigo.yview)
        sx = ttk.Scrollbar(marco, orient="horizontal", command=self.codigo.xview)
        self.codigo.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        sy.pack(side="right", fill="y")
        sx.pack(side="bottom", fill="x")
        self.codigo.pack(side="left", fill="both", expand=True)
        # etiquetas de color (la ultima creada tiene mayor prioridad)
        self.codigo.tag_configure("num", foreground="#6f64b5")
        self.codigo.tag_configure("kw", foreground="#9d8cff")
        self.codigo.tag_configure("tipo", foreground="#4cc9f0")
        self.codigo.tag_configure("lit", foreground="#d8b4fe")
        self.codigo.tag_configure("actual", background="#6d4aff", foreground="#ffffff")

    # ---------- panel de codigo ----------
    def mostrar_codigo(self, nombre):
        t = self.codigo
        t.config(state="normal")
        t.delete("1.0", "end")
        if nombre is None:
            self.lbl_codigo.config(text="Codigo C++")
            t.insert("1.0", "\n  Elige un metodo para ver\n  su codigo en C++ aqui.\n\n"
                            "  La linea que se esta\n  ejecutando se ilumina.")
            t.tag_add("lit", "1.0", "end")
            t.config(state="disabled")
            return
        self.lbl_codigo.config(text=f"Codigo C++ - {nombre}")
        lineas = CODIGO[nombre]
        for k, linea in enumerate(lineas, start=1):
            t.insert("end", f"{k:>2}  {linea}\n")
        # colores de sintaxis
        for k, linea in enumerate(lineas, start=1):
            t.tag_add("num", f"{k}.0", f"{k}.2")
            for patron, tag in ((r"\b(for|while|if|else|return|break)\b", "kw"),
                                (r"\b(void|int|bool)\b", "tipo"),
                                (r"\b(true|false)\b|\b\d+\b", "lit")):
                for m in re.finditer(patron, linea):
                    t.tag_add(tag, f"{k}.{m.start() + 4}", f"{k}.{m.end() + 4}")
        t.config(state="disabled")

    def resaltar(self, linea):
        t = self.codigo
        t.tag_remove("actual", "1.0", "end")
        if linea is None:
            return
        n = linea + 1
        t.tag_add("actual", f"{n}.0", f"{n}.end+1c")
        t.see(f"{n}.0")

    def copiar_codigo(self):
        if self.algo is None:
            messagebox.showinfo("Elige un metodo", "Primero pulsa uno de los metodos de ordenamiento.")
            return
        self.clipboard_clear()
        self.clipboard_append("\n".join(CODIGO[self.algo]))
        self.lbl_estado.config(text="Codigo C++ copiado al portapapeles")

    # ---------- datos ----------
    def _leer_valores(self):
        txt = self.entrada.get().replace(",", " ").split()
        try:
            vals = [int(x) for x in txt]
        except ValueError:
            messagebox.showerror("Valores no validos", "Escribe solo numeros enteros.")
            return None
        if not 2 <= len(vals) <= 30:
            messagebox.showerror("Cantidad no valida", "Ingresa entre 2 y 30 valores.")
            return None
        return vals

    def cargar(self):
        vals = self._leer_valores()
        if vals is None:
            return
        self.original = vals
        self.reiniciar()

    def aleatorio(self):
        n = random.randint(8, 15)
        self.original = random.sample(range(5, 100), n)
        self.entrada.delete(0, "end")
        self.entrada.insert(0, ", ".join(map(str, self.original)))
        self.reiniciar()

    # ---------- dibujo ----------
    def dibujar(self, arr, marcas):
        self.estado = (arr, marcas)
        c = self.canvas
        c.delete("all")
        w, h = c.winfo_width(), c.winfo_height()
        if w < 50 or h < 50 or not arr:
            return
        n = len(arr)
        margen, arriba, abajo = 24, 26, 26
        bw = (w - 2 * margen) / n
        lo, hi = min(arr), max(arr)
        rango = hi - lo + 1
        base = h - abajo
        alto = h - arriba - abajo
        tam = max(7, min(13, int(bw / 3.2)))
        for i, v in enumerate(arr):
            x0 = margen + i * bw + bw * 0.08
            x1 = margen + (i + 1) * bw - bw * 0.08
            y0 = base - alto * (v - lo + 1) / rango
            rol = marcas.get(i, "normal")
            borde = "#ffffff" if rol in ("swap", "pivot", "key") else COLORES[rol]
            c.create_rectangle(x0, y0, x1, base, fill=COLORES[rol], outline=borde,
                               width=2 if borde == "#ffffff" else 1)
            c.create_text((x0 + x1) / 2, y0 - 9, text=str(v), fill=TXT,
                          font=("Segoe UI", tam, "bold"))
            c.create_text((x0 + x1) / 2, base + 12, text=str(i), fill=MUTED,
                          font=("Segoe UI", max(7, tam - 2)))

    # ---------- ejecucion ----------
    def _cancelar(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.corriendo = False

    def _marcar_boton(self, nombre):
        for n, b in self.botones_algo.items():
            b.config(relief="sunken" if n == nombre else "flat")

    def _preparar(self, nombre):
        self._cancelar()
        self.algo = nombre
        self.pasos = 0
        self.tabla.delete(*self.tabla.get_children())
        trabajo = list(self.original)
        self.gen = ALGORITMOS[nombre](trabajo)
        self.estado = (list(self.original), {})
        self.dibujar(*self.estado)
        self.mostrar_codigo(nombre)
        self._marcar_boton(nombre)
        self.lbl_estado.config(text=f"{nombre}: inicial {self.original}")

    def iniciar(self, nombre):
        self._preparar(nombre)
        self.corriendo = True
        self.b_pausa.config(text="Pausar")
        self._tick()

    def _tick(self):
        if not self.corriendo:
            return
        if self._paso():
            delay = 1060 - self.vel.get() * 10
            self.after_id = self.after(delay, self._tick)

    def _paso(self):
        if self.gen is None:
            return False
        try:
            arr, marcas, fila, linea = next(self.gen)
        except StopIteration:
            self._terminar()
            return False
        self.dibujar(arr, marcas)
        self.resaltar(linea)
        if fila:
            self.pasos += 1
            ref, comp, acc = fila
            n = len(self.tabla.get_children())
            tags = ["par" if n % 2 == 0 else "impar"]
            if any(p in acc for p in ("ntercambio", "splazo", "nserta")):
                tags.append("mov")
            self.tabla.insert("", "end", values=(self.pasos, ref, comp, acc,
                                                 "[" + ", ".join(map(str, arr)) + "]"),
                              tags=tags)
            self.tabla.yview_moveto(1)
            self.lbl_estado.config(text=f"{self.algo}: paso {self.pasos}")
        return True

    def _terminar(self):
        self._cancelar()
        self.gen = None
        arr = self.estado[0]
        self.dibujar(arr, {i: "sorted" for i in range(len(arr))})
        self.resaltar(None)
        self.lbl_estado.config(text=f"{self.algo}: ordenado en {self.pasos} pasos")
        self.b_pausa.config(text="Pausar")

    def pausar(self):
        if self.gen is None:
            return
        if self.corriendo:
            self._cancelar()
            self.b_pausa.config(text="Continuar")
        else:
            self.corriendo = True
            self.b_pausa.config(text="Pausar")
            self._tick()

    def un_paso(self):
        if self.gen is None:
            if self.algo is None:
                messagebox.showinfo("Elige un metodo", "Primero pulsa uno de los metodos de ordenamiento.")
                return
            self._preparar(self.algo)
        if self.corriendo:
            self._cancelar()
            self.b_pausa.config(text="Continuar")
        self._paso()

    def reiniciar(self):
        self._cancelar()
        self.gen = None
        self.algo = None
        self.pasos = 0
        self.tabla.delete(*self.tabla.get_children())
        self._marcar_boton(None)
        self.estado = (list(self.original), {})
        self.dibujar(*self.estado)
        self.mostrar_codigo(None)
        self.lbl_estado.config(text="Listo")
        self.b_pausa.config(text="Pausar")


if __name__ == "__main__":
    App().mainloop()
