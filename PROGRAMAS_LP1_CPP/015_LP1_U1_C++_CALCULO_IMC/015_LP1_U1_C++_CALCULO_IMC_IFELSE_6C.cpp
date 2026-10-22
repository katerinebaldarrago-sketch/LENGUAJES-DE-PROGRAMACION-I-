// Programa: Calculo de IMC (version if/else if directo)
// Funcion : Solicita el peso y la altura, calcula el Indice de Masa Corporal y lo clasifica en 6 categorias (Bajo peso, Normal, Sobrepeso, Obesidad I, II y III) usando if/else if encadenados.
#include <iostream>
using namespace std;

int main() {
    float peso, altura, imc;

    cout << "Ingrese su peso en kilogramos: ";
    cin >> peso;
    cout << "Ingrese su altura en metros: ";
    cin >> altura;

    if (peso <= 0 || altura <= 0) {
        cout << "Error: El peso y la altura deben ser mayores a cero." << endl;
    } else {
        imc = peso / (altura * altura);
        cout << "Su Indice de Masa Corporal (IMC) es: " << imc << endl;

        if (imc < 18.5) {
            cout << "Clasificacion: Bajo peso" << endl;
        }
        else if (imc >= 18.5 && imc <= 24.9) {
            cout << "Clasificacion: Peso normal" << endl;
        }
        else if (imc >= 25 && imc <= 29.9) {
            cout << "Clasificacion: Sobrepeso" << endl;
        }
        else if (imc >= 30 && imc <= 34.9) {
            cout << "Clasificacion: Obesidad Grado I" << endl;
        }
        else if (imc >= 35 && imc <= 39.9) {
            cout << "Clasificacion: Obesidad Grado II" << endl;
        }
        else {
            cout << "Clasificacion: Obesidad Grado III" << endl;
        }
    }

    return 0;
}
