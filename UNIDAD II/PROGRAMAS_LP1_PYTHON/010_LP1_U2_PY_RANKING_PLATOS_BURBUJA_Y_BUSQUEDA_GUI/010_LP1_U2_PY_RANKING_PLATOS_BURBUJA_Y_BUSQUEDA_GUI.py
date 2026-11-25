import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import random
import statistics
import difflib
from datetime import datetime

# Datos iniciales de ejemplo (puedes agregar, editar o borrar platos en vivo)
PLATOS_INICIALES = [
    ["Ceviche Clásico", 28.0, 12],   # Ingreso: 336.0
    ["Lomo Saltado", 26.0, 10],      # Ingreso: 260.0
    ["Ají de Gallina", 20.0, 12],    # Ingreso: 240.0
    ["Arroz con Pollo", 15.0, 15],   # Ingreso: 225.0
    ["Causa Rellena", 12.0, 14],     # Ingreso: 168.0
    ["Anticuchos", 22.0, 8],         # Ingreso: 176.0
]

POOL_PLATOS = [
    "Ceviche Clásico", "Lomo Saltado", "Ají de Gallina", "Arroz con Pollo",
    "Causa Rellena", "Anticuchos", "Rocoto Relleno", "Pachamanca", "Trucha Frita",
    "Chairo Puneño", "Cuy Chactado", "Tallarín Saltado", "Papa a la Huancaína",
    "Sopa Wantán", "Pollo a la Brasa", "Tacu Tacu", "Cau Cau", "Parihuela",
]

UMBRAL_DEFECTO = 250.0


# ==============================================================================
# ALGORITMOS: BURBUJA CON BANDERA (2 CRITERIOS) Y BÚSQUEDA SECUENCIAL
# ==============================================================================
def burbuja_bandera_dos_criterios(platos, frames=None):
    """
    Ordena de MAYOR a MENOR usando dos criterios:
      Criterio 1: Ingreso total (índice 3), descendente.
      Criterio 2: Unidades vendidas (índice 2), descendente (desempate).
    Si 'frames' es una lista, guarda cada comparación para animarla/explicarla:
      (copia_del_arreglo, j, hubo_intercambio, numero_de_pasada)
    Retorna: (lista_ordenada, comparaciones, intercambios, pasadas)
    """
    arr = [fila[:] for fila in platos]
    n = len(arr)
    comparaciones = 0
    intercambios = 0
    pasadas = 0

    if frames is not None:
        frames.append(([f[:] for f in arr], None, False, 0))

    for i in range(n - 1):
        bandera_cambio = False
        pasadas += 1
        for j in range(n - 1 - i):
            comparaciones += 1
            actual = (arr[j][3], arr[j][2])
            siguiente = (arr[j + 1][3], arr[j + 1][2])
            cambio = actual < siguiente

            if cambio:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambios += 1
                bandera_cambio = True

            if frames is not None:
                frames.append(([f[:] for f in arr], j, cambio, pasadas))

        if not bandera_cambio:
            break

    return arr, comparaciones, intercambios, pasadas


def busqueda_secuencial_nombre(ranking, nombre_buscado):
    """Retorna: (puesto_1_based_o_None, plato_o_None, pasos_recorridos)"""
    objetivo = nombre_buscado.strip().lower()
    pasos = 0
    for idx, plato in enumerate(ranking):
        pasos += 1
        if plato[0].strip().lower() == objetivo:
            return idx + 1, plato, pasos
    return None, None, pasos


def busqueda_secuencial_primer_menor_umbral(ranking, umbral=250.0):
    """Primer plato del ranking con ingreso < umbral. Retorna (puesto, plato, pasos)"""
    pasos = 0
    for idx, plato in enumerate(ranking):
        pasos += 1
        if plato[3] < umbral:
            return idx + 1, plato, pasos
    return None, None, pasos


def busqueda_secuencial_todos_menor_umbral(ranking, umbral=250.0):
    """Todos los platos con ingreso < umbral. Retorna (lista_de_(puesto, plato), pasos)"""
    encontrados = []
    pasos = 0
    for idx, plato in enumerate(ranking):
        pasos += 1
        if plato[3] < umbral:
            encontrados.append((idx + 1, plato))
    return encontrados, pasos


