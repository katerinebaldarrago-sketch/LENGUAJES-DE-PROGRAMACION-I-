// Programa: Conversion de Segundos a Horas, Minutos y Segundos
// Funcion : Solicita una cantidad de segundos y los convierte a horas, minutos y segundos restantes, mostrando el resultado desglosado.
#include <iostream>
using namespace std;

int main() {
    int segundosTotales, horas, minutos, segundos;

    cout << "Ingrese la cantidad de segundos: ";
    cin >> segundosTotales;

    horas = segundosTotales / 3600;
    minutos = (segundosTotales % 3600) / 60;
    segundos = segundosTotales % 60;

    cout << "Equivale a: " << horas << " horas, "
         << minutos << " minutos y "
         << segundos << " segundos" << endl;

    return 0;
}
