import tkinter as tk
from tkinter import messagebox

# --- Variables globales ---
primer_numero = None
operacion = None
esperando_segundo = False

def agregar_digito(digito):
    """Agrega un dígito al display."""
    global esperando_segundo
    if esperando_segundo:
        display_var.set("")
        esperando_segundo = False
    
    actual = display_var.get()
    if actual == "0":
        display_var.set(digito)
    else:
        display_var.set(actual + digito)

def agregar_punto():
    """Agrega el punto decimal si no existe."""
    actual = display_var.get()
    if "." not in actual:
        display_var.set(actual + ".")

def seleccionar_operacion(op):
    """Guarda el primer número y la operación elegida."""
    global primer_numero, operacion, esperando_segundo
    
    try:
        primer_numero = float(display_var.get())
    except ValueError:
        messagebox.showerror("Error", "Número inválido")
        return
    
    operacion = op
    esperando_segundo = True
    lbl_operacion.config(text=f"{primer_numero} {op}")

def calcular():
    """Realiza la operación y muestra el resultado."""
    global primer_numero, operacion, esperando_segundo
    
    if operacion is None or primer_numero is None:
        return
    
    try:
        segundo_numero = float(display_var.get())
    except ValueError:
        messagebox.showerror("Error", "Número inválido")
        return
    
    try:
        if operacion == "+":
            resultado = primer_numero + segundo_numero
        elif operacion == "-":
            resultado = primer_numero - segundo_numero
        elif operacion == "×":
            resultado = primer_numero * segundo_numero
        elif operacion == "÷":
            if segundo_numero == 0:
                messagebox.showerror("Error", "No se puede dividir entre cero")
                limpiar()
                return
            resultado = primer_numero / segundo_numero
        else:
            return
    except Exception as e:
        messagebox.showerror("Error", f"Error en el cálculo: {e}")
        return
    
    # Mostrar resultado (sin .0 si es entero)
    if resultado == int(resultado):
        display_var.set(str(int(resultado)))
    else:
        display_var.set(str(round(resultado, 6)))
    
    lbl_operacion.config(text=f"{primer_numero} {operacion} {segundo_numero} =")
    
    # Reiniciar para la siguiente operación
    primer_numero = None
    operacion = None
    esperando_segundo = False

def limpiar():
    """Reinicia todo."""
    global primer_numero, operacion, esperando_segundo
    display_var.set("0")
    lbl_operacion.config(text="")
    primer_numero = None
    operacion = None
    esperando_segundo = False

def borrar_ultimo():
    """Borra el último dígito."""
    actual = display_var.get()
    if len(actual) > 1:
        display_var.set(actual[:-1])
    else:
        display_var.set("0")

def cambiar_signo():
    """Cambia el signo del número actual."""
    actual = display_var.get()
    if actual and actual != "0":
        if actual.startswith("-"):
            display_var.set(actual[1:])
        else:
            display_var.set("-" + actual)

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("Calculadora")
ventana.geometry("340x480")
ventana.resizable(False, False)
ventana.configure(bg="#2c3e50")

# --- Variables ---
display_var = tk.StringVar(value="0")

# --- Display ---
marco_display = tk.Frame(ventana, bg="#2c3e50")
marco_display.pack(pady=15, padx=15, fill="x")

lbl_operacion = tk.Label(marco_display, text="", font=("Arial", 11), 
                          bg="#2c3e50", fg="#bdc3c7", anchor="e")
lbl_operacion.pack(fill="x")

lbl_display = tk.Label(marco_display, textvariable=display_var, 
                        font=("Arial", 28, "bold"), 
                        bg="white", fg="#2c3e50", anchor="e", 
                        padx=10, pady=10, relief="sunken", bd=2)
lbl_display.pack(fill="x")

# --- Marco de botones ---
marco_botones = tk.Frame(ventana, bg="#2c3e50")
marco_botones.pack(padx=15, pady=10, fill="both", expand=True)

# Estilos de botones
estilo_numero = {"font": ("Arial", 16, "bold"), "bg": "#ecf0f1", "fg": "#2c3e50",
                 "activebackground": "#bdc3c7", "relief": "raised", "bd": 1}
estilo_operacion = {"font": ("Arial", 16, "bold"), "bg": "#3498db", "fg": "white",
                    "activebackground": "#2980b9", "relief": "raised", "bd": 1}
estilo_igual = {"font": ("Arial", 16, "bold"), "bg": "#27ae60", "fg": "white",
                "activebackground": "#229954", "relief": "raised", "bd": 1}
estilo_limpiar = {"font": ("Arial", 16, "bold"), "bg": "#e74c3c", "fg": "white",
                  "activebackground": "#c0392b", "relief": "raised", "bd": 1}

# --- Fila 0: C, ⌫, +/-, ÷ ---
tk.Button(marco_botones, text="C", command=limpiar, 
          **estilo_limpiar).grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="⌫", command=borrar_ultimo, 
          **estilo_operacion).grid(row=0, column=1, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="+/-", command=cambiar_signo, 
          **estilo_operacion).grid(row=0, column=2, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="÷", command=lambda: seleccionar_operacion("÷"), 
          **estilo_operacion).grid(row=0, column=3, sticky="nsew", padx=3, pady=3)

# --- Fila 1: 7, 8, 9, × ---
tk.Button(marco_botones, text="7", command=lambda: agregar_digito("7"), 
          **estilo_numero).grid(row=1, column=0, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="8", command=lambda: agregar_digito("8"), 
          **estilo_numero).grid(row=1, column=1, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="9", command=lambda: agregar_digito("9"), 
          **estilo_numero).grid(row=1, column=2, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="×", command=lambda: seleccionar_operacion("×"), 
          **estilo_operacion).grid(row=1, column=3, sticky="nsew", padx=3, pady=3)

# --- Fila 2: 4, 5, 6, - ---
tk.Button(marco_botones, text="4", command=lambda: agregar_digito("4"), 
          **estilo_numero).grid(row=2, column=0, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="5", command=lambda: agregar_digito("5"), 
          **estilo_numero).grid(row=2, column=1, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="6", command=lambda: agregar_digito("6"), 
          **estilo_numero).grid(row=2, column=2, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="-", command=lambda: seleccionar_operacion("-"), 
          **estilo_operacion).grid(row=2, column=3, sticky="nsew", padx=3, pady=3)

# --- Fila 3: 1, 2, 3, + ---
tk.Button(marco_botones, text="1", command=lambda: agregar_digito("1"), 
          **estilo_numero).grid(row=3, column=0, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="2", command=lambda: agregar_digito("2"), 
          **estilo_numero).grid(row=3, column=1, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="3", command=lambda: agregar_digito("3"), 
          **estilo_numero).grid(row=3, column=2, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="+", command=lambda: seleccionar_operacion("+"), 
          **estilo_operacion).grid(row=3, column=3, sticky="nsew", padx=3, pady=3)

# --- Fila 4: 0, ., = ---
tk.Button(marco_botones, text="0", command=lambda: agregar_digito("0"), 
          **estilo_numero).grid(row=4, column=0, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text=".", command=agregar_punto, 
          **estilo_numero).grid(row=4, column=1, sticky="nsew", padx=3, pady=3)
tk.Button(marco_botones, text="=", command=calcular, 
          **estilo_igual).grid(row=4, column=2, columnspan=2, sticky="nsew", padx=3, pady=3)

# --- Configurar grid para que se expanda ---
for i in range(4):
    marco_botones.columnconfigure(i, weight=1)
for i in range(5):
    marco_botones.rowconfigure(i, weight=1)

# --- Iniciar aplicación ---
ventana.mainloop()