# ==============================================================================
# TOOLTIP SENCILLO
# ==============================================================================
class Tooltip:
    def __init__(self, widget, texto):
        self.widget = widget
        self.texto = texto
        self.tip = None
        widget.bind("<Enter>", self.mostrar, add="+")
        widget.bind("<Leave>", self.ocultar, add="+")

    def mostrar(self, _=None):
        if self.tip:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        tk.Label(self.tip, text=self.texto, bg="#FDE68A", fg="#1E1B4B",
                 font=("Segoe UI", 8), padx=6, pady=2, relief="solid", bd=1).pack()

    def ocultar(self, _=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


# ==============================================================================
# INTERFAZ GRÁFICA DINÁMICA (TONOS AZULES Y MORADOS)
# ==============================================================================
class AppRankingPlatosDinamico:
    def __init__(self, root):
        self.root = root
        self.root.title("Ranking de Platos Dinámico PRO - Burbuja con Bandera & Búsqueda")
        self.root.geometry("1300x840")
        self.root.minsize(1100, 740)

        # Paleta Azul y Morado
        self.c_bg = "#0E0B24"
        self.c_panel = "#1A153E"
        self.c_card = "#251E54"
        self.c_header = "#3B0764"
        self.c_btn_morado = "#7C3AED"
        self.c_btn_azul = "#2563EB"
        self.c_btn_rosa = "#DB2777"
        self.c_btn_gris = "#4338CA"
        self.c_lavanda = "#C4B5FD"
        self.c_celeste = "#7DD3FC"
        self.c_texto = "#F8FAFC"

        self.platos_base = [fila[:] for fila in PLATOS_INICIALES]
        self.historial = []            # pila para deshacer
        self.resaltados = set()        # puestos resaltados
        self.umbral_actual = UMBRAL_DEFECTO
        self.frames = []
        self.original = []
        self.anim_data = None
        self.anim_hl = None
        self.anim_job = None
        self.anim_i = 0
        self.animando = False
        self.barras = []
        self.reporte_plano = ""

        self.var_umbral = tk.StringVar(value="250")
        self.var_filtro = tk.StringVar()
        self.var_metrica = tk.StringVar(value="ingreso")
        self.var_vel = tk.IntVar(value=450)

        self.construir_menu()
        self.construir_ui()
        self.configurar_atajos()
        self.recalcular_todo()
        self.actualizar_reloj()
        self.status("Listo ✨ Agrega platos, ordena y busca. (Ayuda → Atajos de teclado)")

    # ------------------------------------------------------------------ utilidades UI
    def boton(self, parent, texto, color, comando, tip=None, **kw):
        b = tk.Button(parent, text=texto, bg=color, fg="white", activebackground=self.c_lavanda,
                      activeforeground="#1E1B4B", font=("Segoe UI", 9, "bold"), relief="flat",
                      padx=kw.pop("padx", 10), pady=kw.pop("pady", 4), cursor="hand2",
                      command=comando, **kw)
        if tip:
            Tooltip(b, tip)
        return b

    def status(self, texto):
        self.lbl_status.config(text=texto)

    def actualizar_reloj(self):
        self.lbl_reloj.config(text=datetime.now().strftime("📅 %d/%m/%Y  🕒 %H:%M:%S"))
        self.root.after(1000, self.actualizar_reloj)

    def crear_texto(self, parent):
        marco = tk.Frame(parent, bg=self.c_card)
        sb = tk.Scrollbar(marco)
        sb.pack(side="right", fill="y")
        txt = tk.Text(marco, bg=self.c_card, fg=self.c_texto, font=("Segoe UI", 9.5), wrap="word",
                      relief="flat", padx=10, pady=8, yscrollcommand=sb.set, state="disabled")
        txt.pack(side="left", fill="both", expand=True)
        sb.config(command=txt.yview)
        txt.tag_configure("h", foreground=self.c_lavanda, font=("Segoe UI", 10.5, "bold"))
        txt.tag_configure("ok", foreground="#86EFAC")
        txt.tag_configure("warn", foreground="#F9A8D4")
        txt.tag_configure("info", foreground=self.c_celeste)
        txt.tag_configure("dim", foreground="#94A3B8", font=("Segoe UI", 8.5, "italic"))
        txt.tag_configure("n", foreground=self.c_texto)
        return marco, txt

    def escribir(self, txt, partes):
        txt.config(state="normal")
        txt.delete("1.0", tk.END)
        for contenido, tag in partes:
            txt.insert(tk.END, contenido, tag)
        txt.config(state="disabled")

    # ------------------------------------------------------------------ menú
    def construir_menu(self):
        barra = tk.Menu(self.root)
        m_arch = tk.Menu(barra, tearoff=0)
        m_arch.add_command(label="📂 Importar CSV…", command=self.importar_csv)
        m_arch.add_command(label="💾 Exportar ranking a CSV…  (Ctrl+S)", command=self.exportar_csv)
        m_arch.add_command(label="📝 Exportar reporte a TXT…", command=self.exportar_reporte)
        m_arch.add_separator()
        m_arch.add_command(label="Salir", command=self.root.destroy)
        barra.add_cascade(label="Archivo", menu=m_arch)

        m_edit = tk.Menu(barra, tearoff=0)
        m_edit.add_command(label="↶ Deshacer  (Ctrl+Z)", command=self.deshacer)
        m_edit.add_command(label="🎲 Datos aleatorios  (Ctrl+R)", command=self.datos_aleatorios)
        m_edit.add_command(label="↺ Restaurar ejemplo  (F5)", command=self.restaurar_ejemplo)
        barra.add_cascade(label="Edición", menu=m_edit)

        m_ayuda = tk.Menu(barra, tearoff=0)
        m_ayuda.add_command(label="⌨️ Atajos de teclado", command=self.mostrar_atajos)
        m_ayuda.add_command(label="ℹ️ Acerca del algoritmo", command=self.mostrar_acerca)
        barra.add_cascade(label="Ayuda", menu=m_ayuda)
        self.root.config(menu=barra)

    def mostrar_atajos(self):
        messagebox.showinfo(
            "Atajos de teclado",
            "Enter (en formulario)  →  Guardar / Añadir\n"
            "Enter (en búsqueda)  →  Buscar plato\n"
            "Supr  →  Eliminar plato(s) seleccionado(s)\n"
            "Ctrl+Z  →  Deshacer\n"
            "Ctrl+S  →  Exportar CSV\n"
            "Ctrl+R  →  Datos aleatorios\n"
            "F5  →  Restaurar ejemplo\n"
            "Esc  →  Limpiar resaltado y campos\n"
            "Doble clic en fila  →  Resaltar en el gráfico\n"
            "Clic derecho en fila  →  Menú contextual\n"
            "Clic en una barra  →  Resalta ese plato"
        )

    def mostrar_acerca(self):
        messagebox.showinfo(
            "Burbuja con bandera",
            "Burbuja con bandera compara pares adyacentes y los intercambia si están\n"
            "en el orden incorrecto. Si en una pasada NO hubo intercambios, la bandera\n"
            "queda en falso y el algoritmo se detiene antes.\n\n"
            "Criterios (de mayor a menor):\n  1° Ingreso total (precio × unidades)\n  2° Unidades vendidas (desempate)\n\n"
            "Mejor caso: n-1 comparaciones, 0 intercambios, 1 pasada.\n"
            "Peor caso: n(n-1)/2 comparaciones e intercambios."
        )

    # ------------------------------------------------------------------ construcción
    def construir_ui(self):
        # Encabezado
        header = tk.Frame(self.root, bg=self.c_header, pady=10, padx=20)
        header.pack(fill="x")
        tk.Label(
            header,
            text="🍽️ RANKING DINÁMICO DE PLATOS • BURBUJA CON BANDERA & BÚSQUEDA SECUENCIAL",
            font=("Segoe UI", 14, "bold"), bg=self.c_header, fg="#F3E8FF"
        ).pack(side="left")

        # Barra de herramientas
        tools = tk.Frame(self.root, bg=self.c_panel, padx=14, pady=6)
        tools.pack(fill="x")
        for texto, color, cmd, tip in [
            ("↶ Deshacer", self.c_btn_gris, self.deshacer, "Revierte el último cambio (Ctrl+Z)"),
            ("↺ Restaurar", "#4C1D95", self.restaurar_ejemplo, "Vuelve a los 6 platos de ejemplo (F5)"),
            ("🎲 Aleatorio", self.c_btn_morado, self.datos_aleatorios, "Genera platos y ventas al azar (Ctrl+R)"),
            ("📂 Importar CSV", self.c_btn_azul, self.importar_csv, "Columnas: Plato, Precio, Unidades"),
            ("💾 Exportar CSV", self.c_btn_azul, self.exportar_csv, "Guarda el ranking actual (Ctrl+S)"),
            ("📝 Exportar reporte", self.c_btn_morado, self.exportar_reporte, "Guarda el reporte completo en .txt"),
            ("🧹 Limpiar resaltado", self.c_btn_rosa, self.limpiar_resaltado, "Quita los resaltados (Esc)"),
        ]:
            self.boton(tools, texto, color, cmd, tip).pack(side="left", padx=(0, 6))

        # Barra de estado (abajo)
        barra = tk.Frame(self.root, bg=self.c_header, padx=12, pady=4)
        barra.pack(side="bottom", fill="x")
        self.lbl_status = tk.Label(barra, text="", bg=self.c_header, fg="#F3E8FF", font=("Segoe UI", 9), anchor="w")
        self.lbl_status.pack(side="left", fill="x", expand=True)
        self.lbl_reloj = tk.Label(barra, text="", bg=self.c_header, fg=self.c_celeste, font=("Segoe UI", 9, "bold"))
        self.lbl_reloj.pack(side="right")

        # Cuerpo principal
        main = tk.Frame(self.root, bg=self.c_bg, padx=14, pady=12)
        main.pack(fill="both", expand=True)

        left = tk.Frame(main, bg=self.c_bg)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.Frame(main, bg=self.c_panel, padx=12, pady=12, width=500)
        right.pack(side="right", fill="both")
        right.pack_propagate(False)

        self.construir_formulario(left)
        self.construir_tabla(left)
        self.construir_grafico(left)
        self.construir_panel_derecho(right)

    def construir_formulario(self, left):
        form_box = tk.LabelFrame(
            left, text=" ➕ Gestión Dinámica de Platos (Agregar / Actualizar / Eliminar) ",
            font=("Segoe UI", 10, "bold"), bg=self.c_panel, fg=self.c_celeste,
            bd=1, relief="solid", padx=10, pady=8)
        form_box.pack(fill="x", pady=(0, 8))

        def lbl(txt, c):
            tk.Label(form_box, text=txt, bg=self.c_panel, fg=self.c_texto,
                     font=("Segoe UI", 9)).grid(row=0, column=c, padx=(0, 4))

        def ent(w, c):
            e = tk.Entry(form_box, width=w, bg=self.c_bg, fg="white", insertbackground="white", font=("Segoe UI", 9))
            e.grid(row=0, column=c, padx=(0, 10))
            e.bind("<Return>", lambda ev: self.guardar_plato())
            return e

        lbl("Plato:", 0); self.ent_nombre = ent(18, 1)
        lbl("Precio (S/):", 2); self.ent_precio = ent(8, 3)
        lbl("Unidades:", 4); self.ent_unidades = ent(8, 5)

        self.boton(form_box, "Guardar / Añadir", self.c_btn_morado, self.guardar_plato,
                   "Si el plato ya existe, lo actualiza", padx=8, pady=3).grid(row=0, column=6, padx=(0, 5))
        self.boton(form_box, "Eliminar Sel.", self.c_btn_azul, self.eliminar_seleccionado,
                   "Elimina los platos seleccionados (Supr)", padx=8, pady=3).grid(row=0, column=7, padx=(0, 5))
        self.boton(form_box, "✖ Campos", self.c_btn_gris, self.limpiar_campos,
                   "Vacía el formulario", padx=8, pady=3).grid(row=0, column=8)

    def construir_tabla(self, left):
        fila_titulo = tk.Frame(left, bg=self.c_bg)
        fila_titulo.pack(fill="x", pady=(2, 4))
        tk.Label(
            fila_titulo,
            text="🏆 Ranking (1° Ingreso ↓ | 2° Unidades ↓)",
            font=("Segoe UI", 10.5, "bold"), bg=self.c_bg, fg=self.c_lavanda
        ).pack(side="left")

        ent_f = tk.Entry(fila_titulo, textvariable=self.var_filtro, width=18, bg=self.c_panel, fg="white",
                         insertbackground="white", font=("Segoe UI", 9))
        ent_f.pack(side="right")
        tk.Label(fila_titulo, text="🔍 Filtrar:", bg=self.c_bg, fg=self.c_celeste,
                 font=("Segoe UI", 9)).pack(side="right", padx=(0, 4))
        self.var_filtro.trace_add("write", lambda *a: self.actualizar_tabla())

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("MoradoAzul.Treeview", background=self.c_panel, foreground=self.c_texto,
                        fieldbackground=self.c_panel, rowheight=26, font=("Segoe UI", 9.5))
        style.configure("MoradoAzul.Treeview.Heading", background="#4C1D95", foreground="#F3E8FF",
                        font=("Segoe UI", 9.5, "bold"))
        style.map("MoradoAzul.Treeview", background=[("selected", "#6D28D9")])
        style.configure("TNotebook", background=self.c_panel, borderwidth=0)
        style.configure("TNotebook.Tab", background="#312E81", foreground="#E0E7FF",
                        padding=(10, 4), font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.c_btn_morado)])

        cont = tk.Frame(left, bg=self.c_bg)
        cont.pack(fill="x", pady=(0, 8))
        cols = ("Puesto", "Plato", "Precio (S/)", "Unidades", "Ingreso (S/)", "% Total", "vs Promedio")
        self.tree = ttk.Treeview(cont, columns=cols, show="headings", height=7,
                                 style="MoradoAzul.Treeview", selectmode="extended")
        anchos = [80, 150, 85, 75, 95, 70, 105]
        for col, w in zip(cols, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center" if col != "Plato" else "w", width=w)
        sb = ttk.Scrollbar(cont, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="x", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.tag_configure("destacado", background="#5B21B6", foreground="#FFFBEB")
        self.tree.tag_configure("bajo_umbral", background="#1E3A8A", foreground="#E0F2FE")
        self.tree.tag_configure("podio", foreground="#FDE68A")
        self.tree.bind("<<TreeviewSelect>>", self.on_select_fila)
        self.tree.bind("<Delete>", lambda e: self.eliminar_seleccionado())
        self.tree.bind("<Double-1>", self.doble_clic_fila)
        self.tree.bind("<Button-3>", self.menu_contextual)
        self.tree.bind("<Button-2>", self.menu_contextual)

        self.menu_ctx = tk.Menu(self.root, tearoff=0)
        self.menu_ctx.add_command(label="✏️ Cargar en el formulario", command=self.ctx_cargar)
        self.menu_ctx.add_command(label="⭐ Resaltar en el gráfico", command=self.ctx_resaltar)
        self.menu_ctx.add_command(label="📋 Copiar nombre", command=self.ctx_copiar)
        self.menu_ctx.add_separator()
        self.menu_ctx.add_command(label="🗑️ Eliminar", command=self.eliminar_seleccionado)

    def construir_grafico(self, left):
        fila = tk.Frame(left, bg=self.c_bg)
        fila.pack(fill="x", pady=(0, 4))
        tk.Label(fila, text="📊 Gráfico dinámico", font=("Segoe UI", 10, "bold"),
                 bg=self.c_bg, fg=self.c_celeste).pack(side="left")
        for texto, valor in [("Ingreso (S/)", "ingreso"), ("Unidades", "unidades")]:
            tk.Radiobutton(fila, text=texto, value=valor, variable=self.var_metrica, bg=self.c_bg,
                           fg=self.c_texto, selectcolor=self.c_card, activebackground=self.c_bg,
                           activeforeground=self.c_lavanda, font=("Segoe UI", 9),
                           command=self.dibujar_grafico).pack(side="left", padx=(10, 0))
        tk.Label(fila, text="Línea rosa = promedio | Celeste = umbral | Azul ≥ umbral | Morado < umbral",
                 bg=self.c_bg, fg="#94A3B8", font=("Segoe UI", 8)).pack(side="right")

        self.canvas = tk.Canvas(left, bg=self.c_panel, height=250, highlightthickness=1,
                                highlightbackground="#6D28D9")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.dibujar_grafico())
        self.canvas.bind("<Button-1>", self.click_grafico)

    def construir_panel_derecho(self, right):
        # ---- búsqueda
        search_box = tk.Frame(right, bg=self.c_card, padx=10, pady=10)
        search_box.pack(fill="x", pady=(0, 8))
        tk.Label(search_box, text="🔎 Búsqueda Secuencial en Vivo", font=("Segoe UI", 10, "bold"),
                 bg=self.c_card, fg="#EDE9FE").pack(anchor="w")

        row_b = tk.Frame(search_box, bg=self.c_card)
        row_b.pack(fill="x", pady=(6, 0))
        self.ent_buscar = tk.Entry(row_b, bg=self.c_bg, fg="white", insertbackground="white", font=("Segoe UI", 9.5))
        self.ent_buscar.insert(0, "Ceviche Clásico")
        self.ent_buscar.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.ent_buscar.bind("<Return>", lambda e: self.buscar_plato_interactivo())
        self.boton(row_b, "Buscar plato", self.c_btn_morado, self.buscar_plato_interactivo,
                   "Búsqueda secuencial por nombre (Enter)", padx=8).pack(side="left")

        row_u = tk.Frame(search_box, bg=self.c_card)
        row_u.pack(fill="x", pady=(8, 0))
        tk.Label(row_u, text="Umbral S/", bg=self.c_card, fg=self.c_texto, font=("Segoe UI", 9)).pack(side="left")
        e_u = tk.Entry(row_u, textvariable=self.var_umbral, width=7, bg=self.c_bg, fg="white",
                       insertbackground="white", font=("Segoe UI", 9.5), justify="center")
        e_u.pack(side="left", padx=(4, 6))
        e_u.bind("<Return>", lambda e: self.aplicar_umbral())
        self.boton(row_u, "Aplicar", self.c_btn_gris, self.aplicar_umbral,
                   "Cambia el umbral en todo el reporte y el gráfico", padx=6, pady=2).pack(side="left", padx=(0, 6))
        self.boton(row_u, "1° < umbral", self.c_btn_azul, self.buscar_menor_umbral_interactivo,
                   "Primer plato del ranking bajo el umbral", padx=6, pady=2).pack(side="left", padx=(0, 4))
        self.boton(row_u, "Todos < umbral", self.c_btn_rosa, self.buscar_todos_menor_umbral,
                   "Recorre todo el ranking y marca los que no llegan", padx=6, pady=2).pack(side="left")

        self.lbl_busqueda_vivo = tk.Label(search_box, text="Listo para buscar en el ranking ordenado.",
                                          font=("Segoe UI", 9), bg=self.c_card, fg=self.c_celeste,
                                          wraplength=450, justify="left")
        self.lbl_busqueda_vivo.pack(anchor="w", pady=(8, 0))

        # ---- pestañas
        self.nb = ttk.Notebook(right)
        self.nb.pack(fill="both", expand=True)
        f1, self.txt_reporte = self.crear_texto(self.nb)
        f2, self.txt_traza = self.crear_texto(self.nb)
        f3, self.txt_stats = self.crear_texto(self.nb)
        self.nb.add(f1, text="📋 Reporte")
        self.nb.add(f2, text="🫧 Paso a paso")
        self.nb.add(f3, text="📈 Estadísticas")
        self.tab_traza = f2

        # ---- controles de animación y copia
        ctrl = tk.Frame(right, bg=self.c_panel, pady=8)
        ctrl.pack(fill="x")
        self.btn_anim = self.boton(ctrl, "▶ Animar burbuja", self.c_btn_morado, self.toggle_animacion,
                                   "Muestra cada comparación sobre el gráfico (con los datos sin ordenar)")
        self.btn_anim.pack(side="left")
        tk.Label(ctrl, text="  Velocidad:", bg=self.c_panel, fg=self.c_texto, font=("Segoe UI", 8)).pack(side="left")
        tk.Scale(ctrl, from_=900, to=80, orient="horizontal", variable=self.var_vel, showvalue=False,
                 length=90, bg=self.c_panel, fg=self.c_texto, troughcolor=self.c_card,
                 highlightthickness=0, bd=0).pack(side="left", padx=(2, 6))
        self.boton(ctrl, "📋 Copiar", self.c_btn_azul, self.copiar_reporte,
                   "Copia el reporte al portapapeles", padx=8).pack(side="right")

    # ------------------------------------------------------------------ atajos
    def configurar_atajos(self):
        self.root.bind("<Control-z>", lambda e: self.deshacer())
        self.root.bind("<Control-s>", lambda e: self.exportar_csv())
        self.root.bind("<Control-r>", lambda e: self.datos_aleatorios())
        self.root.bind("<F5>", lambda e: self.restaurar_ejemplo())
        self.root.bind("<Escape>", lambda e: (self.limpiar_resaltado(), self.limpiar_campos()))

    # ------------------------------------------------------------------ datos / edición
    def push_undo(self):
        self.historial.append([f[:] for f in self.platos_base])
        if len(self.historial) > 50:
            self.historial.pop(0)

    def deshacer(self):
        if not self.historial:
            self.status("ℹ️ No hay nada que deshacer.")
            return
        self.platos_base = self.historial.pop()
        self.resaltados = set()
        self.recalcular_todo()
        self.status("↶ Último cambio revertido.")

    def guardar_plato(self):
        nombre = self.ent_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Dato faltante", "Escribe el nombre del plato.")
            return
        try:
            precio = float(self.ent_precio.get().replace(",", "."))
            unidades = int(self.ent_unidades.get())
            if precio <= 0 or unidades < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error de formato", "Ingresa un precio mayor a 0 y unidades enteras (>= 0).")
            return

        self.push_undo()
        actualizado = False
        for fila in self.platos_base:
            if fila[0].lower() == nombre.lower():
                fila[0], fila[1], fila[2] = nombre, precio, unidades
                actualizado = True
                break
        if not actualizado:
            self.platos_base.append([nombre, precio, unidades])

        self.limpiar_campos()
        self.resaltados = set()
        self.recalcular_todo()
        self.status(f"{'✏️ Plato actualizado' if actualizado else '➕ Plato añadido'}: {nombre}")

    def limpiar_campos(self):
        for e in (self.ent_nombre, self.ent_precio, self.ent_unidades):
            e.delete(0, tk.END)

    def nombres_seleccionados(self):
        return [self.tree.item(s, "values")[1] for s in self.tree.selection()]

    def eliminar_seleccionado(self):
        nombres = self.nombres_seleccionados()
        if not nombres:
            messagebox.showinfo("Sin selección", "Selecciona un plato de la tabla para eliminarlo.")
            return
        restantes = [p for p in self.platos_base if p[0] not in nombres]
        if not restantes:
            messagebox.showwarning("Mínimo requerido", "Debe quedar al menos 1 plato en el ranking.")
            return
        if len(nombres) > 1 and not messagebox.askyesno("Confirmar", f"¿Eliminar {len(nombres)} platos?"):
            return
        self.push_undo()
        self.platos_base = restantes
        self.resaltados = set()
        self.recalcular_todo()
        self.status(f"🗑️ Eliminado(s): {', '.join(nombres)}")

    def restaurar_ejemplo(self):
        self.push_undo()
        self.platos_base = [fila[:] for fila in PLATOS_INICIALES]
        self.resaltados = set()
        self.var_umbral.set("250")
        self.recalcular_todo()
        self.lbl_busqueda_vivo.config(text="Datos restaurados al ejemplo inicial.")
        self.status("↺ Ejemplo restaurado.")

    def datos_aleatorios(self):
        self.push_undo()
        k = random.randint(6, 9)
        nombres = random.sample(POOL_PLATOS, k)
        self.platos_base = [
            [n, round(random.randint(16, 80) / 2, 1), random.randint(3, 25)] for n in nombres
        ]
        self.resaltados = set()
        self.recalcular_todo()
        self.status(f"🎲 Se generaron {k} platos al azar.")

    def importar_csv(self):
        ruta = filedialog.askopenfilename(title="Importar platos", filetypes=[("CSV", "*.csv"), ("Todos", "*.*")])
        if not ruta:
            return
        try:
            with open(ruta, newline="", encoding="utf-8-sig") as f:
                muestra = f.read(2048)
                f.seek(0)
                try:
                    dialecto = csv.Sniffer().sniff(muestra, delimiters=",;\t")
                except csv.Error:
                    dialecto = csv.excel
                nuevos = []
                for fila in csv.reader(f, dialecto):
                    if len(fila) < 3:
                        continue
                    try:
                        nuevos.append([fila[0].strip(), float(fila[1].replace(",", ".")), int(float(fila[2]))])
                    except ValueError:
                        continue  # encabezado u fila inválida
            if not nuevos:
                messagebox.showwarning("Importar", "No se encontraron filas válidas (Plato, Precio, Unidades).")
                return
            resp = messagebox.askyesnocancel("Importar", f"Se leyeron {len(nuevos)} platos.\n\n"
                                             "Sí = reemplazar los actuales\nNo = agregarlos a los actuales")
            if resp is None:
                return
            self.push_undo()
            if resp:
                self.platos_base = nuevos
            else:
                existentes = {p[0].lower(): p for p in self.platos_base}
                for n in nuevos:
                    if n[0].lower() in existentes:
                        existentes[n[0].lower()][1:] = n[1:]
                    else:
                        self.platos_base.append(n)
            self.resaltados = set()
            self.recalcular_todo()
            self.status(f"📂 Importados {len(nuevos)} platos desde {ruta.split('/')[-1]}")
        except OSError as err:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{err}")

    def exportar_csv(self):
        ruta = filedialog.asksaveasfilename(title="Exportar ranking", defaultextension=".csv",
                                            initialfile="ranking_platos.csv", filetypes=[("CSV", "*.csv")])
        if not ruta:
            return
        try:
            with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(["Puesto", "Plato", "Precio", "Unidades", "Ingreso"])
                for i, p in enumerate(self.ranking, 1):
                    w.writerow([i, p[0], f"{p[1]:.2f}", p[2], f"{p[3]:.2f}"])
            self.status(f"💾 Ranking exportado: {ruta}")
        except OSError as err:
            messagebox.showerror("Error", f"No se pudo guardar:\n{err}")

    def exportar_reporte(self):
        ruta = filedialog.asksaveasfilename(title="Exportar reporte", defaultextension=".txt",
                                            initialfile="reporte_ranking.txt", filetypes=[("Texto", "*.txt")])
        if not ruta:
            return
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(self.reporte_plano)
            self.status(f"📝 Reporte exportado: {ruta}")
        except OSError as err:
            messagebox.showerror("Error", f"No se pudo guardar:\n{err}")

    def copiar_reporte(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.reporte_plano)
        self.status("📋 Reporte copiado al portapapeles.")

    # ------------------------------------------------------------------ selección / menú contextual
    def on_select_fila(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        nombre = self.tree.item(sel[0], "values")[1]
        for p in self.platos_base:
            if p[0] == nombre:
                self.limpiar_campos()
                self.ent_nombre.insert(0, p[0])
                self.ent_precio.insert(0, str(p[1]))
                self.ent_unidades.insert(0, str(p[2]))
                break

    def doble_clic_fila(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.resaltados = {int(item)}
            self.actualizar_tabla()
            self.dibujar_grafico()

    def menu_contextual(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            if item not in self.tree.selection():
                self.tree.selection_set(item)
            self.menu_ctx.tk_popup(event.x_root, event.y_root)

    def ctx_cargar(self):
        self.on_select_fila(None)
        self.ent_nombre.focus_set()

    def ctx_resaltar(self):
        self.resaltados = {int(s) for s in self.tree.selection()}
        self.actualizar_tabla()
        self.dibujar_grafico()

    def ctx_copiar(self):
        nombres = self.nombres_seleccionados()
        if nombres:
            self.root.clipboard_clear()
            self.root.clipboard_append(nombres[0])
            self.status(f"📋 Copiado: {nombres[0]}")

    def limpiar_resaltado(self):
        self.resaltados = set()
        self.actualizar_tabla()
        self.dibujar_grafico()
        self.status("🧹 Resaltado limpiado.")

    # ------------------------------------------------------------------ umbral
    def aplicar_umbral(self):
        try:
            u = float(self.var_umbral.get().replace(",", "."))
            if u < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Umbral inválido", "Ingresa un número mayor o igual a 0.")
            self.var_umbral.set(f"{self.umbral_actual:g}")
            return
        self.umbral_actual = u
        self.resaltados = set()
        self.recalcular_todo()
        self.status(f"🎯 Umbral actualizado a S/ {u:.2f}")

    # ------------------------------------------------------------------ cálculo principal
    def recalcular_todo(self):
        self.detener_animacion(silencioso=True)

        # 1. Ingreso de cada plato: [nombre, precio, unidades, ingreso]
        self.original = [[n, pr, un, round(pr * un, 2)] for n, pr, un in self.platos_base]

        # 2. Burbuja con bandera (2 criterios), guardando los pasos
        self.frames = []
        self.ranking, self.comp, self.inter, self.pas = burbuja_bandera_dos_criterios(self.original, self.frames)

        # 3. Métricas generales
        n = len(self.ranking)
        self.ingreso_total = sum(p[3] for p in self.ranking)
        self.promedio = self.ingreso_total / n
        self.num_sobre_prom = sum(1 for p in self.ranking if p[3] > self.promedio)
        self.unidades_totales = sum(p[2] for p in self.ranking)
        self.mas_vendido = max(self.ranking, key=lambda x: x[2])

        # 4. Búsquedas secuenciales
        u = self.umbral_actual
        self.ejemplo_existente = self.ranking[0][0]
        self.p_ex, self.d_ex, self.pas_ex = busqueda_secuencial_nombre(self.ranking, self.ejemplo_existente)
        self.p_no, _, self.pas_no = busqueda_secuencial_nombre(self.ranking, "Plato Inexistente XYZ")
        self.p_u, self.d_u, self.pas_u = busqueda_secuencial_primer_menor_umbral(self.ranking, u)
        self.lista_u, _ = busqueda_secuencial_todos_menor_umbral(self.ranking, u)

        # 5. Escenarios extra: ya ordenado e invertido
        _, self.comp_ord, self.inter_ord, self.pas_ord = burbuja_bandera_dos_criterios(self.ranking)
        _, self.comp_inv, self.inter_inv, self.pas_inv = burbuja_bandera_dos_criterios(self.ranking[::-1])

        self.actualizar_tabla()
        self.actualizar_reporte()
        self.actualizar_traza()
        self.actualizar_estadisticas()
        self.dibujar_grafico()
        self.status(f"✅ {n} platos | Ingreso total S/ {self.ingreso_total:.2f} | "
                    f"{self.comp} comparaciones, {self.inter} intercambios, {self.pas} pasadas")

    # ------------------------------------------------------------------ tabla
    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        filtro = self.var_filtro.get().strip().lower()
        medallas = {1: "🥇", 2: "🥈", 3: "🥉"}
        for idx, p in enumerate(self.ranking, start=1):
            if filtro and filtro not in p[0].lower():
                continue
            dif = p[3] - self.promedio
            txt_dif = f"+S/{dif:.2f}" if dif >= 0 else f"-S/{abs(dif):.2f}"
            pct = p[3] / self.ingreso_total * 100 if self.ingreso_total else 0
            tags = ()
            if idx in self.resaltados:
                tags = ("destacado",)
            elif p[3] < self.umbral_actual:
                tags = ("bajo_umbral",)
            elif idx <= 3:
                tags = ("podio",)

            self.tree.insert(
                "", "end", iid=str(idx),
                values=(f"{medallas.get(idx, '')} #{idx}".strip(), p[0], f"S/ {p[1]:.2f}", p[2],
                        f"S/ {p[3]:.2f}", f"{pct:.1f}%", txt_dif),
                tags=tags)

    # ------------------------------------------------------------------ reporte
    def actualizar_reporte(self):
        n = len(self.ranking)
        u = self.umbral_actual
        R = []

        def h(t):
            R.append(("\n" + t + "\n", "h"))

        def l(t, tag="n"):
            R.append(("   " + t + "\n", tag))

        R.append((f"Reporte generado: {datetime.now():%d/%m/%Y %H:%M:%S}  |  Umbral: S/ {u:.2f}\n", "dim"))

        h("1️⃣ INGRESO POR PLATO (Precio × Unidades)")
        for p in self.ranking:
            l(f"• {p[0]}: S/ {p[1]:.2f} × {p[2]} = S/ {p[3]:.2f}")

        h("2️⃣ RANKING CON BURBUJA CON BANDERA (2 criterios)")
        l("Criterio 1: mayor ingreso (S/) | Criterio 2: más unidades vendidas.", "dim")
        medallas = {1: "🥇", 2: "🥈", 3: "🥉"}
        for i, p in enumerate(self.ranking, 1):
            l(f"{medallas.get(i, '  ')} #{i}  {p[0]} — S/ {p[3]:.2f} ({p[2]} u)")

        h("3️⃣ RESUMEN DE VENTAS")
        l(f"• Ingreso total: S/ {self.ingreso_total:.2f}")
        l(f"• Ingreso promedio por plato: S/ {self.promedio:.2f}")
        l(f"• Platos que superan el promedio: {self.num_sobre_prom} de {n}")
        l(f"• Unidades totales vendidas: {self.unidades_totales}")
        l(f"• Plato más vendido: {self.mas_vendido[0]} ({self.mas_vendido[2]} unidades)")

        h("4️⃣ BÚSQUEDA SECUENCIAL")
        l(f"• (a) Existe ('{self.d_ex[0]}'): Puesto #{self.p_ex} ({self.pas_ex} comparaciones)", "ok")
        l(f"• (a) No existe ('Plato Inexistente XYZ'): No encontrado ({self.pas_no} comparaciones)", "warn")
        if self.d_u:
            l(f"• (b) 1° con ingreso < S/ {u:.2f}: Puesto #{self.p_u} — {self.d_u[0]} "
              f"(S/ {self.d_u[3]:.2f}, en {self.pas_u} pasos)", "info")
            l(f"• Total de platos bajo el umbral: {len(self.lista_u)} de {n}")
        else:
            l(f"• (b) Ningún plato tiene ingreso < S/ {u:.2f} (revisados {self.pas_u})", "info")

        h("5️⃣ TRABAJO DEL ALGORITMO Y ESCENARIOS EXTRA")
        l(f"• Caso original: {self.comp} comp. | {self.inter} interc. | {self.pas} pasadas")
        l(f"• Ya ordenado:   {self.comp_ord} comp. | {self.inter_ord} interc. | {self.pas_ord} pasadas")
        l(f"• Invertido:     {self.comp_inv} comp. | {self.inter_inv} interc. | {self.pas_inv} pasadas")
        l(f"• Teoría con n = {n}: mejor caso {n - 1} comp.; peor caso {n * (n - 1) // 2} comp.", "dim")

        h("6️⃣ INTERPRETACIÓN DE RESULTADOS")
        lider = self.ranking[0]
        if lider[0] == self.mas_vendido[0]:
            l(f"• {lider[0]} lidera en ingresos y además es el más vendido: precio y demanda se refuerzan.")
        else:
            l(f"• El liderazgo de ingresos no coincide con el más vendido: {lider[0]} lidera con "
              f"S/ {lider[3]:.2f} (precio S/ {lider[1]:.2f}), mientras {self.mas_vendido[0]} vende más "
              f"unidades ({self.mas_vendido[2]}). Un precio mayor puede generar más caja con menos porciones.")
        l(f"• {self.num_sobre_prom} de {n} platos superan el promedio (S/ {self.promedio:.2f}); "
          f"el resto aporta menos de lo esperado.")
        l(f"• La bandera detiene el algoritmo apenas una pasada no hace intercambios: ya ordenado necesita solo "
          f"{self.comp_ord} comparaciones y {self.inter_ord} intercambios, mientras que invertido exige "
          f"{self.comp_inv} comparaciones y {self.inter_inv} intercambios.")
        if self.d_u:
            l(f"• La búsqueda secuencial recorre desde el puesto #1; como el ranking está ordenado, el primer "
              f"plato bajo S/ {u:.2f} marca el 'corte': desde el puesto #{self.p_u} todos quedan por debajo.")
        else:
            l(f"• Todos los platos alcanzan S/ {u:.2f}: la búsqueda recorrió los {n} elementos sin hallar corte.")

        self.escribir(self.txt_reporte, R)
        self.reporte_plano = "".join(t for t, _ in R)

    # ------------------------------------------------------------------ paso a paso
    def actualizar_traza(self):
        R = [("Burbuja con bandera sobre los datos en el orden en que fueron ingresados.\n"
              "Se compara (ingreso, unidades) del par j y j+1; si el de la izquierda es MENOR, se intercambian.\n", "dim")]
        pasadas = {}
        for arr, j, cambio, pas in self.frames[1:]:
            pasadas.setdefault(pas, []).append((arr, j, cambio))

        for pas, eventos in pasadas.items():
            R.append((f"\nPASADA {pas}\n", "h"))
            hubo = False
            for arr, j, cambio in eventos:
                a, b = (arr[j + 1], arr[j]) if cambio else (arr[j], arr[j + 1])  # estado ANTES de comparar
                txt = (f"   j={j}: {a[0]} (S/{a[3]:.0f}, {a[2]}u)  vs  {b[0]} (S/{b[3]:.0f}, {b[2]}u)  → "
                       f"{'INTERCAMBIA' if cambio else 'no cambia'}\n")
                R.append((txt, "warn" if cambio else "n"))
                hubo = hubo or cambio
            if hubo:
                R.append(("   🚩 bandera = VERDADERA → continúa otra pasada\n", "info"))
            else:
                R.append(("   🏁 bandera = FALSA (sin intercambios) → el algoritmo se detiene\n", "ok"))
            R.append(("   Orden: " + " > ".join(p[0] for p in eventos[-1][0]) + "\n", "dim"))

        R.append((f"\nTOTAL: {self.comp} comparaciones | {self.inter} intercambios | {self.pas} pasadas\n", "h"))
        self.escribir(self.txt_traza, R)

    # ------------------------------------------------------------------ estadísticas
    def actualizar_estadisticas(self):
        n = len(self.ranking)
        ingresos = [p[3] for p in self.ranking]
        mediana = statistics.median(ingresos)
        desv = statistics.pstdev(ingresos) if n > 1 else 0.0
        cv = desv / self.promedio * 100 if self.promedio else 0
        precio_prom = sum(p[1] for p in self.ranking) / n
        ticket = self.ingreso_total / self.unidades_totales if self.unidades_totales else 0
        mayor, menor = self.ranking[0], self.ranking[-1]

        acum, k80 = 0.0, 0
        for p in self.ranking:
            acum += p[3]
            k80 += 1
            if self.ingreso_total and acum >= 0.8 * self.ingreso_total:
                break
        top3 = sum(p[3] for p in self.ranking[:3])
        pct3 = top3 / self.ingreso_total * 100 if self.ingreso_total else 0
        menos_vendido = min(self.ranking, key=lambda x: x[2])

        R = [("📈 ESTADÍSTICAS DEL MENÚ\n", "h"),
             (f"\n• Platos en el ranking: {n}\n"
              f"• Mayor ingreso: {mayor[0]} (S/ {mayor[3]:.2f})\n"
              f"• Menor ingreso: {menor[0]} (S/ {menor[3]:.2f})\n"
              f"• Rango de ingresos: S/ {mayor[3] - menor[3]:.2f}\n"
              f"• Mediana de ingresos: S/ {mediana:.2f}\n"
              f"• Desviación estándar: S/ {desv:.2f}  (coef. de variación {cv:.1f}%)\n", "n"),
             ("\n💰 PRECIOS Y VENTAS\n", "h"),
             (f"\n• Precio promedio (simple): S/ {precio_prom:.2f}\n"
              f"• Precio promedio ponderado por unidad vendida: S/ {ticket:.2f}\n"
              f"• Unidades promedio por plato: {self.unidades_totales / n:.1f}\n"
              f"• Menos vendido: {menos_vendido[0]} ({menos_vendido[2]} u)\n", "n"),
             ("\n🎯 CONCENTRACIÓN (Pareto)\n", "h"),
             (f"\n• El Top 3 aporta el {pct3:.1f}% del ingreso total.\n"
              f"• Se necesitan {k80} de {n} platos para alcanzar el 80% del ingreso.\n", "n"),
             (f"\n• Platos bajo el umbral (S/ {self.umbral_actual:.2f}): {len(self.lista_u)} de {n}\n", "info")]
        self.escribir(self.txt_stats, R)

    # ------------------------------------------------------------------ gráfico
    def dibujar_grafico(self):
        c = self.canvas
        c.delete("all")
        self.barras = []
        w, h = c.winfo_width(), c.winfo_height()
        data = self.anim_data if self.anim_data is not None else self.ranking
        if w < 150 or h < 110 or not data:
            return

        idx = 3 if self.var_metrica.get() == "ingreso" else 2
        simb = "S/" if idx == 3 else ""
        vals = [p[idx] for p in data]
        prom = sum(vals) / len(vals)
        u = self.umbral_actual
        max_val = max(max(vals), prom, u if idx == 3 else 0, 1.0)

        ml, mr, ms, mi = 52, 20, 26, 46
        aw = max(w - ml - mr, 60)
        ah = max(h - ms - mi, 40)
        y_base = ms + ah

        # Cuadrícula y eje Y
        for k in range(5):
            v = max_val * k / 4
            y = y_base - (v / max_val) * ah
            c.create_line(ml, y, w - mr, y, fill="#2E2766")
            c.create_text(ml - 6, y, text=f"{v:.0f}", anchor="e", fill="#8B8FC7", font=("Segoe UI", 8))

        titulo = "Ingreso por plato (S/)" if idx == 3 else "Unidades vendidas"
        if self.animando:
            titulo += "  •  ANIMACIÓN (orden de ingreso → ordenado)"
        c.create_text(ml, 10, text=titulo, anchor="w", fill=self.c_lavanda, font=("Segoe UI", 8.5, "bold"))

        # Línea de promedio
        y_prom = y_base - (prom / max_val) * ah
        c.create_line(ml - 5, y_prom, w - mr, y_prom, fill="#F472B6", dash=(5, 4), width=1.8)
        c.create_text(w - mr - 4, y_prom - 9, text=f"Prom: {simb}{prom:.0f}", anchor="e",
                      fill="#F9A8D4", font=("Segoe UI", 8, "bold"))

        # Línea de umbral (solo ingreso)
        if idx == 3:
            y_u = y_base - (u / max_val) * ah
            c.create_line(ml - 5, y_u, w - mr, y_u, fill="#7DD3FC", dash=(2, 3), width=1.5)
            c.create_text(ml + 4, y_u - 9, text=f"Umbral: S/{u:.0f}", anchor="w",
                          fill="#7DD3FC", font=("Segoe UI", 8, "bold"))

        n = len(data)
        hueco = aw / n
        ancho = max(min(hueco * 0.62, 68), 16)
        for i, p in enumerate(data):
            cx = ml + i * hueco + hueco / 2
            x0, x1 = cx - ancho / 2, cx + ancho / 2
            alto = (p[idx] / max_val) * ah
            y0 = y_base - alto

            if self.animando and self.anim_hl and self.anim_hl[0] is not None and i in (self.anim_hl[0], self.anim_hl[0] + 1):
                fill_c, out_c = ("#F472B6", "#FDF2F8") if self.anim_hl[1] else ("#38BDF8", "#E0F2FE")
            elif not self.animando and (i + 1) in self.resaltados:
                fill_c, out_c = "#A855F7", "#FEF08A"
            elif idx == 3 and p[3] < u:
                fill_c, out_c = "#7C3AED", "#DDD6FE"
            else:
                fill_c, out_c = "#3B82F6", "#BFDBFE"

            c.create_rectangle(x0, y0, x1, y_base, fill=fill_c, outline=out_c, width=1.5)
            c.create_text(cx, y0 - 10, text=f"{simb}{p[idx]:.0f}", fill="white", font=("Segoe UI", 8.5, "bold"))
            etiqueta = p[0] if len(p[0]) <= 10 else p[0][:9] + "…"
            c.create_text(cx, y_base + 13, text=etiqueta, fill=self.c_lavanda, font=("Segoe UI", 8.5))
            if not self.animando:
                med = {0: "🥇", 1: "🥈", 2: "🥉"}.get(i, f"#{i + 1}")
                c.create_text(cx, y_base + 30, text=med, fill="#FDE68A", font=("Segoe UI", 9))
            self.barras.append((x0, x1, i))

    def click_grafico(self, event):
        if self.animando or self.anim_data is not None:
            return
        for x0, x1, i in self.barras:
            if x0 <= event.x <= x1:
                p = self.ranking[i]
                self.resaltados = {i + 1}
                self.actualizar_tabla()
                self.dibujar_grafico()
                self.status(f"⭐ #{i + 1} {p[0]} — S/ {p[3]:.2f} ({p[2]} unidades)")
                return

    # ------------------------------------------------------------------ animación
    def toggle_animacion(self):
        if self.animando:
            self.detener_animacion()
            return
        if len(self.frames) < 2:
            self.status("ℹ️ Se necesitan al menos 2 platos para animar.")
            return
        self.resaltados = set()
        self.actualizar_tabla()
        self.animando = True
        self.anim_i = 0
        self.btn_anim.config(text="⏹ Detener animación")
        self.nb.select(self.tab_traza)
        self.paso_animacion()

    def paso_animacion(self):
        if not self.animando:
            return
        if self.anim_i >= len(self.frames):
            self.detener_animacion()
            self.status("🎉 Animación completada: el ranking quedó ordenado.")
            return
        arr, j, cambio, pas = self.frames[self.anim_i]
        self.anim_data = arr
        self.anim_hl = (j, cambio)
        self.dibujar_grafico()
        if j is None:
            self.status("▶ Datos en el orden original (sin ordenar)…")
        else:
            a, b = arr[j], arr[j + 1]
            self.status(f"🫧 Pasada {pas}, j={j}: comparando {arr[j][0]} y {arr[j + 1][0]} → "
                        f"{'INTERCAMBIO' if cambio else 'sin cambio'}")
        self.anim_i += 1
        self.anim_job = self.root.after(self.var_vel.get(), self.paso_animacion)

    def detener_animacion(self, silencioso=False):
        if self.anim_job is not None:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None
        was = self.animando
        self.animando = False
        self.anim_data = None
        self.anim_hl = None
        self.btn_anim.config(text="▶ Animar burbuja")
        if was and not silencioso:
            self.dibujar_grafico()
            self.status("⏹ Animación detenida.")

    # ------------------------------------------------------------------ búsquedas interactivas
    def buscar_plato_interactivo(self):
        nombre = self.ent_buscar.get().strip()
        if not nombre:
            messagebox.showinfo("Búsqueda", "Escribe un nombre de plato para buscar.")
            return
        puesto, plato, pasos = busqueda_secuencial_nombre(self.ranking, nombre)
        if puesto is not None:
            self.resaltados = {puesto}
            self.lbl_busqueda_vivo.config(
                text=f"✅ '{plato[0]}' está en el Puesto #{puesto} (Ingreso: S/ {plato[3]:.2f}, {pasos} pasos).")
        else:
            self.resaltados = set()
            sugeridos = difflib.get_close_matches(nombre, [p[0] for p in self.ranking], n=2, cutoff=0.5)
            extra = f" ¿Quisiste decir: {' o '.join(sugeridos)}?" if sugeridos else ""
            self.lbl_busqueda_vivo.config(
                text=f"❌ '{nombre}' no existe en el ranking ({pasos} pasos secuenciales).{extra}")
        self.actualizar_tabla()
        self.dibujar_grafico()
        if puesto is not None and self.tree.exists(str(puesto)):
            self.tree.see(str(puesto))

    def buscar_menor_umbral_interactivo(self):
        self.aplicar_umbral_silencioso()
        u = self.umbral_actual
        puesto, plato, pasos = busqueda_secuencial_primer_menor_umbral(self.ranking, u)
        if puesto is not None:
            self.resaltados = {puesto}
            self.lbl_busqueda_vivo.config(
                text=f"🎯 1° < S/{u:.0f}: Puesto #{puesto} — {plato[0]} (S/ {plato[3]:.2f}, en {pasos} pasos).")
        else:
            self.resaltados = set()
            self.lbl_busqueda_vivo.config(text=f"ℹ️ Todos los platos tienen ingreso ≥ S/ {u:.2f} ({pasos} pasos).")
        self.actualizar_tabla()
        self.dibujar_grafico()
        if puesto is not None and self.tree.exists(str(puesto)):
            self.tree.see(str(puesto))

    def buscar_todos_menor_umbral(self):
        self.aplicar_umbral_silencioso()
        u = self.umbral_actual
        lista, pasos = busqueda_secuencial_todos_menor_umbral(self.ranking, u)
        self.resaltados = {pu for pu, _ in lista}
        if lista:
            nombres = ", ".join(f"#{pu} {p[0]}" for pu, p in lista)
            self.lbl_busqueda_vivo.config(text=f"📉 {len(lista)} plato(s) < S/{u:.0f} ({pasos} pasos): {nombres}")
        else:
            self.lbl_busqueda_vivo.config(text=f"✅ Ningún plato está por debajo de S/ {u:.2f} ({pasos} pasos).")
        self.actualizar_tabla()
        self.dibujar_grafico()

    def aplicar_umbral_silencioso(self):
        """Si el usuario cambió el umbral sin pulsar 'Aplicar', lo toma antes de buscar."""
        try:
            u = float(self.var_umbral.get().replace(",", "."))
            if u >= 0 and u != self.umbral_actual:
                self.umbral_actual = u
                self.recalcular_todo()
        except ValueError:
            self.var_umbral.set(f"{self.umbral_actual:g}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppRankingPlatosDinamico(root)
    root.mainloop()
