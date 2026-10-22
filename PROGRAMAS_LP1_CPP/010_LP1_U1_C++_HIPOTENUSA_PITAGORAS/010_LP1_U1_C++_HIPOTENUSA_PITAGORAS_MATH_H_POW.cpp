// Programa: Hipotenusa de un Triangulo (version con math.h y pow)
// Funcion : Solicita los dos catetos de un triangulo rectangulo y calcula la hipotenusa usando la libreria math.h y la funcion pow para elevar al cuadrado, aplicando el Teorema de Pitagoras.
#include <iostream>
#include <math.h>
using namespace std;

int main() {
    float a, b, h;

    cout << "Sistema de calculo de hipotenusa de un triangulo rectangulo!" << endl;
    cout << "Ingrese el valor del cateto a: ";
    cin >> a;
    cout << "Ingrese el valor del cateto b: ";
    cin >> b;

    h = sqrt(pow(a, 2) + pow(b, 2));

    cout << "La Hipotenusa es: " << h << endl;

    return 0;
}
