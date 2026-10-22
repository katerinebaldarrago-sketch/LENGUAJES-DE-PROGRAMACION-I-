// Programa: Teorema de Pitagoras
// Funcion : Solicita los dos catetos de un triangulo rectangulo y calcula la hipotenusa con la formula hip = sqrt(ca^2 + co^2), mostrando el resultado por pantalla.
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    double ca, co, hip;

    cout << "Ingrese el cateto ca: ";
    cin >> ca;
    cout << "Ingrese el cateto co: ";
    cin >> co;

    hip = sqrt(ca * ca + co * co);

    cout << "La hipotenusa es: " << hip << endl;

    return 0;
}
