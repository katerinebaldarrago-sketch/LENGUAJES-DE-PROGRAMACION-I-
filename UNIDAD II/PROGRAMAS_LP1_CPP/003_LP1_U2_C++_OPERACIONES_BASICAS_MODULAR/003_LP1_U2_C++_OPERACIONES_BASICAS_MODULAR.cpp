#include <iostream>
using namespace std;

// Variables globales
int a, b;

// Prototipos de funciones
void sumar(int, int);
void restar(int, int);
void multiplicar(int, int);
void dividir(int, int);

int main(){
    cout << "Ingrese el numero a : ";
    cin >> a;
    
    cout << "Ingrese el numero b : ";
    cin >> b;

    sumar(a, b);
    restar(a, b);
    multiplicar(a, b);
    dividir(a, b);

    return 0;
}

void sumar(int a, int b){
    cout << "Suma: " << a + b << endl;
}

void restar(int a, int b){
    cout << "Resta: " << a - b << endl;
}

void multiplicar(int a, int b){
    cout << "Multiplicacion: " << a * b << endl;
}

void dividir(int a, int b){
    if (b == 0)
        cout << "Division:       Error: no se puede dividir entre cero." << endl;
    else
        cout << "Division:       " << (float)a / b << endl;
}