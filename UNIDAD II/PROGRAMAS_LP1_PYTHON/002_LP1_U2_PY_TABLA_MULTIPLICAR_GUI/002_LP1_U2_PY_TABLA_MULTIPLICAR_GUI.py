import tkinter as tk
from tkinter import messagebox

def mostrar_tabla():
    # Obtener el número ingresado
    entrada = campo_numero.get().strip()
    
    # Validar que sea un entero
    try:
        n = int(entrada)
    except ValueError:
        messagebox.showerror("Error", "Debes ingresar un número entero válido.")
        return
    
    # Limpiar el área de resultados
    texto_resultado.config(state="normal")
    texto_resultado.delete("1.0", tk.END)
    
    # Generar la tabla
    texto_resultado.insert(tk.END, f"Tabla de multiplicar del {n}:\n")
    texto_resultado.insert(tk.END, "-" * 25 + "\n")
    for i in range(1, 11):
        texto_resultado.insert(tk.END, f"{n} x {i:2} = {n * i}\n")
    
    texto_resultado.config(state="disabled")

def limpiar():
    campo_numero.delete(0, tk.END)
    texto_resultado.config(state="normal")
    texto_resultado.delete("1.0", tk.END)
    texto_resultado.config(state="disabled")
    campo_numero.focus()

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("Tabla de Multiplicar")
ventana.geometry("400x450")
ventana.resizable(False, False)

# --- Título ---
titulo = tk.Label(ventana, text="Tabla de Multiplicar", 
                  font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# --- Marco para entrada ---
marco_entrada = tk.Frame(ventana)
marco_entrada.pack(pady=5)

tk.Label(marco_entrada, text="Número entero:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)

campo_numero = tk.Entry(marco_entrada, font=("Arial", 12), width=10, justify="center")
campo_numero.pack(side=tk.LEFT, padx=5)
campo_numero.focus()

# Permitir presionar Enter para calcular
campo_numero.bind("<Return>", lambda event: mostrar_tabla())

# --- Botones ---
marco_botones = tk.Frame(ventana)
marco_botones.pack(pady=10)

btn_calcular = tk.Button(marco_botones, text="Mostrar tabla", 
                         command=mostrar_tabla, 
                         font=("Arial", 11), bg="#4CAF50", fg="white", width=14)
btn_calcular.pack(side=tk.LEFT, padx=5)

btn_limpiar = tk.Button(marco_botones, text="Limpiar", 
                        command=limpiar,
                        font=("Arial", 11), bg="#f44336", fg="white", width=10)
btn_limpiar.pack(side=tk.LEFT, padx=5)

# --- Área de resultados ---
texto_resultado = tk.Text(ventana, font=("Courier", 11), width=32, height=13, 
                          state="disabled", bg="#f5f5f5")
texto_resultado.pack(pady=10, padx=20)

# --- Iniciar ---
ventana.mainloop()
