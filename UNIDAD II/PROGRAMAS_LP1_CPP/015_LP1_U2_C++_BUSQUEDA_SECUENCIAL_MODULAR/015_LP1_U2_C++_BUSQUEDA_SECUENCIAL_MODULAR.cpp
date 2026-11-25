#include <iostream>
#include <vector>

using namespace std;

void leerArreglo(int arreglo[], int n) {
    cout << "Ingreso de valores: " << endl;
    for (int i = 0; i < n; i++) {
        cout << "Elemento [" << i+1 << "]: ";
        cin >> arreglo[i];
    }
}
 
void mostrarArreglo(int arreglo[], int n) {
    cout << "Arreglo : " << endl;
    cout << "[ ";
    for (int i = 0; i < n; i++) {
        cout << arreglo[i] << " ";
    }
    cout << "]" << endl;
}

int busquedaSecuencial(int arreglo[], int n, int valor, int& iteracion) {
    int indice = -1;
    iteracion = 0;
    for (int i = 0; i < n; i++) {
        iteracion++;
        if (arreglo[i] == valor) {
            indice = i;
            break;
        }
    }
    return indice;
}

void mostrarResultado(int arreglo[], int valor, int indice, int iteracion) {
    if (indice != -1) {
        cout << "Valor buscado: " << valor << endl;
        cout << "Indice: " << indice << endl;
        cout << "Iteracion: " << iteracion << endl;
        cout << "Contenido:  arreglo[" << indice << "] = " << arreglo[indice] << endl;
    } else {
        cout << "El valor " << valor << " NO se encontro en el arreglo" << endl;
    }
}

int main() {
    int n, valor, iteracion;
    int arreglo[100];

    cout << "Ingrese la cantidad de elementos del arreglo: ";
    cin >> n;

    leerArreglo(arreglo, n);
    mostrarArreglo(arreglo, n);

    cout << "Que valor desea buscar? ";
    cin >> valor;

    int indice = busquedaSecuencial(arreglo, n, valor, iteracion);
    mostrarResultado(arreglo, valor, indice, iteracion);

    return 0;
}