#include <iostream>
using namespace std;

const int N = 5;

// Muestra el arreglo con el formato [a, b, c, d, e]
void mostrarArreglo(int numeros[], int n) {
    cout << "[";
    for (int k = 0; k < n; k++) {
        cout << numeros[k];
        if (k < n - 1) cout << ", ";
    }
    cout << "]";
}

// Intercambia dos elementos del arreglo
void intercambiar(int numeros[], int a, int b) {
    int aux = numeros[a];
    numeros[a] = numeros[b];
    numeros[b] = aux;
}

// Ordena el arreglo con el método burbuja (muestra cada paso como en la prueba de escritorio)
void ordenarBurbuja(int numeros[], int n) {
    for (int i = 0; i < n - 1; i++) {
        cout << "\nPasada " << i + 1 << " (cuando i=" << i << ") j varia 0 a " << n - 2 - i << endl;

        for (int j = 0; j < n - 1 - i; j++) {
            cout << "  j=" << j << ": " << numeros[j] << ">" << numeros[j + 1] << "? ";

            if (numeros[j] > numeros[j + 1]) {
                intercambiar(numeros, j, j + 1);
                cout << "Si, intercambio <-> ";
                mostrarArreglo(numeros, n);
                cout << endl;
            } else {
                cout << "No" << endl;
            }
        }

        cout << "  Resultado: ";
        mostrarArreglo(numeros, n);
        cout << endl;
    }
}

int main() {
    int numeros[N] = {64, 25, 12, 22, 11};

    cout << "Numeros originales: ";
    mostrarArreglo(numeros, N);
    cout << endl;

    ordenarBurbuja(numeros, N);

    cout << "\nResultado final: ";
    mostrarArreglo(numeros, N);
    cout << endl;

    return 0;
}