// Programa: Area del Circulo
// Funcion : Solicita el radio de un circulo y calcula su area con la formula PI * radio^2, mostrando el resultado por pantalla.
#include <iostream>
using namespace std;

int main() {
    const double PI = 3.14159265358979;
    double radio, area;

    cout << "Ingrese el radio del circulo: ";
    cin >> radio;

    area = PI * radio * radio;

    cout << "El area del circulo es: " << area << endl;

    return 0;
}
