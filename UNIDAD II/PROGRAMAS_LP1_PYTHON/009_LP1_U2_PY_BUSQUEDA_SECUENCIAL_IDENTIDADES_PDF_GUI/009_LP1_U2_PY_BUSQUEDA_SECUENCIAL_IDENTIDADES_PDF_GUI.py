import os
import random
import tempfile
import tkinter as tk
from tkinter import messagebox, ttk
import unicodedata
import webbrowser

# Generar 100 registros iniciales de manera automática
nombres_base = [
    "María Sofía",
    "Carlos Alberto",
    "Lucía Elena",
    "José Luis",
    "Ana Valeria",
    "Juan Carlos",
    "Rosa María",
    "Pedro Pablo",
    "Carmen Rosa",
    "Luis Alberto",
    "Diana Patricia",
    "Jorge Luis",
    "Miguel Ángel",
    "Rosa Elena",
    "Víctor Manuel",
    "Sofía Isabel",
    "Marco Antonio",
    "Elena Beatriz",
    "Ricardo José",
    "Claudia Patricia",
]
paternos_base = [
    "Pérez",
    "Quispe",
    "Rodríguez",
    "Mamani",
    "Torres",
    "Flores",
    "Rojas",
    "García",
    "Mendoza",
    "Huamán",
    "Silva",
    "Vargas",
    "Ramos",
    "Castro",
    "Morales",
    "Gonzales",
    "Castillo",
    "Chávez",
    "Rivera",
    "Juárez",
]
maternos_base = [
    "Gómez",
    "Huamán",
    "Silva",
    "Mamani",
    "Vargas",
    "Ramos",
    "Castro",
    "Morales",
    "Paredes",
    "Vega",
    "Cáceres",
    "Salas",
    "Medina",
    "Herrera",
    "Campos",
    "Espinoza",
    "Romero",
    "Navarro",
    "Ortega",
    "Pacheco",
]

random.seed(42)
registros_iniciales = []
for _ in range(100):
  dni = f"{random.randint(10, 99)}{random.randint(100000, 999999)}"
  paterno = random.choice(paternos_base)
  materno = random.choice(maternos_base)
  nombre = random.choice(nombres_base)
  registros_iniciales.append(
      {"dni": dni, "paterno": paterno, "materno": materno, "nombre": nombre}
  )


