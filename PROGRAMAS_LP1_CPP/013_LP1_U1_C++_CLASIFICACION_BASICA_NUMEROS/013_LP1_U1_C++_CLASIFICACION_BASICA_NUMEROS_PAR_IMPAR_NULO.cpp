// Programa: Clasificacion Basica de Numeros (paridad)
// Funcion : Solicita un numero entero y determina si es nulo (cero), par o impar usando el operador modulo (%) y una estructura if/else if/else.
#include <iostream>
using namespace std;

int main() {
    int numero;

    cout << "Ingrese un numero: ";
    cin >> numero;

    if (numero == 0) {
        cout << "El numero es nulo." << endl;
    } else if (numero % 2 == 0) {
        cout << "El numero es par" << endl;
    } else {
        cout << "El numero es impar" << endl;
    }

    return 0;
}
