// Programa: Calculo de IMC (version if + switch, 5 categorias)
// Funcion : Solicita peso y estatura, calcula el IMC y lo clasifica en 5 categorias (Bajo peso, Normal, Sobrepeso, Obesidad I y II) usando if/else if para asignar rango y switch para mostrar el resultado.
#include <iostream>
using namespace std;

int main() {
    float peso, estatura, imc;
    int opcionRango;

    cout << "=== CALCULADORA DE INDICE DE MASA CORPORAL ===" << endl;
    cout << "Ingrese su peso en kg: ";
    cin >> peso;
    cout << "Ingrese su estatura en metros: ";
    cin >> estatura;

    if (peso <= 0 || estatura <= 0) {
        cout << "ERROR: El peso y la estatura deben ser mayores a 0." << endl;
    } else {
        imc = peso / (estatura * estatura);
        cout << "Su IMC es: " << imc << endl;

        if (imc < 18.5) opcionRango = 1;
        else if (imc >= 18.5 && imc <= 24.9) opcionRango = 2;
        else if (imc >= 25 && imc <= 29.9) opcionRango = 3;
        else if (imc >= 30.0 && imc <= 34.9) opcionRango = 4;
        else opcionRango = 5;

        switch (opcionRango) {
            case 1: cout << "Bajo peso" << endl; break;
            case 2: cout << "Peso Normal" << endl; break;
            case 3: cout << "Sobrepeso" << endl; break;
            case 4: cout << "Obesidad grado I" << endl; break;
            case 5: cout << "Obesidad de grado II" << endl; break;
            default: cout << "No se pudo clasificar el IMC" << endl; break;
        }
    }

    return 0;
}
