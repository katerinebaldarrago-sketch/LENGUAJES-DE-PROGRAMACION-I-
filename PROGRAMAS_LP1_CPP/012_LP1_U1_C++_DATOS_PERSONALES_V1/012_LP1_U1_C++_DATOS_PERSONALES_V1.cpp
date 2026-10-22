// Programa: Datos Personales
// Funcion : Solicita nombre, apellido y edad al usuario y los muestra formateados en pantalla (nombre completo y edad).
#include <iostream>
#include <string>
using namespace std;

int main() {
    string nombre, apellido;
    int edad;

    cout << "Ingresa tu nombre: ";
    cin >> nombre;
    cout << "Ingresa tu apellido: ";
    cin >> apellido;
    cout << "Ingresa tu edad: ";
    cin >> edad;

    cout << "Nombre completo: " << nombre << " " << apellido << endl;
    cout << "Edad: " << edad << " anios" << endl;

    return 0;
}
