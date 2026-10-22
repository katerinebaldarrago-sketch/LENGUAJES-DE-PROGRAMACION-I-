// Programa: Area y Perimetro de un Rectangulo
// Funcion : Solicita la base y la altura de un rectangulo y calcula su area (base * altura) y su perimetro (2 * (base + altura)), mostrando ambos resultados.
#include <iostream>
using namespace std;

int main() {
    double base, altura, area, perimetro;

    cout << "Ingrese la base del rectangulo: ";
    cin >> base;
    cout << "Ingrese la altura del rectangulo: ";
    cin >> altura;

    area = base * altura;
    perimetro = 2 * (base + altura);

    cout << "El area del rectangulo es: " << area << endl;
    cout << "El perimetro del rectangulo es: " << perimetro << endl;

    return 0;
}
