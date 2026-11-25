import tkinter as tk
from tkinter import messagebox
import random

# --- PALETA PASTEL & AESTHETIC ---
BG_MAIN = "#F5F3FF"        # Lavanda ultra claro (Fondo principal)
BG_CARD = "#FFFFFF"        # Blanco puro (Tarjetas)
BG_SOFT_BLUE = "#E0F2FE"   # Azul cielo pastel (Inputs y detalles)
BG_SOFT_PURPLE = "#EDE9FE" # Lila suave (Celdas)

PURPLE_PRIMARY = "#7C3AED" # Morado elegante
PURPLE_PASTEL = "#A78BFA"  # Lila pastel (Botones)
BLUE_PASTEL = "#38BDF8"    # Azul celeste vibrante
PINK_PASTEL = "#F472B6"    # Rosa suave para acentos
MINT_SUCCESS = "#10B981"   # Verde esmeralda pastel (Encontrado)
YELLOW_SCAN = "#FBBF24"    # Ámbar suave (Evaluando)
CORAL_ERROR = "#F43F5E"    # Coral (No encontrado)

TEXT_DARK = "#1E1B4B"      # Azul/Morado oscuro muy legible
TEXT_MUTED = "#6B7280"     # Gris suave para subtítulos

class BotonPastel(tk.Canvas):
    """Botón personalizado con esquinas redondeadas estilo píldora."""
    def __init__(self, parent, text, bg_color, hover_color, command, width=130, height=36, fg_color="#FFFFFF"):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0, cursor="hand2")
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.fg_color = fg_color
        self.text = text
        self.w = width
        self.h = height

        self.rect = self._dibujar_pildora(2, 2, width-2, height-2, radius=16, fill=bg_color)
        self.txt = self.create_text(width/2, height/2, text=text, fill=fg_color, font=("Segoe UI", 9, "bold"))

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _dibujar_pildora(self, x1, y1, x2, y2, radius=18, **kwargs):
        points = [
            x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1,
            x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
            x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
            x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
            x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_enter(self, e):
        self.itemconfig(self.rect, fill=self.hover_color)

    def _on_leave(self, e):
        self.itemconfig(self.rect, fill=self.bg_color)

    def _on_click(self, e):
        if self.command:
            self.command()


class BuscadorPastelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Buscador Secuencial — Estilo Pastel ✨")
        self.root.geometry("940x760")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        self.arreglo = []
        self.cajas_elementos = []
        self.historial_busquedas = []
        self.buscando = False

        self._construir_interfaz()

    def _construir_interfaz(self):
        # --- ENCABEZADO ---
        header = tk.Frame(self.root, bg=BG_MAIN)
        header.pack(fill="x", pady=(15, 5), padx=30)

        tk.Label(
            header, text="Visualizador de Búsqueda Lineal", 
            font=("Segoe UI", 18, "bold"), bg=BG_MAIN, fg=TEXT_DARK
        ).pack(side="left")

        # Asistente virtual de estado (sin nombres explícitos)
        self.lbl_estado_sistema = tk.Label(
            header, text="● Sistema listo para operar", 
            font=("Segoe UI", 10, "bold"), bg=BG_CARD, fg=PURPLE_PRIMARY,
            padx=12, pady=5, highlightbackground=PURPLE_PASTEL, highlightthickness=1
        )
        self.lbl_estado_sistema.pack(side="right")

        # --- PANEL 1: GESTIÓN DE DATOS Y ESTADÍSTICAS ---
        panel_datos = tk.Frame(self.root, bg=BG_CARD, highlightbackground=PURPLE_PASTEL, highlightthickness=1)
        panel_datos.pack(fill="x", padx=30, pady=6)

        tk.Label(
            panel_datos, text="1. Configuración del Arreglo (Clic en cualquier celda para eliminarla individualmente)", 
            font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_MUTED
        ).grid(row=0, column=0, columnspan=6, sticky="w", padx=15, pady=(8, 2))

        tk.Label(panel_datos, text="Valor:", font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_DARK).grid(row=1, column=0, padx=(15, 4), pady=8)

        self.entry_elemento = tk.Entry(
            panel_datos, font=("Segoe UI", 10, "bold"), width=7, justify="center",
            bg=BG_SOFT_BLUE, fg=TEXT_DARK, insertbackground=PURPLE_PRIMARY,
            relief="flat", highlightbackground=BLUE_PASTEL, highlightthickness=1
        )
        self.entry_elemento.grid(row=1, column=1, padx=4, pady=8, ipady=3)
        self.entry_elemento.bind("<Return>", lambda e: self.agregar_elemento())

        BotonPastel(panel_datos, "+ Agregar", PURPLE_PASTEL, "#8B5CF6", self.agregar_elemento, width=110).grid(row=1, column=2, padx=4)
        BotonPastel(panel_datos, "🎲 Aleatorio", BLUE_PASTEL, "#0284C7", self.generar_aleatorio, width=110).grid(row=1, column=3, padx=4)
        BotonPastel(panel_datos, "📊 Ordenar", "#6366F1", "#4F46E5", self.ordenar_arreglo, width=110).grid(row=1, column=4, padx=4)
        BotonPastel(panel_datos, "🗑️ Limpiar", PINK_PASTEL, "#EC4899", self.limpiar_arreglo, width=110).grid(row=1, column=5, padx=(4, 15))

        # Sub-panel de Estadísticas instantáneas (NUEVA FUNCIÓN 1)
        stats_frame = tk.Frame(panel_datos, bg=BG_SOFT_PURPLE, padx=10, pady=4)
        stats_frame.grid(row=2, column=0, columnspan=6, sticky="ew", padx=15, pady=(0, 8))
        
        self.lbl_stat_count = tk.Label(stats_frame, text="Elementos: 0", font=("Segoe UI", 8, "bold"), bg=BG_SOFT_PURPLE, fg=TEXT_DARK)
        self.lbl_stat_count.pack(side="left", padx=10)
        self.lbl_stat_min = tk.Label(stats_frame, text="Mínimo: -", font=("Segoe UI", 8, "bold"), bg=BG_SOFT_PURPLE, fg=TEXT_DARK)
        self.lbl_stat_min.pack(side="left", padx=10)
        self.lbl_stat_max = tk.Label(stats_frame, text="Máximo: -", font=("Segoe UI", 8, "bold"), bg=BG_SOFT_PURPLE, fg=TEXT_DARK)
        self.lbl_stat_max.pack(side="left", padx=10)
        self.lbl_stat_prom = tk.Label(stats_frame, text="Promedio: -", font=("Segoe UI", 8, "bold"), bg=BG_SOFT_PURPLE, fg=TEXT_DARK)
        self.lbl_stat_prom.pack(side="left", padx=10)

        # --- PANEL 2: VISUALIZACIÓN DEL ARREGLO ---
        panel_visual = tk.Frame(self.root, bg=BG_CARD, highlightbackground=BLUE_PASTEL, highlightthickness=1)
        panel_visual.pack(fill="x", padx=30, pady=6)

        tk.Label(
            panel_visual, text="2. Memoria Activa", 
            font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_MUTED
        ).pack(anchor="w", padx=15, pady=(8, 2))

        self.frame_arreglo = tk.Frame(panel_visual, bg=BG_CARD, height=105)
        self.frame_arreglo.pack(fill="x", padx=15, pady=8)
        self.frame_arreglo.pack_propagate(False)

        self._mostrar_placeholder_vacio()

        # --- PANEL 3: CONTROLES DE BÚSQUEDA ---
        panel_busqueda = tk.Frame(self.root, bg=BG_CARD, highlightbackground=PURPLE_PASTEL, highlightthickness=1)
        panel_busqueda.pack(fill="x", padx=30, pady=6)

        tk.Label(
            panel_busqueda, text="3. Ejecución de Búsqueda Secuencial", 
            font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_MUTED
        ).grid(row=0, column=0, columnspan=5, sticky="w", padx=15, pady=(8, 2))

        tk.Label(panel_busqueda, text="Valor a buscar:", font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_DARK).grid(row=1, column=0, padx=(15, 4), pady=10)

        self.entry_buscar = tk.Entry(
            panel_busqueda, font=("Segoe UI", 10, "bold"), width=7, justify="center",
            bg=BG_SOFT_BLUE, fg=TEXT_DARK, insertbackground=PURPLE_PRIMARY,
            relief="flat", highlightbackground=BLUE_PASTEL, highlightthickness=1
        )
        self.entry_buscar.grid(row=1, column=1, padx=4, pady=10, ipady=3)
        self.entry_buscar.bind("<Return>", lambda e: self.iniciar_busqueda())

        BotonPastel(panel_busqueda, "🚀 Iniciar Búsqueda", PURPLE_PRIMARY, "#6D28D9", self.iniciar_busqueda, width=150).grid(row=1, column=2, padx=10)

        tk.Label(panel_busqueda, text="Velocidad (ms):", font=("Segoe UI", 8, "bold"), bg=BG_CARD, fg=TEXT_MUTED).grid(row=1, column=3, padx=(15, 4))
        
        self.velocidad = tk.Scale(
            panel_busqueda, from_=800, to=100, orient="horizontal", showvalue=False,
            bg=BG_CARD, troughcolor=BG_SOFT_PURPLE, activebackground=PINK_PASTEL,
            highlightthickness=0, length=120
        )
        self.velocidad.set(400)
        self.velocidad.grid(row=1, column=4, padx=4)

        # --- PANEL 4: RESULTADOS Y MÉTRICAS (Similares a tu C++) ---
        panel_resultados = tk.Frame(self.root, bg=BG_CARD, highlightbackground=PINK_PASTEL, highlightthickness=1)
        panel_resultados.pack(fill="x", padx=30, pady=6)

        tk.Label(
            panel_resultados, text="4. Reporte y Métricas de Ejecución", 
            font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_MUTED
        ).pack(anchor="w", padx=15, pady=(8, 4))

        metrics_frame = tk.Frame(panel_resultados, bg=BG_CARD)
        metrics_frame.pack(fill="x", padx=12, pady=(0, 8))

        self.lbl_estado = self._crear_tarjeta_metrica(metrics_frame, "ESTADO", "En espera", TEXT_MUTED, BG_SOFT_PURPLE)
        self.lbl_indice = self._crear_tarjeta_metrica(metrics_frame, "ÍNDICE (i)", "-", PURPLE_PRIMARY, BG_SOFT_BLUE)
        self.lbl_iteracion = self._crear_tarjeta_metrica(metrics_frame, "ITERACIÓN", "0", "#0284C7", BG_SOFT_PURPLE)
        self.lbl_contenido = self._crear_tarjeta_metrica(metrics_frame, "CONTENIDO", "-", "#DB2777", BG_SOFT_BLUE)

        # --- PANEL 5: HISTORIAL DE BÚSQUEDAS (NUEVA FUNCIÓN 2) ---
        panel_historial = tk.Frame(self.root, bg=BG_CARD, highlightbackground=BLUE_PASTEL, highlightthickness=1)
        panel_historial.pack(fill="both", expand=True, padx=30, pady=(6, 15))

        tk.Label(
            panel_historial, text="5. Historial de Búsquedas Recientes", 
            font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_MUTED
        ).pack(anchor="w", padx=15, pady=(6, 2))

        # Listbox con scroll para ver el historial
        hist_container = tk.Frame(panel_historial, bg=BG_CARD)
        hist_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self.listbox_historial = tk.Listbox(
            hist_container, font=("Consolas", 9), bg=BG_MAIN, fg=TEXT_DARK,
            relief="flat", highlightthickness=1, highlightbackground=BG_SOFT_PURPLE, height=4
        )
        self.listbox_historial.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(hist_container, orient="vertical", command=self.listbox_historial.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox_historial.config(yscrollcommand=scrollbar.set)

    def _crear_tarjeta_metrica(self, parent, titulo, valor_inicial, color_valor, bg_tarjeta):
        card = tk.Frame(parent, bg=bg_tarjeta, padx=10, pady=8, highlightbackground="#E2E8F0", highlightthickness=1)
        card.pack(side="left", expand=True, fill="both", padx=4)
        
        tk.Label(card, text=titulo, font=("Segoe UI", 8, "bold"), bg=bg_tarjeta, fg=TEXT_MUTED).pack()
        lbl_val = tk.Label(card, text=valor_inicial, font=("Consolas", 11, "bold"), bg=bg_tarjeta, fg=color_valor)
        lbl_val.pack(pady=(3, 0))
        return lbl_val

    def _mostrar_placeholder_vacio(self):
        tk.Label(
            self.frame_arreglo, text="[ El arreglo está vacío. Agrega valores o genera un conjunto aleatorio ]", 
            font=("Consolas", 9), bg=BG_CARD, fg=TEXT_MUTED
        ).pack(expand=True)

    def actualizar_estadisticas(self):
        if not self.arreglo:
            self.lbl_stat_count.config(text="Elementos: 0")
            self.lbl_stat_min.config(text="Mínimo: -")
            self.lbl_stat_max.config(text="Máximo: -")
            self.lbl_stat_prom.config(text="Promedio: -")
        else:
            n = len(self.arreglo)
            self.lbl_stat_count.config(text=f"Elementos: {n}")
            self.lbl_stat_min.config(text=f"Mínimo: {min(self.arreglo)}")
            self.lbl_stat_max.config(text=f"Máximo: {max(self.arreglo)}")
            self.lbl_stat_prom.config(text=f"Promedio: {sum(self.arreglo)/n:.1f}")

    # --- LÓGICA DEL ARREGLO ---
    def agregar_elemento(self):
        if self.buscando: return
        val_str = self.entry_elemento.get().strip()
        if not val_str: return
        try:
            val = int(val_str)
            if len(self.arreglo) >= 15:
                messagebox.showwarning("Límite sugerido", "Se recomiendan máximo 15 elementos para una visualización fluida.")
                return
            self.arreglo.append(val)
            self.entry_elemento.delete(0, tk.END)
            self.dibujar_arreglo()
            self.actualizar_estadisticas()
            self.resetear_metricas()
        except ValueError:
            messagebox.showerror("Error de formato", "Ingrese un número entero válido.")

    def generar_aleatorio(self):
        if self.buscando: return
        cantidad = random.randint(8, 12)
        self.arreglo = [random.randint(1, 99) for _ in range(cantidad)]
        self.dibujar_arreglo()
        self.actualizar_estadisticas()
        self.resetear_metricas()

    def ordenar_arreglo(self):
        if self.buscando or not self.arreglo: return
        self.arreglo.sort()
        self.dibujar_arreglo()
        self.actualizar_estadisticas()
        self.resetear_metricas()

    def limpiar_arreglo(self):
        if self.buscando: return
        self.arreglo.clear()
        self.dibujar_arreglo()
        self.actualizar_estadisticas()
        self.resetear_metricas()

    def eliminar_indice(self, idx):
        if self.buscando: return
        self.arreglo.pop(idx)
        self.dibujar_arreglo()
        self.actualizar_estadisticas()
        self.resetear_metricas()

    def dibujar_arreglo(self):
        for widget in self.frame_arreglo.winfo_children():
            widget.destroy()
        self.cajas_elementos.clear()

        if not self.arreglo:
            self._mostrar_placeholder_vacio()
            return

        contenedor = tk.Frame(self.frame_arreglo, bg=BG_CARD)
        contenedor.pack(expand=True)

        for idx, num in enumerate(self.arreglo):
            bg_celda = BG_SOFT_PURPLE if idx % 2 == 0 else BG_SOFT_BLUE
            borde_celda = PURPLE_PASTEL if idx % 2 == 0 else BLUE_PASTEL

            celda = tk.Frame(contenedor, bg=bg_celda, highlightthickness=1, highlightbackground=borde_celda, cursor="hand2")
            celda.pack(side="left", padx=4)

            lbl_num = tk.Label(celda, text=str(num), font=("Consolas", 12, "bold"), bg=bg_celda, fg=TEXT_DARK, width=3, pady=6)
            lbl_num.pack()

            lbl_idx = tk.Label(celda, text=f"[{idx}]", font=("Consolas", 8, "bold"), bg="#FFFFFF", fg=TEXT_MUTED, width=5)
            lbl_idx.pack()

            celda.bind("<Button-1>", lambda e, i=idx: self.eliminar_indice(i))
            lbl_num.bind("<Button-1>", lambda e, i=idx: self.eliminar_indice(i))
            lbl_idx.bind("<Button-1>", lambda e, i=idx: self.eliminar_indice(i))

            self.cajas_elementos.append((celda, lbl_num, bg_celda, borde_celda))

    def resetear_metricas(self):
        self.lbl_estado.config(text="En espera", fg=TEXT_MUTED)
        self.lbl_indice.config(text="-")
        self.lbl_iteracion.config(text="0")
        self.lbl_contenido.config(text="-")

    # --- ALGORITMO DE BÚSQUEDA ---
    def iniciar_busqueda(self):
        if self.buscando: return
        if not self.arreglo:
            messagebox.showwarning("Arreglo vacío", "Agregue elementos antes de realizar una búsqueda.")
            return

        val_str = self.entry_buscar.get().strip()
        try:
            valor_buscado = int(val_str)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero válido para buscar.")
            return

        for celda, lbl_num, bg_orig, borde_orig in self.cajas_elementos:
            celda.config(highlightbackground=borde_orig, bg=bg_orig)
            lbl_num.config(bg=bg_orig, fg=TEXT_DARK)

        self.buscando = True
        self.lbl_estado.config(text="Buscando...", fg="#D97706")
        self.lbl_estado_sistema.config(text="● Ejecutando búsqueda lineal...", fg="#D97706")
        self._paso_busqueda(i=0, iteracion=0, valor=valor_buscado)

    def _paso_busqueda(self, i, iteracion, valor):
        if i >= len(self.arreglo):
            self.lbl_estado.config(text=f"No encontrado ({valor})", fg=CORAL_ERROR)
            self.lbl_estado_sistema.config(text="● Búsqueda finalizada: Sin coincidencias", fg=CORAL_ERROR)
            self.lbl_indice.config(text="-1")
            self.lbl_iteracion.config(text=str(iteracion))
            self.lbl_contenido.config(text="N/A")
            
            # Registrar en historial
            self.historial_busquedas.insert(0, f"Búsqueda: {valor} ➔ No encontrado (Pasos: {iteracion})")
            self.actualizar_historial_ui()
            self.buscando = False
            return

        iteracion += 1
        self.lbl_iteracion.config(text=str(iteracion))
        self.lbl_indice.config(text=str(i))
        self.lbl_contenido.config(text=f"arreglo[{i}] = {self.arreglo[i]}")

        celda_actual, lbl_actual, _, _ = self.cajas_elementos[i]
        celda_actual.config(highlightbackground=YELLOW_SCAN, bg="#FEF3C7")
        lbl_actual.config(bg="#FEF3C7", fg="#B45309")

        if self.arreglo[i] == valor:
            celda_actual.config(highlightbackground=MINT_SUCCESS, bg="#D1FAE5")
            lbl_actual.config(bg="#D1FAE5", fg="#047857")
            
            self.lbl_estado.config(text=f"¡Encontrado!", fg=MINT_SUCCESS)
            self.lbl_estado_sistema.config(text=f"● ¡Valor {valor} localizado en índice {i}!", fg=MINT_SUCCESS)
            
            # Registrar en historial
            self.historial_busquedas.insert(0, f"Búsqueda: {valor} ➔ Encontrado en índice [{i}] (Pasos: {iteracion})")
            self.actualizar_historial_ui()
            self.buscando = False
            return
        else:
            delay = self.velocidad.get()
            self.root.after(delay, lambda: self._desmarcar_y_continuar(i, iteracion, valor))

    def _desmarcar_y_continuar(self, i, iteracion, valor):
        celda_prev, lbl_prev, _, _ = self.cajas_elementos[i]
        celda_prev.config(highlightbackground="#CBD5E1", bg="#F8FAFC")
        lbl_prev.config(bg="#F8FAFC", fg="#94A3B8")

        self._paso_busqueda(i + 1, iteracion, valor)

    def actualizar_historial_ui(self):
        self.listbox_historial.delete(0, tk.END)
        for item in self.historial_busquedas:
            self.listbox_historial.insert(tk.END, item)

if __name__ == "__main__":
    root = tk.Tk()
    app = BuscadorPastelApp(root)
    root.mainloop()
