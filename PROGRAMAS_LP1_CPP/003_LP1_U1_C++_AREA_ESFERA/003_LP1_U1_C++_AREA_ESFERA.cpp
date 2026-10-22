// Programa: Area de una Esfera
// Funcion : Solicita el radio de una esfera y calcula su area superficial con la formula A = 4 * PI * r^2, mostrando el resultado por pantalla.
#include <iostream>
using namespace std;

int main() {
    const double PI = 3.14159265358979;
    double radio, area;

    cout << "Ingrese el radio de la esfera: ";
    cin >> radio;

    area = 4 * PI * radio * radio;

    cout << "El area de la esfera es: " << area << endl;

    return 0;
}
