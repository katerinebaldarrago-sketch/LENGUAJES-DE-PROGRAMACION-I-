#include <iostream>
using namespace std;

// Muestra el arreglo en pantalla
void mostrarArreglo(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;
}

// Ordena el arreglo con el método Shell (inserción con incremento)
void ordenacionShell(int arr[], int n) {
    int paso = 1;

    for (int gap = n / 2; gap > 0; gap /= 2) {
        cout << "\n--- Incremento (gap) = " << gap << " ---" << endl;

        for (int i = gap; i < n; i++) {
            int temp = arr[i];
            int j = i;

            while (j >= gap && arr[j - gap] > temp) {
                arr[j] = arr[j - gap];   // desplaza
                j -= gap;
            }
            arr[j] = temp;               // inserta

            cout << "Paso " << paso++ << " (i = " << i << "): ";
            mostrarArreglo(arr, n);
        }
    }
}

int main() {
    int arr[] = {64, 25, 12, 22, 11};
    int n = sizeof(arr) / sizeof(arr[0]);

    cout << "Arreglo original: ";
    mostrarArreglo(arr, n);

    ordenacionShell(arr, n);

    cout << "\nArreglo ordenado: ";
    mostrarArreglo(arr, n);

    return 0;
}t