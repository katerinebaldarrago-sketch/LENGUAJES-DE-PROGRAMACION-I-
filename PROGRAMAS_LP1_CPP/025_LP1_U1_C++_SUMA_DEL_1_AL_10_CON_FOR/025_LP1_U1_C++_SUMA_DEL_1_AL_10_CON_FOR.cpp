// Programa: Suma del 1 al 10 con bucle for
// Funcion : Calcula la suma de los numeros del 1 al 10 usando un bucle for y muestra el resultado por pantalla.
#include <iostream>
using namespace std;

int main() {
    int suma = 0;

    cout << "SUMAR NUMEROS DEL 1 AL 10" << endl;

    for (int i = 1; i <= 10; i++) {
    	cout << i << endl;
        suma = suma + i;
    }

    cout << "La suma es: " << suma << endl;

    return 0;
}