class AppPastelDNI:

  def __init__(self, root):
    self.root = root
    self.root.title("Sistema de Gestión de Identidades - Reportes PDF Nativos")
    self.root.geometry("1060x600")
    self.root.config(bg="#F3E8FF")  # Fondo lavanda pastel

    self.style = ttk.Style()
    if "clam" in self.style.theme_names():
      self.style.theme_use("clam")
    self.configurar_estilos()

    self.registros = list(registros_iniciales)
    self.registro_actual = None

    self.crear_widgets()
    self.cargar_tabla(self.registros)

  def configurar_estilos(self):
    self.style.configure(
        "TButton",
        background="#A78BFA",
        foreground="white",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
        relief="flat",
    )
    self.style.map(
        "TButton", background=[("active", "#8B5CF6"), ("pressed", "#7C3AED")]
    )

    self.style.configure(
        "Verde.TButton",
        background="#34D399",
        foreground="#064E3B",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
    )
    self.style.map(
        "Verde.TButton",
        background=[("active", "#10B981"), ("pressed", "#059669")],
    )

    # Estilo especial color ámbar/dorado para el botón de PDF
    self.style.configure(
        "PDF.TButton",
        background="#F59E0B",
        foreground="white",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
    )
    self.style.map(
        "PDF.TButton",
        background=[("active", "#D97706"), ("pressed", "#B45309")],
    )

    self.style.configure(
        "Treeview",
        background="#FFFFFF",
        foreground="#334155",
        fieldbackground="#FFFFFF",
        font=("Segoe UI", 10),
        rowheight=32,
    )
    self.style.configure(
        "Treeview.Heading",
        background="#C4B5FD",
        foreground="#4C1D95",
        font=("Segoe UI", 10, "bold"),
    )
    self.style.map(
        "Treeview",
        background=[("selected", "#EDE9FE")],
        foreground=[("selected", "#1E1B4B")],
    )

  def limpiar_acentos(self, texto):
    nfkd_form = unicodedata.normalize("NFKD", str(texto))
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

  def crear_widgets(self):
    main_frame = tk.Frame(self.root, bg="#F3E8FF", padx=15, pady=15)
    main_frame.pack(fill=tk.BOTH, expand=True)

    lbl_titulo = tk.Label(
        main_frame,
        text=(
            "✨ Panel de Control, Búsqueda Alfabética y Reportes PDF Nativos ✨"
        ),
        bg="#F3E8FF",
        fg="#6D28D9",
        font=("Segoe UI", 15, "bold"),
    )
    lbl_titulo.pack(anchor=tk.W, pady=(0, 10))

    # --- BARRA DE BÚSQUEDA Y ACCIONES ---
    card_busqueda = tk.Frame(
        main_frame,
        bg="#FFFFFF",
        highlightbackground="#DDD6FE",
        highlightthickness=2,
        padx=12,
        pady=10,
    )
    card_busqueda.pack(fill=tk.X, pady=(0, 10))

    lbl_buscar = tk.Label(
        card_busqueda,
        text="Buscar Apellido:",
        bg="#FFFFFF",
        fg="#7C3AED",
        font=("Segoe UI", 10, "bold"),
    )
    lbl_buscar.pack(side=tk.LEFT, padx=(0, 6))

    self.entry_busqueda = tk.Entry(
        card_busqueda,
        font=("Segoe UI", 11),
        bd=1,
        relief="solid",
        bg="#FAF5FF",
        fg="#334155",
    )
    self.entry_busqueda.pack(
        side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=3
    )
    self.entry_busqueda.bind("<Return>", lambda event: self.buscar_registro())

    btn_buscar = ttk.Button(
        card_busqueda, text="🔍 Buscar", command=self.buscar_registro
    )
    btn_buscar.pack(side=tk.LEFT, padx=(0, 4))

    btn_reset = ttk.Button(
        card_busqueda, text="🌈 Ver Todos", command=self.resetear_tabla
    )
    btn_reset.pack(side=tk.LEFT, padx=(0, 4))

    btn_nuevo = ttk.Button(
        card_busqueda,
        text="➕ Registrar",
        style="Verde.TButton",
        command=self.abrir_ventana_registro,
    )
    btn_nuevo.pack(side=tk.LEFT)

    # --- CONTENEDOR INFERIOR: TABLA (IZQ) Y PESTAÑA LATERAL (DER) ---
    cuerpo_frame = tk.Frame(main_frame, bg="#F3E8FF")
    cuerpo_frame.pack(fill=tk.BOTH, expand=True)

    # 1. Tabla a la izquierda
    card_tabla = tk.Frame(
        cuerpo_frame,
        bg="#FFFFFF",
        highlightbackground="#DDD6FE",
        highlightthickness=2,
        padx=8,
        pady=8,
    )
    card_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    columns = ("indice", "dni", "paterno", "materno", "nombre")
    self.tree = ttk.Treeview(
        card_tabla, columns=columns, show="headings", selectmode="browse"
    )

    self.tree.heading("indice", text="Índice / Iteración")
    self.tree.heading("dni", text="DNI")
    self.tree.heading("paterno", text="Ap. Paterno")
    self.tree.heading("materno", text="Ap. Materno")
    self.tree.heading("nombre", text="Nombres")

    self.tree.column("indice", width=100, anchor=tk.CENTER)
    self.tree.column("dni", width=90, anchor=tk.CENTER)
    self.tree.column("paterno", width=120, anchor=tk.W)
    self.tree.column("materno", width=120, anchor=tk.W)
    self.tree.column("nombre", width=150, anchor=tk.W)

    self.tree.bind("<<TreeviewSelect>>", self.mostrar_detalle_seleccion)

    scrollbar = ttk.Scrollbar(
        card_tabla, orient=tk.VERTICAL, command=self.tree.yview
    )
    self.tree.configure(yscrollcommand=scrollbar.set)

    self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 2. Pestaña Lateral Derecha (Detalles y Botón de PDF)
    card_lateral = tk.Frame(
        cuerpo_frame,
        bg="#FEF3C7",
        highlightbackground="#FDE68A",
        highlightthickness=2,
        padx=15,
        pady=15,
        width=280,
    )
    card_lateral.pack(side=tk.RIGHT, fill=tk.Y)
    card_lateral.pack_propagate(False)

    lbl_lateral_titulo = tk.Label(
        card_lateral,
        text="📌 Detalle del Registro",
        bg="#FEF3C7",
        fg="#B45309",
        font=("Segoe UI", 11, "bold"),
    )
    lbl_lateral_titulo.pack(anchor=tk.W, pady=(0, 10))

    self.lbl_info_indice = tk.Label(
        card_lateral,
        text="• Índice: ---",
        bg="#FEF3C7",
        fg="#78350F",
        font=("Segoe UI", 10),
        anchor="w",
    )
    self.lbl_info_indice.pack(anchor=tk.W, pady=4)

    self.lbl_info_dni = tk.Label(
        card_lateral,
        text="• DNI: ---",
        bg="#FEF3C7",
        fg="#78350F",
        font=("Segoe UI", 10),
        anchor="w",
    )
    self.lbl_info_dni.pack(anchor=tk.W, pady=4)

    self.lbl_info_paterno = tk.Label(
        card_lateral,
        text="• Ap. Paterno: ---",
        bg="#FEF3C7",
        fg="#78350F",
        font=("Segoe UI", 10),
        anchor="w",
    )
    self.lbl_info_paterno.pack(anchor=tk.W, pady=4)

    self.lbl_info_materno = tk.Label(
        card_lateral,
        text="• Ap. Materno: ---",
        bg="#FEF3C7",
        fg="#78350F",
        font=("Segoe UI", 10),
        anchor="w",
    )
    self.lbl_info_materno.pack(anchor=tk.W, pady=4)

    self.lbl_info_nombre = tk.Label(
        card_lateral,
        text="• Nombres: ---",
        bg="#FEF3C7",
        fg="#78350F",
        font=("Segoe UI", 10),
        anchor="w",
    )
    self.lbl_info_nombre.pack(anchor=tk.W, pady=4)

    # Botón para generar el reporte PDF nativo
    btn_pdf = ttk.Button(
        card_lateral,
        text="📄 Generar Reporte PDF",
        style="PDF.TButton",
        command=self.generar_reporte_pdf_nativo,
    )
    btn_pdf.pack(side=tk.BOTTOM, fill=tk.X, pady=(15, 0))

    # Barra de estado inferior
    self.lbl_estado = tk.Label(
        main_frame,
        text="💡 Selecciona una persona para ver sus detalles y generar su reporte PDF.",
        bg="#F3E8FF",
        fg="#7C3AED",
        font=("Segoe UI", 9, "italic"),
    )
    self.lbl_estado.pack(anchor=tk.W, pady=(8, 0))

  def generar_reporte_pdf_nativo(self):
    """Genera una ficha elegante en HTML y la abre para imprimir o guardar como PDF"""
    if not self.registro_actual:
      messagebox.showwarning(
          "Aviso",
          "Por favor, selecciona una persona de la lista para generar su"
          " reporte.",
      )
      return

    indice, dni, paterno, materno, nombre = self.registro_actual

    # Contenido HTML con diseño profesional corporativo/pastel
    html_contenido = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Ficha de Identidad - {paterno} {nombre}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #F8FAFC;
                    color: #1E293B;
                    margin: 0;
                    padding: 40px;
                }}
                .card {{
                    background: #FFFFFF;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                    border-top: 6px solid #8B5CF6;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 2px solid #F1F5F9;
                    padding-bottom: 20px;
                    margin-bottom: 25px;
                }}
                .header h1 {{
                    color: #6D28D9;
                    margin: 0;
                    font-size: 22px;
                }}
                .header p {{
                    color: #64748B;
                    font-size: 13px;
                    margin: 5px 0 0 0;
                }}
                .info-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 30px;
                }}
                .info-table th, .info-table td {{
                    padding: 12px 15px;
                    text-align: left;
                    border-bottom: 1px solid #E2E8F0;
                }}
                .info-table th {{
                    background-color: #F3E8FF;
                    color: #5B21B6;
                    width: 35%;
                    font-size: 14px;
                }}
                .info-table td {{
                    color: #334155;
                    font-size: 14px;
                    font-weight: 500;
                }}
                .footer {{
                    text-align: center;
                    color: #94A3B8;
                    font-size: 12px;
                    border-top: 1px solid #F1F5F9;
                    padding-top: 15px;
                }}
                .btn-print {{
                    display: block;
                    width: 100%;
                    background-color: #8B5CF6;
                    color: white;
                    border: none;
                    padding: 12px;
                    font-size: 15px;
                    font-weight: bold;
                    border-radius: 6px;
                    cursor: pointer;
                    text-align: center;
                    text-decoration: none;
                }}
                .btn-print:hover {{
                    background-color: #7C3AED;
                }}
                @media print {{
                    .btn-print {{ display: none; }}
                    body {{ background-color: #FFFFFF; padding: 0; }}
                    .card {{ box-shadow: none; border: none; }}
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="header">
                    <h1>Ficha Individual de Identidad</h1>
                    <p>Sistema de Gestión de Registros</p>
                </div>
                
                <table class="info-table">
                    <tr>
                        <th>Índice / Iteración</th>
                        <td>{indice}</td>
                    </tr>
                    <tr>
                        <th>Número de DNI</th>
                        <td>{dni}</td>
                    </tr>
                    <tr>
                        <th>Apellido Paterno</th>
                        <td>{paterno}</td>
                    </tr>
                    <tr>
                        <th>Apellido Materno</th>
                        <td>{materno}</td>
                    </tr>
                    <tr>
                        <th>Nombres Completos</th>
                        <td>{nombre}</td>
                    </tr>
                </table>

                <button class="btn-print" onclick="window.print()">🖨️ Guardar como PDF / Imprimir Ficha</button>

                <div class="footer" style="margin-top: 20px;">
                    Documento generado automáticamente desde la aplicación de escritorio.
                </div>
            </div>
        </body>
        </html>
        """

    try:
      # Crear un archivo HTML temporal
      fd, ruta_html = tempfile.mkstemp(suffix=".html")
      with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(html_contenido)

      # Abrir en el navegador predeterminado del usuario
      webbrowser.open("file://" + os.path.abspath(ruta_html))

      messagebox.showinfo(
          "Reporte Abierto 📄",
          "Se ha abierto la ficha en tu navegador.\n\nPara guardarla como PDF,"
          " presiona Ctrl + P y selecciona 'Guardar como PDF'.",
      )
    except Exception as e:
      messagebox.showerror(
          "Error", f"No se pudo abrir el reporte en el navegador:\n{e}"
      )

  def abrir_ventana_registro(self):
    ventana_reg = tk.Toplevel(self.root)
    ventana_reg.title("Registrar Nueva Persona")
    ventana_reg.geometry("360x310")
    ventana_reg.config(bg="#F3E8FF")
    ventana_reg.grab_set()

    lbl_head = tk.Label(
        ventana_reg,
        text="📝 Ingrese los datos:",
        bg="#F3E8FF",
        fg="#6D28D9",
        font=("Segoe UI", 11, "bold"),
    )
    lbl_head.pack(pady=10)

    tk.Label(
        ventana_reg,
        text="DNI (8 dígitos):",
        bg="#F3E8FF",
        fg="#4C1D95",
        font=("Segoe UI", 9, "bold"),
    ).pack(anchor="w", padx=25)
    entry_dni = tk.Entry(ventana_reg, font=("Segoe UI", 10), width=32)
    entry_dni.pack(padx=25, pady=2)

    tk.Label(
        ventana_reg,
        text="Apellido Paterno:",
        bg="#F3E8FF",
        fg="#4C1D95",
        font=("Segoe UI", 9, "bold"),
    ).pack(anchor="w", padx=25)
    entry_pat = tk.Entry(ventana_reg, font=("Segoe UI", 10), width=32)
    entry_pat.pack(padx=25, pady=2)

    tk.Label(
        ventana_reg,
        text="Apellido Materno:",
        bg="#F3E8FF",
        fg="#4C1D95",
        font=("Segoe UI", 9, "bold"),
    ).pack(anchor="w", padx=25)
    entry_mat = tk.Entry(ventana_reg, font=("Segoe UI", 10), width=32)
    entry_mat.pack(padx=25, pady=2)

    tk.Label(
        ventana_reg,
        text="Nombres:",
        bg="#F3E8FF",
        fg="#4C1D95",
        font=("Segoe UI", 9, "bold"),
    ).pack(anchor="w", padx=25)
    entry_nom = tk.Entry(ventana_reg, font=("Segoe UI", 10), width=32)
    entry_nom.pack(padx=25, pady=2)

    def guardar_registro():
      d = entry_dni.get().strip()
      p = entry_pat.get().strip()
      m = entry_mat.get().strip()
      n = entry_nom.get().strip()

      if not d or not p or not m or not n:
        messagebox.showerror(
            "Error", "Todos los campos son obligatorios.", parent=ventana_reg
        )
        return

      if not d.isdigit() or len(d) != 8:
        messagebox.showerror(
            "Error",
            "El DNI debe contener exactamente 8 números.",
            parent=ventana_reg,
        )
        return

      self.registros.append(
          {"dni": d, "paterno": p, "materno": m, "nombre": n}
      )
      self.cargar_tabla(self.registros)
      messagebox.showinfo(
          "Éxito", "Persona registrada correctamente.", parent=ventana_reg
      )
      ventana_reg.destroy()

    btn_guardar = tk.Button(
        ventana_reg,
        text="Guardar Registro",
        bg="#8B5CF6",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        command=guardar_registro,
        relief="flat",
        padx=10,
        pady=5,
    )
    btn_guardar.pack(pady=15)

  def cargar_tabla(self, lista_registros):
    for item in self.tree.get_children():
      self.tree.delete(item)

    # Ordenar alfabéticamente por Apellido Paterno (A-Z)
    registros_ordenados = sorted(
        lista_registros, key=lambda r: self.limpiar_acentos(r["paterno"])
    )

    for idx, reg in enumerate(registros_ordenados, start=1):
      self.tree.insert(
          "",
          tk.END,
          values=(
              f"#{idx}",
              reg["dni"],
              reg["paterno"],
              reg["materno"],
              reg["nombre"],
          ),
      )

    items = self.tree.get_children()
    if items:
      self.tree.selection_set(items[0])
      self.mostrar_detalle_seleccion(None)
    else:
      self.registro_actual = None

    self.lbl_estado.config(
        text=(
            f"✨ Total de registros: {len(self.registros)} (Ordenados"
            " alfabéticamente A-Z)."
        )
    )

  def mostrar_detalle_seleccion(self, event):
    seleccion = self.tree.selection()
    if seleccion:
      item = self.tree.item(seleccion)
      valores = item["values"]
      if valores:
        self.registro_actual = valores
        self.lbl_info_indice.config(text=f"• Índice: {valores[0]}")
        self.lbl_info_dni.config(text=f"• DNI: {valores[1]}")
        self.lbl_info_paterno.config(text=f"• Ap. Paterno: {valores[2]}")
        self.lbl_info_materno.config(text=f"• Ap. Materno: {valores[3]}")
        self.lbl_info_nombre.config(text=f"• Nombres: {valores[4]}")

  def buscar_registro(self):
    criterio = self.entry_busqueda.get().strip()
    if not criterio:
      messagebox.showwarning(
          "Aviso", "Por favor, escribe un apellido paterno para buscar."
      )
      return

    criterio_limpio = self.limpiar_acentos(criterio)
    resultados = [
        reg
        for reg in self.registros
        if criterio_limpio in self.limpiar_acentos(reg["paterno"])
    ]

    if resultados:
      self.cargar_tabla(resultados)
    else:
      messagebox.showinfo(
          "Sin Resultados",
          f"No se encontró ningún registro con el apellido '{criterio}'.",
      )
      self.cargar_tabla([])

  def resetear_tabla(self):
    self.entry_busqueda.delete(0, tk.END)
    self.cargar_tabla(self.registros)


if __name__ == "__main__":
  root = tk.Tk()
  app = AppPastelDNI(root)
  root.mainloop()
