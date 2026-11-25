#include <iostream>
using namespace std;

int contador = 0; // numero de particion

void mostrar(int datos[], int n) {
    cout << "[";
    for (int k = 0; k < n; k++) {
        cout << datos[k];
        if (k < n - 1) cout << ",";
    }
    cout << "]";
}

void intercambiar(int &a, int &b) {
    int aux = a;
    a = b;
    b = aux;
}

// Particion (Lomuto): el pivote es el ultimo elemento del tramo
int particion(int datos[], int n, int inicio, int fin) {
    contador++;
    int pivote = datos[fin];
    int i = inicio - 1;

    cout << "\nParticion " << contador << ": tramo [" << inicio << ".." << fin
         << "], pivote = " << pivote << ", i = " << i << endl;

    for (int j = inicio; j < fin; j++) {
        cout << "   j = " << j << " : " << datos[j] << " <= " << pivote << "? ";
        if (datos[j] <= pivote) {
            i++;
            intercambiar(datos[i], datos[j]);
            cout << "Si -> i = " << i << ", intercambio datos[" << i << "] <-> datos[" << j << "]" << endl;
        } else {
            cout << "No" << endl;
        }
    }

    int p = i + 1;
    cout << "\n   P = i + 1 => P = " << i << "+1 = " << p
         << ", intercambio datos[" << p << "] <-> datos[" << fin << "]" << endl;
    cout << "   " << datos[p] << " <-> " << datos[fin] << endl;
    intercambiar(datos[p], datos[fin]);

    cout << "   Resultado : ";
    mostrar(datos, n);
    cout << endl;

    return p;
}

void quickSort(int datos[], int n, int inicio, int fin) {
    if (inicio < fin) {
        int p = particion(datos, n, inicio, fin);
        quickSort(datos, n, inicio, p - 1);  // sublista izquierda
        quickSort(datos, n, p + 1, fin);     // sublista derecha
    }
}

int main() {
    int datos[] = {64, 25, 12, 22, 11};
    int n = sizeof(datos) / sizeof(datos[0]);

    cout << "Arreglo original: ";
    mostrar(datos, n);
    cout << endl;

    quickSort(datos, n, 0, n - 1);

    cout << "\nArreglo ordenado: ";
    mostrar(datos, n);
    cout << endl;

    return 0;
}