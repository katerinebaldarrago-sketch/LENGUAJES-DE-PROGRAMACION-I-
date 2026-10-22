// Programa: Calculo de IMC (version con if + switch, pow, rango corregido)
// Funcion : Solicita el peso y la estatura, calcula el IMC usando pow, lo clasifica en 5 categorias (Bajo peso, Normal, Sobrepeso, Obesidad I y II) mediante if/else if para asignar rango y switch para mostrar el diagnostico.
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    float peso, estatura, IMC;
    int opcionRango;

    cout << "Calculo del Indice de masa corporal" << endl;
    cout << "Ingrese su peso (kg): ";
    cin >> peso;
    cout << "Ingrese su talla (m): ";
    cin >> estatura;

    if (peso <= 0 || estatura <= 0) {
        cout << "\nError: el peso y estatura deben ser mayores a cero\n" << endl;
    }
    else {
        IMC = peso / pow(estatura, 2);

        if (IMC < 18.5) opcionRango = 1;
        else if (IMC >= 18.5 && IMC <= 24.9) opcionRango = 2;
        else if (IMC >= 25.00 && IMC <= 29.9) opcionRango = 3;
        else if (IMC >= 30.00 && IMC <= 34.9) opcionRango = 4;
        else opcionRango = 5;

        cout << "Su Indice de masa corporal calculado es: " << IMC << " kg/m2" << endl;
        cout << "\nDiagnostico: ";

        switch (opcionRango) {
            case 1: cout << "Bajo peso" << endl; break;
            case 2: cout << "Peso normal" << endl; break;
            case 3: cout << "Sobrepeso" << endl; break;
            case 4: cout << "Obesidad grado 1" << endl; break;
            case 5: cout << "Obesidad grado 2" << endl; break;
            default: cout << "No se pudo clasificar el IMC" << endl; break;
        }
    }

    return 0;
}
