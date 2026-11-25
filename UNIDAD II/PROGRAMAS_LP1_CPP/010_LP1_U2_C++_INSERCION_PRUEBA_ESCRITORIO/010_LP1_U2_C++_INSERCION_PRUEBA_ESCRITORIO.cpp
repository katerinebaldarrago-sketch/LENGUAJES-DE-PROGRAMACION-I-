#include <iostream>
using namespace std;

// Muestra el arreglo
void imprimirArreglo(int arr[], int n) {
    for (int i = 0; i < n; i++)
        cout << arr[i] << " ";
    cout << endl;
}

// Ordenación por inserción con prueba de escritorio
void ordenacionInsercion(int arr[], int n) {
    int totalDesplazamientos = 0;

    for (int i = 1; i < n; i++) {
        int clave = arr[i];
        int j = i - 1;
        int paso = 1;

        cout << "PASADA " << i << ": i = " << i
             << ", clave = " << clave << ", j = " << j << endl;

        // Desplaza los elementos mayores que la clave
        while (j >= 0 && arr[j] > clave) {
            cout << "  Paso " << paso << ": j = " << j << " -> "
                 << arr[j] << " > " << clave << " (verdadero) -> arr["
                 << j + 1 << "] = arr[" << j << "] -> ";
            arr[j + 1] = arr[j];
            j--;
            paso++;
            totalDesplazamientos++;
            imprimirArreglo(arr, n);
        }

        // Motivo por el que terminó el while
        if (j >= 0)
            cout << "  Paso " << paso << ": j = " << j << " -> "
                 << arr[j] << " > " << clave << " (falso) -> sale del while" << endl;
        else
            cout << "  Paso " << paso << ": j = -1 -> sale del while" << endl;

        // Inserta la clave en su posición
        arr[j + 1] = clave;
        cout << "  Insercion: arr[" << j + 1 << "] = " << clave << endl;
        cout << "  Resultado: ";
        imprimirArreglo(arr, n);
        cout << endl;
    }

    cout << "Total de desplazamientos: " << totalDesplazamientos << endl;
}

int main() {
    int datos[] = {64, 25, 12, 22, 11};
    int n = sizeof(datos) / sizeof(datos[0]);

    cout << "Arreglo original: ";
    imprimirArreglo(datos, n);
    cout << endl;

    ordenacionInsercion(datos, n);

    cout << "\nArreglo ordenado: ";
    imprimirArreglo(datos, n);

    return 0;
}