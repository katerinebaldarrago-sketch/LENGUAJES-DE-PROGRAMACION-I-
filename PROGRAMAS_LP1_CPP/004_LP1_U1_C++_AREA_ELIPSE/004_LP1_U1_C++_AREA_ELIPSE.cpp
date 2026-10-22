// Programa: Area de una Elipse
// Funcion : Solicita el semieje mayor y el semieje menor de una elipse y calcula su area con la formula A = PI * a * b, mostrando el resultado.
#include <iostream>
using namespace std;

int main() {
    const double PI = 3.14159265358979;
    double semiejeMayor, semiejeMenor, area;

    cout << "Ingrese el semieje mayor: ";
    cin >> semiejeMayor;
    cout << "Ingrese el semieje menor: ";
    cin >> semiejeMenor;

    area = PI * semiejeMayor * semiejeMenor;

    cout << "El area de la elipse es: " << area << endl;

    return 0;
}
