// Programa: Evaluacion de Notas (version con if/else if + switch)
// Funcion : Solicita una nota entre 0 y 20, muestra su estado (Excelente, Bueno, Regular, Desaprobado) y su categoria (A, B, C, D) usando dos bloques de if/else if y un switch.
#include <iostream>
using namespace std;

int main() {
    float nota;

    cout << "SISTEMA DE EVALUACION DE NOTAS (ESCALA 0 - 20) " << endl;
    cout << "Ingrese su nota final (0 - 20): ";
    cin >> nota;

    if (nota < 0 || nota > 20) {
        cout << "ERROR: La nota ingresada no es valida. Debe escribir entre 0 y 20" << endl;
        return 1;
    }

    if (nota >= 18) cout << "Estado: Excelente (Sobresaliente)." << endl;
    else if (nota >= 14) cout << "Estado: Aprobado (Bueno)." << endl;
    else if (nota >= 11) cout << "Estado: Aprobado (Regular)." << endl;
    else cout << "Estado: Desaprobado" << endl;

    int nivel;
    if (nota >= 18) nivel = 1;
    else if (nota >= 14) nivel = 2;
    else if (nota >= 11) nivel = 3;
    else nivel = 4;

    switch (nivel) {
        case 1: cout << "Categoria A: Postulante de cuadro de honor o beca" << endl; break;
        case 2: cout << "Categoria B: Buen rendimiento academico" << endl; break;
        case 3: cout << "Categoria C: Aprobado, pero requiere reforzamiento" << endl; break;
        case 4: cout << "Categoria D: Desaprobado, requiere recuperacion" << endl; break;
    }

    return 0;
}
