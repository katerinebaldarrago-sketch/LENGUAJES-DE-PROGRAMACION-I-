# Leer un número entero
n = int(input("Ingresa un número entero: "))

# Mostrar la tabla de multiplicar del 1 al 10
print(f"\nTabla de multiplicar del {n}:")
for i in range(1, 11):
    print(f"{n} x {i} = {n * i}")
